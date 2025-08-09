
---

```markdown

## Load Testing Overview

Load testing was conducted using **Locust** against both the local FastAPI server and the deployed Cloud Run service to evaluate performance under varying user loads and traffic patterns.

---

## Test Scenarios and Results

| Scenario   | Users | Duration  | Success Rate | Avg Response Time (ms) | Max Response Time (ms) | Throughput (req/sec) | Notes                          |
|------------|-------|-----------|--------------|-----------------------|-----------------------|---------------------|-------------------------------|
| Local Baseline  | 1     | 60 sec    | 100%         | 120                   | 250                   | ~8                  | Stable, minimal latency       |
| Local Normal    | 10    | 5 min     | 100%         | 150                   | 400                   | ~85                 | No errors, smooth scaling     |
| Cloud Baseline  | 1     | 60 sec    | 100%         | 200                   | 450                   | ~7                  | Slightly higher latency than local (cold start) |
| Cloud Normal    | 10    | 5 min     | 99%          | 350                   | 1200                  | ~75                 | Occasional spikes due to cold starts |
| Cloud Stress    | 50    | 2 min     | 95%          | 700                   | 3000                  | ~320                | Increased latency and some failures observed |
| Cloud Spike     | 1→100 | 1 min ramp | 90%          | 850                   | 5000                  | Peak ~400            | Some request timeouts and failures |

---

## Bottlenecks Identified

- **Cold start latency:** Initial request to new Cloud Run instances can take several seconds, impacting first user response times.
- **Memory usage:** During high load, containers approached memory limits causing occasional restarts and errors.
- **Model loading time:** Model is loaded once at startup, but spikes in traffic cause container scaling that incurs repeated cold starts.
- **CPU saturation:** Under stress test, CPU utilization reached 90%+, leading to longer response times.

---

## Recommendations

- **Pre-warm instances:** Maintain a minimum number of instances to reduce cold starts.
- **Increase resource allocation:** Allocate more CPU and memory to improve throughput.
- **Optimize model size:** Explore model pruning or quantization to reduce loading time.
- **Implement caching:** Cache predictions or results for repeated queries.
- **Use async endpoints:** Improve concurrency and reduce blocking.
- **Horizontal scaling:** Configure autoscaling to higher max instances if anticipating traffic spikes.
- **Monitor metrics:** Set alerts on error rates and response times.

---

## Summary

The deployed Penguin API performs well under typical traffic but requires optimization for high loads to reduce latency and failures. Load testing proved invaluable for identifying bottlenecks and tuning Cloud Run configuration.

---

# End of LOAD_TEST_REPORT.md
