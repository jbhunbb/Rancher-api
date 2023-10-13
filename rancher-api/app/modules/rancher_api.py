import requests


class RancherAPI:
  def __init__(self, rancher_url, key_id, secret_key, cluster_name, namespace):
    self.rancher_url = rancher_url
    self.key_id = key_id
    self.secret_key = secret_key
    self.cluster_name = cluster_name
    self.namespace = namespace
    
    self.session = requests.Session()
    self.session.verify = False
    self.session.headers.update({'Content-type': 'application/json'})
    self.session.auth = (key_id, secret_key)
    
    self.cluster_id = self.get_cluster_id(cluster_name)
    self.base_url = f"{rancher_url}/k8s/clusters/{self.cluster_id}"
  
  def get_cluster_id(self, cluster_name):
    url = f"{self.rancher_url}/v3/clusters"
    resp = self.session.get(url)
    cluster_list = resp.json()['data']
    target_cluster = next((c for c in cluster_list if c['name'] == cluster_name), None)
    if target_cluster is None:
      raise Exception(f"Cluster '{cluster_name}' not found")
    cluster_id = target_cluster['id']
    return cluster_id
  
  def list_namespace(self):
    path = '/api/v1/namespaces'
    namespaces = []
    resp = self.session.get(self.base_url + path)
    item_list = resp.json()['items']
    for item in item_list:
      namespaces.append(item['metadata']['name'])
    return namespaces
    
  def update_rancher(self, image):
    headers = {
      'Content-Type': 'application/json-patch+json',
    }
    data = [{"op": "replace", "path":"/spec/template/spec/containers/0/image", "value": "<new image>"}]
    resp = self.session.put(self.baseurl)
  