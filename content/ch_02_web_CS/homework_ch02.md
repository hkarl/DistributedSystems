# Chapter 2 — Web Client/Server: Homework Assignments

---

### Homework 1 — HTTP Methods and REST Semantics

**Learning goal:** Understand the safety and idempotency conventions for HTTP
methods and apply them correctly to API design.

**Tasks:**

1. The HTTP standard defines some methods as *safe* (must not alter server
   state) and some as *idempotent* (repeating the request has the same effect
   as sending it once).  Fill in the table:

   | Method  | Safe? | Idempotent? |
   |---------|-------|-------------|
   | GET     |       |             |
   | HEAD    |       |             |
   | POST    |       |             |
   | PUT     |       |             |
   | DELETE  |       |             |

   Justify each answer in one sentence.

2. A developer builds a "delete account" feature.  She implements it as
   `GET /account/delete?user=alice` so users can trigger it by clicking a
   link.  Explain what can go wrong, and propose a correct HTTP method and
   endpoint design instead.

3. Design the HTTP API (method + URL + brief description of request and
   response body) for a simple to-do list service with the following
   operations: list all items, get one item by ID, create a new item, update
   an existing item, delete an item.

---

### Homework 2 — Implement a REST Endpoint with FastAPI

**Learning goal:** Experience URL routing, path/query parameters, and JSON
responses in a modern Python web framework.

**Tasks:**

1. Install FastAPI and uvicorn (`pip install fastapi uvicorn`) and implement
   the following endpoints for an in-memory to-do list (a plain Python dict
   is sufficient for storage):

   - `GET /todos` — return all items as a JSON list
   - `GET /todos/{id}` — return one item; return HTTP 404 if not found
   - `POST /todos` — create a new item from a JSON body `{"title": "...",
     "done": false}`; return the created item with its assigned ID
   - `DELETE /todos/{id}` — delete an item; return HTTP 404 if not found

2. Visit `http://localhost:8000/docs` after starting the server.  Screenshot
   or describe what you see.  What generates this page automatically, and what
   is the underlying standard?

3. Add a query parameter `?done=true` to `GET /todos` that filters the list
   to only completed items.  Implement it and demonstrate it with `curl`.

---

### Homework 3 — Cookies and Session State

**Learning goal:** Trace session state across HTTP requests; understand the
cookie lifecycle and its security implications.

**Tasks:**

1. Using browser developer tools (Network tab), log into any website that
   uses cookie-based sessions (e.g., a university portal, GitHub, or a
   locally-running Django app).  Record:
   - The `Set-Cookie` header sent by the server after login (redact any
     sensitive value — just describe the fields: name, `HttpOnly`, `Secure`,
     `SameSite`, expiry).
   - Whether the cookie is sent back with subsequent requests, and to which
     URLs.

2. A stateful server stores the user's shopping cart in server-side memory,
   keyed by a session ID in a cookie.  A stateless redesign instead serialises
   the entire cart into a signed cookie sent to the browser.

   Compare the two designs on the following dimensions:
   - What happens to cart data if the server restarts?
   - What is the maximum size of the cart?
   - What is the security risk if the signing key is weak or leaked?

3. The slides mention that cookies can be stolen maliciously.  Name and
   briefly explain two browser security attributes (`HttpOnly`, `Secure`,
   `SameSite`) and describe what attack each one mitigates.

---

### Homework 4 — AJAX with the fetch API

**Learning goal:** Implement asynchronous page updates using `fetch`,
Promises, and `async`/`await`.

**Tasks:**

1. Build a minimal single-file HTML page (`todo.html`) that:
   - On load, calls `GET /todos` (from Homework 2) and renders the list
     of to-do items in a `<ul>` without reloading the page.
   - Has a form with a text input and a "Add" button.  On submit, calls
     `POST /todos` with the new title, then refreshes the displayed list —
     again without a full page reload.
   - Uses `async`/`await` and checks `response.ok`, displaying an error
     message in the page (not an `alert()`) if the server returns a non-2xx
     status.

2. Open the browser's Network tab while using your page.  Identify which
   requests are triggered by clicking "Add" and describe what you see
   (method, URL, request body, response status, response body).

3. Rewrite the `loadTodos()` function first using plain `.then()` chains
   (no `async`/`await`), then using `async`/`await`.  Compare readability.

