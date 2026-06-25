# Homework: Chapter 7 — Multicast and Group Communication

## Dependency Map

```
HW1 (Multicast basics & IP multicast)
  |
  +--> HW2 (Reliable multicast & ACK implosion)
         |
         +--> HW3 (Ordering semantics: FIFO, Atomic, Causal)
                |
                +--> HW4 (Lamport clocks & vector clocks)
                       |
                       +--> HW5 (CBCAST protocol)
                              |
                              +--> HW6 (View-synchronous communication & dynamic groups)
```

HW1 and HW2 can be attempted with only a basic understanding of unicast networking. HW3 requires HW1–2. HW4–5 require HW3 and a comfort with mathematical notation. HW6 requires all prior assignments.

---

## Notes for Instructor

- **HW1** is deliberately broad to anchor students before formal definitions appear. Expect a range of quality; use discussion to align the class on terminology.
- **HW2** targets the reliability layer. The ACK-implosion question (2c) often surprises students who assumed acknowledgements are cheap — use it to motivate tree-based dissemination.
- **HW3** is the conceptual core of the chapter. Scenario-based questions force students to distinguish the three orderings rather than just recite definitions. A shared whiteboard session works well for the bank-account scenario.
- **HW4** bridges theory and practice. Common mistake: students believe L(e) < L(e') implies e → e'. Make sure they work through at least one counterexample.
- **HW5** is the only protocol-level implementation exercise. Encourage students to trace the algorithm step by step before trying to write code.
- **HW6** is the most open-ended. The view-synchrony design question (6c) can be used as a small group project or essay prompt.

---

## HW1 — Multicast Fundamentals and Motivation

**Topic:** Unicast vs. multicast, group abstraction, IP multicast basics

### Questions

**1a.** A content-delivery application needs to push a 10 MB software update to 500 clients simultaneously. Compare the network load (in terms of bytes transmitted from the server's perspective) when using (i) replicated unicast and (ii) IP multicast, assuming the network has no shared links. Under what practical conditions does IP multicast provide a measurable bandwidth saving?

**1b.** In the lecture, multicast is described as "sending a single message to a *group* of receivers." List three concrete distributed-systems scenarios (different from the server-group example given in the lecture) where multicast is the natural communication primitive. For each scenario, identify what ordering guarantee (if any) the application actually needs.

**1c.** Explain the distinction between *origination*, *delivery*, *transmission*, and *reception* as used by a multicast protocol layer. Draw a simple layer diagram showing where each of these four events occurs, and explain why this separation is useful when building reliable multicast on top of an unreliable network.

**1d.** IP multicast uses Class D addresses (224.0.0.0–239.255.255.255) and the IGMP protocol for group management. Explain, at a high level, how a router learns that at least one host on a directly connected subnet is interested in a particular multicast group. What happens when the last interested host on a subnet leaves the group?

---

## HW2 — Reliable Multicast and Scalability

**Topic:** Reliability properties, sequence numbers, NACKs, ACK implosion, tree-based dissemination

### Questions

**2a.** The lecture states three properties for reliable multicast: VALIDITY, UNIFORM AGREEMENT, and UNIFORM INTEGRITY. For each property, give a short informal explanation (one or two sentences) and a concrete example of a scenario that would violate that property if it were not enforced.

**2b.** A simple implementation of reliable multicast uses sequence numbers and acknowledgements (ACKs): the sender retransmits any message that is not acknowledged within a timeout. Explain how this mechanism detects and repairs message loss. Why does the lecture describe this as "basically replicated unicast"?

**2c — ACK Implosion.** Consider a multicast group with *n* = 1000 members. The sender multicasts a message and waits for ACKs before declaring delivery complete.

  - (i) In the worst case, how many ACK messages does the sender receive for a single multicast?
  - (ii) If the ACK rate grows with *n*, what is the practical effect on the sender as *n* increases?
  - (iii) Sketch a tree-based scheme that reduces the number of ACKs the original sender must process. What are the trade-offs of this approach?

**2d.** *Negative acknowledgements (NACKs)* are an alternative to positive ACKs. Describe the NACK-based approach: when does a receiver send a NACK, and to whom? Under what conditions is the NACK approach more scalable than the ACK approach? Under what conditions might NACKs themselves cause an "implosion" problem, and how can this be mitigated?

---

## HW3 — Ordering Semantics: FIFO, Causal, and Total Order

**Topic:** FIFO, causal, and total-order multicast; state machine replication; relationships between orderings

### Questions

**3a.** Three processes P1, P2, P3 belong to a multicast group. P1 sends message A, then message B. P2 delivers B before A. Identify which ordering guarantee (FIFO, causal, total) has been violated, and which have not. Justify your answers.

**3b — Bank account scenario.** A replicated bank account is maintained by three server replicas S1, S2, S3. Two clients simultaneously issue:
  - Client X: "Deposit €100" (message D)
  - Client Y: "Apply 10% interest" (message I)

  - (i) Show, with a concrete execution trace, how FIFO multicast alone is insufficient to keep the replicas consistent.
  - (ii) Show how total-order multicast solves the problem.
  - (iii) Does causal multicast also solve it? Explain why or why not.

**3c.** The lecture states "Total order = Atomic + FIFO." Construct a small example (three processes, two messages) that satisfies atomic order but violates FIFO order. Then show what additional constraint FIFO imposes.

**3d.** Explain why total-order multicast supports *state machine replication*. What assumption about the state machines is required for replication to work correctly? Give an example where this assumption is violated and replication breaks down even with total-order multicast.

**3e.** Rank the four ordering levels — reliable, FIFO, causal, total — in terms of implementation overhead (roughly, from cheapest to most expensive). Give a brief justification for each ranking step.

---

## HW4 — Logical Time: Lamport Clocks and Vector Clocks

**Topic:** Happened-before relation, Lamport timestamps, vector clocks, concurrency detection

### Questions

**4a.** Consider four processes P1–P4 exchanging messages. Draw a space-time diagram with at least three messages crossing process boundaries. Apply the LamportTime algorithm to assign Lamport timestamps to every event. Find at least two pairs of events (e, e') where L(e) < L(e') but e does NOT happen-before e'. What does this tell you about the relationship between Lamport timestamps and causality?

**4b.** Define the *happened-before* relation (→) precisely in terms of the two base cases and transitive closure. Why is it called "potential causality" rather than "actual causality"? Give an example where two events are ordered by → but there is clearly no causal relationship between them in the application.

**4c.** Repeat the exercise from 4a using vector clocks (assume three processes for simplicity). For each pair of events, determine whether e → e', e' → e, or e and e' are concurrent, using the vector clock comparison rules from the lecture. Verify that your vector clock results are consistent with the space-time diagram.

**4d.** Prove (informally but rigorously) that for vector clocks: VC(e) < VC(e') if and only if e → e'. Your proof should cover both directions of the "if and only if."

**4e.** A student claims: "Vector clocks are too expensive for large groups because each message must carry an O(n) vector." Describe two practical optimizations that reduce the overhead of vector clocks in systems with many processes, and explain what trade-offs each optimization introduces.

---

## HW5 — CBCAST: Implementing Causal Multicast

**Topic:** CBCAST protocol, vector timestamps, holdback queue, delivery conditions

### Questions

**5a.** State the two delivery conditions of the CBCAST protocol precisely (using the notation from the lecture: vt, VTj, i, k). Explain in plain English what each condition checks, and why both are needed.

**5b — CBCAST trace.** Three processes P1, P2, P3 each start with vector timestamp [0, 0, 0].

  - P1 multicasts message M1 (its first message).
  - P2, upon receiving M1, multicasts message M2.
  - P3 receives M2 before M1.

  Work through the CBCAST delivery conditions at P3 for both M1 and M2. Which message can P3 deliver first? Which must be held back, and until when?

**5c.** The CBCAST protocol assumes that messages from the same sender arrive in order (FIFO channel). What goes wrong if this assumption is violated? Sketch a modified delivery condition that would handle out-of-order delivery from the same sender.

**5d.** Compare CBCAST (causal ordering) with total-order multicast using a central sequencer from the perspective of:
  - (i) Message overhead per multicast operation
  - (ii) Latency of message delivery
  - (iii) Fault tolerance (what happens when a node fails)

  For each dimension, state which approach performs better and why.

---

## HW6 — Dynamic Groups and View-Synchronous Communication

**Topic:** Group views, view-synchronous communication, reliable multicast with failures, terminating reliable multicast

### Questions

**6a.** The lecture identifies four failure cases for reliable multicast when nodes can crash:
  1. Receiver fails before delivering
  2. Receiver fails after delivering
  3. Sender fails after transmitting to everyone
  4. Sender fails after transmitting to some but not all

  For each case, explain whether the basic reliable multicast property (UNIFORM AGREEMENT) is maintained and why. Which case is described as "critical," and why?

**6b.** Define a *view* and explain the *view-synchronous* communication model. The lecture shows two "plausible" sequences and two "disallowed" sequences when a view change and a message are in transit simultaneously. Summarize the rule that distinguishes plausible from disallowed sequences in one sentence.

**6c — Design question.** You are building a distributed key-value store using view-synchronous group communication. The store must satisfy:
  - All replicas always agree on the current set of key-value pairs.
  - A client PUT operation is acknowledged only after all current group members have applied it.
  - When a replica fails, the remaining replicas continue operating without data loss.

  Sketch the protocol your group-communication layer must provide (ordering level, view management, failure handling). Identify at least two places where your design requires trade-offs between consistency and availability.

**6d.** The lecture contrasts *terminating reliable multicast* (with the "correct processes" qualifier) with the simpler reliable multicast defined earlier. Explain why the "correct processes" qualifier is necessary. Is it possible to guarantee that ALL processes (correct or not) deliver a message? Relate your answer to the FLP impossibility result (which you may reference without proof).
