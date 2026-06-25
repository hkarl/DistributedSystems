# Homework Assignments — Chapter 6: Peer-to-Peer Networks

---

## Dependency Map

```
HW1 (Strawman DHT simulation)
  └─► HW2 (Chord finger tables — extend HW1)
        └─► HW3 (Kademlia XOR routing — compare with HW2)

HW4 (Plaxton routing table construction) — standalone

HW5 (BitTorrent piece-selection analysis) — standalone

HW6 (Churn and consistent hashing design) — builds on HW1/HW2 concepts
```

HW1 and HW2 are tightly coupled and should be attempted in order. HW3 can follow after HW2 or be done independently if students are comfortable with XOR arithmetic. HW4–HW6 are largely standalone.

---

## Notes for Instructor

- HW1–HW3 exercise the core DHT routing concepts from the lecture; they are appropriate for a weekly homework set after the DHT sections.
- HW4 works well as a pen-and-paper exercise in a tutorial session before being submitted.
- HW5 is intentionally more analytical/reading-based; it suits a week where students are reading primary sources.
- HW6 is a design exercise; evaluate for reasoning quality and trade-off awareness rather than a single correct answer.
- Skeleton code for HW1–HW3 is provided in `homework_hints_ch06.md`.

---

## HW1 — Implementing and Analysing a Strawman Ring DHT

**Topic:** Distributed Hash Tables, ring routing, complexity

**Learning goals:**
- Understand the structure of a ring-based DHT.
- Measure empirically the O(N) routing overhead of the strawman design.

**Task:**

Implement a simulation of the strawman DHT described in the lecture:

1. Represent N nodes as Python objects arranged in a sorted list that forms a logical ring (modulo maximum GUID). Each node stores only a reference to its single successor.
2. Implement `put(key, value)` and `get(key)` operations. A `get` starts at a random node and forwards around the ring until it reaches the node responsible for the key. Count the number of forwarding hops.
3. Simulate the following scenario:
   - Create rings of size N = 10, 50, 100, 500, 1000.
   - For each ring size, issue 1000 random `get` requests starting from random nodes.
   - Record the average, minimum, and maximum hop counts.
4. Plot average hop count vs. N. Does the empirical result match the theoretical O(N) complexity? Discuss briefly (3–5 sentences).

**Deliverables:**
- Python source file `hw1_strawman_dht.py`
- A plot (PNG or PDF) of hop count vs. N
- A short written discussion (max one page)

**Hints:** Use `random.randint(0, 2**16 - 1)` for GUIDs. Represent "responsible node" as the node with the smallest GUID greater than or equal to the key (wrap around for the maximum node).

---

## HW2 — Chord Finger Tables and Logarithmic Routing

**Topic:** Chord DHT, finger tables, logarithmic search

**Learning goals:**
- Construct Chord finger tables correctly.
- Observe the logarithmic reduction in hop count compared to HW1.

**Task:**

Extend your HW1 simulation to implement Chord-style routing:

1. Use m = 16 bits for GUIDs (ring size 2^16).
2. For each node n, compute its finger table: the i-th entry (i = 1 … m) points to the node responsible for GUID (n + 2^(i-1)) mod 2^m. Store at most m finger entries per node.
3. Implement Chord's `find_successor(key)` algorithm: at each hop, forward to the finger table entry whose GUID is the largest that does not exceed the key (in clockwise order).
4. Repeat the measurement from HW1:
   - Ring sizes N = 10, 50, 100, 500, 1000 (GUIDs drawn uniformly at random from [0, 2^16)).
   - 1000 random `get` requests per ring size.
   - Record average hop counts.
5. Plot both the strawman (HW1) and Chord average hop counts on the same graph. Add a reference curve for log2(N).
6. Discuss: At what ring size does the difference become practically significant? What are the costs of the larger finger tables?

**Deliverables:**
- Python source file `hw2_chord.py` (may import from `hw1_strawman_dht.py`)
- Combined plot (PNG or PDF)
- Written discussion (max one page)

**Hints:** When selecting the next hop in Chord, be careful about the circular comparison (clockwise). A helper `in_range(key, start, end)` that handles wraparound is strongly recommended.

---

## HW3 — Kademlia XOR Routing

**Topic:** Kademlia DHT, XOR metric, routing table structure

**Learning goals:**
- Understand why the XOR metric is a valid distance metric (symmetry, triangle inequality).
- Build and query a Kademlia-style routing table.

**Task:**

1. **XOR metric properties (pen and paper):** Prove that the XOR metric d(x, y) = x XOR y (interpreted as a non-negative integer) satisfies:
   - d(x, y) = 0 if and only if x = y
   - d(x, y) = d(y, x) (symmetry)
   - d(x, z) ≤ d(x, y) + d(y, z) (triangle inequality)
   Write your proof in the submitted document (max half a page per property).

2. **Routing table construction (implementation):** For m = 8 bits, implement a Kademlia routing table for a node with a given GUID. The table has m "k-buckets", one per bit position. Bucket i holds nodes whose GUID shares the first (m - i - 1) bits with the local node but differs in bit i (from the most-significant bit). Limit each bucket to k = 3 entries.

3. **Routing simulation:** Implement `find_node(target)`: at each step, pick the known node with the smallest XOR distance to the target and ask it for its k closest known nodes; add any new ones to the routing table; stop when the closest node is the local node or the target is found. Simulate with N = 100 randomly placed nodes, 200 random lookups, and report average hop count.

