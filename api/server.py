from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import traceback
from database import Database

class APIHandler(BaseHTTPRequestHandler):
    db = Database()
    
    def _send_response(self, status_code, data=None, message="", status_text=""):
        # error statusi
        if status_code == 200 and not status_text:
            status_text = "OK"
        elif status_code == 201:
            status_text = "Created"
        elif status_code == 400:
            status_text = "Bad Request"
        elif status_code == 404:
            status_text = "Not Found"
        elif status_code == 500:
            status_text = "Internal Server Error"
        
        # wrapper odgovora
        response = {
            "status": status_text,
            "message": message,
            "response": data
        }
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')    # tip sadrzaja
        self.end_headers()  # kraj zaglavlja
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))  # slanje odgovora u tocnom formatu
    
    # parsira json tijelo zahtjeva
    def _parse_body(self): 
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            raw_data = self.rfile.read(content_length).decode('utf-8')
            try:
                return json.loads(raw_data)
            except json.JSONDecodeError:
                return None
        return {}
    
    def _handle_error(self, e):
        print(f"Error: {str(e)}")
        self._send_response(500, None, "Internal server error", "Internal Server Error")    # genericno da se ne otkrije vrsta greske korisniku
    

    def do_GET(self):
        try:
            parsed_path = urllib.parse.urlparse(self.path)  # razdvajanje putanje i parametara
            path_parts = parsed_path.path.strip('/').split('/') # dijeljenje putanje na dijelove prema /
            
            # openapi endpoint
            if self.path == '/openapi.json':
                try:
                    with open('api/openapi.json', 'r', encoding='utf-8') as f:  # otvaranje openapi specifikacije
                        spec = json.load(f)
                    self._send_response(200, spec, "OpenAPI specification fetched") # uspjesno dohvatili spec
                except:
                    self._send_response(404, None, "OpenAPI specification not found", "Not Found")  # spec nije pronadena
                return
            
            # dohvat svega
            elif self.path == '/api/genres' or self.path == '/api/genres/': # svi zanrovi
                data = self.db.get_all()    
                self._send_response(200, data, "All genres fetched successfully")   
            
            # dohvat po id-u
            elif len(path_parts) == 3 and path_parts[0] == 'api' and path_parts[1] == 'genres': # potrebna 3 dijela patha (api/genres/{id})
                genre_id = path_parts[2]
                genre = self.db.get_by_id(genre_id) # dohvat zanra po id-u
                if genre:
                    self._send_response(200, genre, f"Genre with ID {genre_id} fetched successfully")
                else:
                    self._send_response(404, None, f"Genre with ID {genre_id} not found", "Not Found")
            
            # dohvat po eri
            elif self.path.startswith('/api/genres/era/'):
                era = path_parts[3] if len(path_parts) > 3 else ''  # dohvat ere iz patha (3. dio)
                genres = self.db.get_by_era(era)
                self._send_response(200, genres, f"Genres from {era} era fetched")
            
            # dohvat po drzavi
            elif self.path.startswith('/api/genres/country/'):
                country = path_parts[3] if len(path_parts) > 3 else ''
                genres = self.db.get_by_country(country)
                self._send_response(200, genres, f"Genres from {country} fetched")
            
            # dohvat po artistu
            elif self.path.startswith('/api/genres/artist/'):
                artist = path_parts[3] if len(path_parts) > 3 else ''
                genres = self.db.get_by_artist(artist)
                self._send_response(200, genres, f"Genres by artist {artist} fetched")
            
            # ako nije pronadeno
            else:
                self._send_response(404, None, "Endpoint not found", "Not Found")
                
        except Exception as e:
            self._handle_error(e)
    
    def do_POST(self):
        try:
            if self.path == '/api/genres' or self.path == '/api/genres/':
                data = self._parse_body()
                if not data:
                    self._send_response(400, None, "Invalid JSON data", "Bad Request")
                    return
                
                # validacija obaveznih polja
                required_fields = ['name', 'artist', 'era_of_origin', 'years_active']
                for field in required_fields:
                    if field not in data:
                        self._send_response(400, None, f"Missing required field: {field}", "Bad Request")
                        return
                
                # defaultne vrijednosti
                data.setdefault('top_ranked_album', '')
                data.setdefault('origin_country', '')
                data.setdefault('main_instruments', '')
                data.setdefault('typical_bpm_range', '')
                data.setdefault('vocal_style', '')
                data.setdefault('subgenres', [])
                
                new_genre = self.db.create(data)
                self._send_response(201, new_genre, "Genre created successfully", "Created")
            else:
                self._send_response(404, None, "Endpoint not found", "Not Found")
                
        except Exception as e:
            self._handle_error(e)
    
    def do_PUT(self):
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            path_parts = parsed_path.path.strip('/').split('/')
            
            if len(path_parts) == 3 and path_parts[0] == 'api' and path_parts[1] == 'genres':
                genre_id = path_parts[2]
                data = self._parse_body()
                
                if not data:
                    self._send_response(400, None, "Invalid JSON data", "Bad Request")
                    return
                
                updated = self.db.update(genre_id, data)
                if updated:
                    self._send_response(200, updated, f"Genre with ID {genre_id} updated successfully")
                else:
                    self._send_response(404, None, f"Genre with ID {genre_id} not found", "Not Found")
            else:
                self._send_response(404, None, "Endpoint not found", "Not Found")
                
        except Exception as e:
            self._handle_error(e)
    
    def do_DELETE(self):
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            path_parts = parsed_path.path.strip('/').split('/')
            
            if len(path_parts) == 3 and path_parts[0] == 'api' and path_parts[1] == 'genres':
                genre_id = path_parts[2]
                deleted = self.db.delete(genre_id)
                if deleted:
                    self._send_response(200, deleted, f"Genre with ID {genre_id} deleted successfully")
                else:
                    self._send_response(404, None, f"Genre with ID {genre_id} not found", "Not Found")
            else:
                self._send_response(404, None, "Endpoint not found", "Not Found")
                
        except Exception as e:
            self._handle_error(e)

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f'API server running on port {port}')
    httpd.serve_forever()   # otvoren dok se ne zatvori

if __name__ == '__main__':
    run_server()