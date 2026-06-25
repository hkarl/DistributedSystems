# Homework Assignments – Chapter 12: Distributed Transactions

## Dependency Map

```
HW1 (ACID & serializability) ──► HW2 (2PL & anomalies)
                                        │
                                        ▼
HW3 (2PC protocol & failures) ──► HW4 (3PC & blocking vs. liveness)
                                        │
                                        ▼
HW5 (Distributed snapshot / Chandy-Lamport) ──► HW6 (Saga pattern)
```

HW1–HW2 cover foundational concepts; HW3–HW4 deepen protocol understanding; HW5 applies snapshot theory; HW6 connects to modern microservice practice.

---

## Notes for Instructor

- HW1 and HW2 are suitable for the first week after the lecture; the remaining assignments build on each other and work best as a two-week arc.
- HW3 asks students to trace a protocol by hand — a whiteboard session or peer-review works well.
- HW4 requires careful reasoning about indistinguishability; expect common mistakes around the partition scenario.
- HW5 is algorithmically demanding; provide the pseudocode slides as reference material.
- HW6 is deliberately open-ended and invites discussion of trade-offs; there is no single correct answer.

---

## HW1 – ACID Properties and Anomalies

**Learning goal:** Understand the four ACID properties and identify which one is violated by concrete anomaly scenarios.

**Background:** ACID stands for Atomicity, Consistency, Isolation, and Durability. These properties define the guarantees a database transaction provides.

### Tasks

1. For each of the following scenarios, identify which ACID property (or properties) is violated and briefly explain why:

   a. Bank transfer: €100 is debited from account A, but the server crashes before crediting account B. After recovery, account B is unchanged.

   b. Two concurrent transactions both read a product's stock level (10 units) and each sells 8 units, resulting in a stock level of −6.

   c. A transaction successfully commits a salary update. After a power failure, the database restores from an old backup and the update is gone.

   d. An audit transaction reads account balances while a concurrent transfer is partially executed, reading the debited account but not yet the credited one.

2. Define *serializability* in your own words. Give a concrete counterexample: two transactions T1 and T2 whose interleaved execution produces a result that no serial ordering (T1 then T2, or T2 then T1) would produce.

3. Is serializability sufficient to guarantee full ACID? Justify your answer for each of the four properties.

**Deliverable:** A written answer (max 1 page) addressing all three tasks.

---

## HW2 – Two-Phase Locking and Deadlocks

**Learning goal:** Apply two-phase locking rules, identify deadlock scenarios, and reason about resolution strategies.

**Background:** Two-Phase Locking (2PL) guarantees serializability by requiring that a transaction acquires all locks before releasing any. The *growing phase* allows only acquisitions; the *shrinking phase* allows only releases.

### Tasks

1. Consider three transactions operating on data items X, Y, and Z:
   - T1: read(X), write(Y)
   - T2: read(Y), write(Z)
   - T3: read(Z), write(X)

   Construct a concurrent schedule in which these three transactions deadlock under 2PL. Draw the wait-for graph.

2. For the deadlock you constructed in Task 1, describe two different resolution strategies (victim selection) and discuss the trade-offs of each.

3. Strict 2PL holds all write locks until commit/abort. Explain why Strict 2PL prevents *cascading aborts* whereas basic 2PL does not.

4. Does 2PL prevent the *lost update* anomaly described in the lecture (account X, transactions A and B)? Show the lock acquisition sequence for both transactions that would prevent the anomaly.

**Deliverable:** Written answers plus diagrams for Tasks 1 and 4.

---

## HW3 – Two-Phase Commit: Protocol Trace and Failure Scenarios

**Learning goal:** Trace 2PC execution step-by-step, identify blocking states, and reason about what can and cannot be decided by surviving nodes.

**Background:** 2PC has a coordinator and one or more participants. Phases: (1) voting, (2) decision. Key states for participants: *Init*, *Ready* (can abort), *Voted* (sent VOTE-COMMIT, waiting), *Commit*, *Abort*.

### Tasks

1. **Normal commit run.** Draw a message-sequence diagram for a 2PC commit with one coordinator C and three participants P1, P2, P3. Label all messages (VOTE-REQUEST, VOTE-COMMIT, GLOBAL-COMMIT, ACK) and state transitions.

2. **Participant failure.** Suppose P2 crashes after receiving VOTE-REQUEST but before sending its vote. Describe the state of C and P1/P3. What does C do? What eventually happens to P2 when it recovers?

3. **Coordinator failure.** Suppose C crashes after sending GLOBAL-COMMIT to P1 but before sending it to P2 and P3. Describe the states of P1, P2, P3. Can they resolve the situation? Why or why not?

4. **Termination protocol.** For each participant state (*Ready* and *Voted*), state what action a participant should take on timeout, with justification. Which state is called *critical* and why?

