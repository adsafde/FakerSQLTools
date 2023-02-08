from pathlib import Path
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from faker_create_tool.faker_constant import constants, e
from faker_create_tool.my_faker import get_faker_attribute

STATIC_URL = Path(__file__).parent / 'assets'
app = FastAPI()
app.mount("/assets",
          StaticFiles(directory=str(STATIC_URL)),
          name="static")

template = Jinja2Templates(directory="templates")


class Item(BaseModel):
    nums: int
    values: dict


@app.get("/")
async def server(req: Request):
    return template.TemplateResponse("index.html", context={"request": req})


@app.get("/api/sample")
async def sample(name: str):
    try:
        return {'code': 200, 'data': get_faker_attribute(name)}
    except AttributeError:
        return {'code': 200, 'data': 'Please change to another one'}


@app.get("/api")
async def root():
    data = [{'constant': key, 'description': value} for key, value in constants.items()]
    return {'code': 200, 'message': 'success', 'data': data, 'total': len(data)}


@app.get('/api/getconstant')
async def get_constant():
    return {'code': 200, 'message': 'success', 'data': e, 'constants': constants}


@app.get("/api/getvalue")
async def make_faker(name: str):
    value = get_faker_attribute(name)
    return {'code': 200, 'message': 'success', 'data': value}


@app.post("/api/sql")
async def make_sql(item: Item):
    data_lists = []
    for _ in range(item.nums):
        data = [get_faker_attribute(v) for _, v in item.values.items()]
        data_lists.append(data)
    keys = [k for k, _ in item.values.items()]
    return {'code': 200, 'message': 'success', 'data': data_lists, 'total': len(data_lists), 'nums': item,
            'keys': keys}


@app.post("/api/sqlmake")
async def make_sql_make(data: dict = Depends(make_sql)):
    datas = str(tuple(data.get('keys'))).replace("'", '')
    f = str(data.get('data')).replace('[', '(').replace(']', ')')[1:-1]
    sql = f"INSERT INTO table {datas} VALUES " + f
    return sql
