from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from html import escape

def do_math(operand1, operand2, operator):
    if operator == 'add':
        return str(float(operand1) + float(operand2))
    elif operator == 'subtract':
        return str(float(operand1) - float(operand2))
    elif operator == 'multiply':
        return str(float(operand1) * float(operand2))
    elif operator == 'divide':
        return str(float(operand1) / float(operand2))


class CalculatorRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''
            <html>
                <head>
                    <title>Calculator</title>
                </head>
                <body>
                    <h1>Calculator</h1>
                    <form method="post">
                        <label for="operand1">Operand 1:</label>
                        <input type="number" id="operand1" name="operand1" required><br>
                        <label for="operand2">Operand 2:</label>
                        <input type="number" id="operand2" name="operand2" required><br>
                        <label for="operator">Operator:</label>
                        <select id="operator" name="operator">
                            <option value="add">+</option>
                            <option value="subtract">-</option>
                            <option value="multiply">*</option>
                            <option value="divide">/</option>
                        </select><br>
                        <button type="submit">Calculate</button>
                    </form>
                </body>
            </html>
            '''
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('404 Not Found'.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = parse_qs(post_data.decode('utf-8'))
        operand1 = parsed_data['operand1'][0]
        operand2 = parsed_data['operand2'][0]
        operator = parsed_data['operator'][0]
        result = do_math(operand1, operand2, operator)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = '''
        <html>
            <head>
                <title>Calculator Result</title>
            </head>
            <body>
                <h1>Calculator Result</h1>
                <p>{operand1} {operator} {operand2} = {result}</p>
            </body>
        </html>
        '''
        html = html.format(operand1=escape(operand1), operator=escape(operator),
                           operand2=escape(operand2), result=escape(result))
        self.wfile.write(html.encode('utf-8'))

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, CalculatorRequestHandler)
    print('Starting calculator server...')
    httpd.serve_forever()
