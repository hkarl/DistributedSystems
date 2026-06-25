# Homework: Chapter 9 – Message Queuing

## Dependency Map

| # | Assignment | Depends on | Tools / Reading |
|---|-----------|-----------|----------------|
| 1 | MQ semantics comparison | None | Slides §1, §2 |
| 2 | Delivery guarantees analysis | HW 1 | Slides §Dependability |
| 3 | RabbitMQ hands-on | HW 1 | RabbitMQ docs, pika |
| 4 | Kafka partitioning design | HW 1, HW 2 | Slides §Kafka |
| 5 | Consumer-group experiment | HW 4 | Kafka CLI / Python |
| 6 | Leader election trace | HW 4 | Slides §Leader election |

---

## Notes for Instructor

- **HW 1** is purely conceptual and can be given after the first lecture session on MQ semantics.
- **HW 2** requires students to reason carefully about failure scenarios; pair it with the *Exactly-once, with failures* slides.
- **HW 3** is the first hands-on assignment; students need a running RabbitMQ instance. Docker (`rabbitmq:3-management`) is the easiest setup. Time budget: ~2–3 hours.
- **HW 4 and HW 5** build toward Kafka. HW 5 is exploratory and intentionally open-ended; accept any empirically grounded answer.
- **HW 6** connects the MQ chapter to the Leader Election section; it is largely pencil-and-paper and consolidates lecture content from both topics.
- Emphasise that *exactly-once delivery is impossible in general*; several questions probe whether students have internalised this.

---

## Assignment 1: MQ Semantics vs. Pub/Sub

**Background.** Pub/sub (as studied in Chapter 8) and message queuing are closely related but differ in important ways.

**Tasks.**

1. List the three dimensions of loose coupling discussed in the slides (temporal, spatial, identity). For each dimension, explain how MQ's coupling is *tighter or looser* than pub/sub's.
2. In pub/sub, a message published when no subscriber is active is silently dropped. Explain the MQ behaviour in the same scenario. What trade-off does this introduce?
3. The slides mention *load balancing* as a key MQ feature. Sketch a scenario (draw a simple diagram) showing three consumers on the same queue receiving messages from one producer. What delivery guarantee does MQ provide in this scenario?
4. Define *dead-letter queue*. Give two concrete reasons why a message might end up there.

**Deliverable.** Written answers (max 1 A4 page) and one diagram.

---

## Assignment 2: Delivery Guarantees Under Failure

**Background.** Achieving reliable delivery in the presence of broker or consumer failures is a core challenge of MQ systems.

**Tasks.**

1. Explain in your own words the difference between *at-most-once*, *at-least-once*, and *exactly-once* delivery semantics.
2. The slides contain a theorem: *exactly-once delivery is impossible*. Construct a concrete failure scenario (involving a broker crash at a specific point) that shows why a broker cannot guarantee exactly-once delivery even with stable storage and ACKs.
3. Kafka's consumer offset mechanism (writing the offset *before* or *after* consuming) implements at-most-once or at-least-once semantics respectively. Write out the failure scenario for *each* option that leads to the stated consequence.
4. AMQP marketing material claims "reliable, exactly-once delivery." Given the theorem above, what do you think this claim means in practice? What conditions must hold for the claim to be approximately true?

**Deliverable.** Written answers (max 1.5 A4 pages).

---

## Assignment 3: RabbitMQ – Work Queues and Exchanges

**Background.** This is a hands-on assignment. You will run a local RabbitMQ broker and implement a small producer–consumer system.

**Setup.** Start RabbitMQ with the management plugin:

```bash
docker run -d --name rabbitmq \
  -p 5672:5672 -p 15672:15672 \
  rabbitmq:3-management
```

Access the management UI at `http://localhost:15672` (guest/guest).

**Tasks.**

1. Using the Python `pika` library, implement a *producer* that sends 20 numbered messages (`"task 1"` … `"task 20"`) to a queue called `"work_queue"`. Each message should be *persistent*.
2. Implement two *worker* processes. Each worker receives messages and simulates processing by sleeping for a number of seconds equal to the number of dots in the message body (a common RabbitMQ tutorial technique). Worker 1 and Worker 2 should run concurrently. Use *manual acknowledgements* (do **not** use `auto_ack=True`).
3. Start both workers, then start the producer. Record which worker received which message numbers. Does the distribution match your expectation from the slides (round-robin)?
4. Kill one worker mid-run (Ctrl-C). Observe what happens to unacknowledged messages. Does RabbitMQ redeliver them to the surviving worker? Explain why or why not, given your `basic_ack` call placement.
5. Add a *dead-letter exchange*: configure the work queue so that messages rejected (via `basic_reject` with `requeue=False`) are routed to a `"dead_letter_queue"`. Verify with the management UI.

