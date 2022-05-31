from fastapi import FastAPI, File, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from inference import Model
from utils import *


app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')
model = Model('yolov5l.pt')


@app.get("/")
async def main():
    content = """
    <body>
        <form action="/figma/" enctype="multipart/form-data" method="post">
            <input name="file" type="file" multiple>
            <input type="submit">
        </form>
        <h1>
            <a href="/result/">Rendered</a><br>
        </h1>
    </body>
    """
    return HTMLResponse(content=content)


@app.post("/figma/")
async def create_knn_files(request: Request, file: bytes = File(...)):
    image = image_from_bytes(file)
    resized = image_resize(image, height=800)
    cv2.imwrite('request_images/original_image.jpeg', resized)
    model.run('request_images')
    return RedirectResponse('/result/', status_code=302)


@app.get("/result/")
async def static_result(request: Request):
    content = """
        <img src="/static/res.jpg">
    """
    # return HTMLResponse(content=content)
    with open('template_data.json') as f:
        template_data = json.load(f)
    return templates.TemplateResponse('result.html', {'data': template_data, 'request': request})
