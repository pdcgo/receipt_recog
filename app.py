from flask import Flask, render_template, request, flash
import fitz 
from PIL import Image
from pyzbar.pyzbar import decode
import re, json

app = Flask(__name__)
app.secret_key = 'secret_key'

# Fungsi untuk mengekstrak data dari PDF
def extract_codes_from_pdf(pdf_path, dpi=300):
    codes = []
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            decoded_objects = decode(img)
            for obj in decoded_objects:
                codes.append({
                    "type": obj.type,
                    "data": obj.data.decode("utf-8"),
                    "page": page_num + 1
                })
    return list({frozenset(item.items()): item for item in codes}.values())

def extract_tracking_info(pdf_path):
    tracking_info = {}
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            text = page.get_text()
            
            resi_match = re.search(r"\bNo\.\s*Resi:\s*([^\n]+)", text)
            if resi_match:
                tracking_info['no_resi'] = resi_match.group(1).strip()
            order_match = re.search(r"\bNo\.\s*Pesanan:\s*([^\n]+)", text) or re.search(r"\bINV\s*([^\n]+)", text)
            #print(order_match.group())
            if order_match:
                id_pesanan = re.sub(r".*?:\s*", "", order_match.group())
                tracking_info['no_pesanan'] = id_pesanan.strip()
    return tracking_info

def extract_long_integers(pdf_path):
    long_integers = []
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            text = page.get_text()
            matches = re.findall(r"\b\d{15,}\b(?=\n)", text)
            long_integers.extend(matches)
    return list(set(long_integers))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['pdf_file']
        response ={}
        status = 'status'
        no_pesanan = 'order_id'
        no_resi = 'no_resi'
        response[status] = 'None'
        response[no_pesanan] = ''
        response[no_resi] = ''
        if file and file.filename.endswith('.pdf'):
            pdf_path = f"uploaded_{file.filename}"
            file.save(pdf_path)
            # Proses PDF
            try:
                codes = extract_codes_from_pdf(pdf_path)
                tracking_info = extract_tracking_info(pdf_path)
                long_integers = extract_long_integers(pdf_path)
                resi_tenan = tracking_info.get('no_resi') or codes[-1].get('data')
                no_pesanan_tenan = long_integers[0] if len(long_integers) > 0 else tracking_info.get('no_pesanan') or codes[0].get('data')
                response[status] = 'success'
                response[no_pesanan] = no_pesanan_tenan
                response[no_resi] = resi_tenan
                response_json = json.dumps(response)
                flash(response_json)
            except Exception as e:
                response[status] = f'Read PDF Error: {str(e)}'
                response_json = json.dumps(response)
                flash(response_json)
        else:
            response_json = json.dumps(response)
            flash("File yang diupload bukan file PDF. Silakan unggah file PDF.")
            flash(response_json)
    
    return render_template('index.html', codes=None, tracking_info=None, long_integers=None)

if __name__ == "__main__":
    app.run(debug=True)
