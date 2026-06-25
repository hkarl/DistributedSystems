# Homework — Chapter 11: Distributed Storage

## Dependency Map

```
HW1 (Consistency models: ranking)
  └─► HW2 (Quorum arithmetic)
        └─► HW3 (CAP + design trade-offs)

HW4 (Client-centric guarantees: trace analysis)   [independent]

HW5 (CRDT design)                                 [independent]

HW6 (etcd hands-on)                               [requires basic Linux CLI]
```

## Notes for Instructor

- **HW1** is purely conceptual and suitable as a warm-up before the lecture ends.
- **HW2** is mathematical but elementary; nudge students to think about what "overlap" means physically.
- **HW3** combines CAP theory with engineering judgment; intentionally open-ended — expect a range of quality answers.
- **HW4** requires careful reading of a short execution trace; the point is to force students to apply the formal definitions.
- **HW5** asks students to *design* a CRDT rather than just describe one from the slides. It is the hardest homework and can be assigned as an optional challenge or as a pair exercise.
- **HW6** is practical and short; requires Docker or a local Go installation. Provide the etcd binary or a Docker image URL. Students unfamiliar with key/value stores benefit greatly from hands-on use.

---

## HW1 — Consistency Model Ranking

**Topic:** Data-centric consistency models — comparative strength

**Background.** The lecture introduced several consistency models: strict consistency, linearizability, sequential consistency, causal consistency, FIFO consistency, and eventual consistency.

**Tasks.**

1. Arrange the six models above in a strict partial order from **strongest** (most restrictive for the data store, most convenient for the programmer) to **weakest**. Draw a Hasse diagram showing which models are strictly stronger than others. Mark any models that are **incomparable** (neither is stronger than the other).

2. For each model, name **one real-world scenario** in which that model is the *natural minimum requirement* and explain in one sentence why a weaker model would not suffice.

3. Strict consistency is described as "impossible to implement" in a distributed system. Write a short proof sketch (3–5 sentences, no formal notation needed) explaining *why* it is impossible, referencing the absence of a global clock and the finite speed of signal propagation.

---

## HW2 — Quorum Arithmetic

**Topic:** Quorum-based consistency protocols

**Background.** A quorum-based protocol over N replicas uses a write quorum N_W and a read quorum N_R satisfying:

- N_R + N_W > N  (read–write overlap)
- N_W > N / 2    (write–write overlap, prevents split-brain)

**Tasks.**

1. For **N = 7**, find *all* pairs (N_R, N_W) with 1 ≤ N_R, N_W ≤ 7 that satisfy both conditions simultaneously. Present your answer in a table.

2. Identify the pair that minimises the **total quorum size** N_R + N_W. Explain what this choice optimises for in practice.

3. Identify the pair that minimises **N_W** while still satisfying both conditions. Explain the practical trade-off compared to your answer in (2).

4. Consider the **Read-One Write-All (ROWA)** scheme (N_R = 1, N_W = N). Does ROWA satisfy both quorum conditions? What is the advantage and the disadvantage of ROWA compared to the pair you found in (2)?

5. Suppose 2 of the 7 replicas crash and become unreachable. What is the *minimum* value of N_W such that write operations are still possible among the surviving replicas, while still guaranteeing that the next read (from surviving replicas) returns the up-to-date value?

---

## HW3 — CAP Theorem: Analysis and Design Trade-offs

**Topic:** CAP theorem — practical implications

**Background.** The CAP theorem states that a distributed system can simultaneously guarantee at most two of: **Consistency** (here: linearizability), **Availability**, and **Partition tolerance**. A network partition means that some nodes cannot communicate with others.

**Tasks.**

1. Explain in your own words what a **network partition** is and why a real-world internet-scale system *cannot* simply choose to ignore partition tolerance. Give a concrete example of a partition event.

2. For each of the following systems, state which two of the three CAP properties the system *chooses* to prioritise and explain the consequence of giving up the third:
   - A banking system processing money transfers
   - A social-media "like" counter
   - A DNS resolver

3. A common misconception is that "CA systems" (consistent + available, not partition-tolerant) are a real and useful design choice. Argue **for or against** this claim. (Hint: what happens to a CA system *when* a partition occurs?)

4. The CAP theorem applies during a partition event. When there is *no* partition, a system can be both consistent and available. Describe one protocol or technique that allows a system to provide strong consistency during normal operation and gracefully degrade to availability during a partition. Name one real system that follows this approach.

---

## HW4 — Client-Centric Consistency: Trace Analysis

