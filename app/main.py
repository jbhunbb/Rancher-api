from fastapi import Depends, FastAPI
from pydantic import BaseModel
from .modules import RancherAPI

class Auth_Item(BaseModel):
    rancher_url: str
    key_id: str
    secret_key: str

class Deploy_Update_Item(BaseModel):
    name: str
    image: str

app = FastAPI()
app.state.rancher = None

@app.get("/")
async def main():
    return {"message": "Rancher API"}
    
@app.post("/auth")
def auth(item: Auth_Item): 
    item = item.dict()
    app.state.rancher = RancherAPI(
        rancher_url = item['rancher_url'],
        key_id = item['key_id'],
        secret_key = item['secret_key'],
    )
    return 200

@app.get("/namespace")
async def list_namespace(cluster: str):
    return { "data": app.state.rancher.list_namespace(cluster)}

@app.get("/deploy")
async def list_deploy(cluster: str, ns: str):
    return {"data" : app.state.rancher.list_deploy(cluster, ns)}
    
@app.patch("/deploy")
async def update_deploy(item: Deploy_Update_Item, cluster: str, ns: str):
    item = item.dict()
    return {"status": app.state.rancher.update_image(cluster, ns, item['name'], item['image'])}