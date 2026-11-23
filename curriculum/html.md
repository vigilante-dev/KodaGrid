---
kind: learning_path
title: HTML: Structure for the Web
slug: html-foundations
category: web
level: beginner
duration: 6 stages · self-paced
skill_stack: HTML, semantic markup, forms, accessibility
summary: Build accessible, meaningful web documents from content structure to reusable page patterns.
language: en
stages:
  - {order: 1, stage: Beginner, slug: beginner-html, estimated_minutes: 40}
  - {order: 2, stage: Intermediate, slug: intermediate-html, estimated_minutes: 45}
  - {order: 3, stage: Advanced, slug: advanced-html, estimated_minutes: 50}
  - {order: 4, stage: Projects, slug: html-projects, estimated_minutes: 60}
  - {order: 5, stage: Challenges, slug: html-challenges, estimated_minutes: 35}
  - {order: 6, stage: Final Assessment, slug: html-assessment, estimated_minutes: 45}
references:
  - https://html.spec.whatwg.org/multipage/
  - https://www.w3.org/WAI/fundamentals/accessibility-intro/
originality: Original KodaGrid instructional content; references identify authoritative standards.
---

# HTML · Structure for the Web

HTML describes document structure and meaning. A browser turns that structure into a page; CSS controls appearance and JavaScript can add behaviour. You can practise offline by saving a file with the `.html` extension and opening it in a browser.

## Beginner

**Objective.** Create a valid page with headings, paragraphs, links, lists, and images, and explain why elements carry meaning.

An element normally has an opening tag, content, and a closing tag. Attributes add information to the opening tag. Indent nested elements so their parent-child relationship is easy to inspect.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Market Garden Club</title>
  </head>
  <body>
    <h1>Market Garden Club</h1>
    <p>We share practical growing ideas in our neighbourhood.</p>
    <a href="meeting.html">See the next meeting</a>
  </body>
</html>
```

**Syntax breakdown.** `<!doctype html>` selects modern HTML parsing; `lang` declares the document language; `head` contains metadata; `body` contains visible content; `h1` is the page's main heading; `href` gives a link destination. Heading levels express outline, not font size.

**Try it.** Add an `h2`, a three-item list of local crops, and an image with descriptive `alt`. Use a supplied or locally created image so the exercise works without data.

**Practice.** What does `lang="en"` help tools determine? When is `alt=""` appropriate? **Answers:** the page's language for assistive technology and language tools; when an image is purely decorative and adds no information.

**Common mistakes and habits.** Avoid choosing headings only for their appearance; do not use a file path as alt text; give links descriptive text such as “Read meeting notes” rather than “click here.” Validate nesting and include a useful page title.

## Intermediate

**Objective.** Organize a multi-section page semantically and build a form with labels and appropriate controls.

Use landmarks such as `header`, `nav`, `main`, `section`, and `footer` to describe page regions. A form control's `name` is the key used when its value is submitted; a `label` makes the control easier to identify and operate.

```html
<main>
  <section aria-labelledby="signup-title">
    <h2 id="signup-title">Join the coding circle</h2>
    <form action="/join" method="post">
      <label for="first-name">First name</label>
      <input id="first-name" name="first_name" autocomplete="given-name" required>
      <button type="submit">Request a place</button>
    </form>
  </section>
</main>
```

**Interactive exercise.** Add an email input (`type="email"`), a select for preferred session (morning/afternoon), and a submit button. Test every control using only Tab, Shift+Tab, and Enter. Do not collect real learner data in a demo.

**Practice questions.** Why connect `for` and `id`? What does `required` do, and what does it not do? **Answers:** it programmatically associates a label with a control; the browser provides a basic constraint check, but a server must still validate submitted data.

**Mini project.** Make a one-page community event announcement with a clear heading outline, date in `<time datetime="2026-11-21">21 November 2026</time>`, venue, schedule list, accessible image, and registration form mock-up.

**Common mistakes and habits.** Do not nest interactive controls inside one another. Give every input a label, use the right input type, and keep a sensible heading order. HTML validation is useful, but a valid page can still be confusing or inaccessible.

## Advanced

**Objective.** Use native HTML features thoughtfully for responsive media, disclosure, and accessible data.

```html
<details>
  <summary>What should I bring?</summary>
  <p>A notebook, a charged device if available, and questions.</p>
</details>
<picture>
  <source srcset="garden-small.webp" media="(max-width: 600px)">
  <img src="garden-wide.webp" alt="Learners tending raised beds together">
</picture>
```

`details` and `summary` provide a native disclosure interaction. `picture` offers source choices; the nested `img` remains the fallback and owns the alternative text. For tables, use them for genuinely tabular data, add header cells, and associate complex headers deliberately.

**Challenge exercise.** Create a weekly timetable table with captions, row and column headers, and a mobile-friendly explanation of the schedule. Check the document with an HTML conformance checker and a screen reader or keyboard-only navigation.

**Best practices.** Prefer built-in elements over custom ARIA widgets. Add ARIA only when native HTML cannot express the needed semantics. Keep forms understandable without relying on placeholder text. Treat user-entered text as untrusted when it is later rendered by an application.

**Quiz.** Is `<section>` a generic replacement for every `<div>`? **Answer:** no; use it for a thematic grouping, usually with a heading. What keeps an image useful when it cannot be seen? **Answer:** context-appropriate alternative text, or empty alt when decorative.

## Projects

Build **Neighbourhood Skills Exchange**, a small static site for offering and finding practical skills. Include a home page, an “offer a skill” form mock-up, a schedule, and a contact section. Use semantic landmarks, a skip link, useful titles, labels, descriptive link names, and text alternatives. Keep the first version usable on a slow connection: local assets, small images, and no required third-party scripts.

**Deliverables:** source files, a short README, a keyboard test checklist, and a paragraph explaining two accessibility decisions. **Review:** Can a visitor understand the page without CSS? Can they reach and identify each control? Is every page's purpose clear from its title and main heading?

## Challenges

1. Repair a page where headings jump from `h1` to `h4`, labels are missing, and a button is being used as a link. Explain each fix.
2. Add a language attribute and a correctly machine-readable date.
3. Make an image decorative without leaving an unhelpful announcement.
4. Add a form error summary design that identifies each invalid field in text.

**Hints:** choose elements by purpose; link to destinations and use buttons for actions; keep visible error text next to the relevant control. Test the page with keyboard navigation and at least one browser validator.

## Final Assessment

Create a semantic event page and submit it with an explanation of its structure.

1. Which element should hold the unique primary content? **Answer:** `<main>` (normally one visible main landmark per document).
2. What makes a label explicit? **Answer:** its `for` value matches the input's `id`.
3. Does client-side `required` replace server validation? **Answer:** no.
4. What belongs in image alt text? **Answer:** the image's relevant purpose or information in context.
5. Which element is suited to an action such as “Register”? **Answer:** a `<button>` inside the form.

**Assessment rubric (20 points):** semantic structure 5; accessible names and keyboard use 5; correct forms and metadata 4; valid, readable markup 3; explanation and testing evidence 3. A passing page works without relying on colour, placeholder text, or a mouse.
