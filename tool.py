import fitz 
from PIL import Image
from pyzbar.pyzbar import decode
import re

def extract_codes_from_pdf(streamdata, dpi=300):
    codes = []
    with fitz.open(stream=streamdata, filetype="pdf") as pdf:
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

def extract_tracking_info(streamdata):
    tracking_info = {}
    with fitz.open(stream=streamdata, filetype="pdf") as pdf:
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


def extract_long_integers(streamdata):
    long_integers = []
    with fitz.open(stream=streamdata, filetype="pdf")  as pdf:
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            text = page.get_text()
            matches = re.findall(r"\b\d{15,}\b(?=\n)", text)
            long_integers.extend(matches)
    return list(set(long_integers))