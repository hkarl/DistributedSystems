# Homework: Chapter 8 — Distributed Event Systems & Publish/Subscribe

## Dependency Map

```
HW1 (P/S concepts & decoupling)
 └─► HW2 (subscription models & matching)
      └─► HW3 (0mq hands-on)
           └─► HW5 (Redis hands-on)
HW2 └─► HW4 (distributed routing & CBCB)
HW1 └─► HW6 (design & scalability trade-offs)
```

HW3 and HW5 are independent of each other and can be done in parallel
after completing HW1–HW2.

---

## Notes for Instructor

- HW1–HW2 are conceptual and can be assessed via written submission or
  in-class discussion.
- HW3 and HW5 require a running Python environment; 0mq and Redis can
  each be installed in minutes. Provide a Docker Compose file if lab
  infrastructure is constrained.
- HW4 is the most mathematically demanding; give students the CBCB and
  SIENA papers \cite{Carzaniga:2001:WideAreaEventNotification,
  Carzaniga:2004:ContentBasedNetworking} as reference reading.
- HW6 is open-ended design work; assess via a short written report
  (1–2 pages) or a 5-minute in-class presentation.
- Suggested timeline: HW1 after lecture 1 (P/S basics); HW2–HW3 after
  lecture 2 (matching + 0mq); HW4–HW5 after lecture 3 (CBCB + Redis);
  HW6 as a capstone.

---

## HW1 — Publish/Subscribe Concepts and Decoupling

**Learning goals:** Understand the three decoupling dimensions of P/S
systems and compare P/S with classical message-passing APIs.

**Tasks:**

1. *Decoupling dimensions.* A publish/subscribe system is said to
   provide decoupling in *time*, *identity*, and *space*. For each
   dimension, give:
   - a precise definition (one sentence), and
   - a concrete example from a real-world application domain
     (e.g., financial trading, social media, IoT sensor networks).

2. *Comparison with send/receive.* Consider a distributed system built
   with a classical blocking `send`/`receive` API.
   - Which of the three decoupling dimensions does it provide?
   - Which does it lack?
   - Justify each answer.

3. *No-memory semantics.* A strict P/S system does not deliver
   publications that occurred *before* a subscription was registered.
   - Describe a use case where this is acceptable.
   - Describe a use case where this is a serious problem, and suggest
     what mechanism could address it (no implementation needed).

---

## HW2 — Subscription Models and Matching

**Learning goals:** Understand and compare topic-based, subject-based,
and content-based subscription models; reason about matching rules.

**Tasks:**

1. *Topic-based matching.* Given the following publications and
   subscriptions, state for each (sub, pub) pair whether it matches and
   why.

   | ID  | Type | Topics                  |
   |-----|------|-------------------------|
   | P1  | pub  | {sports, football, UEFA}|
   | P2  | pub  | {finance, EUR/USD}      |
   | S1  | sub  | {sports, basketball}    |
   | S2  | sub  | {finance}               |
   | S3  | sub  | {sports}                |

2. *Subject-based matching.* Using the TIBCO/Rendezvous-style rules
   from the lecture, determine whether each publication matches the
   subscription. Justify each answer.

   - Subscription: `{ (price, [50, 150]), (currency, "EUR") }`
   - P1: `{ (price, 99), (currency, "EUR"), (ticker, "ACME") }`
   - P2: `{ (price, 200), (currency, "EUR") }`
   - P3: `{ (price, 99), (currency, "USD") }`

3. *Content-based subscriptions.* A subscriber wants to receive any
   news article whose body contains the phrase "interest rate" and was
   published after 2023. Write a predicate in the SIENA-style
   conjunction-of-constraints notation that captures this requirement.
   State explicitly what metadata fields you assume the publication
   carries.

4. *Trade-offs.* Fill in the table below with "Low/Medium/High" and a
   one-sentence justification.

   | Criterion             | Topic-based | Subject-based | Content-based |
   |-----------------------|-------------|---------------|---------------|
   | Expressiveness        |             |               |               |
   | Routing complexity    |             |               |               |
   | Ease of implementation|             |               |               |

---

## HW3 — Hands-On: 0mq Pub/Sub

**Learning goals:** Implement and evaluate a simple pub/sub system
using ZeroMQ; observe the effect of subscriber-side filtering.

**Prerequisites:** Python ≥ 3.9, `pyzmq` (`pip install pyzmq`).

**Tasks:**

1. *Basic pub/sub.* Implement a publisher that continuously emits
   messages on two topics, `"weather"` and `"news"`, with random
   payloads. Implement two subscribers: one that subscribes to
   `"weather"` only, one that subscribes to both topics. Run all three
   in separate terminals and confirm correct message delivery.

2. *Observe subscriber-side filtering.* Add a message counter to the
   publisher. After 100 published messages:
   - How many messages did each subscriber *receive*?
   - How many messages did each subscriber *process* (i.e., passed the
     local filter)?
   - Explain the difference. What does this imply for network bandwidth
     at scale?

3. *Multiple publishers.* Extend the setup so that two publishers emit
   on `"weather"` and one subscriber subscribes to both. Demonstrate
   that the subscriber receives from both publishers. What topology does
   0mq create in this case?