**Topic:** Client-centric consistency guarantees (monotonic reads, read-your-writes, monotonic writes, writes-follow-reads)

**Background.** Consider a distributed key-value store with two replicas, L1 and L2. A single mobile client C performs the following operations in order, with the indicated replica connections:

```
t=1  C connects to L1, writes x = "hello"       [W1 at L1]
t=2  C connects to L2, reads x, gets x = ""     [R2 at L2, got old value]
t=3  C connects to L2, reads x, gets x = "hello"[R3 at L2]
t=4  C connects to L1, writes x = "world"       [W4 at L1]
t=5  C connects to L2, reads x, gets x = "hello"[R5 at L2]
t=6  C connects to L1, reads x, gets x = "hello"[R6 at L1, but W4 not yet applied!]
```

**Tasks.**

1. Identify **all** client-centric guarantee violations in the trace above. For each violation, name the guarantee, cite the relevant operations by their label (e.g., W1, R2), and explain in one sentence why it is a violation.

2. For the **monotonic-reads** guarantee specifically: what mechanism could the system use to prevent the violation you identified? Describe it in terms of the session token approach outlined in the lecture.

3. Suppose the system is upgraded to provide **causal consistency** (data-centric). Which of the four client-centric guarantees does causal consistency subsume, and which must still be explicitly enforced?

---

## HW5 — CRDT Design

**Topic:** Conflict-Free Replicated Data Types

**Background.** A state-based CRDT is defined by a local state type, an `Update` function, and a `Merge` function that is commutative, associative, and idempotent.

**Tasks.**

1. Define a **Grow-Only Set (G-Set)** CRDT formally by specifying:
   - The state type
   - `Initialize`
   - `Update(state, element)` — adds one element
   - `Merge(state_A, state_B)` — merges two states
   Prove (informally, in a few sentences each) that your `Merge` is commutative, associative, and idempotent.

2. A **Two-Phase Set (2P-Set)** extends the G-Set to allow element removal by using two G-Sets: an *add set* A and a *remove set* (tombstone set) R. An element is in the 2P-Set if and only if it is in A but not in R. Define `Update_add`, `Update_remove`, and `Merge` for the 2P-Set. What constraint must be respected between add and remove operations to keep the semantics consistent?

3. Consider building a collaborative text editor where users on different replicas can insert and delete characters. Explain in 3–5 sentences why a naive "last-write-wins" approach fails for concurrent character insertions, and describe at a high level how the **OR-Set (Observed-Remove Set)** CRDT avoids this problem.

4. CRDTs eliminate the need for coordination. What is the *cost* of this approach? Name at least two limitations or trade-offs compared to a strongly consistent replicated system.

---

## HW6 — etcd Hands-On: Key-Value Operations and Leases

**Topic:** etcd — practical distributed coordination

**Background.** etcd is a distributed key-value store used as the backing store of Kubernetes. It provides linearizable reads and writes through the Raft consensus protocol.

**Setup.** Start a single-node etcd instance with Docker:

```bash
docker run -d --name etcd \
  -p 2379:2379 \
  quay.io/coreos/etcd:v3.5.9 \
  etcd --advertise-client-urls http://0.0.0.0:2379 \
       --listen-client-urls http://0.0.0.0:2379
```

Install the `etcdctl` client (v3) or use it from inside the container:
```bash
docker exec -it etcd etcdctl version
```

**Tasks.**

1. **Basic operations.** Use `etcdctl` to:
   - Put the key `course/name` with value `DistributedSystems`
   - Put the key `course/year` with value `2026`
   - Read both keys with a single range query (use prefix `course/`)
   - Delete `course/year` and confirm it is gone
   Record all commands and their output.

2. **Versioning.** Update `course/name` three times with different values. Then use `etcdctl get --rev=<N>` to retrieve the value at an earlier revision. Explain what the `revision` field in the etcd response represents and how it differs from a per-key `version`.

3. **Leases.** Create a lease with a 10-second TTL. Attach the key `lock/leader` with value `node-A` to that lease. Wait for the lease to expire and confirm the key is gone. Then repeat but use `etcdctl lease keep-alive` in a background process to prevent expiry. Explain how leases enable distributed leader election.

4. **Watch.** In one terminal, start `etcdctl watch course/name`. In a second terminal, update the value of `course/name` twice. Capture the watch output. Explain how the watch mechanism could be used to build a configuration-push system where client applications automatically reload their config when an administrator updates a key in etcd.

5. **Reflection.** etcd guarantees linearizability. What does this mean for a client that reads a key immediately after another client writes it (possibly on a different cluster node)? Contrast with what would happen under eventual consistency.
