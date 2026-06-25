# Homework Assignments — Chapter 13: Consensus

## Dependency Map

```
HW1 (Consensus Foundations)
  └─► HW2 (FLP & Practical Limits)
        └─► HW3 (Raft Log Replication)
              └─► HW4 (Raft Safety & Leader Election)
HW2 (FLP & Practical Limits)
  └─► HW5 (Byzantine Agreement)
HW3 (Raft Log Replication)
  └─► HW6 (Applying Consensus: etcd & ZooKeeper)
```

## Notes for Instructor

- HW1 is suitable as a first written assignment after the introductory lecture; no implementation needed.
- HW2 consolidates the theoretical impossibility result; encourage students to search for real FLP violations in practice.
- HW3 and HW4 pair well: assign them together and give students the Raft paper extended version as reading.
- HW5 can be given as an optional advanced problem; the EIG section is deliberately left for self-study.
- HW6 is a hands-on lab that works in parallel with the dslab material on Docker/Kubernetes; coordinate with that track.

---

## HW1 — Consensus: Definitions and Simple Cases

**Learning goal.** Understand the formal definition of consensus and why simple approaches fail.

**Background.** A set of processes, each proposing 0 or 1, must satisfy Agreement, Termination, and Validity.

### Tasks

1. **Formalise.** State the three consensus properties precisely (in your own words) and give one concrete example of an algorithm that violates Agreement but satisfies the other two properties, and one that violates Termination but satisfies the other two.

2. **FloodSet analysis.** The FloodSet algorithm runs in *f* + 1 rounds for *f* possible crash failures.
   - (a) Explain intuitively why *f* + 1 rounds are necessary and sufficient.
   - (b) Construct a concrete 3-process, *f* = 1 execution where deciding after only 1 round (instead of 2) would yield an incorrect result. Trace the messages each process sends and receives.

3. **Crash vs Byzantine.** Without looking at algorithms, explain in 3–5 sentences why you would expect Byzantine agreement to require strictly more nodes than crash-fault-tolerant consensus. What property of Byzantine nodes makes the problem harder?

**Submission.** Written answers (PDF or plain text), maximum 2 pages.

---

## HW2 — The FLP Impossibility Result and Its Practical Significance

**Learning goal.** Understand what FLP rules out, what it does *not* rule out, and how practical systems sidestep it.

**Background.** Fischer, Lynch, and Paterson (1985) proved that no *deterministic* algorithm can guarantee consensus in an *asynchronous* system even if only *one* process may crash.

### Tasks

1. **Scope of FLP.** For each of the following settings, state whether FLP applies and justify your answer in 2–3 sentences:
   - (a) Synchronous system, crash failures.
   - (b) Asynchronous system, no failures.
   - (c) Asynchronous system, Byzantine failures only.
   - (d) Asynchronous system, crash failures, randomised algorithm.

2. **Practical escape hatches.** Raft and Paxos are used in production despite FLP. Explain two distinct mechanisms these protocols use to make progress in practice even though they cannot guarantee it in theory.

3. **Two-army problem.** The two-army problem is used in the lecture as an illustration.
   - (a) Map the two-army problem onto the formal consensus definition: what are the processes, proposals, and the required decision?
   - (b) Why does the two-army problem demonstrate the difficulty of *terminating reliable broadcast* rather than consensus directly?

**Submission.** Written answers, maximum 2 pages.

---

## HW3 — Raft Log Replication

**Learning goal.** Trace Raft's normal-case log replication and understand how follower logs are kept consistent.

**Background.** Read Sections 5.2 and 5.3 of the Raft extended paper (Ongaro & Ousterhout 2014).

### Tasks

1. **Normal operation trace.** Consider a 5-node Raft cluster (leader L, followers F1–F4). A client sends three sequential commands C1, C2, C3 to L.
   - Draw a message sequence chart (MSC) showing all messages exchanged until all three commands are committed.
   - Annotate each message with its type (AppendEntries / AppendEntriesResponse) and indicate the commit index at each step.

2. **Follower inconsistency.** After the three commands above are committed, the leader crashes. Show three different possible states of follower logs (one with missing entries, one with extra uncommitted entries, one with both). How does the new leader bring each follower back into a consistent state? Which Raft invariant guarantees that no committed entry is ever lost?

3. **Leader-Only-Appends.** State the Leader-Only-Appends property and explain why violating it would break the safety guarantee.

**Submission.** MSC diagram (hand-drawn or digital) plus written explanations, maximum 3 pages.

---

