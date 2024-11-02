import requests

# untuk docker
# BASE_URL = "http://127.0.0.1:8080"
# untuk local
BASE_URL = "http://127.0.0.1:8000"
# BASE_URL = "https://pdf-recog-service-1008190962565.asia-southeast2.run.app"

fnames = [
    # "test/assets/uploaded_jne.pdf",
    # "test/assets/uploaded_JP.pdf",
    # "test/assets/uploaded_JX.pdf",
    # "test/assets/uploaded_lazada.pdf",
    # "test/assets/uploaded_ninjalaz.pdf",
    # "test/assets/uploaded_pdf_kosong.pdf",
    # "test/assets/uploaded_sicepat.pdf",
    # "test/assets/uploaded_spx.pdf",
    # "test/assets/uploaded_toped.pdf",
    # "test/assets/uploaded_toped2.pdf",
    "test/assets/uploaded_trisnatiktok.pdf",
]

for fname in fnames:
    with open(fname, "rb") as file:
        print(fname)
        data = file.read()
        res = requests.post(BASE_URL + "/v1/pdfreader", data=data)
        print(res)
        
        print(res.status_code)
        print(res.text)