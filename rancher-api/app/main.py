from fastapi import Depends, FastAPI
from pydantic import BaseModel
from .modules import RancherAPI

class Auth_Item(BaseModel):
    rancher_url: str
    key_id: str
    secret_key: str
    cluster_name: str
    namespace: str

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
        cluster_name = item['cluster_name'],
        namespace = item['namespace'],
    )
    return 200

@app.get("/namespace")
async def namespace():
    return app.state.rancher.list_namespace()