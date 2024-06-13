from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
import yaml
from kubernetes import client
from kubernetes.config.kube_config import KubeConfigLoader
import os

credential = DefaultAzureCredential()
container_service_client = ContainerServiceClient(credential, '60f3ac75-ce11-4deb-9030-d3896b73c46c')

kubeconfig = container_service_client.managed_clusters.list_cluster_user_credentials("bhapathak-rg", "kubcluster_testing").kubeconfigs[0].value.decode("utf-8")
cfg_dict = yaml.safe_load(kubeconfig)
loader = KubeConfigLoader(cfg_dict)
config = client.Configuration()
loader.load_and_set(config)
client.Configuration.set_default(config)

core_v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

print("Deleting config map ")
with open(os.path.join(os.path.dirname(__file__), "configs.yaml")) as f:
        dep = yaml.safe_load(f)
        import pdb
        resp = core_v1.delete_namespaced_config_map(dep['metadata']['name'], "default")


print("Deleting Volume")
with open(os.path.join(os.path.dirname(__file__), "fio_pv.yaml")) as f:
        dep = yaml.safe_load(f)
        resp = core_v1.delete_persistent_volume(dep['metadata']['name'])

print("Deleting Persistent Volume Claim")
with open(os.path.join(os.path.dirname(__file__), "fio_pvc.yaml")) as f:
    dep = yaml.safe_load(f)
    resp = core_v1.delete_namespaced_persistent_volume_claim(dep['metadata']['name'], "default")

print("Deleting fio deployment")
with open(os.path.join(os.path.dirname(__file__), "fio_deployment_pvc.yaml")) as f:
        dep = yaml.safe_load(f)
        resp = apps_v1.delete_namespaced_deployment(
            dep['metadata']['name'], namespace="default")
