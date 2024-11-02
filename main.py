import logging
from pydantic import BaseModel
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from tool import *


logger = logging.getLogger(__name__)

app = FastAPI()

# cors middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Response(BaseModel):
    status: str
    order_id: str
    receipt: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/v1/pdfreader")
async def readpdf(req: Request):
    data = await req.body()
    res = Response(status="unknown", order_id="", receipt="")
    
    # mulai processing
    try:
        codes = extract_codes_from_pdf(data)
        tracking_info = extract_tracking_info(data)
        long_integers = extract_long_integers(data)
        resi_tenan = tracking_info.get('no_resi') or codes[-1].get('data')
        no_pesanan_tenan = long_integers[0] if len(long_integers) > 0 else tracking_info.get('no_pesanan') or codes[0].get('data')
        
        res.status = "success"
        res.order_id = no_pesanan_tenan
        res.receipt = resi_tenan
        
    except Exception as e:
        res.status = "error"
        logger.error(e, exc_info=True)
    
    return res.model_dump()