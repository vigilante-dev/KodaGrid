---
kind: learning_path
title: Node.js: JavaScript Beyond the Browser
slug: nodejs-foundations
category: programming
level: beginner
duration: 6 stages · self-paced
skill_stack: Node.js, JavaScript, npm, HTTP, asynchronous I/O
summary: Use JavaScript on the server to build command-line tools and small, secure HTTP services.
language: en
stages:
  - {order: 1, stage: Beginner, slug: beginner-nodejs, estimated_minutes: 45}
  - {order: 2, stage: Intermediate, slug: intermediate-nodejs, estimated_minutes: 50}
  - {order: 3, stage: Advanced, slug: advanced-nodejs, estimated_minutes: 55}
  - {order: 4, stage: Projects, slug: nodejs-projects, estimated_minutes: 70}
  - {order: 5, stage: Challenges, slug: nodejs-challenges, estimated_minutes: 40}
  - {order: 6, stage: Final Assessment, slug: nodejs-assessment, estimated_minutes: 50}
references:
  - https://nodejs.org/docs/latest/api/
  - https://nodejs.org/en/learn
originality: Original CoderGrid instructional content; references identify official documentation.
---

# Node.js · JavaScript Beyond the Browser

Node.js runs JavaScript outside a browser and provides APIs for files, processes, networking, and other server tasks. Its event-driven I/O model is useful for many network services, but long CPU work can still delay other work on the event loop.

## Beginner

**Objectives:** run a script, use modules, read command-line arguments, and distinguish browser APIs from Node APIs.

```js
// greet.mjs
const learner = process.argv[2] ?? "friend";
console.log(`Welcome to the coding circle, ${learner}!`);
```

Run with `node greet.mjs Amina`. `process.argv` contains command-line arguments; `??` supplies a fallback only for `null` or `undefined`. Node modules have explicit exports/imports; browser globals such as `document` do not exist in ordinary Node processes.

**Try it:** write a script that accepts a fictional club name and prints a welcome line. Test missing arguments and names with spaces.

**Practice / answers:** Which command runs the file? `node file.mjs`. What is `process.argv`? An array of process arguments. Is `document.querySelector` available by default in Node? No.

**Mistakes / habits:** forgetting module mode, assuming browser APIs, and treating all input as valid. State supported Node version and script command in the README.

## Intermediate

**Objectives:** use promises and built-in modules, and expose a small HTTP endpoint.

```js
import { createServer } from "node:http";
const server = createServer((request, response) => {
  response.writeHead(200, { "content-type": "text/plain; charset=utf-8" });
  response.end("CoderGrid practice server is ready.\n");
});
server.listen(3000, "127.0.0.1");
```

The server callback receives a request and response. Binding to loopback makes this local practice service accessible from the same device only. A public server needs deliberate host, HTTPS, deployment, and security configuration.

**Exercise:** add `/health` and `/about` routes; return 404 for unknown paths. Try with a browser or command-line HTTP client. Do not build routes by concatenating untrusted file paths.

**Practice:** What does `writeHead` set? Status and headers. Why return 404? The route was not found. Why bind to `127.0.0.1` for local work? It restricts access to the local machine.

**Mini project:** create a local JSON endpoint for fictional workshop schedules with a clear content type and status codes.

**Habits:** use asynchronous filesystem APIs, handle rejected promises, validate request bodies, and keep configuration outside source code.

## Advanced

**Objectives:** structure request handling, limit resource use, and design graceful shutdown and error paths.

```js
import { readFile } from "node:fs/promises";
try {
  const text = await readFile(new URL("./notice.txt", import.meta.url), "utf8");
  console.log(text.trim());
} catch (error) {
  if (error.code === "ENOENT") console.log("No notice file yet.");
  else throw error;
}
```

`node:fs/promises` provides promise-based file operations. Resolving from `import.meta.url` avoids dependence on the caller's working directory. Handle expected errors narrowly; unexpected errors should remain observable. For HTTP services, cap request sizes and avoid blocking synchronous work in request handlers.

**Challenge:** add a graceful shutdown handler and a request timeout strategy to the local server. Document how malformed paths, oversized payloads, and failures are handled.

**Best practices:** keep dependencies minimal and maintained, lock dependency versions, avoid logging credentials, use parameterized database calls, and keep secrets in environment/configuration stores.

**Quiz / answers:** What is the event loop's risk with CPU-heavy work? It blocks timely handling of other callbacks. What is a lockfile for? Reproducible dependency resolution. Why use `node:` specifiers? They clearly identify built-in modules.

## Projects

Build **Offline Club Notice API** that serves fictional notices and a health route. Include input bounds, correct HTTP status codes, structured logs without secrets, and tests for normal and unknown routes. Keep it bound to localhost by default and describe what would be required before public deployment.

**Review:** are requests bounded? Are errors mapped appropriately? Does startup fail clearly if a required configuration is absent? Can a reviewer reproduce the app from its package manifest and lockfile?

## Challenges

1. Convert a callback-based flow to `async`/`await` while preserving errors.
2. Prevent a path traversal issue in a file-serving route.
3. Add content type and a 404 response for an unknown endpoint.
4. Find synchronous work that blocks request handling.

**Hint:** treat paths and request bodies as untrusted; use allow-lists and size limits.

## Final Assessment

Implement and test a local read-only JSON service.

1. What runs JavaScript outside a browser? Node.js runtime.
2. Does Node's event loop make CPU-heavy code harmless? No.
3. Which status indicates no matching route? 404.
4. How should SQL values be inserted? Parameterized statements through a database driver.
5. Why use async file APIs? They avoid synchronously blocking the event loop for routine I/O.

**Rubric (20):** correct routes and status 5; async/error handling 4; input/security boundaries 5; reproducibility 3; tests and explanation 3.
