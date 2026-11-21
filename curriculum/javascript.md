---
kind: learning_path
title: JavaScript: Logic and Interaction
slug: javascript-foundations
category: programming
level: beginner
duration: 6 stages · self-paced
skill_stack: JavaScript, DOM, asynchronous programming, testing
summary: Learn core JavaScript and use it to make accessible, resilient web interactions.
language: en
stages:
  - {order: 1, stage: Beginner, slug: beginner-javascript, estimated_minutes: 45}
  - {order: 2, stage: Intermediate, slug: intermediate-javascript, estimated_minutes: 50}
  - {order: 3, stage: Advanced, slug: advanced-javascript, estimated_minutes: 55}
  - {order: 4, stage: Projects, slug: javascript-projects, estimated_minutes: 70}
  - {order: 5, stage: Challenges, slug: javascript-challenges, estimated_minutes: 40}
  - {order: 6, stage: Final Assessment, slug: javascript-assessment, estimated_minutes: 50}
references:
  - https://tc39.es/ecma262/
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript
originality: Original CoderGrid instructional content; references identify authoritative standards.
---

# JavaScript · Logic and Interaction

JavaScript is a programming language standardized as ECMAScript. In a browser, it can respond to user actions and update a document. Begin with values and decisions, then learn the browser APIs that host your code.

## Beginner

**Objectives:** store values, choose types, write a function, and use conditions and loops.

```js
const item = "mango seedlings";
let boxes = 4;
function totalPlants(perBox) {
  return boxes * perBox;
}
if (totalPlants(6) >= 20) console.log(`Prepare ${totalPlants(6)} labels for ${item}.`);
```

`const` prevents rebinding a name; `let` allows reassignment. Values still have their own types. A function groups reusable work; parameters are inputs and `return` gives a result. Template literals interpolate expressions with `${}`.

**Try it:** calculate the cost of five notebooks at 120 shillings each and apply a 10% discount. Keep money as integer shillings in this exercise to avoid floating-point rounding surprises.

**Practice / answers:** What does `===` check? Equality without type coercion. What is returned from a function with no `return`? `undefined`. Which loop suits iterating over an array's values? `for...of`.

**Common errors and habits:** misspelled names, confusing `=` with comparison, and mutating shared data unexpectedly. Use descriptive names, strict equality, small functions, and inspect values with `console.log` or devtools.

## Intermediate

**Objectives:** transform arrays and objects, respond to DOM events, and handle input safely.

```js
const prices = [80, 120, 60];
const total = prices.reduce((sum, price) => sum + price, 0);
const button = document.querySelector("#add-item");
button.addEventListener("click", () => {
  document.querySelector("#status").textContent = `Basket total: KSh ${total}`;
});
```

`reduce` combines values into one result. `querySelector` returns a matching element or `null`; event listeners run a callback when an event occurs. `textContent` inserts text rather than parsing user data as HTML.

**Exercise:** make a study-session counter with “Add 25 minutes” and “Reset” buttons. Update a status region and ensure each button works by keyboard. Add a guard if an element may be absent.

**Questions:** Why is `textContent` safer for untrusted text than `innerHTML`? It does not interpret input as markup. What does an array's `map` return? A new array of transformed values. What can `querySelector` return? An element or `null`.

**Mini project:** build a transport fare estimator using fictional route distance and fare bands. Validate empty or invalid values and explain the estimate. Never collect or store real travel histories.

**Habits:** separate calculation from DOM updates, validate input, avoid inline event attributes, and provide visible feedback in text.

## Advanced

**Objectives:** coordinate asynchronous work, propagate failures, and reason about scope and modules.

```js
async function loadNotices() {
  try {
    const response = await fetch("/api/notices");
    if (!response.ok) throw new Error(`Request failed: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Could not load notices", error);
    return [];
  }
}
```

`await` pauses this async function until a promise settles; it does not block the whole browser. A fulfilled HTTP request can still have a non-success status, so check `response.ok`. Modules use explicit `export` and `import` boundaries.

**Challenge:** add an abortable search that avoids rendering stale responses. Consider `AbortController`, debouncing, loading state, empty state, and request failure. Test with delayed and failed network responses.

**Best practices:** avoid blocking the main thread with long loops; use semantic controls; do not place secrets in browser code; avoid `eval`; handle promise rejection and empty data deliberately.

**Quiz / answers:** Does `fetch` reject on HTTP 404? Typically no; check `ok`/status. What keyword declares an async function? `async`. Why split modules? To make dependencies and responsibilities explicit.

## Projects

Build **Community Water Point Log (Demo)**: enter fictional water-point status, filter by availability, and show the last updated time. Keep the data in memory or local demo data; do not publish real household locations. Include input validation, empty/error states, keyboard operation, and a README explaining the data boundary.

**Review:** does the core calculation work independently of the UI? Are failures visible? Does user input appear as text? Can another learner reproduce the project offline?

## Challenges

1. Trace a loop and predict its output before running it.
2. Refactor repeated fare calculation into one pure function.
3. Prevent a stale network response from replacing newer search results.
4. Find and fix an unhandled `null` element and rejected promise.

**Hint:** use browser devtools breakpoints and small reproducible inputs. Write down expected outputs before changing code.

## Final Assessment

Create a small interactive expense split calculator and explain its data flow.

1. Why use `const` by default? It prevents accidental rebinding.
2. Which operator checks strict equality? `===`.
3. How do you safely display untrusted plain text in the DOM? `textContent`.
4. What should code check after `fetch`? Response status/`ok`, then parse the body as appropriate.
5. What does a pure function avoid? Side effects and dependence on hidden mutable state.

**Rubric (20):** correct logic 5; clear functions and data structures 4; validation and errors 4; accessible DOM feedback 4; explanation and readable code 3.
