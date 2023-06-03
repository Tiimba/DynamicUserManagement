import http.server

# Configurações do servidor
host = 'localhost'
port = 8080

# Inicia o servidor web
server_address = (host, port)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

print(f"HTTP running in http://{host}:{port}")
httpd.serve_forever()
