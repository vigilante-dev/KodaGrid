---
kind: learning_path
title: CSS: Layout and Visual Design
slug: css-foundations
category: web
level: beginner
duration: 6 stages · self-paced
skill_stack: CSS, responsive design, accessibility
summary: Style readable, adaptable interfaces with the cascade, layout systems, and reusable design rules.
language: en
stages:
  - {order: 1, stage: Beginner, slug: beginner-css, estimated_minutes: 40}
  - {order: 2, stage: Intermediate, slug: intermediate-css, estimated_minutes: 45}
  - {order: 3, stage: Advanced, slug: advanced-css, estimated_minutes: 50}
  - {order: 4, stage: Projects, slug: css-projects, estimated_minutes: 60}
  - {order: 5, stage: Challenges, slug: css-challenges, estimated_minutes: 35}
  - {order: 6, stage: Final Assessment, slug: css-assessment, estimated_minutes: 45}
references:
  - https://www.w3.org/TR/css/
  - https://www.w3.org/WAI/WCAG22/Understanding/
originality: Original KodaGrid instructional content; references identify authoritative standards.
---

# CSS · Layout and Visual Design

CSS describes how a document is presented. A rule has a selector and declarations; the cascade resolves competing rules using origin, importance, specificity, and source order. Learn to build a clear layout before decorating it.

## Beginner

**Objectives:** connect a stylesheet, select elements by class, apply readable type and colour, and explain the box model.

```html
<article class="notice"><h1>Community coding day</h1><p>Bring a question to explore.</p></article>
```
```css
* { box-sizing: border-box; }
body { margin: 0; font-family: system-ui, sans-serif; color: #17324d; }
.notice { max-width: 42rem; margin: 2rem auto; padding: 1.5rem; border: 2px solid #167c67; }
```

**Breakdown:** `.notice` selects a class; declarations are `property: value`; `max-width` limits line length; margin sits outside the border, padding inside. `box-sizing` makes declared widths include padding and border.

**Try it:** make a three-item list of local services into cards, then resize the browser. Keep text legible and avoid using colour as the only status signal.

**Practice with answers:** Which selector targets `id="menu"`? `#menu`. Is padding inside or outside the border? Inside. Why prefer a class for repeated styling? It can be reused without pretending the element is unique.

**Mistakes / habits:** overly broad selectors create surprises; fixed widths overflow small screens; low contrast excludes readers. Start with semantic HTML, use classes for reusable patterns, and inspect the page at narrow widths.

## Intermediate

**Objectives:** use Flexbox and Grid for layout, add responsive rules, and centralize repeated values.

```css
:root { --ink: #15354b; --brand: #087e68; --space: 1rem; }
.service-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr)); gap: var(--space); }
.service-card { padding: calc(var(--space) * 1.25); color: var(--ink); }
```

Grid handles two-dimensional tracks; Flexbox distributes items along one axis. `auto-fit` and `minmax()` allow columns to adapt to available width. A custom property declared on `:root` can be reused via `var()`.

**Interactive exercise:** build a schedule with a flexible header and cards. Use browser devtools to toggle a declaration and observe the cascade. Add a `:focus-visible` style that is easy to see.

**Practice:** When is Grid useful? For row-and-column relationships. What does `@media (max-width: 40rem)` do? Applies enclosed rules when the viewport matches that condition. What is a focus indicator for? Showing keyboard focus location.

**Mini project:** style a mobile-first community market directory with category cards, clear headings, a visible contact action, and readable spacing. Test at 320px, tablet, and desktop widths.

**Mistakes / habits:** avoid specificity arms races and `!important` as a routine fix; don't hide focus outlines without replacement; test zoom and long text. Keep design tokens and layout rules grouped clearly.

## Advanced

**Objectives:** reason about cascade layers, container-aware components, motion preferences, and maintainable architecture.

```css
@layer reset, components, utilities;
@layer components {
  .price { font-variant-numeric: tabular-nums; }
  @container (min-width: 34rem) { .profile { grid-template-columns: 8rem 1fr; } }
}
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { scroll-behavior: auto; animation-duration: .01ms !important; } }
```

Container queries let a component respond to its containing space when its parent establishes a query container (`container-type`). Reduced-motion preferences should remove nonessential movement; avoid breaking essential state transitions. Cascade layers make intended precedence explicit.

**Challenge exercise:** create a reusable card that works in both narrow sidebar and wide content placements without viewport-specific assumptions. Audit contrast, zoom to 200%, and emulate reduced motion.

**Best practices:** progressive enhancement, logical properties (`margin-inline`), fluid sizing with sensible bounds, and documented tokens. Do not use CSS to reorder content in a way that conflicts with reading or keyboard order.

**Quiz / answers:** Does higher specificity always win? No; cascade origin, importance, and layer precedence are considered first. What enables a container query? A query container ancestor. Which user preference can signal less motion? `prefers-reduced-motion`.

## Projects

Create **Mtaa Market Directory**, a responsive listing of fictional vendors, opening times, and payment methods. Include a filter bar mock-up, useful empty state, clear focus style, and layout that remains usable with enlarged text. Use fictional data and locally stored assets. Submit HTML, CSS, screenshots at three widths, and a short rationale for the selected layout and contrast choices.

**Review:** does content reflow without horizontal scrolling? Are actions visibly interactive? Can a learner identify the styles responsible for each component without tracing many overrides?

## Challenges

1. Fix a card layout that overflows when its text doubles in length.
2. Replace repeated colours and spacing with custom properties.
3. Make keyboard focus visible without changing the page's layout unexpectedly.
4. Respect reduced-motion preference while retaining clear feedback.

**Hint:** test content, not just empty boxes; use flexible tracks, `min-width: 0` where needed, and browser devtools' accessibility and responsive views.

## Final Assessment

Style an accessible directory page from supplied semantic HTML.

1. What are the three box-model regions inside to outside? Content, padding, border (then margin outside).
2. What does a class selector look like? `.name`.
3. Flexbox or Grid for a two-dimensional card matrix? Usually Grid.
4. How should keyboard focus be presented? With a visible indicator.
5. How can a page adapt to reduced motion? Use the matching media query and remove nonessential movement.

**Rubric (20):** responsive layout 5; cascade and reusable rules 4; readability and contrast 4; focus and motion support 4; maintainability and explanation 3.
