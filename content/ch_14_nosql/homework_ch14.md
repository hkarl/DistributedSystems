# Chapter 14 Homework — NoSQL Databases

## Dependency Map

```
HW1 (CAP / BASE theory)
  └── HW2 (CAP + PACELEC applied)
        └── HW3 (Dynamo internals)
              └── HW4 (Cassandra vs. Dynamo)
HW5 (MongoDB data-modelling) — standalone
HW6 (Graph databases) — standalone
```

## Notes for Instructor

- HW1–HW2 are conceptual; suitable as pre-class preparation or short
  in-class exercises.
- HW3–HW4 require reading the referenced papers or their summaries;
  plan at least one week.
- HW5 can be paired with a hands-on MongoDB Community Server session.
- HW6 works well as a group exercise; recommend providing a small
  Neo4j Sandbox or AuraDB free-tier account.

---

## HW1 — CAP Theorem: Understanding the Triangle

**Topic:** CAP theorem fundamentals  
**Estimated effort:** 1–2 hours  
**Prerequisites:** Lecture slides on CAP theorem (Section "CAP and friends")

### Tasks

1. State the three properties of the CAP theorem in your own words
   (one sentence each).  Explain why all three cannot be achieved
   simultaneously by constructing a minimal counter-example: two
   replicated nodes connected by a network that can partition.

2. For each of the following systems, identify which two CAP
   properties it primarily favours and justify your answer:
   - A traditional SQL database (e.g., PostgreSQL with synchronous
     streaming replication)
   - Amazon Dynamo
   - Apache Zookeeper

3. The CAP theorem is sometimes called "2-of-3", but critics argue
   this framing is misleading.  Look up Eric Brewer's 2012 article
   "CAP twelve years later: How the 'rules' have changed" and
   summarise in 150–200 words what nuance he adds.

### Deliverable

A PDF or Markdown document with answers to all three tasks (≤ 2 pages).

---

## HW2 — PACELEC: Beyond CAP

**Topic:** PACELEC theorem, BASE semantics  
**Estimated effort:** 1–2 hours  
**Prerequisites:** HW1; lecture slides on PACELEC and BASE

### Tasks

1. Explain the PACELEC theorem.  Draw a 2 × 2 grid with axes
   "partition / no partition" and "consistency / latency trade-off
   chosen" and place the following systems in it (with justification):
   Dynamo, Zookeeper, MySQL (sync replication), Cassandra (QUORUM
   consistency level).

2. A startup proposes a product recommendation service backed by a
   NoSQL store.  They say: "Eventual consistency is fine—if a user
   sees yesterday's recommendations, who cares?"  Critically evaluate
   this claim.  Under what circumstances does eventual consistency
   cause real problems, and what mitigations exist?

3. Explain the meaning of "Soft state" in BASE.  Give one concrete
   example from the lecture where a storage system exhibits soft
   state.

### Deliverable

A PDF or Markdown document (≤ 2 pages).

---

## HW3 — Amazon Dynamo: Internals

**Topic:** Key-value stores, consistent hashing, vector clocks, quorum  
**Estimated effort:** 3–4 hours  
**Prerequisites:** HW1; lecture slides on Dynamo; optionally read the
original paper (DeCandia et al., SOSP 2007)

### Tasks

1. **Consistent hashing.** Suppose a Dynamo ring has 6 nodes with
   token positions 0, 60, 120, 180, 240, 300 (out of 360).  The
   replication factor is N = 3.  Which nodes store the key with hash
   value 250?  What happens when the node at position 300 fails?

2. **Vector clocks.** Two clients concurrently update the same key:
   - Client A reads version `[A:1]`, adds item X, writes
     `[A:2]`.
   - Client B also reads `[A:1]`, adds item Y, writes
     `[B:1]`.
   - Draw the vector-clock history.  Are these versions concurrent or
     causally ordered?  How does Dynamo handle this situation at read
     time?

3. **Sloppy quorum.** Dynamo uses a sloppy quorum with hinted
   handoff.  Explain what "hinted handoff" means, why it is necessary
   for availability, and what risk it introduces.

4. **Merkle trees.** Why does Dynamo use Merkle trees for replica
   synchronisation after a failure?  What would be the cost of a
   naive alternative (compare all key-value pairs directly)?

### Deliverable

