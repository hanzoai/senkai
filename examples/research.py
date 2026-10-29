"""Measure API creation latency and file private evidence using the real Research SDK."""
import os
import statistics
import time
import uuid
from hanzo_research import Benchmark, Research, Run, capture, now
from sekai_cookbook import Worlds

client, research = Worlds(), Research(api_key=os.getenv("RESEARCH_API_KEY"), org=os.getenv("RESEARCH_ORG"))
provenance = capture(device="api-client")
benchmark = Benchmark(id="sekai.alpha.api-create", title="Sekai alpha world creation HTTP latency",
                      version="1", metric="p50_ms", metrics=["p50_ms", "errors"])
run = Run(id="sekai-alpha-"+uuid.uuid4().hex, benchmark=benchmark.id, system="sekai-1-alpha",
          questions=10, answered=0, when=now(), visibility="private", trainable=False, publishable=False)
rows, latency = [], []
for i in range(10):
    start = time.perf_counter()
    try:
        client.create()
        elapsed = (time.perf_counter()-start)*1000
        latency.append(elapsed)
        rows.append(dict(item=i, ok=True, latency_ms=elapsed))
        run.answered += 1
    except Exception as error:
        rows.append(dict(item=i, ok=False, error_type=type(error).__name__))
run.ended = now()
if latency:
    run.put("all", "p50_ms", statistics.median(latency), n=len(latency), of=10)
run.put("all", "errors", 10-len(latency), n=10, of=10)
provenance.apply(run)
research.record(benchmarks=[benchmark], runs=[run])
research.upload_json_artifact("report", run.id, {"attempts": rows})
print("Recorded privately:", run.id, "; successful requests:", run.answered)
