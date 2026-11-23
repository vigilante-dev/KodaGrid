---
kind: learning_path
title: React: Build Interfaces from Components
slug: react-foundations
category: web
level: beginner
duration: 6 stages · self-paced
skill_stack: React, JavaScript, components, state, accessibility
summary: Compose interactive interfaces from components, props, state, and event-driven updates.
language: en
stages:
  - {order: 1, stage: Beginner, slug: beginner-react, estimated_minutes: 45}
  - {order: 2, stage: Intermediate, slug: intermediate-react, estimated_minutes: 50}
  - {order: 3, stage: Advanced, slug: advanced-react, estimated_minutes: 55}
  - {order: 4, stage: Projects, slug: react-projects, estimated_minutes: 70}
  - {order: 5, stage: Challenges, slug: react-challenges, estimated_minutes: 40}
  - {order: 6, stage: Final Assessment, slug: react-assessment, estimated_minutes: 50}
references:
  - https://react.dev/learn
originality: Original KodaGrid instructional content; references identify official documentation.
---

# React · Build Interfaces from Components

React is a JavaScript library for building user interfaces from components. Components describe what should appear for current props and state; React updates the rendered interface as data changes. Examples use function components and JSX.

## Beginner

**Objectives:** write a component, pass props, render lists with stable keys, and express conditional content.

```jsx
function SessionCard({ title, seats }) {
  return <article><h2>{title}</h2><p>{seats} places available</p></article>;
}
function Sessions() {
  const items = [{ id: "s1", title: "Solar lantern basics", seats: 8 }];
  return <main>{items.map(item => <SessionCard key={item.id} {...item} />)}</main>;
}
```

JSX lets JavaScript describe elements. A component begins with a capital letter; props are inputs and should be treated as read-only. A stable `key` helps React match list items across updates.

**Try it:** add two fictional sessions and render a “No sessions yet” message when the list is empty. Use unique ids, not array positions, when entries can move.

**Practice / answers:** What are props? Inputs from a parent. Why is a key needed? To identify list items between renders. What does `{}` do in JSX? Inserts a JavaScript expression.

**Common mistakes / habits:** lowercase component names become HTML tags; missing keys cause warnings; changing props inside a child breaks one-way data flow. Keep components focused and use semantic HTML.

## Intermediate

**Objectives:** manage local state, handle events, and control a form input.

```jsx
import { useState } from "react";
function Counter() {
  const [places, setPlaces] = useState(0);
  return <section>
    <p aria-live="polite">Places reserved: {places}</p>
    <button onClick={() => setPlaces(current => current + 1)}>Reserve one</button>
  </section>;
}
```

`useState` returns current state and a setter. The functional setter receives the latest value, useful when deriving the next value from the previous one. State updates schedule a render; they do not mutate the existing variable.

**Exercise:** make a controlled search field that filters fictional service cards. Include a clear button and a helpful no-results message. Ensure inputs have labels.

**Practice:** When should state be lifted? When sibling components need to coordinate on the same value. What does an event handler receive? The event, when its parameter is used. Should derived filtered results usually be stored as separate state? No; calculate them from source state and query.

**Mini project:** build a simple study checklist with add, complete, and remove actions. Use stable ids and descriptive button names.

**Habits:** keep state minimal, never mutate arrays/objects in state, and show loading/error/empty states.

## Advanced

**Objectives:** design effects around external systems, reduce unnecessary work, and test accessible behaviour.

```jsx
useEffect(() => {
  const controller = new AbortController();
  fetch("/api/sessions", { signal: controller.signal })
    .then(response => { if (!response.ok) throw new Error("Load failed"); return response.json(); })
    .then(setSessions)
    .catch(error => { if (error.name !== "AbortError") setError(error.message); });
  return () => controller.abort();
}, []);
```

Effects synchronize with external systems and need cleanup where subscriptions or requests outlive a render. Don't use an effect for a value that can be calculated during render. Real APIs also need response shape validation.

**Challenge:** implement a searchable session list with loading, empty, and retryable error states. Test from a user's perspective using accessible roles and labels. Avoid premature memoization; measure before optimizing.

**Best practices:** keep components pure, place state near its users, keep effects narrow, and use context for genuinely shared cross-tree values. Do not store secrets in client-side code.

**Quiz / answers:** What causes a component to re-render? Relevant state/props/context changes, among other scheduling reasons. Why cleanup an effect? To release or cancel external work. Does `useMemo` guarantee performance improvement? No; profile and use it when useful.

## Projects

Build **Local Learning Circle Board** with sessions, category filter, saved items, and a form. Use fictional data, keyboard-accessible controls, clear empty/error states, and responsive layout. Keep state transitions understandable and include a short component map.

**Review:** are list keys stable? Can a screen reader identify controls? Is derived data calculated instead of duplicated? Are effects limited to external synchronization?

## Challenges

1. Fix a component that mutates an array in state.
2. Lift a filter value so two sibling components stay in sync.
3. Clean up a subscription when a component unmounts.
4. Find why an effect repeats due to an unstable dependency.

**Hint:** draw the parent-child data flow; distinguish render calculations from external side effects.

## Final Assessment

Create an accessible React directory with filtering and a reserve action.

1. What is a prop? Read-only input to a component.
2. What does state represent? Values that change over time and affect rendering.
3. Why use keys? Stable identity for rendered list items.
4. What belongs in an effect? Synchronization with an external system.
5. How should state arrays be updated? By producing a new array, not mutating the existing one.

**Rubric (20):** component design 4; correct state/data flow 5; accessible interaction 4; resilient states 4; code explanation 3.
