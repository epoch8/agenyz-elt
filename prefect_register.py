from prefect.deployments import Deployment
from prefect.infrastructure import KubernetesJob
from update_flow import elt
from constants import PROJECT_NAME


BASE_IMAGE_NAME = f"ghcr.io/epoch8/{PROJECT_NAME}"
BASE_IMAGE_TAG = open("pyproject.toml").readlines()[2].strip().split(" = ")[1].replace('"', '')
BASE_IMAGE = f"{BASE_IMAGE_NAME}:{BASE_IMAGE_TAG}"
K8S_NAMESPACE = "botfront"


kubernetes_job_block = KubernetesJob.load("k8s-job-block")


deployment = Deployment.build_from_flow(
    flow=elt,
    name=f"{PROJECT_NAME}-elt",
    tags=[PROJECT_NAME, BASE_IMAGE_TAG],
    work_pool_name="agenyz-elt",
    work_queue_name="agenyz-elt",
    infrastructure=kubernetes_job_block,
    infra_overrides={
        "image": BASE_IMAGE,
        "namespace": K8S_NAMESPACE
    },
    path="/opt/prefect"
)
deployment.apply()
