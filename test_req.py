import requests
from fastapi.testclient import TestClient
from main import app

# untuk docker
# BASE_URL = "http://127.0.0.1:8080"
# untuk local
BASE_URL = "http://127.0.0.1:8000"
# BASE_URL = "https://pdf-recog-service-1008190962565.asia-southeast2.run.app"

client = TestClient(app)

def upload_file(filepath: str) -> requests.Response:
    with open(filepath, "rb") as file:
        data = file.read()
        response = client.post(f"{BASE_URL}/v1/pdfreader", content=data)
        return response

def test_pdf_reader_jne():
    filepath = "test/assets/uploaded_jne.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == "241028PS9CUJSX"
    assert response.json()["receipt"] == "CM22433765888"

def test_pdf_reader_jp():
    filepath = "test/assets/uploaded_JP.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == "241028Q0AVC8NW"
    assert response.json()["receipt"] == "JP1480470567"

def test_pdf_reader_jx():
    filepath = "test/assets/uploaded_JX.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == "577368042531292914"
    assert response.json()["receipt"] == "JX2947703889"

def test_pdf_reader_lazada():
    filepath = "test/assets/uploaded_lazada.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == "1568059344220651"
    assert response.json()["receipt"] == "LXAD-3682244149"

def test_pdf_reader_ninjalaz():
    filepath = "test/assets/uploaded_ninjalaz.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == "1567709969788544"
    assert response.json()["receipt"] == "NLIDAP1794779450"

def test_pdf_reader_pdf_kosong():
    filepath = "test/assets/uploaded_pdf_kosong.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == ""
    assert response.json()["receipt"] == ""

def test_pdf_reader_sicepat():
    filepath = "test/assets/uploaded_sicepat.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == "241028Q0Y1X0YE"
    assert response.json()["receipt"] == "004366619468"

def test_pdf_reader_spx():
    filepath = "test/assets/uploaded_spx.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == "241028QGUYW11Y"
    assert response.json()["receipt"] == "SPXID04448120353A"

def test_pdf_reader_spx_eco():
    filepath = "test/assets/uploaded_spx_eco.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == "250429HTKNTDBR"
    assert response.json()["receipt"] == "SPXID057787703504"

def test_pdf_reader_spx_std():
    filepath = "test/assets/uploaded_spx_std.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200

    print(response.json())

    assert response.json()["order_id"] == "250707F5G3EYVP"
    assert response.json()["receipt"] == "SPXID052494793227"

def test_pdf_reader_toped():
    filepath = "test/assets/uploaded_toped.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == "INV/20241029/MPL/4247435594"
    assert response.json()["receipt"] == "TKSC-000007243NV"

def test_pdf_reader_toped2():
    filepath = "test/assets/uploaded_toped2.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == "INV/20241023/MPL/4234716240"
    assert response.json()["receipt"] == "TKP01-LVF16LNH"

def test_pdf_reader_trisnatiktok():
    filepath = "test/assets/uploaded_trisnatiktok.pdf"
    response = upload_file(filepath)
    assert response.status_code == 200
    assert response.json()["order_id"] == "577385207862036077"
    assert response.json()["receipt"] == "JX3005164280"

def test_pdf_reader():

    fnames = [
        # "test/assets/uploaded_jne.pdf",
        # "test/assets/uploaded_JP.pdf",
        # "test/assets/uploaded_JX.pdf",
        # "test/assets/uploaded_lazada.pdf",
        # "test/assets/uploaded_ninjalaz.pdf",
        # "test/assets/uploaded_pdf_kosong.pdf",
        # "test/assets/uploaded_sicepat.pdf",
        # "test/assets/uploaded_spx.pdf",
        # "test/assets/uploaded_spx_eco.pdf",
        # "test/assets/uploaded_spx_std.pdf",
        # "test/assets/uploaded_toped.pdf",
        # "test/assets/uploaded_toped2.pdf",
        # "test/assets/uploaded_trisnatiktok.pdf",
        # "test/new_receipt/get.pdf",
        # "test/new_receipt/get (1).pdf",
        # "test/new_receipt/get (2).pdf",
        # "test/new_receipt/get (3).pdf",
        # "test/new_receipt/get (4).pdf",
    ]

    for fname in fnames:
        with open(fname, "rb") as file:
            print(fname)
            data = file.read()
            res = requests.post(BASE_URL + "/v1/pdfreader", data=data)
            print(res)
            
            print(res.status_code)
            print(res.text)

if __name__ == "__main__":
    # test_pdf_reader_jne()
    # test_pdf_reader_jp()
    # test_pdf_reader_pdf_kosong()

    # test_pdf_reader_spx()
    # test_pdf_reader_spx_std()
    # test_pdf_reader_spx_std()

    test_pdf_reader()