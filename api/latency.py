from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

DATA = [
    {"region":"apac","latency_ms":152.39,"uptime_pct":99.353},
    {"region":"apac","latency_ms":141.53,"uptime_pct":98.57},
    {"region":"apac","latency_ms":226.18,"uptime_pct":99.396},
    {"region":"apac","latency_ms":145.10,"uptime_pct":97.135},
    {"region":"apac","latency_ms":218.10,"uptime_pct":98.809},
    {"region":"apac","latency_ms":120.06,"uptime_pct":97.654},
    {"region":"apac","latency_ms":192.37,"uptime_pct":97.826},
    {"region":"apac","latency_ms":123.01,"uptime_pct":99.407},
    {"region":"apac","latency_ms":217.57,"uptime_pct":97.667},
    {"region":"apac","latency_ms":226.29,"uptime_pct":97.15},
    {"region":"apac","latency_ms":209.53,"uptime_pct":98.969},
    {"region":"apac","latency_ms":140.35,"uptime_pct":99.479},

    {"region":"emea","latency_ms":154.35,"uptime_pct":98.229},
    {"region":"emea","latency_ms":218.82,"uptime_pct":97.712},
    {"region":"emea","latency_ms":145.11,"uptime_pct":98.494},
    {"region":"emea","latency_ms":171.41,"uptime_pct":97.142},
    {"region":"emea","latency_ms":188.93,"uptime_pct":98.294},
    {"region":"emea","latency_ms":171.92,"uptime_pct":98.79},
    {"region":"emea","latency_ms":174.17,"uptime_pct":97.395},
    {"region":"emea","latency_ms":235.41,"uptime_pct":97.722},
    {"region":"emea","latency_ms":124.35,"uptime_pct":99.247},
    {"region":"emea","latency_ms":191.46,"uptime_pct":97.909},
    {"region":"emea","latency_ms":233.28,"uptime_pct":98.086},
    {"region":"emea","latency_ms":132.17,"uptime_pct":97.23},

    {"region":"amer","latency_ms":234.54,"uptime_pct":99.4},
    {"region":"amer","latency_ms":212.31,"uptime_pct":98.519},
    {"region":"amer","latency_ms":147.66,"uptime_pct":97.204},
    {"region":"amer","latency_ms":164.17,"uptime_pct":98.519},
    {"region":"amer","latency_ms":218.17,"uptime_pct":97.401},
    {"region":"amer","latency_ms":171.93,"uptime_pct":98.613},
    {"region":"amer","latency_ms":115.40,"uptime_pct":98.774},
    {"region":"amer","latency_ms":189.69,"uptime_pct":97.946},
    {"region":"amer","latency_ms":143.67,"uptime_pct":98.816},
    {"region":"amer","latency_ms":172.25,"uptime_pct":98.361},
    {"region":"amer","latency_ms":239.44,"uptime_pct":98.237},
    {"region":"amer","latency_ms":187.08,"uptime_pct":98.517},
]

class RequestBody(BaseModel):
    regions: list[str]
    threshold_ms: float

@app.post("/")
def metrics(req: RequestBody):
    result = {}

    for region in req.regions:
        rows = [r for r in DATA if r["region"] == region]

        latencies = [r["latency_ms"] for r in rows]
        uptimes = [r["uptime_pct"] for r in rows]

        result[region] = {
            "avg_latency": round(float(np.mean(latencies)), 2),
            "p95_latency": round(float(np.percentile(latencies, 95)), 2),
            "avg_uptime": round(float(np.mean(uptimes)), 3),
            "breaches": sum(
                1 for x in latencies
                if x > req.threshold_ms
            )
        }

    return result