## HW4 — Raft Safety: Leader Election and Term Handling

**Learning goal.** Understand the safety mechanisms that distinguish Raft from a naive primary/backup approach.

**Background.** Sections 5.4 and 5.6 of the Raft extended paper cover restricted leader election and committing across terms.

### Tasks

1. **Restricted leader election.** 
   - (a) State the exact condition a candidate's log must meet to receive a vote from a follower.
   - (b) Show a 5-node scenario where, without this restriction, a newly elected leader could be missing a committed entry. Trace through what would go wrong.
   - (c) Explain how the restriction prevents the scenario in (b).

2. **Committing across terms.**
   - (a) Construct the specific scenario from Figure 8 of the Raft paper (or an analogous one) where an entry from a *previous* term is on a majority of servers but must still not be committed.
   - (b) Explain Raft's rule for handling this and why it is safe.

3. **Network partition recovery.** A 5-node cluster is partitioned into two groups of 3 and 2. After 60 seconds the partition heals.
   - (a) Describe the state of both groups immediately before healing.
   - (b) Describe how the cluster converges to a single consistent state after healing.
   - (c) What happens to clients that were talking to the leader in the minority partition during the partition?

**Submission.** Written answers with diagrams where appropriate, maximum 3 pages.

---

## HW5 — Byzantine Agreement

**Learning goal.** Understand why Byzantine agreement is harder than crash-fault-tolerant consensus and why 3f + 1 nodes are required.

**Background.** The lecture shows via a 3-node, 1-traitor argument that n = 3f is insufficient. The EIG algorithm achieves n > 3f.

### Tasks

1. **Why 3 nodes are not enough.** Reproduce and explain the indistinguishability argument from the lecture (the three cases: C faulty, A faulty, B faulty). Make your argument self-contained: a reader unfamiliar with the lecture should be able to follow it.

2. **Triple Modular Redundancy.** TMR is a well-known technique in safety-critical systems. 
   - (a) Why does TMR not solve Byzantine agreement even though it uses majority voting?
   - (b) Under what restricted conditions (if any) can TMR-like majority voting work correctly?

3. **Berman-Garay-Perry algorithm.** The lecture describes a synchronous Byzantine agreement algorithm that runs in 2(f+1) rounds with n > 4f nodes.
   - (a) Why is n > 4f required here instead of the tight bound n > 3f?
   - (b) Trace through the worked example from the lecture (n=5, f=1) for the case where node 2 is the traitor, and verify that all correct nodes decide the same value.
   - (c) What role does the "king" node play in each even round?

4. **(Optional / advanced)** Practical Byzantine Fault Tolerance (PBFT) achieves n > 3f. What is the cost compared to crash-fault-tolerant consensus in terms of message complexity?

**Submission.** Written answers, maximum 4 pages.

---

## HW6 — Applying Consensus: etcd, ZooKeeper, and Distributed Coordination

**Learning goal.** Connect the theoretical consensus material to real-world distributed systems.

**Background.** etcd uses Raft; ZooKeeper uses a variant of Paxos (ZAB). Both expose a key/value interface and are used for distributed coordination (Kubernetes, Kafka, etc.).

### Tasks

1. **etcd hands-on.**
   - (a) Start a 3-node etcd cluster locally using Docker Compose (or use a provided cluster). Write a `docker-compose.yml` that sets up the three nodes with correct peer URLs.
   - (b) Use `etcdctl put` / `etcdctl get` to store and retrieve a key. Observe the cluster's response.
   - (c) Stop one node and repeat (b). Does the cluster remain available? Explain using Raft's majority requirement.
   - (d) Stop a second node (so only 1 of 3 remains). Repeat (b). What happens and why?

2. **Leadership observation.** Use `etcdctl endpoint status` to identify the current leader. Then gracefully stop the leader node. Observe how long leader election takes and identify the new leader. Record the old and new term numbers. What does the term number change tell you?

3. **ZooKeeper vs etcd.** Without needing to run ZooKeeper, answer based on documentation and the lecture:
   - (a) ZooKeeper uses ZAB (ZooKeeper Atomic Broadcast) rather than plain Paxos. What is the key difference between ZAB and Multi-Paxos?
   - (b) What is the intended primary use case for each system, and how does that use case shape the API design?
   - (c) A Kubernetes cluster uses etcd. What data does Kubernetes store in etcd, and what would happen to the cluster if etcd lost quorum?

**Submission.** Written answers for tasks 2 and 3; for task 1 submit `docker-compose.yml` and a short shell session transcript. Maximum 4 pages total.
