# Chapter 4 — Improving Client/Server Systems: Homework Assignments

---

### Homework 1 — Availability Calculations and Stochastic Models

**Learning goal:** Apply the MTTF/MTTR/availability framework to realistic scenarios; understand
the effect of redundancy on availability.

**Tasks:**

1. A web server has MTTF = 2,000 hours and MTTR = 4 hours.
   - Compute its steady-state availability.
   - How many minutes of downtime per year does this correspond to?
   - To reach "five nines" (99.999%) availability, by what factor would you need to reduce MTTR
     (assuming MTTF stays constant)?

2. A data center runs 5,000 SSDs, each with MTTF = 2,000,000 hours, failing independently.
   - Compute the expected time to the first SSD failure.
   - Does the result surprise you?  What does it imply for backup strategies?

3. Suppose you deploy two independent copies of the web server from Task 1 in active/active
   configuration.  The combined system fails only when *both* copies have failed simultaneously.
   Assume failures are independent.
   - Model the combined system's reliability.  What is the combined MTTF, approximately?
   - What is the combined availability?
   - Discuss: do real deployments achieve this theoretical gain?  What assumption typically breaks?

4. **Reflection (≤ 100 words):** The lecture states that exponential lifetime distributions have a
   *constant* hazard rate.  Most real hardware follows a bathtub curve instead.  What does this
   imply for the validity of MTTF as a single-number summary of reliability?

---

### Homework 2 — Load Balancing Policies

**Learning goal:** Implement and compare different load balancing policies; experience the "power
of two choices" result empirically.

**Tasks:**

1. Simulate a server farm with N = 10 workers and M = 10,000 requests using the following
   policies.  For each policy, record the maximum load any single worker received at the end of the
   simulation:
   - **Round-robin**: assign request i to worker i mod N.
   - **Random**: assign each request to a uniformly random worker.
   - **Power of two choices**: pick 2 workers at random; assign to the less loaded one.

   Run each simulation 100 times and report mean and 95th-percentile maximum load.

2. Repeat with N = 100 workers and M = 100,000 requests.  Does the relative advantage of
   "power of two" grow, shrink, or stay the same as N increases?  Relate your observation to the
   theoretical results from the lecture (O(log log n / log d)).

3. Now model *sticky sessions*: a client always returns to the same worker after the first
   request.  Assume 1,000 clients each make 10 requests.  How does this constraint affect your
   ability to use round-robin or power-of-two?  What policy would you use instead?

---

### Homework 3 — Consistent Hashing Implementation

**Learning goal:** Understand why simple modulo hashing breaks under server churn; implement
consistent hashing and observe its stability.

**Tasks:**

1. Implement simple modulo hashing in Python:
   - Hash function: `hashlib.md5(key.encode()).hexdigest()` converted to an integer, then `% N`.
   - Generate 10,000 random keys; assign each to a server for N = 4 servers.
   - Add a 5th server (N = 5).  Recompute assignments and count how many keys moved.
   - Report the fraction that moved.  Compare to the theoretical expectation.

2. Implement consistent hashing:
   - Represent the ring as a sorted list of `(hash_value, server_name)` pairs.
   - Each server places **100 virtual nodes** (points) on the ring, using
     `hashlib.md5(f"{server}#{i}".encode()).hexdigest()` as the hash.
   - Assignment: for each key, find the nearest point clockwise; the owning server is that
     point's server.
   - Use the same 10,000 keys and the same 4→5 server experiment.  How many keys moved this
     time?

3. Measure load distribution: with 4 servers and 10,000 keys, report the min, max, and
   standard deviation of keys per server for both hashing schemes.  Do the 100 virtual nodes
   per server achieve a reasonably uniform distribution?

4. **Reflection (≤ 100 words):** Memcached uses consistent hashing for its distributed cache.
   When a server fails in Memcached, the cached data on that server is *not* preserved — clients
   simply get cache misses.  Why is this acceptable for a cache but would not be acceptable for
   a persistent database?

---

### Homework 4 — Kubernetes Load Balancing and DNS (Investigation)

**Learning goal:** Trace how an actual production system implements the load-balancing mechanisms
from the lecture; connect theory to Kubernetes internals.

*This homework uses a local Kubernetes cluster (Minikube or kind).  If you do not have one, the
reading tasks still apply.*

**Tasks:**

1. **Mechanism identification (reading):**  Study how Kubernetes routes traffic from a Service's
   ClusterIP to its backing Pods.  Key sources:
   - The `kube-proxy` iptables/DNAT approach (see the Scalingo blog post linked in the lecture
     slides and the Kubernetes network model documentation).
   - The `IPVS` mode as an alternative.

   Answer: which of the four load balancing mechanisms from the lecture
   (reply-via-frontend, redirect, rewrite, DNS-based) most closely describes what kube-proxy does?
   Justify your answer in 3–4 sentences.

2. **DNS investigation (hands-on):**  Deploy a simple Service (e.g., the `itemstore` service from
   the lab) in Minikube.
   - From inside a Pod: run `nslookup <service>.<namespace>.svc.cluster.local`.  What IP does it
     resolve to?  Is it a Pod IP or the ClusterIP?
   - From outside the cluster (your laptop): can you resolve the same name?  Why or why not?
   - The lecture asks: does DNS-based load balancing in Kubernetes suffer from the classic DNS-LB
     problem (stale cached records pointing to dead servers)?  Explain how Kubernetes sidesteps it.

3. **eBPF / Cilium (reading):**  The lecture mentions eBPF-based load balancing (Cilium) as a
   fancier alternative to iptables.  In 3–5 sentences, explain what the main limitation of the
   iptables approach is and how eBPF addresses it.

