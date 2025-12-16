
import httpx
from common.logging_util import log


JAVA_BACKEND_URL = "http://java-backend-service/api/v1"

class JavaAPIClient:
    def __init__(self):
        self.client = httpx.Client(base_url=JAVA_BACKEND_URL)
        log.info(f"JavaAPIClient initialized with base URL: {JAVA_BACKEND_URL}")

    def call_api(self, method: str, endpoint: str, json: dict = None):
       
        log.info(f"Calling Java API: {method} {endpoint}", extra={'java_endpoint': endpoint, 'method': method})
        
       
        if endpoint == "/leave/apply":
            return {"status": "success", "message": "Leave application successful."}
        elif endpoint == "/leave/balance/123":
            return {"status": "success", "data": {"sick_leaves": 3, "casual_leaves": 5}}
        else:
           
            return {"status": "success", "data": {"message": f"Successfully executed action on {endpoint}"}}

java_client = JavaAPIClient()