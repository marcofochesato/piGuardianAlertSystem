import http.server
import socketserver
import sqlite3

PORT = 8000

class PinRecordsHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Connect to the SQLite database
            conn = sqlite3.connect('pin_records.db')
            cursor = conn.cursor()

            # Fetch all records from the database
            cursor.execute('SELECT * FROM pin_records ORDER BY created_at DESC')
            records = cursor.fetchall()

            # Close the database connection
            conn.close()

            # Render HTML with the records
            records_html = self.render_records(records)

            self.wfile.write(records_html.encode('utf-8'))
            return

        # Serve other requests using SimpleHTTPRequestHandler
        return super().do_GET()

    def render_records(self, records):
        records_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pin Records</title>
        </head>
        <body>
            <h1>Pin Records</h1>
            <table border="1">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Pin Number</th>
                        <th>Description</th>
                        <th>Pin State</th>
                        <th>Created At</th>
                    </tr>
                </thead>
                <tbody>
        """

        for record in records:
            records_html += f"""
                <tr>
                    <td>{record[0]}</td>
                    <td>{record[1]}</td>
                    <td>{record[2]}</td>
                    <td>{record[3]}</td>
                    <td>{record[4]}</td>
                </tr>
            """

        records_html += """
                </tbody>
            </table>
        </body>
        </html>
        """

        return records_html

# Start the web server
with socketserver.TCPServer(("", PORT), PinRecordsHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