---

### Homework 5 — Cache Consistency Protocols

**Learning goal:** Experience the trade-off between cache freshness, server load, and
implementation complexity.

**Tasks:**

1. **TTL-based cache:** Implement a simple key/value cache in Python with a configurable TTL.
   When a key is requested:
   - If present and not expired: return the cached value.
   - If absent or expired: fetch from the "origin" (simulate with a function that increments a
     counter each time it is called) and cache the result.

   Simulate 1,000 requests for the same key with TTL = 10 s; advance simulated time by 1 s per
   request.  Report: how many times was the origin called?

2. **Conditional GET / freshness check:** Extend your cache so that on expiry it sends a
   conditional request (simulated: compare a version counter from the origin with the one stored
   in the cache).  If the origin version has not changed, the cache entry is refreshed *without*
   replacing the value.  Count: how many full re-fetches vs. freshness checks occurred?

3. **Server-push invalidation:** Now flip the model: the origin calls `cache.invalidate(key)`
   whenever the value changes.  Simulate 1,000 requests where the origin updates every 50
   requests.  Report cache hit rate and staleness (how often did a client read a value that had
   already changed at the origin but had not yet been invalidated)?

4. **Comparison table:** Fill in the following for each of the three approaches:

   | Approach | Extra origin load per hit | Handles sudden bursts? | Complexity |
   |----------|--------------------------|------------------------|-----------|
   | TTL-based | | | |
   | Conditional GET | | | |
   | Server push | | | |

---

### Homework 6 — Content Delivery Networks: Design and Analysis

**Learning goal:** Understand how CDNs combine the mechanisms from the chapter (caching, DNS
redirection, reverse proxies) into a coherent architecture.

**Tasks:**

1. A popular news site publishes a breaking-news article that suddenly receives 500,000 requests
   per minute globally.  The origin server can handle 10,000 requests per minute.  Describe how a
   CDN would serve this traffic.  Your answer must mention:
   - How the CDN edge servers are selected for each client (DNS-based redirection, anycast, …)
   - What happens on the first request to an edge server that has not yet cached the article
     (*cache miss* / *cache fill*)
   - How the CDN ensures that an updated version of the article reaches all edge servers

2. **DNS-based redirection in a CDN (sequence diagram):** Draw a sequence diagram (ASCII or
   hand-drawn) showing:
   - Client resolves `www.news-cdn.com`
   - CDN's authoritative DNS responds with the IP of the nearest edge server
   - Client fetches the article from the edge server (cache hit path)

   Include the TTL value on the DNS response and explain why CDNs typically use very short TTLs
   (30–60 s) compared to ordinary DNS records (24 h).

3. **Forward vs. reverse proxy:** The lecture distinguishes forward proxies (act on behalf of
   clients) from reverse proxies (act on behalf of servers).  For each of the following scenarios,
   state which type is in use and why:
   - An HPI student's laptop is configured to route all HTTP traffic through a campus proxy.
   - Cloudflare sits in front of a small e-commerce site and absorbs DDoS traffic.
   - A developer runs a local nginx server that fans out requests to three backend services.

4. **Reflection (≤ 100 words):** The lecture says CDNs have evolved from "coordinated caches"
   into "application-delivery networks".  Give one concrete example of a CDN capability that goes
   beyond simple caching, and explain what distributed-systems challenge it introduces.

---

## Dependency Map

```
Slides: Fault/Error/Failure taxonomy, MTTF/MTTR/availability
    → Quiz 1, 2, 3
    → Homework 1 (availability calculations)

Slides: Redundancy, standby categories
    → Quiz 4
    → Homework 1 task 3 (active/active availability)

Slides: Failure detection
    → Quiz 5

Slides: Load balancing mechanisms (naive, via-FE, redirect, DNS)
    → Quiz 6
    → Homework 4 (Kubernetes LB investigation)

Slides: LB policy, balls-in-bins, power of two choices
    → Quiz 7
    → Homework 2 (LB policy simulation)

Slides: Simple hashing, consistent hashing
    → Quiz 8, 9
    → Homework 3 (consistent hashing implementation)

Slides: Cache consistency, HTTP proxies
    → Quiz 10
    → Homework 5 (cache consistency protocols)

Slides: CDN, DNS, proxy
    → Homework 6 (CDN design and analysis)
```

Homework 3 (consistent hashing) builds on the serialization/hashing intuition from Chapter 1.
Homework 4 (Kubernetes) extends the lab assignments and the Chapter 3 microservices discussion.
Homework 5 (cache consistency) sets the stage for the consistency chapter later in the course.

---

## Notes for the Instructor

- **Quiz 2** (10,000 disks, expected first failure in 50 hours) reliably shocks students.  It
  is worth taking 2 minutes to do the calculation live.  Follow up: "So you have a new disk fail
  roughly every two days — what does your backup strategy need to look like?"

- **Quiz 7** (power of two choices) pairs directly with Homework 2.  Students who do the
  simulation first often find the empirical O(log log n) improvement hard to believe; the quiz
  makes them commit to an answer before seeing the data.

- **Homework 3** (consistent hashing) works best if students implement it from scratch rather
  than using a library.  The act of implementing the virtual-node ring makes the "only 1/(N+1)
  keys move" property viscerally clear.

- **Homework 4** (Kubernetes) can be split: the reading tasks are individual, the hands-on part
  works well in pairs sharing a Minikube cluster.

- **Quiz 10** (server-push cache invalidation) is a good bridge to the consistency chapter.
  Ask: "What if the server is unavailable when it wants to push an invalidation — what happens
  to the cache's correctness?"
