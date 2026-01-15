import code
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import traceback
from database import Database
import os
from authlib.integrations.requests_client import OAuth2Session
import requests
import secrets
import token

AUTH0_DOMAIN = "dev-gq3pzktnj7mobyrc.us.auth0.com"
CLIENT_ID = "regZXFJMzRCHMTsLT3dDbN4CPX3s2hHA"
CLIENT_SECRET = "wHr8GjJ0QV43ggJTlCFGUFJmoLf9m0_fG-iNoJJtEgtS8Ire43zXFcY0PAmjWBAs"
REDIRECT_URI = "http://localhost:8000/callback"

AUTHORIZATION_BASE_URL = f"https://{AUTH0_DOMAIN}/authorize"
TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"

SESSION = {}  # mem sesija


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
        import traceback
        traceback.print_exc()  # ispisuje pun stack trace u terminal
        self._send_response(500, None, "Internal server error", "Internal Server Error")


    def do_GET(self):
        try:
            parsed_path = urllib.parse.urlparse(self.path)  # razdvajanje putanje i parametara
            path_parts = parsed_path.path.strip('/').split('/') # dijeljenje putanje na dijelove prema /
            
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # root folder projekta

            if self.path == '/':
                try:
                    with open("index.html", "r", encoding="utf-8") as f:
                        html = f.read()
        
                    # Dinamički sadržaj za korisničke linkove
                    if 'user' in SESSION:
                        user_links = """
                        <a href="/profile">Korisnički profil</a><br>
                        <a href="/refresh">Osvježi preslike</a><br>
                        <a href="/logout">Odjava</a>
                        """
                    else:
                        user_links = '<a href="/login">Prijava</a>'

                    # placeholder za linkove
                    html = html.replace("<!--linkovi-->", user_links)

                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(html.encode("utf-8"))

                except FileNotFoundError:
                    self._send_response(404, None, "index.html not found", "Not Found")
                return

            
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
            elif len(path_parts) == 3 and path_parts[0] == 'api' and path_parts[1] == 'genres':
                genre_id = path_parts[2]
                genre = self.db.get_by_id(genre_id)

                if genre:
                    semantic_genre = {
                        "@context": "https://schema.org/",
                        "@type": "MusicRecording",     # ne postoji MusicGenre u Schema.org

                        "genre": genre.get("name", ""),

                        "byArtist": {
                            "@type": "MusicGroup",
                            "name": genre["artist"]
                        },

                        "countryOfOrigin": {
                            "@type": "Country",
                            "name": genre["origin_country"]
                        },

                        "inLanguage": "hr"
                }

                self._send_response(200, semantic_genre, f"Genre with ID {genre_id} fetched")
            
            # dohvat po eri
            elif self.path.startswith('/api/genres/era/'):
                era = path_parts[3] if len(path_parts) > 3 else ''  # dohvat ere iz patha (3. dio)
                genres = self.db.get_by_era(era)
                
                semantic_genres = []
                for genre in genres:
                    semantic_genres.append({
                        "@context": "https://schema.org/",
                        "@type": "MusicRecording",     # ne postoji MusicGenre u Schema.org

                        "genre": genre["name"],

                        "byArtist": {
                            "@type": "MusicGroup",
                            "name": genre["artist"]
                        },

                        "countryOfOrigin": {
                            "@type": "Country",
                            "name": genre["origin_country"]
                        },

                        "inLanguage": "hr"
                })

                self._send_response(200, semantic_genres, f"Genres from {era} era fetched")
            
            # dohvat po drzavi
            elif self.path.startswith('/api/genres/country/'):
                country = path_parts[3] if len(path_parts) > 3 else ''
                genres = self.db.get_by_country(country)
                
                semantic_genres = []
                for genre in genres:
                    semantic_genres.append({
                        "@context": "https://schema.org/",
                        "@type": "MusicRecording",     # ne postoji MusicGenre u Schema.org

                        "genre": genre["name"],

                        "byArtist": {
                            "@type": "MusicGroup",
                            "name": genre["artist"]
                        },

                        "countryOfOrigin": {
                            "@type": "Country",
                            "name": genre["origin_country"]
                        },

                        "inLanguage": "hr"
                })

                self._send_response(200, semantic_genres, f"Genres from {country} fetched")

            # dohvat po artistu
            elif self.path.startswith('/api/genres/artist/'):
                artist = "/".join(path_parts[3:])   # podrzava i imena s razmakom
                artist = urllib.parse.unquote(artist)
                genres = self.db.get_by_artist(artist)

                semantic_genres = []
                for genre in genres:
                    semantic_genres.append({
                        "@context": "https://schema.org/",
                        "@type": "MusicRecording",     # ne postoji MusicGenre u Schema.org

                        "genre": genre["name"],

                        "byArtist": {
                            "@type": "MusicGroup",
                            "name": genre["artist"]
                        },

                        "countryOfOrigin": {
                            "@type": "Country",
                            "name": genre["origin_country"]
                        },

                        "inLanguage": "hr"
                })

                self._send_response(200, semantic_genres, f"Genres by artist {artist} fetched")

            # OAuth2 prijava
            elif self.path == '/login':
                oauth = OAuth2Session(
                    CLIENT_ID,
                    CLIENT_SECRET,
                    scope="openid profile email",
                    redirect_uri=REDIRECT_URI
                )
                uri, state = oauth.create_authorization_url(AUTHORIZATION_BASE_URL)
    
                SESSION['oauth_state'] = state
    
                self.send_response(302)
                self.send_header('Location', uri)
                self.end_headers()
                return
            
            # OAuth2 callback
            elif self.path.startswith('/callback'):
                query = urllib.parse.parse_qs(parsed_path.query)
               
                if 'code' not in query:
                    self._send_response(400, None, "Missing code")
                    return

                code = query['code'][0]

                oauth = OAuth2Session(
                    CLIENT_ID,
                    CLIENT_SECRET,
                    redirect_uri=REDIRECT_URI
                )
        
                token = oauth.fetch_token(
                    TOKEN_URL,
                    code=code,
                    client_secret=CLIENT_SECRET
                )

                userinfo = requests.get(
                    USERINFO_URL,
                    headers={'Authorization': f"Bearer {token['access_token']}"}
                ).json()

                SESSION['user'] = userinfo

                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return
            
            # prikaz profila
            elif self.path == '/profile':
                if 'user' not in SESSION:
                    self._send_response(401, None, "Unauthorized")
                    return

                u = SESSION['user']
                html = f"""
                <html lang="hr"><body>
                <h2>Korisnički profil</h2>
                <p>Email: {u.get('email')}</p>
                <p>Ime: {u.get('name')}</p>
                <a href="/">Natrag</a>
                </body></html>
                """
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
                
                
            elif self.path == '/refresh':
                if 'user' not in SESSION:
                    self._send_response(401, None, "Unauthorized")
                    return

                data = self.db.get_all()
                with open("music_genres.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                with open("music_genres.csv", "w", encoding="utf-8") as f:
                    f.write("id,name,artist\n")
                    for g in data:
                        id_ = g.get('id', '')
                        name = g.get('name', '')
                        artist = g.get('artist', '')
                        f.write(f"{id_},{name},{artist}\n")

                self._send_response(200, None, "Preslike osvježene")
                return
            
            # odjava
            elif self.path == '/logout':
                SESSION.clear()
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return

            
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