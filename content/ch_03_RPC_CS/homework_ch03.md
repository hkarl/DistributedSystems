# Chapter 3 — RPC, REST, Microservices: Homework Assignments

---

### Homework 1 — RPC Mechanics: Stubs and Marshalling by Hand

**Learning goal:** Understand what a stub/skeleton pair actually does by
building a minimal version manually.

**Tasks:**

1. Without using any RPC framework, implement a toy RPC layer in Python
   over plain TCP sockets:

   - **Protocol:** The client sends a JSON object
     `{"method": "add", "args": [3, 4]}` to the server.  The server
     dispatches to the corresponding local function, executes it, and
     sends back `{"result": 7}`.
   - **Server stub (skeleton):** A loop that reads a request, looks up
     the method name in a dict of registered functions, calls it with the
     given args, and sends the result.
   - **Client stub:** A function `remote_call(method, *args)` that
     marshals the call to JSON, sends it, waits for the reply, and returns
     the result — so the caller writes `remote_call("add", 3, 4)` and
     gets `7` back.

2. Add a second function `multiply` on the server side.  Verify that the
   client can call both without any code change to the transport layer.

3. **Reflection (≤ 100 words):** In real RPC frameworks (gRPC, zerorpc),
   which parts of your hand-rolled implementation are replaced by generated
   code, and which remain as hand-written application logic?

---

### Homework 2 — gRPC: Define, Generate, Implement

**Learning goal:** Experience the schema-first IDL workflow of gRPC end-to-end.

**Tasks:**

1. Install gRPC tools:
   ```bash
   pip install grpcio grpcio-tools
   ```

   Write a `calculator.proto` file that defines a `Calculator` service with
   two RPCs:
   - `Add(BinaryRequest) returns (Result)` 
   - `Divide(BinaryRequest) returns (Result)`

   where `BinaryRequest` has two `double` fields (`a`, `b`) and `Result`
   has one `double` field (`value`) and one `string` field (`error`).

2. Generate Python code with `protoc`:
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
   ```
   Implement the server (handle division by zero by returning an error
   message in the `error` field) and a client that calls both operations.

3. Now add a `Multiply` RPC to the `.proto` file.  Regenerate.  What code
   do you have to write, and what is automatically regenerated?  What breaks
   if you forget to regenerate?

4. **Comparison (≤ 100 words):** Compare the gRPC IDL workflow with the
   Python msgpack approach from Chapter 1 Homework 3.  When would you choose
   each?

---

### Homework 3 — RPC Failure Scenarios: Analysis and Sequence Diagrams

**Learning goal:** Reason through all failure cases in the RPC request/reply
protocol; understand execution semantics.

**Tasks:**

1. Draw sequence diagrams for all five failure scenarios discussed in the
   lecture:
   - (a) No errors
   - (b) Request lost
   - (c) Reply lost — operation is idempotent (server recomputes)
   - (d) Reply lost — operation is NOT idempotent (server uses reply cache)
   - (e) Server crash and restart

   For each diagram, show: client, network, server, timeout events,
   retransmissions, and sequence numbers.

2. Classify the following operations as idempotent or non-idempotent.
   Justify each answer in one sentence.
   - `GET /users/42` (read a user record)
   - `PUT /users/42` with a complete replacement body
   - `POST /orders` (create a new order)
   - `DELETE /users/42`
   - `PATCH /account/balance` with body `{"add": 100}`

3. The slides prove that with finite sequence numbers and arbitrary message
   delays, exactly-once delivery is impossible.  A colleague argues:
   "But in practice we use TCP, which guarantees delivery — so exactly-once
   is fine."  Explain where this argument breaks down.

---

### Homework 4 — Build a RESTful API with OpenAPI Documentation

**Learning goal:** Design and implement a proper REST API; observe how
FastAPI auto-generates OpenAPI specs.

**Tasks:**

1. Design a RESTful API for a simple **book lending library**.  The API
   must support:
   - A `books` collection (list, create, retrieve by ID, delete)
   - A `members` collection (list, create, retrieve by ID)
   - A `loans` resource: a member borrows a book (create loan), returns it
     (delete loan), list all current loans for a member

   Document your URL patterns and HTTP methods in a table before writing
   any code.

2. Implement the API using FastAPI with in-memory storage (plain dicts).
   - Returning 404 for missing resources
   - Returning 409 Conflict if a book is already on loan when a borrow is
     attempted
   - Using Pydantic models for request/response bodies

3. Open `/docs` and inspect the auto-generated OpenAPI UI.  Export the
   OpenAPI JSON (available at `/openapi.json`) and paste the `paths` section
   into your submission.  Does the generated spec match your design table
   from task 1?

---

### Homework 5 — Microservices Decomposition Design

**Learning goal:** Apply microservice decomposition principles to a realistic
scenario; reason about coupling, data ownership, and inter-service
communication.

**Scenario:** You are re-architecting the university course registration
system (PAUL) as microservices.  The monolith handles: student profiles,
course catalogue, exam registration, room booking, and grade publication.

**Tasks:**

1. Propose a decomposition into microservices.  For each service state:
   - Its name and single responsibility
   - The data it owns (and why no other service should own it)
   - Its public API (REST endpoints or event types it publishes)

2. Two services need to interact: when a student registers for an exam,
   the exam service must verify the student exists (student service) and
   that the room has capacity (room service).

   Design this interaction twice:
   - As **orchestration**: which service is the orchestrator?  Draw a
     sequence diagram.
   - As **choreography**: which events are emitted?  What does each service
     subscribe to?  Draw an event-flow diagram.

   Discuss: which is easier to understand?  Which is easier to change
   independently?

3. The grade publication service writes grades, and a separate analytics
   service reads aggregated grade statistics.  Explain why these could
   benefit from CQRS (Command Query Responsibility Segregation) and sketch
   how the two models would differ.

---

### Homework 6 — REST vs RPC: Comparative Analysis

**Learning goal:** Evaluate trade-offs between RPC-style (gRPC) and
REST-style APIs for a given scenario.

**Tasks:**

1. You must expose a function `recommendBooks(userId, maxResults)` that
   returns a ranked list of book recommendations.  Compare implementing
   this as:
   - A **gRPC RPC** (`rpc RecommendBooks(RecommendRequest) returns
     (RecommendResponse)`)
   - A **REST endpoint** (`GET /users/{userId}/recommendations?max=10`)

   Evaluate on: discoverability, client language support, streaming
   capability, ease of schema evolution, and tooling.

2. The REST approach is stateless.  The recommendation engine needs the
   user's recent browsing history (last 20 viewed books) to make good
   suggestions.  Describe two different ways to provide this history to
   the service while keeping it stateless, and the trade-off of each.

3. REST's HATEOAS constraint says the client should discover resources
   from links in responses rather than hard-coding URLs.  Implement a
   minimal example: a `GET /library` root endpoint that returns a JSON
   response containing links to the `books` and `members` collections,
   and a `GET /books/` response that includes a `self` link for each book.
   The client code should follow these links rather than constructing URLs.

---

## Dependency Map

```
Slides: RPC stubs and transparency
    → Quiz 1
    → Homework 1 (hand-rolled RPC)

