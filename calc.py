from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from html import escape

def evaluate_expression(expression):
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: Invalid expression"

class CalculatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
            <html>
            <head><title>Calculator</title></head>
            <body>
            <h1>Calculator</h1>
            <form method="POST">
            <input type="text" name="expression" placeholder="Enter expression">
            <input type="submit" value="Evaluate">
            </form>
            </body>
            </html>
            ''')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        expression = params['expression'][0]
        result = evaluate_expression(expression)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
            <html>
            <head><title>Calculator</title></head>
            <body>
            <h1>Calculator</h1>
            <form method="POST">
            <input type="text" name="expression" value="{}">
            <input type="submit" value="Evaluate">
            </form>
            <p>Result: {}</p>
            </body>
            </html>
            '''.format(escape(expression), escape(result)))

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, CalculatorHandler)
    print('Running calculator on port 8000...')
    httpd.serve_forever()
