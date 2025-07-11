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
        
        real_receipt = tracking_info.get('no_resi')
        if real_receipt is None:
            real_receipt = codes[-1].get('data')

        real_order_id = tracking_info.get('no_pesanan')
        if real_order_id is None:
            if len(long_integers) > 0:
                real_order_id = long_integers[0]
            else:
                real_order_id = codes[0].get('data')
        
        res.status = "success"
        res.order_id = real_order_id
        res.receipt = real_receipt
        
    except Exception as e:
        res.status = "error"
        logger.error(e, exc_info=True)
    
    return res.model_dump()