Slides: Copy-and-restore, IDL
    → Quiz 2
    → Homework 2 (gRPC end-to-end)

Slides: RPC execution semantics, request/reply failures
    → Quiz 3, Quiz 4
    → Homework 3 (failure scenarios + sequence diagrams)

Slides: REST, uniform interface, RESTful URLs, HATEOAS
    → Quiz 5, Quiz 6
    → Homework 4 (FastAPI REST library)
    → Homework 6 (REST vs RPC comparison)

Slides: Microservices, orchestration/choreography, scale-out
    → Quiz 7, Quiz 8
    → Homework 5 (decomposition design)

Slides: gRPC, protoc, service definitions
    → Quiz 9
    → Homework 2 (gRPC)

Slides: Database per microservice, CQRS
    → Quiz 10
    → Homework 5 task 3 (CQRS)
```

Homework 4 (FastAPI REST) builds on the FastAPI experience from Chapter 2
Homework 2.  Homework 2 (gRPC) uses the protobuf knowledge from Chapter 1
Homework 3 (msgpack/protobuf).

---

## Notes for the Instructor

- **Quiz 2** (copy-and-restore aliasing) is almost always answered incorrectly
  on first attempt.  The C example `f(&a, &a)` is simple but the aliasing
  effect is non-obvious.  Worth working through on the board.

- **Quiz 3** (exactly-once impossible) sets up a deeper discussion for the
  consensus chapter later.  Plant the seed here: "We will prove this formally
  in Chapter 13."

- **Homework 3, task 3** (TCP doesn't save you) is an important
  misconception to address.  The key insight: TCP guarantees delivery *within
  a session*, but crashes terminate sessions.  After a crash and reconnect,
  the application has no way to know whether the last operation before the
  crash was executed.

- **Homework 5** (microservices decomposition) works very well as a group
  exercise or tutorial task.  The PAUL system is familiar to students,
  making the scenario concrete.

- **Quiz 7** (orchestration vs choreography) pairs well with the RabbitMQ
  lab assignment, where choreography via message queues is directly
  observable.