**Deliverable.** Python source files, terminal output (copy-paste or screenshot), and written answers to tasks 3–5 (max 1 A4 page).

---

## Assignment 4: Kafka Partitioning Design

**Background.** Kafka's partitioning model determines parallelism, ordering, and fault tolerance. Designing the right partition scheme is a critical real-world skill.

**Scenario.** You are building a ride-hailing platform. Events emitted: `ride_requested`, `driver_assigned`, `ride_started`, `ride_completed`, `payment_processed`. Volume: ~50,000 events/second at peak. Ordering requirement: all events for the *same ride* must be processed in order.

**Tasks.**

1. How many topics would you create, and why? (Consider: one topic per event type vs. one topic for all ride events.)
2. What would you use as the *partition key* and why? What ordering guarantee does Kafka provide within a partition?
3. Suppose you use 12 partitions. How many consumer instances can you run in a single consumer group before adding more partitions would be necessary?
4. The slides state that total order is guaranteed *within* a partition but not across partitions. How does this interact with your ordering requirement from the scenario?
5. You need your data to be replicated to 3 brokers. Write the Kafka CLI command to create the topic `ride_events` with 12 partitions and replication factor 3.

**Deliverable.** Written design document (max 1.5 A4 pages) and the CLI command.

---

## Assignment 5: Consumer Group Experiment

**Background.** Consumer groups are Kafka's mechanism for scaling consumers while controlling the broadcast vs. load-balancing trade-off.

**Setup.** Use the Kafka CLI (or `confluent-kafka-python`) with a local Kafka instance. (A Docker Compose with Kafka + ZooKeeper or KRaft is fine.)

**Tasks.**

1. Create a topic `experiment` with 4 partitions.
2. Start a producer that continuously sends messages of the form `"msg-<sequence_number>"` to the topic (round-robin across partitions).
3. Start *three* consumers all in the same consumer group `"group-A"`. Observe which consumer receives which messages. How many partitions does each consumer handle? Is any consumer idle?
4. Now start a *fourth* consumer in `"group-A"`. What changes? Start a *fifth*. What happens to the fifth consumer and why?
5. Start a *sixth* consumer in a *different* group `"group-B"`. Does this consumer receive the same messages as `"group-A"` consumers or different ones? Explain using the consumer group rule from the slides.
6. (Bonus) Kill one of the `"group-A"` consumers. Observe and describe the *partition rebalancing* behaviour. How long does rebalancing take?

**Deliverable.** Terminal output (trimmed to relevant lines), written answers to tasks 3–6 (max 1 A4 page).

---

## Assignment 6: Leader Election Trace

**Background.** Kafka uses the KRaft protocol (a variant of Raft) for leader election. This assignment asks you to trace the simpler LCR algorithm by hand, then connect it to Raft's approach.

**Tasks.**

1. Consider a ring of 5 nodes with UIDs: 3, 7, 1, 9, 4 (clockwise order). Trace the LCR algorithm step by step:
   - Show which UID each node sends in each round.
   - Identify which node declares itself leader and after how many rounds.
2. Compute the *message complexity* of your trace. How does this compare with the worst-case $O(n^2)$ stated in the slides?
3. In Raft's leader election (as used by Kafka/KRaft), nodes use *randomised timeouts* instead of ring topology. Explain in 3–5 sentences why randomised timeouts reduce the number of election conflicts compared to all nodes timing out simultaneously.
4. The Raft slides show three possible outcomes from a candidate's perspective (*won*, *lost*, *nobody won*). For each outcome, describe what the candidate does next.
5. In KRaft, Kafka switches from Raft's push-based log replication to a *pull-based* model. Explain in 2–3 sentences why this architectural choice is natural given how Kafka consumers already work.

**Deliverable.** Completed trace table (task 1), message count (task 2), and written answers to tasks 3–5 (max 1 A4 page).
