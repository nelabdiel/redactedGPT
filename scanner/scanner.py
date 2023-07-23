import os
from dotenv import load_dotenv
import tempfile
import psycopg2
import tlsh
import PyPDF2
from docx import Document
from flask import Flask, request, jsonify



# Replace with your PostgreSQL database connection details
load_dotenv()
db_host = os.environ.get('HOST_DB')
db_user = os.environ.get('USERNAME_DB')
db_password = os.environ.get('PASSWORD_DB')
db_name = os.environ.get('DB_DB')



def create_table():
    conn = psycopg2.connect(host=db_host, user=db_user, password=db_password, dbname=db_name)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS document_hashes (
            id SERIAL PRIMARY KEY,
            hash_value TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    
create_table()    


scanner = Flask(__name__)


@scanner.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)
        file_extension = os.path.splitext(file.filename)[1]

        if file_extension == '.pdf':
            tls_hash = get_tls_hash_pdf(temp_file.name)
        elif file_extension == '.docx':
            tls_hash = get_tls_hash_docx(temp_file.name)
        else:
            return jsonify({'error': 'Invalid file format. Only PDF and DOCX files are supported.'}), 400
        save_hash_to_database(tls_hash)
        os.remove(temp_file.name)
        return jsonify({'hash': tls_hash})
    else:
        return jsonify({'error': 'Invalid file. Only PDF and DOCX files are allowed.'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}

def get_tls_hash_pdf(file_path):
    pdf_reader = PyPDF2.PdfFileReader(file_path)
    pdf_text = ''
    for page_num in range(pdf_reader.numPages):
        pdf_page = pdf_reader.getPage(page_num)
        pdf_text += pdf_page.extractText()
    return tlsh.hash(pdf_text.encode('utf-8'))

def get_tls_hash_docx(file_path):
    doc = Document(file_path)
    doc_text = ''
    for para in doc.paragraphs:
        doc_text += para.text
    return tlsh.hash(doc_text.encode('utf-8'))

def save_hash_to_database(hash_value):
    conn = psycopg2.connect(host=db_host, user=db_user, password=db_password, dbname=db_name)
    cur = conn.cursor()
    cur.execute("INSERT INTO document_hashes (hash_value) VALUES (%s);", (hash_value,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
    #scanner.run(debug=True)
    port = int(os.environ.get("PORT", 5004))
    scanner.run(host='0.0.0.0', port=port)