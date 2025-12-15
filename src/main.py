import time
import random
from fastapi import FastAPI
from prometheus_client import Counter, Histogram, start_http_server

app = FastAPI(title="ML Service (Demo)")

PREDICT_REQUESTS = Counter("predict_requests_total", "Total /predict requests")
PREDICT_ERRORS = Counter("predict_errors_total", "Total /predict errors")
LATENCY = Histogram("prediction_latency_seconds", "Prediction latency in seconds")

@app.on_event("startup")
def startup():
    start_http_server(8001)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/predict")
def predict(delay: float = 0.0, fail: int = 0):
    """
    delay: adds artificial latency in seconds (for alert triggering)
    fail: if 1, simulates an error (for error-rate monitoring)
    """
    PREDICT_REQUESTS.inc()
    start = time.time()

    try:
        time.sleep(max(0.0, float(delay)) + random.uniform(0.05, 0.25))

        if int(fail) == 1:
            raise RuntimeError("simulated failure")

        return {"prediction": random.random()}
    except Exception:
        PREDICT_ERRORS.inc()
        raise
    finally:
        LATENCY.observe(time.time() - start)
