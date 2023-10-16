import requests
import json

class RancherAPI:
  def __init__(self, rancher_url, key_id, secret_key):
    self.rancher_url = rancher_url
    self.key_id = key_id
    self.secret_key = secret_key
    self.cluster_name = ""
    
    self.session = requests.Session()
    self.session.verify = False
    self.session.headers.update({'Content-type': 'application/json'})
    self.session.auth = (key_id, secret_key)
    
    self.cluster_name = ""
    self.base_url = ""
  
  def get_base_url(self, cluster_name):
    if self.cluster_name == cluster_name:
      return self.base_url
    
    url = f"{self.rancher_url}/v3/clusters"
    resp = self.session.get(url)
    cluster_list = resp.json()['data']
    target_cluster = next((c for c in cluster_list if c['name'] == cluster_name), None)
    if target_cluster is None:
      raise Exception(f"Cluster '{cluster_name}' not found")
    cluster_id = target_cluster['id']
    self.base_url = f"{self.rancher_url}/k8s/clusters/{cluster_id}"
    return self.base_url
  
  def list_namespace(self, cluster_name):
    path = '/api/v1/namespaces'
    namespaces = []
    resp = self.session.get(self.get_base_url(cluster_name) + path)
    item_list = resp.json()['items']
    for item in item_list:
      namespaces.append(item['metadata']['name'])
    return namespaces
  
  def list_deploy(self, cluster_name, ns):
    path= f"/apis/apps/v1/namespaces/{ns}/deployments"
    resp = self.session.get(self.get_base_url(cluster_name) + path)
    item_list = resp.json()['items']
    deploys = []
    for item in item_list:
      deploys.append({
        "name": item['metadata']['name'], 
        "image": item['spec']['template']['spec']['containers'][0]['image']
      })
    return deploys
    
  def update_image(self, cluster_name, ns, name, image): 
    path= f"/apis/apps/v1/namespaces/{ns}/deployments/{name}"
    url = self.get_base_url(cluster_name) + path
    headers = {
      'Content-Type': 'application/json-patch+json',
    }
    body = [{"op": "replace", "path":"/spec/template/spec/containers/0/image", "value": image}]
    resp = self.session.patch(url, headers=headers, data = json.dumps(body))
    status = True if resp.status_code == 200 else False
    return status
  