---

### Homework 5 — From Callback Hell to Promises to async/await

**Learning goal:** Recognise and refactor deeply nested callbacks; understand
the event loop execution model.

**Tasks:**

1. The following Node.js pseudocode reads a config file, then fetches a URL
   listed in the config, then writes the result to a log file — all with
   callbacks:

   ```javascript
   fs.readFile('config.json', (err, data) => {
     if (err) { console.error(err); return; }
     const config = JSON.parse(data);
     fetch(config.url)
       .then(res => res.text())
       .then(body => {
         fs.writeFile('log.txt', body, (err) => {
           if (err) console.error(err);
           else console.log('Done');
         });
       });
   });
   ```

   Identify the problems with this code (error propagation, readability,
   nesting depth).

2. Rewrite the code using `async`/`await` with `fs.promises` (Node's
   promise-based file API).  Handle all errors in a single `try/catch` block.

3. The slides explain that the event loop calls callbacks
   *synchronously and to completion*.  Predict the output order of the
   following snippet and explain why:

   ```javascript
   console.log('A');
   setTimeout(() => console.log('B'), 0);
   Promise.resolve().then(() => console.log('C'));
   console.log('D');
   ```

   (Hint: microtask queue vs. macrotask queue.)

---

### Homework 6 — CORS Preflight: Sequence Diagram

**Learning goal:** Understand the CORS handshake; know when a preflight
request is triggered and what the browser checks.

*(This exercise is mentioned explicitly in the lecture slides.)*

**Tasks:**

1. Draw a sequence diagram showing the full CORS preflight flow for the
   following scenario:
   - JavaScript running at `https://app.foo.com` calls
     `fetch('https://api.bar.com/data', { method: 'POST',
     headers: { 'Content-Type': 'application/json' } })`
   - `api.bar.com` is configured to allow cross-origin requests from
     `app.foo.com`.

   Your diagram must show: browser, `app.foo.com` (origin server),
   `api.bar.com` (target server).  Include the `OPTIONS` preflight request,
   the preflight response with `Access-Control-*` headers, the actual POST
   request, and the actual response.

2. Under what conditions does the browser skip the preflight `OPTIONS` request
   and send the actual request directly?  (These are called *simple requests*
   — look up the criteria in the MDN CORS documentation.)

3. A backend developer says: "CORS is just a frontend problem — if I disable
   it on the server the browser will block the request anyway, so my API is
   safe."  Is this correct?  Explain why or why not, and describe one attack
   that CORS does *not* protect against.

---

## Dependency Map

```
Slides: HTTP methods (GET/POST/PUT/DELETE)
    → Quiz 1, Quiz 2
    → Homework 1 (REST semantics)
    → Homework 2 (FastAPI implementation)

Slides: HTTP statelessness, cookies
    → Quiz 4
    → Homework 3 (cookies and session state)

Slides: AJAX, event loop, callbacks, promises, fetch
    → Quiz 5, Quiz 6, Quiz 7
    → Homework 4 (fetch API)
    → Homework 5 (callbacks → async/await)

Slides: HTTP/2 multiplexing, HOL blocking
    → Quiz 8

Slides: WebSocket, server push
    → Quiz 9

Slides: SOP, CORS
    → Quiz 10
    → Homework 6 (CORS sequence diagram)
```

Homework 4 (AJAX) depends on Homework 2 (FastAPI server) being running.

---

## Notes for the Instructor

- **Quiz 6** (fetch and HTTP 404) is a reliable misconception trap —
  almost every student assumes fetch rejects on 4xx/5xx.  Worth dwelling on.

- **Quiz 5** (event loop runs callbacks to completion) sets up Homework 5,
  question 3.  The microtask vs. macrotask output order (`A D C B`) reliably
  surprises students and provokes good discussion about the event loop
  internals.

- **Homework 3, task 2** (signed cookie cart vs. server-side session) maps
  directly to JWT (JSON Web Tokens), which appears later in the security
  section.  Consider revisiting it then.

- **Homework 6** (CORS diagram) is the explicit "Homework!" callout in the
  slides.  Keep it — the act of drawing the sequence makes the
  browser-initiates-OPTIONS flow stick far better than just describing it.
