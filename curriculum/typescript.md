---
kind: learning_path
title: TypeScript: Safer JavaScript at Scale
slug: typescript-foundations
category: programming
level: beginner
duration: 6 stages · self-paced
skill_stack: TypeScript, JavaScript, type modeling, tooling
summary: Add useful static checks to JavaScript projects and model data and functions with confidence.
language: en
stages:
  - {order: 1, stage: Beginner, slug: beginner-typescript, estimated_minutes: 45}
  - {order: 2, stage: Intermediate, slug: intermediate-typescript, estimated_minutes: 50}
  - {order: 3, stage: Advanced, slug: advanced-typescript, estimated_minutes: 55}
  - {order: 4, stage: Projects, slug: typescript-projects, estimated_minutes: 70}
  - {order: 5, stage: Challenges, slug: typescript-challenges, estimated_minutes: 40}
  - {order: 6, stage: Final Assessment, slug: typescript-assessment, estimated_minutes: 50}
references:
  - https://www.typescriptlang.org/docs/handbook/intro.html
  - https://tc39.es/ecma262/
originality: Original KodaGrid instructional content; references identify authoritative standards.
---

# TypeScript · Safer JavaScript at Scale

TypeScript checks relationships in your code before runtime and then emits JavaScript. Its types are erased during compilation: a type annotation does not validate data arriving from a form, file, or network. Use runtime checks at those boundaries.

## Beginner

**Objectives:** annotate values and function parameters, describe object shapes, and read compiler errors as feedback.

```ts
type Workshop = { title: string; seats: number; isOpen: boolean };
function seatsRemaining(workshop: Workshop, booked: number): number {
  return Math.max(0, workshop.seats - booked);
}
const robotics: Workshop = { title: "Solar rover lab", seats: 18, isOpen: true };
```

`type` names a reusable shape; `: string` and `: number` annotate types; a function's return annotation comes after `)`. TypeScript can infer many local types, so annotations are most useful at interfaces and function boundaries.

**Try it:** define a `Product` shape with `name`, `priceKsh`, and optional `stock`; write a function that returns whether it is available.

**Practice / answers:** Does a type annotation convert a string to a number? No. What does `?` on a property mean? The property may be omitted. Is TypeScript a runtime? No, it compiles to JavaScript.

**Common mistakes and habits:** using `any` removes checking; a type assertion does not transform data; non-null `!` can hide a real bug. Prefer inference, narrow types, and model uncertainty honestly.

## Intermediate

**Objectives:** use unions, narrowing, interfaces, and generics to express alternatives and reusable operations.

```ts
type Result = { ok: true; value: number } | { ok: false; message: string };
function describe(result: Result): string {
  if (result.ok) return `Total: KSh ${result.value}`;
  return `Could not calculate: ${result.message}`;
}
function first<T>(items: T[]): T | undefined { return items[0]; }
```

The discriminant `ok` lets control flow narrow `Result` to the appropriate member. `T` is a type parameter, preserving the input element type rather than weakening it to `any`.

**Exercise:** model an order as `"draft" | "paid" | "cancelled"`; write a function whose return text handles every state. Add a new state and observe where checking reveals missing logic.

**Questions:** What does a union mean? A value may conform to one of several alternatives. What is narrowing? Using runtime checks/control flow to refine a type. Why use generics? Reuse code while preserving relationships between types.

**Mini project:** make a typed inventory summary for fictional market goods. Separate item data, calculation functions, and presentation; represent “not found” without unsafe assertions.

**Habits:** use strict compiler settings, discriminated unions for state, and `unknown` for untrusted values until checked.

## Advanced

**Objectives:** design module boundaries, constrain generic functions, and validate external data at runtime.

```ts
type ApiItem = { id: string; label: string };
function isApiItem(value: unknown): value is ApiItem {
  return typeof value === "object" && value !== null
    && "id" in value && typeof value.id === "string"
    && "label" in value && typeof value.label === "string";
}
```

The predicate `value is ApiItem` informs the checker after the function returns true; the checks themselves are runtime JavaScript. A production parser should also decide how to handle extra or malformed fields and report useful errors.

**Challenge:** parse a JSON response that may be incomplete, validate each record, and return a typed success/error result. Keep transport errors distinct from invalid data.

**Best practices:** enable `strict`; avoid widening literal states unnecessarily; expose small public types from modules; don't mirror every implementation detail in a type. Keep runtime validation at trust boundaries.

**Quiz / answers:** Does `as ApiItem` validate JSON? No. What does `unknown` require? Narrowing before use. Does emitted JavaScript contain interfaces? No, type-only constructs are erased.

## Projects

Build **Typed Study Group Planner** with typed session and participant models, capacity checks, and explicit success/failure results. Use local fictional entries, strict mode, and at least one runtime parser for imported JSON. Include instructions to install TypeScript, run the type checker, and produce a build.

**Review:** can invalid states be represented? Are unchecked external values constrained before use? Does the project separate compile-time guarantees from runtime behaviour?

## Challenges

1. Replace an `any` array with a type-safe model.
2. Make a union exhaustive and ensure adding a state causes a useful compiler signal.
3. Write a generic `groupBy` signature without losing element types.
4. Validate an `unknown` value without type assertions.

**Hint:** use `never` in an exhaustive switch and inspect narrowed types in your editor.

## Final Assessment

Model and implement a typed attendance summary from an untrusted JSON value.

1. What does the compiler do with `interface` in emitted JS? Erases it.
2. What is the role of a union? Describe allowed alternatives.
3. How does a type guard help? It narrows after a runtime check.
4. Why is `any` risky? It disables checking across its use.
5. What protects a network boundary? Runtime validation plus error handling.

**Rubric (20):** accurate model 5; useful narrowing/generics 4; runtime validation 5; strict readable implementation 3; explanation 3.