5. Explain in one paragraph why 2PC is classified as a *safe but not always live* protocol.

**Deliverable:** Message-sequence diagrams for Tasks 1–3 and written answers for Tasks 4–5.

---

## HW4 – Three-Phase Commit: Non-Blocking Properties and Limits

**Learning goal:** Understand how 3PC extends 2PC to handle coordinator crashes, and why network partitions break the non-blocking guarantee.

**Background:** 3PC introduces a *PreCommit* state for both coordinator and participants. The key invariant is: **if any node is in PreCommit, no node can be in Abort**.

### Tasks

1. Draw the 3PC FSM for both coordinator and participant (you may sketch by hand). Mark the new state compared to 2PC and the new messages (PREPARE-COMMIT).

2. In 3PC, a participant times out in the *Voted* state because the coordinator has crashed. Describe the decision procedure: what does the participant do when it contacts other participants and finds them in (a) Abort, (b) PreCommit, (c) all Voted? Justify each case using the key invariant.

3. Reproduce (as a message-sequence diagram) the partition scenario from the lecture: coordinator C crashes; nodes B, C, E never receive PREPARE-COMMIT; node A (in PreCommit) is partitioned off from B, C, E.
   - What should A do?
   - What should B, C, E do?
   - Why are A's two options (commit or abort) *both* potentially wrong?

4. The lecture states that 3PC is *safe and live under node crashes alone*, but *not under network partitions*. Explain in your own words why node crashes and network partitions are handled differently by 3PC.

5. (Challenge) In what sense does the indistinguishability argument in Task 3 foreshadow the FLP impossibility result?

**Deliverable:** FSM sketches, message-sequence diagram, and written answers.

---

## HW5 – Distributed Snapshot Algorithm (Chandy-Lamport)

**Learning goal:** Understand and apply the Chandy-Lamport snapshot algorithm; reason about consistent cuts.

**Background:** A *consistent cut* is a set of process states such that no message is recorded as received but not as sent. The Chandy-Lamport algorithm uses *marker* messages to establish consistent cuts in FIFO channels without stopping the system.

### Tasks

1. **Consistent vs. inconsistent cuts.** Given a system with processes P1, P2, P3 exchanging messages, draw one consistent cut and one inconsistent cut on the same timeline. Explain why the inconsistent cut violates the consistency condition.

2. **Algorithm trace.** Consider three processes P1, P2, P3 in a ring (P1→P2→P3→P1). P1 initiates the snapshot. Trace the algorithm step-by-step:
   - When does each process record its local state?
   - Which messages end up in each channel's recorded state?
   - When is the snapshot complete?

3. The pseudocode in the lecture has a variable named `self.inchannel_Done` in the `on_marker` method but `self.inchannels_Done` (plural) in `receive_message`. Identify this inconsistency and explain what the correct variable name should be and why.

4. The algorithm assumes FIFO channels. Give a concrete example showing that the algorithm produces an *inconsistent* cut if channels are not FIFO.

5. Explain how the distributed snapshot algorithm can be used to detect distributed deadlocks. What do processes record, and how is the wait-for graph reconstructed?

**Deliverable:** Diagrams for Tasks 1–2 and written answers for Tasks 3–5.

---

## HW6 – The Saga Pattern as an Alternative to Distributed Transactions

**Learning goal:** Understand the Saga pattern as a practical alternative to 2PC in microservice architectures, and reason about its trade-offs.

**Background:** The Saga pattern (Garcia-Molina & Salem, 1987; popularized in microservices by Clemens Vasters and Chris Richardson) replaces a single distributed transaction with a sequence of local transactions, each with a corresponding *compensating transaction* that undoes its effect. There are two coordination styles: *choreography* (event-driven) and *orchestration* (central coordinator).

### Tasks

1. **Motivation.** A travel booking system must reserve a flight, a hotel, and a rental car across three independent microservices. Why is 2PC problematic here? Name at least three concrete reasons.

2. **Design a Saga.** Design a Saga for the travel booking scenario:
   - List the forward transactions (T1, T2, T3) and their corresponding compensating transactions (C1, C2, C3).
   - Describe what happens when the hotel reservation (T2) fails after the flight has been reserved (T1 succeeded).

3. **ACID comparison.** Which ACID properties does a Saga guarantee, and which does it not? For each property it does *not* guarantee, describe a concrete anomaly that could occur.

4. **Choreography vs. Orchestration.** Compare the two Saga coordination styles in terms of: coupling between services, ease of debugging, failure handling, and suitability for adding new services later.

5. **When to use Sagas.** Describe a scenario in which 2PC is clearly preferable to Sagas, and a scenario in which Sagas are clearly preferable to 2PC. Justify both choices.

**Deliverable:** Written answers (max 2 pages total).

