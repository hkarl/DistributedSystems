# Chapter 1 — Basic Client/Server: Quizzes & Homework Assignments

---

## In-Class Quizzes

These are short questions suitable for clicker polls, Moodle quizzes, or
warm-up exercises (2–5 minutes each).  Intended to surface misconceptions
before or after the relevant slide section.

---

### Quiz 1 — Blocking vs. Non-blocking Send

**Context:** The chapter distinguishes three variants of `send`: strictly
blocking (waits for delivery), blocking v2 (waits until copied into OS buffer),
and strictly non-blocking.

**Question:** A process calls `send(buf, dest)` and the call returns
immediately — without waiting for the remote receiver to call `recv`.  
Which of the following statements is *most likely* true?

a) The message has been delivered to the receiver.  
b) The message has been copied into an OS kernel buffer; the process's buffer
   can be reused.  
c) The receiver has acknowledged the message.  
d) The kernel will notify the process later via a signal when the buffer is
   free.  

**Correct answer:** b)

**Discussion point:** The most common OS default is "blocking v2": the call
blocks only long enough to copy the data into a kernel buffer, then returns.
The process gets no direct feedback about delivery.  Option d) describes
strictly non-blocking send (unusual).

---

### Quiz 2 — Combinations of Send/Receive Blocking

**Question:** Which combination of blocking send and non-blocking receive
would *not* make sense for a typical request/reply client?

a) Blocking send + blocking receive  
b) Blocking send + non-blocking receive  
c) Non-blocking send + non-blocking receive  
d) Blocking send + blocking receive on a separate thread  

**Correct answer:** There is no combination that "cannot work", but the class
should discuss trade-offs.

**Discussion prompt (open-ended):** A client uses non-blocking receive and
busy-polls in a loop.  What is the cost compared to blocking receive?  When
would you deliberately choose it?

**Teaching goal:** Surface the CPU-wasting nature of busy-polling; motivate
`select`/`epoll`.

---

### Quiz 3 — Synchronous vs. Asynchronous Timing Model

**Question:** A distributed system designer says: "I will assume that any
message sent from node A to node B arrives within 100 ms."  Which timing
model does this describe?

a) Synchronous model  
b) Asynchronous model  
c) A *partially* synchronous model (bounded delivery time)  
d) The PRAM model  

**Correct answer:** c)

**Follow-up question (think-pair-share):** What happens to a protocol that
relies on this 100 ms bound if a network switch is overloaded and a packet
takes 200 ms?  How does the protocol behave?

---

### Quiz 4 — Serialization: Why an Intermediate Format?

**Question:** Two programs, one written in Java and one in C++, need to
exchange a list of records over a TCP connection.  Without any common wire
format, how many translation functions would be needed in the worst case if
every pair of languages needs its own translator?

a) 2  
b) 4  
c) O(n) where n = number of languages  
d) O(n²) where n = number of languages  

**Correct answer:** d)

**Follow-up:** Why does a single neutral wire format reduce this to O(n)?

---

### Quiz 5 — IDL vs. Runtime Reflection

**Question:** Python's `msgpack` library can serialize a Python dict directly
without any schema file.  Google Protocol Buffers requires a `.proto` file and
a compilation step.  What does the Proto approach give you that the msgpack
approach does not?

(Select *all* that apply)

a) Type checking at compile time — invalid field names are caught before
   running the program.  
b) The ability to serialize data at all.  
c) Language-neutral code generation, making it easy to write one endpoint in
   Go and another in Java.  
d) Smaller wire-format size in all cases.  

**Correct answers:** a) and c)

**Teaching goal:** Distinguish "schema-less" from "schema-first" approaches;
motivate IDL tools.

---

### Quiz 6 — Stateful vs. Stateless Servers

**Question:** A client reads a 10 MB file from a server in 1 MB chunks.  The
server remembers the file offset between calls.

Which statement is *true*?

a) This is a stateless server because the client does not carry state.  
b) This is a stateful server; if the server crashes and restarts, the client's
   next read may fail or return wrong data.  
c) This is a stateless server; the server does not store anything permanently.  
d) Stateful vs. stateless has no impact on fault tolerance.  

**Correct answer:** b)

**Discussion:** How does NFS solve this?  (Answer: NFS is stateless — every
read call carries the file handle *and* byte offset.)

---

### Quiz 7 — Idempotency and Exactly-Once Semantics

**Scenario:** A client sends a request to transfer €100 from account A to
account B.  The server executes the transfer, but the reply is lost in the
network.  The client times out and retransmits the request.