4. *Reflection.* The 0mq guide describes several patterns for scaling
   up pub/sub (e.g., a forwarder proxy). Sketch (in words or a
   diagram) how a forwarder proxy addresses the subscriber-side
   filtering problem. Does it fully solve it?

---

## HW4 — Distributed Event Routing and CBCB

**Learning goals:** Understand content-based routing; reason about the
covering relation and CBCB routing-table construction.

**Reference:** Carzaniga et al., "A Routing Scheme for Content-Based
Networking" (2004); SIENA paper (2001).

**Tasks:**

1. *Covering relation.* Consider the following predicates over a single
   attribute `price` (a real number):
   - p1: `price ∈ [0, 200]`
   - p2: `price ∈ [50, 150]`
   - p3: `price ∈ [100, 300]`
   - p4: `price > 0`

   For each ordered pair (pA, pB), determine whether pA covers pB
   (write pB ≺ pA). Draw the partial order as a Hasse diagram.

2. *Routing table construction.* A CBCB network has four servers
   A, B, C, D connected in a line: A—B—C—D. The following
   subscriptions arrive:
   - At A: S1 = `price ∈ [10, 50]`
   - At D: S2 = `price ∈ [40, 100]`
   - At C: S3 = `price ∈ [0, 200]`

   Show the routing table (covering predicate per interface) at node B
   after all subscriptions have propagated. State which publications
   would be forwarded by B towards A, towards C, and towards D.

3. *Forwarding decision.* Using the routing table from task 2, for each
   of the following publications arriving at B, state to which
   neighbours B forwards the message and why.
   - M1: `price = 45`
   - M2: `price = 75`
   - M3: `price = 5`

4. *Gossiping alternative.* Gossiping does not build a routing
   structure. Explain one advantage and one disadvantage of gossiping
   compared to CBCB for a large-scale pub/sub system.

---

## HW5 — Hands-On: Redis Pub/Sub

**Learning goals:** Use Redis pub/sub from Python; understand
channel-based and pattern-based subscriptions; identify limitations.

**Prerequisites:** Redis server running locally (or via Docker:
`docker run -p 6379:6379 redis`), `pip install redis`.

**Tasks:**

1. *Channel subscription.* Adapt the lecture example so that:
   - Publisher sends 10 messages on channel `"alerts"` and 10 messages
     on channel `"logs"`.
   - Subscriber A listens on `"alerts"` only.
   - Subscriber B listens on both `"alerts"` and `"logs"`.
   Run the code and report which messages each subscriber receives.

2. *Pattern subscription.* Modify Subscriber B to use `PSUBSCRIBE`
   with the pattern `"al*"` instead of explicit channel names.
   - Does B still receive messages on `"alerts"`?
   - What happens if the publisher also sends on channel `"alpha"`?
   - What is the risk of overly broad glob patterns?

3. *No persistence.* Start Subscriber A, then stop it. While it is
   offline, have the publisher send 5 messages on `"alerts"`. Restart
   Subscriber A.
   - Does it receive the missed messages? Why or why not?
   - What Redis feature (introduced in Redis 5.0) would address this?
     (Hint: look up Redis Streams.)

4. *Comparison.* Fill in the table comparing 0mq pub/sub and Redis
   pub/sub on the following criteria:

   | Criterion              | 0mq pub/sub | Redis pub/sub |
   |------------------------|-------------|---------------|
   | Filtering location     |             |               |
   | Broker required        |             |               |
   | Persistence support    |             |               |
   | Pattern subscriptions  |             |               |
   | Ease of horizontal scale|            |               |

---

## HW6 — Design: Scalable Pub/Sub for a Real-World Scenario

**Learning goals:** Apply pub/sub concepts to a realistic design
problem; reason about trade-offs across subscription models, filtering
location, and distribution strategies.

**Scenario:** A smart-city platform collects sensor readings from
50,000 IoT devices (air quality, traffic, noise). Each reading is
tagged with `device_id`, `location` (GPS coordinates), `sensor_type`,
`timestamp`, and a numeric `value`. City departments (environment,
transport, emergency services) subscribe to relevant events; a single
department may have thousands of active subscriptions.

**Tasks:**

1. *Subscription model choice.* Which subscription model (topic-based,
   subject-based, or content-based) is most appropriate? Justify your
   choice, considering the richness of the metadata and the diversity
   of subscriber interests.

2. *Filtering location.* Should filtering happen at the broker, at the
   subscriber, or in a hybrid fashion? Consider the number of devices,
   the number of subscriptions, and the network bandwidth between
   devices and the broker.

3. *Distribution strategy.* The platform must handle 50,000 events per
   second at peak. Describe a distributed matching architecture (you
   may reference CBCB, flooding, gossiping, or another approach) that
   can scale to this load. Include:
   - How subscriptions are stored/routed.
   - How publications are forwarded.
   - How failures of individual matching servers are handled.

4. *Memory semantics.* An emergency-services subscriber may be offline
   for up to 30 minutes during a network partition. What memory
   semantics should the platform provide for this subscriber? Compare
   strict P/S (no memory) with a message-queue approach.

5. *Reflection.* Identify two design tensions (e.g., expressiveness vs.
   routing complexity) in your proposed architecture and explain how
   you resolved them.
