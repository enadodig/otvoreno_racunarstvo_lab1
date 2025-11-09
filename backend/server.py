import http.server, socketserver, json, urllib.parse

PORT = 8000
DATA_FILE = "../data/music_genres.json"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/data"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            search = params.get('search', [''])[0].lower()
            attr = params.get('attr', ['all'])[0]

            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if search:
                filtered = []
                for item in data:
                    if attr == 'all':
                        if any(str(v).lower().find(search) >= 0 for v in item.values()):
                            filtered.append(item)
                    else:
                        if attr in item and search in str(item[attr]).lower():
                            filtered.append(item)
                data = filtered

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