**Question:** What is the risk if the server does not use message IDs and
does not track which requests it has already processed?

a) The client will never get a reply.  
b) €200 may be transferred instead of €100.  
c) The transfer may be rolled back.  
d) Nothing — the server will detect the duplicate automatically.  

**Correct answer:** b)

**Follow-up:** Is a bank transfer an *idempotent* operation?  What would an
idempotent version look like?

---

### Quiz 8 — Single Point of Failure

**Question:** Which of the following is a direct consequence of the basic
two-tier client/server architecture that the slide deck identifies as a
disadvantage?

a) Clients can become overloaded.  
b) The server can become a performance bottleneck *and* a single point of
   failure.  
c) Clients cannot communicate with each other.  
d) The wire format is too complex.  

**Correct answer:** b)

---

## Homework Assignments

These are take-home exercises, expected to take 1–3 hours each.

---

### Homework 1 — Blocking/Non-Blocking Combinations (Conceptual + Code Reading)

**Learning goal:** Understand the four combinations of blocking send/receive
and their implications.

**Tasks:**

1. The slides mention that the `receive` operation can be made non-blocking
   using `fcntl(..., O_NONBLOCK)` on Linux.  Read the man page for `recv(2)`
   and `fcntl(2)` (any Linux system or `man7.org`).

   Explain in your own words (≤ 150 words) what happens when you call
   `recv()` on a non-blocking socket and no data is available yet.

2. The slides also mention `select`, `epoll` (Linux), and `kqueue` (macOS) as
   ways to block on *multiple* sockets simultaneously.

   Sketch (in pseudocode or Python) how a server that handles two clients
   simultaneously on two different sockets would use `select()` to avoid
   busy-polling.  You do not need to write runnable code — a clear pseudocode
   is sufficient.

3. Under what conditions would you prefer a blocking receive over a
   `select`-based loop?  Give one concrete scenario for each choice.

---

### Homework 2 — Implement a Simple Echo Server with 0mq

**Learning goal:** Experience a real messaging API; observe the
request/reply pattern in code.

**Tasks:**

1. Install `pyzmq` (`pip install pyzmq`) and implement:

   - **Server (`echo_server.py`):** Binds a `ZMQ_REP` socket on port 5555.
     Receives any message and sends back the same message prefixed with
     `"ECHO: "`.  Runs in an infinite loop.
   
   - **Client (`echo_client.py`):** Connects a `ZMQ_REQ` socket to the
     server.  Sends five messages (`"Hello 0"` through `"Hello 4"`) one at a
     time, prints each reply, then exits.

2. Modify the client to send requests *asynchronously*: use a `DEALER`
   socket instead of `REQ` and send all five messages before reading any
   replies.  Observe whether the order of replies is guaranteed.
   
   (Hint: `DEALER` does not enforce the send-recv-send-recv cycle that `REQ`
   does.  See the 0mq guide: https://zguide.zeromq.org/docs/chapter3/)

3. **Reflection (≤ 100 words):** What does the `REQ`/`REP` socket pair
   enforce that plain UDP sockets do not?  What does it *not* enforce?

---

### Homework 3 — Serialization: Protobuf vs. msgpack

**Learning goal:** Experience schema-based vs. schema-less serialization;
measure wire-format size.

**Tasks:**

1. Define the following data structure in a Protocol Buffers `.proto` file:

   ```
   A Product with: id (integer), name (string), price (float), 
   tags (list of strings), in_stock (boolean)
   ```

   Generate Python code with `protoc` and write a script that creates 10
   `Product` objects, serializes them to bytes, and prints the total byte
   count.

2. Repeat the exercise using Python's `msgpack` library (no schema file
   needed).  Represent each product as a dict with the same fields.

3. Compare the byte counts.  Which is smaller?  Why?  (Consider: does
   protobuf include field names in the wire format?  Does msgpack?)

4. Now add a *new optional field* `discount_pct` (integer) to the product
   without updating the receiver's schema.  What happens in each system when
   the receiver tries to deserialize a message that contains this unknown
   field?  Test it and describe the result.

---

### Homework 4 — Stateful vs. Stateless: Design Exercise

**Learning goal:** Reason about server design decisions and their fault-tolerance implications.

**Scenario:** You are designing a server for an online document editor
(think: a stripped-down Google Docs).  Multiple clients can simultaneously
edit sections of the same document.  When a client submits a change, the
server applies it and stores the updated document.

**Tasks:**

1. Design the server as a **stateful server**.
   - What state does the server maintain per client session?
   - What happens if the server crashes and restarts while a client is editing?
   - What does the client need to do to recover?

