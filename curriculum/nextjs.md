---
kind: learning_path
title: Next.js: Full-Stack React Applications
slug: nextjs-foundations
category: web
level: beginner
duration: 6 stages · self-paced
skill_stack: Next.js, React, routing, server rendering, data handling
summary: Build routed React applications with clear server/client boundaries and reliable data states.
language: en
stages:
  - {order: 1, stage: Beginner, slug: beginner-nextjs, estimated_minutes: 45}
  - {order: 2, stage: Intermediate, slug: intermediate-nextjs, estimated_minutes: 50}
  - {order: 3, stage: Advanced, slug: advanced-nextjs, estimated_minutes: 55}
  - {order: 4, stage: Projects, slug: nextjs-projects, estimated_minutes: 70}
  - {order: 5, stage: Challenges, slug: nextjs-challenges, estimated_minutes: 40}
  - {order: 6, stage: Final Assessment, slug: nextjs-assessment, estimated_minutes: 50}
references:
  - https://nextjs.org/docs
  - https://react.dev/learn
originality: Original CoderGrid instructional content; references identify official documentation.
---

# Next.js · Full-Stack React Applications

Next.js is a React framework. This path uses the App Router model documented by Next.js. A route is commonly represented by folders and special files; server and client components have different capabilities. Check current official documentation when starting a real project because framework conventions evolve.

## Beginner

**Objectives:** identify a route from the file tree, create a page and shared layout, and render semantic React markup.

```jsx
// app/page.jsx
export default function HomePage() {
  return <main><h1>Skills near you</h1><p>Explore local learning sessions.</p></main>;
}
```

In the App Router, `app/page` defines a route's page and `app/layout` provides shared structure. A server component is the default in this model. Render data and markup on the server when interaction is not needed in the browser.

**Try it:** add `app/sessions/page.jsx` and a shared navigation in the root layout. Run the project using its documented development command and inspect both routes.

**Practice / answers:** Which file supplies a route page? `page` in its route folder. What does a layout share? UI around pages, such as navigation. Is every component automatically a client component? No.

**Mistakes / habits:** placing files in the wrong route folder; using browser-only APIs in a server component; omitting semantic landmarks. Keep route responsibilities small and read errors carefully.

## Intermediate

**Objectives:** fetch data on the server, create dynamic route segments, and build forms with deliberate validation.

```jsx
export default async function SessionPage() {
  const response = await fetch("https://example.invalid/api/sessions");
  if (!response.ok) throw new Error("Sessions are temporarily unavailable");
  const sessions = await response.json(); // Validate untrusted response data in a real application.
  return <main><h1>Sessions</h1>{sessions.map(item => <p key={item.id}>{item.title}</p>)}</main>;
}
```

This illustrative URL is intentionally non-routable. Replace it with a real endpoint for a project. Server-side data access can keep credentials off the browser, but a server still needs authentication, authorization, and validation. Dynamic segments such as `[slug]` represent variable path parts.

**Exercise:** make a dynamic session detail route using fictional local data. Show not-found and empty states. Do not expose private records based only on an untrusted URL parameter.

**Practice:** Why check `response.ok`? HTTP error statuses may still yield a response. What is a dynamic segment? A route folder placeholder for a path value. Where should secrets live? Server-side environment/configuration, never public client bundles.

**Mini project:** create a community event catalogue with list/detail pages and a registration form mock-up that validates required fields.

**Habits:** distinguish server and client needs, validate external data, and make loading/error/not-found behaviour explicit.

## Advanced

**Objectives:** define client boundaries, reason about caching and revalidation, and protect server mutations.

```jsx
"use client";
import { useState } from "react";
export function SaveButton() {
  const [saved, setSaved] = useState(false);
  return <button onClick={() => setSaved(value => !value)} aria-pressed={saved}>
    {saved ? "Saved" : "Save session"}
  </button>;
}
```

`"use client"` marks a client entry boundary when browser interaction/state is needed. Keep it low in the tree where possible. Caching and revalidation behaviour depends on the current Next.js version and fetch/render context; decide freshness and privacy requirements explicitly, and verify supported options in the docs.

**Challenge:** design an authenticated edit flow with server-side authorization, input validation, useful error feedback, and a refresh strategy. Explain which parts must run on the server and why.

**Best practices:** minimize client JavaScript, avoid leaking secrets through public environment variables, protect mutations against unauthorized requests, and test production build behaviour as well as development.

**Quiz / answers:** What requires a client component? Browser interaction such as state/event handling. Does hiding a button enforce permission? No; authorize on the server. Should private user data be cached publicly? No; choose cache policy based on data privacy.

## Projects

Build **Community Event Hub** with an index, dynamic event detail pages, accessible RSVP form, and clear success/failure states. Start with local mock data. Document which data would be server-only, how real registrations would be authorized, and what caching policy suits public event details versus private responses.

**Review:** are routes predictable? Can an unauthorized user invoke a mutation? Do server/client boundaries match actual needs? Are loading and failure messages helpful?

## Challenges

1. Move a component using state behind a client boundary.
2. Add a dynamic detail route with a not-found case.
3. Diagnose stale data by reviewing cache and revalidation choices.
4. Prevent a user from editing another person's record on the server.

**Hint:** inspect the route tree and request lifecycle; never treat UI visibility as a security control.

## Final Assessment

Plan a small Next.js catalogue and implement one list and detail route.

1. What does `page` do? Defines route UI.
2. What is the default component model in the App Router? Server components unless a client boundary is declared.
3. What is the purpose of `"use client"`? Declare a client module boundary for interactive features.
4. Where must authorization happen? On trusted server-side code for the requested operation.
5. What should be reviewed when data looks stale? Fetch/cache/revalidation behaviour for the current version.

**Rubric (20):** route structure 4; correct server/client split 4; error and not-found handling 4; security reasoning 5; setup documentation 3.
