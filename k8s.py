from prefect.infrastructure import KubernetesJob

kubernetes_job_block = KubernetesJob.load("k8s-job")

{
    "kind": "Job",
    "spec": {
        "template": {
            "spec": {
                "containers": [
                    {
                        "env": [], 
                        "name": "prefect-job", 
                        "resources": {
                            "limits": {
                                "cpu": "1", 
                                "memory": "2Gi"
                            }, 
                            "requests": {
                                "cpu": "1", 
                                "memory": "2Gi"
                            }
                        }
                    }
                ], 
                "completions": 1, 
                "parallelism": 1, 
                "restartPolicy": "Never"
                }
            }
        }, 
        "metadata": {
            "labels": {}
        }, 
    "apiVersion": "batch/v1"
}