2. Redesign as a **stateless server**.
   - What information must every client request include that it did not need in
     the stateful design?
   - How does this affect the size of request messages?
   - Is a stateless design practical here?  Justify your answer.

3. The slides mention cookies as an example of client-side state storage.
   Describe how cookies could be used to make an otherwise stateless HTTP
   server behave statelessly from the server's perspective while preserving
   session continuity for the client.

---

### Homework 5 — Fault Tolerance: Request/Reply Protocol

**Learning goal:** Understand timeouts, retransmission, and idempotency;
design a robust request/reply protocol.

**Tasks:**

1. **Analysis:** The slides describe two problems in request/reply: (a) no
   reply received, and (b) duplicate requests arriving at the server.  For
   each problem, state:
   - How it is detected.
   - What information the protocol must maintain to handle it.

2. **Implementation:** Extend your echo server from Homework 2 with the
   following features using plain UDP sockets (not 0mq):

   - Every request carries a monotonically increasing integer message ID.
   - The server maintains a dict mapping `(client_address, message_id)` →
     `reply`.  If a duplicate arrives, the stored reply is resent without
     re-executing the operation.
   - The client retransmits up to 3 times with a 1-second timeout before
     giving up.

   Simulate a lost reply by having the server randomly drop 30 % of its
   outgoing replies *before* adding them to the history dict.  Verify that
   the client always gets the correct answer eventually (or prints a clear
   error after 3 retries).

3. **Reflection (≤ 150 words):** Your echo server's operation ("prefix with
   'ECHO: '") is idempotent.  Give an example of an operation that is *not*
   idempotent.  How does non-idempotency affect the protocol design in task 2?

---

### Homework 6 — Name Resolution and Service Discovery (Research + Design)

**Learning goal:** Connect the "how to find a server" question to real systems.

**Tasks:**

1. The slides mention DNS as one name-resolution mechanism.  In Kubernetes,
   services are discovered by DNS name (e.g., `catalogue.cilium-demo.svc.cluster.local`).
   
   Explain in ≤ 200 words how Kubernetes DNS differs from public Internet DNS
   in the following aspects:
   - Who maintains the zone records and how?
   - What does a record point to (IP address, virtual IP, pod IP)?
   - What happens when the number of pods backing a service changes?

2. The slides mention broadcasting (like ARP) as an alternative to explicit
   directories.  In a local network, mDNS (Multicast DNS, RFC 6762) allows
   devices to announce themselves without a central server.
   
   Describe a scenario where mDNS is preferable to a central DNS server, and
   a scenario where it is not.

3. Design a minimal *service registry* for a cluster of microservices:
   - What information does a service register when it starts?
   - How does a client look up a service?
   - What should happen when a service crashes and stops sending heartbeats?
   
   No implementation required — a design document with clear data structures
   and operations is sufficient.

---

## Dependency Map

The quizzes and assignments form a deliberate progression:

```
Slides: send/receive blocking
    → Quiz 1, Quiz 2
    → Homework 1 (non-blocking + select)
    → Homework 5 (UDP retransmission)

Slides: serialization / wire format
    → Quiz 4, Quiz 5
    → Homework 3 (protobuf vs. msgpack)

Slides: client/server, stateful/stateless
    → Quiz 6
    → Homework 4 (design exercise)

Slides: request/reply reliability
    → Quiz 7
    → Homework 5 (fault-tolerant echo server)

Slides: how to find a server / name resolution
    → Quiz 8 (SPOF)
    → Homework 6 (DNS + service discovery)
```

Homework 2 (0mq echo server) is a prerequisite for Homework 5 (fault-tolerant UDP).
Homework 3 assumes students have completed the 0mq exercise (they know what a
"message" is).

---

## Notes for the Instructor

- **Quiz 1 and Quiz 2** are best run together immediately after the
  "Synchronicity of operations" slides.  Students consistently confuse
  "blocking v2 send returns" with "message delivered".

- **Quiz 7** (bank transfer / idempotency) reliably generates discussion.
  Give 3–4 minutes for the follow-up before revealing the answer.

- **Homework 3** (protobuf vs. msgpack) works well as a pair exercise if lab
  time is available.  The "add an unknown field" sub-task often surprises
  students: msgpack happily deserializes the extra key; protobuf ignores it
  but preserves it in the object for round-tripping.

- **Homework 5** is the most demanding.  Consider offering it as an optional
  extension or grouping students into pairs.

- The slides currently mark "Other combinations: Homework!" in the
  synchronicity section without providing one.  **Quiz 2 and Homework 1 fill
  that gap explicitly.**