4. **Comparison:** Briefly compare the Kademlia routing table structure and its XOR metric to Chord finger tables and the Chord clockwise metric. What are the practical advantages of symmetry in Kademlia? (Max half a page.)

**Deliverables:**
- Handwritten or typeset proof (PDF)
- Python source file `hw3_kademlia.py`
- Written comparison (max one page total for parts 1 and 4)

---

## HW4 — Plaxton Routing Table Construction

**Topic:** Plaxton routing, prefix-based routing tables

**Learning goals:**
- Construct a Plaxton routing table by hand.
- Trace a forwarding path step by step.

**Task:**

Work with 8-bit GUIDs written as two hexadecimal digits (e.g., 0x00 to 0xFF).

1. **Setup:** Consider a small overlay network with the following nodes (GUIDs given in hex): `3A`, `3F`, `4B`, `4C`, `72`, `A1`, `B5`, `C0`. Assume node `3A` is your local node.

2. **Build the routing table for node `3A`:**
   - Row 0: one entry per hex digit (0–F) for nodes whose first digit differs from `3`.
   - Row 1: one entry per hex digit (0–F) for nodes whose first digit equals `3` but second digit differs from `A`.
   - Fill in the entries using the nodes listed above. If no node exists for a digit, leave the cell empty.

3. **Trace a forwarding path** from node `3A` to destination GUID `B5`:
   - At each step, state which routing table row and column you use and which node you forward to.
   - How many hops does it take?

4. **Compare** with the strawman ring DHT: for 8-bit GUIDs and 8 nodes, what is the expected hop count for the strawman design vs. Plaxton routing? Discuss the trade-off between routing table size and hop count.

**Deliverables:**
- Completed routing table (table format, hand-drawn or typeset)
- Forwarding trace (bullet list or table)
- Written comparison paragraph (max half a page)

---

## HW5 — BitTorrent Piece Selection and Swarm Dynamics

**Topic:** BitTorrent, rarest-first strategy, swarming

**Learning goals:**
- Understand how piece-selection policy affects swarm health.
- Reason about incentive mechanisms (tit-for-tat, choking).

**Task:**

1. **Reading:** Read sections 2 and 3 of the original BitTorrent specification (https://www.bittorrent.org/beps/bep_0003.html) and the paper "Incentives Build Robustness in BitTorrent" by Bram Cohen (2003). Both are freely available online.

2. **Rarest-first analysis:** Suppose a swarm has 5 peers (plus 1 seeder) and a file split into 8 pieces. Construct a scenario (i.e., assign a piece availability matrix) in which sequential downloading by all leechers would cause one piece to become unavailable if the seeder leaves. Show that rarest-first downloading avoids this problem in your scenario.

3. **Tit-for-tat simulation (lightweight):** Implement a simplified round-based simulation in Python:
   - N = 10 peers, each starting with 0 pieces. 1 seeder with all pieces.
   - Each round: peers unchoke their top-3 uploaders (by bytes received last round); one optimistic unchoke to a random choked peer.
   - Simulate 20 rounds. Track how many pieces each peer has over time.
   - Plot piece count per peer over rounds.
   - Identify any free-riders (peers that download but never upload) and show what happens to them under tit-for-tat.

4. **Discussion:** In 3–5 sentences, explain why BitTorrent's incentive mechanism is not perfectly cheat-proof and what real-world attacks have been demonstrated against it.

**Deliverables:**
- Python source file `hw5_bittorrent_sim.py`
- Plot (PNG or PDF)
- Written answers to parts 2 and 4 (max one page total)

---

## HW6 — Churn, Replication, and Consistent Hashing Design

**Topic:** Churn, node failure, consistent hashing, replication

**Learning goals:**
- Reason about the impact of churn on DHT availability.
- Design a replication strategy using consistent hashing.

**Task:**

This is a design and analysis exercise; no implementation is required, but you should support your arguments with calculations.

1. **Churn model:** Assume a DHT with N = 1000 nodes. Each node independently fails (permanently) with probability p = 0.01 per hour, and a new node joins with probability q = 0.01 per hour per existing node (so the expected ring size stays roughly constant). Estimate the expected number of node departures per hour. How many routing table entries are invalidated per departure in Chord (assume each node appears in O(log N) other nodes' finger tables)?

2. **Replication strategy:** Design a replication strategy for the DHT: each key-value pair is stored on R successor nodes in the ring (in addition to the primary responsible node).
   - What value of R ensures that a given key-value pair survives an hour with probability at least 99.9%, given the failure rate above? Show your calculation.
   - What is the storage overhead factor?

3. **Consistent hashing with virtual nodes:** Explain how assigning V virtual node IDs per physical node (consistent hashing tokens) reduces the data movement when a physical node joins or leaves. Estimate the fraction of keys that must be moved when a single physical node leaves, as a function of N and V.

4. **Trade-off discussion:** Write a half-page discussion covering:
   - The tension between replication factor R and storage cost.
   - The tension between virtual node count V and routing table size.
   - Under what workload conditions would you increase R vs. V?

**Deliverables:**
- Written calculations and derivations for parts 1–3 (clearly laid out, max 2 pages)
- Discussion for part 4 (max half a page)