A PDF or Markdown document with diagrams where appropriate (≤ 3
pages).

---

## HW4 — Cassandra vs. Dynamo

**Topic:** Column-oriented stores, tunable consistency  
**Estimated effort:** 2–3 hours  
**Prerequisites:** HW3; lecture slides on Cassandra

### Tasks

1. List three architectural properties that Cassandra inherits from
   Dynamo and two properties it inherits from Google BigTable.
   Explain each in one sentence.

2. Cassandra offers consistency levels ONE, QUORUM, and ALL.
   - Under what conditions does a QUORUM read + QUORUM write guarantee
     strong consistency?  Express this in terms of N, R, and W.
   - A cluster has N = 5 replicas.  A QUORUM write requires W = 3
     acknowledgements.  A network partition isolates 2 nodes.  Can a
     QUORUM write still succeed?  What about QUORUM reads?

3. Cassandra is described as "AP by default" yet supports strong
   consistency with QUORUM.  Is calling it an "AP system" accurate?
   Discuss in 100–150 words, referencing PACELEC.

4. Describe two use-case categories (from the lecture or your own
   research) where Cassandra is particularly well-suited and explain
   why the data model (partition key + clustering key + wide rows)
   fits each use case.

### Deliverable

A PDF or Markdown document (≤ 2 pages).

---

## HW5 — MongoDB Data Modelling

**Topic:** Document-oriented databases, schema design  
**Estimated effort:** 3–4 hours  
**Prerequisites:** Lecture slides on document-oriented databases and
MongoDB; access to MongoDB Community Server or MongoDB Atlas free tier

### Tasks

1. **Embedding vs. referencing.** A blogging platform stores authors
   and their posts.  Design two MongoDB schemas: one that *embeds*
   posts inside author documents and one that uses *references*
   (separate collections).  For each, describe a query pattern that
   benefits and one that suffers.

2. **Flexible schema in practice.** Insert the following three
   documents into a `products` collection (using `mongosh` or a
   language driver):
   ```json
   { "name": "Laptop",  "price": 999, "specs": { "ram_gb": 16 } }
   { "name": "Monitor", "price": 299, "diagonal_inch": 27 }
   { "name": "USB Hub", "price": 19 }
   ```
   Write a query that returns all products with a price below 500.
   Write a second query that returns only products that have a `specs`
   field.  Show the MongoDB shell commands and their output.

3. **Aggregation pipeline.** Using the same collection, write an
   aggregation pipeline that computes the average price per product
   category.  (You may need to add a `category` field to your sample
   documents first.)

4. **CAP position.** The lecture states MongoDB is "CP by default".
   What does this mean operationally?  What happens to write
   availability if the primary replica goes down before a new primary
   is elected?

### Deliverable

A PDF or Markdown document with shell transcripts or screenshots
(≤ 3 pages).

---

## HW6 — Graph Databases and When to Use Them

**Topic:** Graph databases, query languages, use-case analysis  
**Estimated effort:** 2–3 hours  
**Prerequisites:** Lecture slides on graph databases; optionally access
to Neo4j Sandbox (free at sandbox.neo4j.com)

### Tasks

1. **Index-free adjacency.** Explain what "index-free adjacency" means
   in a graph database.  Why does this make relationship traversals
   faster than equivalent SQL JOINs at scale?  What is the trade-off
   (hint: think about what changes when the graph grows)?

2. **Cypher query.** Consider a social network graph with nodes
   labelled `Person` (properties: `name`, `age`) and edges labelled
   `FOLLOWS`.  Write Cypher queries for:
   - Find all people that Alice follows.
   - Find all people that follow someone Alice follows (friends-of-friends).
   - Count how many followers each person has and return the top 5.

3. **Use-case comparison.** For each scenario below, decide whether a
   relational database, a document store, or a graph database is most
   appropriate.  Justify each choice in 2–3 sentences:
   - An e-commerce site storing product descriptions with highly
     variable attributes.
   - A fraud-detection system that must find rings of accounts
     connected through suspicious transactions.
   - A payroll system with rigid, well-defined schemas and
     complex multi-table transactions.

4. **CAP position.** Neo4j uses single-master + Raft replication and
   is classified as CP.  What does this mean during a leader election
   (compare: what does Cassandra do in the same situation)?

### Deliverable

A PDF or Markdown document (≤ 2 pages).
