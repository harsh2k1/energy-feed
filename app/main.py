from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import Request
from fastapi.templating import Jinja2Templates
import sys
from fastapi.staticfiles import StaticFiles
from pathlib import Path
sys.path.append("./")
from services.elasticSearch import ElasticSearch


es_obj = ElasticSearch()
templates = Jinja2Templates(directory="templates")
app = FastAPI(debug=True)
# app.mount("/Users/harshpreetsingh/Documents/iit_madras_hackathon/repository/ns-python/app/static", StaticFiles(directory="/Users/harshpreetsingh/Documents/iit_madras_hackathon/repository/ns-python/app/static"), name="static")
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)
origins = ["*"]
# origins = ["http://localhost:4200", "https://localhost:4200", "http://13.213.211.168:4200", "https://13.213.211.168:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/feed", response_class=HTMLResponse)
async def feed(request: Request):
    form_data = await request.form()
    text = form_data['text']
    
    body = {
        "bool":{
            "must":[
                {
                    "term":{
                        "details.category.name":{
                            "value":text  # Solar Energy
                        }
                    }
                }
            ]
        }
    }
    
    res, _ = es_obj.fetchRecord(body=body)
    # print(res[0])
    titles = [ele["_source"]["details"][0]["title"] for ele in res]
    context = {"request":request, "titles":titles}
    # return templates.TemplateResponse("search_result.html",context)
    return templates.TemplateResponse("response.html",context)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8701)