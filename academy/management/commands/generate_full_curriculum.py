"""
Full CodeSavannah curriculum — all 60+ learning paths with complete module content.
Run: python manage.py generate_full_curriculum
Re-runnable safely (uses get_or_create + update).
"""
from django.core.management.base import BaseCommand
from academy.models import LearningPath, Lesson


def upsert(path, order, title, objective, content, exercise, quiz_q, project, notes, mins):
    qs = Lesson.objects.filter(learning_path=path, order=order)
    if qs.count() > 1:
        keep = qs.first().pk
        qs.exclude(pk=keep).delete()
        qs = Lesson.objects.filter(pk=keep)
    lesson = qs.first()
    if lesson:
        lesson.title = title; lesson.objective = objective
        lesson.content = content; lesson.exercise_prompt = exercise
        lesson.quiz_question = quiz_q; lesson.project_prompt = project
        lesson.notes = notes; lesson.estimated_minutes = mins
        lesson.save()
        return False
    Lesson.objects.create(
        learning_path=path, order=order, title=title, objective=objective,
        content=content, exercise_prompt=exercise, quiz_question=quiz_q,
        project_prompt=project, notes=notes, estimated_minutes=mins
    )
    return True


# ─────────────────────────────────────────────────────────────────────────────
# BATCH 1 — WEB FUNDAMENTALS
# ─────────────────────────────────────────────────────────────────────────────

HTML5_LESSONS = [
    (1, "HTML5 Introduction & Document Structure",
     "Understand what HTML5 is, how the browser renders pages, and write a valid HTML5 document.",
     """## What is HTML5?

HTML5 is the fifth and current major version of HyperText Markup Language — the standard language for building web pages. Every website you have ever visited is built on HTML at its core.

**How a browser renders a page:**
1. Browser requests a URL
2. Server returns HTML text
3. Browser parses HTML into a DOM tree
4. CSS is applied (styling)
5. JavaScript runs (interactivity)
6. Page is painted on screen

## A valid HTML5 document

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="My first HTML5 page">
    <title>CodeSavannah — Hello World</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/courses">Courses</a>
            <a href="/contact">Contact</a>
        </nav>
    </header>

    <main>
        <h1>Welcome to CodeSavannah</h1>
        <p>Learning to code changes your life.</p>
    </main>

    <footer>
        <p>&copy; 2025 CodeSavannah Academy</p>
    </footer>

    <script src="app.js"></script>
</body>
</html>
```

## Essential tags

| Tag | Purpose |
|-----|---------|
| `<!DOCTYPE html>` | Declares HTML5 — always first line |
| `<html lang="en">` | Root element; `lang` helps screen readers & SEO |
| `<head>` | Metadata — not visible on page |
| `<meta charset="UTF-8">` | Supports all characters including emoji |
| `<meta name="viewport" ...>` | Makes page mobile-responsive |
| `<title>` | Text shown on browser tab |
| `<body>` | Everything visible goes here |

## Semantic structure tags

HTML5 introduced **semantic elements** — tags that carry meaning:

```html
<header>   — top of page / section
<nav>      — navigation links
<main>     — primary page content (one per page)
<section>  — thematic group of content
<article>  — self-contained piece (blog post, card)
<aside>    — sidebar / supplementary content
<footer>   — bottom of page / section
<figure>   — image + caption
<figcaption> — caption for figure
```

**Why semantics matter:**
- Search engines rank semantic pages higher
- Screen readers navigate by landmarks (accessibility)
- Code is easier to read and maintain

## Headings hierarchy

```html
<h1>Page Title — ONE per page</h1>
<h2>Major Section</h2>
<h3>Sub-section</h3>
<h4>Sub-sub-section</h4>
<h5>Rarely needed</h5>
<h6>Almost never used</h6>
```

Never skip heading levels (h1 → h3 without h2). Screen readers and SEO bots rely on correct hierarchy.

## Text elements

```html
<p>Paragraph of text.</p>
<strong>Bold, important text</strong>
<em>Italic, emphasised text</em>
<br>   — line break (use sparingly)
<hr>   — horizontal rule / divider
<blockquote cite="https://source.com">Quoted text</blockquote>
<code>inline code snippet</code>
<pre><code>
    preserved
    whitespace
</code></pre>
<abbr title="HyperText Markup Language">HTML</abbr>
<mark>highlighted text</mark>
<small>fine print</small>
<sup>superscript</sup> — exponents: x<sup>2</sup>
<sub>subscript</sub>   — chemical: H<sub>2</sub>O
```

## Links and navigation

```html
<!-- External link — always add rel for security -->
<a href="https://example.com" target="_blank" rel="noopener noreferrer">Visit site</a>

<!-- Internal page link -->
<a href="/courses">Our Courses</a>

<!-- Same-page anchor -->
<a href="#contact">Jump to contact</a>
<section id="contact">...</section>

<!-- Email link -->
<a href="mailto:info@codesavannah.ac">Email us</a>

<!-- Phone link -->
<a href="tel:+254712345678">Call us</a>

<!-- Download link -->
<a href="/files/syllabus.pdf" download>Download Syllabus</a>
```

## Images

```html
<img
    src="images/hero.jpg"
    alt="Students coding at CodeSavannah Academy"
    width="1200"
    height="630"
    loading="lazy"
>

<!-- Responsive images — serve different sizes -->
<picture>
    <source srcset="hero-mobile.webp" media="(max-width:600px)">
    <source srcset="hero.webp" type="image/webp">
    <img src="hero.jpg" alt="Hero image">
</picture>
```

**Always include `alt` text** — required for accessibility and SEO. Describe what the image shows for someone who cannot see it.
""",
     "Build a complete HTML5 profile page: header with nav, main with h1 heading, paragraph about yourself, a list of 5 skills, an image, and a footer with your name.",
     "Which HTML5 element should wrap the primary content of a page, used only once?",
     "Build an HTML5 page for a fictional restaurant: header with logo and nav, hero section with restaurant name and tagline, menu section with 3 items (image, name, price, description), a contact section with address and phone, and a footer.",
     "Always add lang='en' on <html> and charset='UTF-8' in <head> — missing these breaks internationalisation and can corrupt special characters.",
     40),

    (2, "HTML5 Forms & Input Elements",
     "Build accessible, validated HTML5 forms for collecting user data.",
     """## HTML5 Forms

Forms are how users send data to your server — logins, registrations, search, checkout — everything interactive depends on forms.

```html
<form action="/submit" method="POST" novalidate>

    <!-- Text input -->
    <label for="username">Username</label>
    <input type="text" id="username" name="username"
           required minlength="3" maxlength="30"
           placeholder="e.g. grace_codes"
           autocomplete="username">

    <!-- Email -->
    <label for="email">Email address</label>
    <input type="email" id="email" name="email"
           required placeholder="you@example.com">

    <!-- Password -->
    <label for="password">Password</label>
    <input type="password" id="password" name="password"
           required minlength="8">

    <!-- Number with range -->
    <label for="age">Age</label>
    <input type="number" id="age" name="age"
           min="13" max="120" value="18">

    <!-- Date picker -->
    <label for="dob">Date of birth</label>
    <input type="date" id="dob" name="dob">

    <!-- Phone -->
    <label for="phone">Phone number</label>
    <input type="tel" id="phone" name="phone"
           pattern="[+]?[0-9]{10,15}"
           placeholder="+254712345678">

    <!-- URL -->
    <label for="website">Website</label>
    <input type="url" id="website" name="website"
           placeholder="https://yoursite.com">

    <!-- Range slider -->
    <label for="skill">Skill level: <output id="skill-output">5</output></label>
    <input type="range" id="skill" name="skill"
           min="1" max="10" value="5"
           oninput="skill-output.value = this.value">

    <!-- File upload -->
    <label for="avatar">Profile picture</label>
    <input type="file" id="avatar" name="avatar"
           accept="image/png, image/jpeg" multiple>

    <!-- Textarea -->
    <label for="bio">About yourself</label>
    <textarea id="bio" name="bio" rows="5" cols="40"
              maxlength="500" placeholder="Tell us about yourself…"></textarea>

    <!-- Select dropdown -->
    <label for="country">Country</label>
    <select id="country" name="country" required>
        <option value="">-- Select country --</option>
        <optgroup label="East Africa">
            <option value="ke">Kenya</option>
            <option value="ug">Uganda</option>
            <option value="tz">Tanzania</option>
        </optgroup>
    </select>

    <!-- Radio buttons — wrap each in label -->
    <fieldset>
        <legend>Experience level</legend>
        <label><input type="radio" name="level" value="beginner" checked> Beginner</label>
        <label><input type="radio" name="level" value="intermediate"> Intermediate</label>
        <label><input type="radio" name="level" value="advanced"> Advanced</label>
    </fieldset>

    <!-- Checkboxes -->
    <fieldset>
        <legend>Interests</legend>
        <label><input type="checkbox" name="interests" value="python"> Python</label>
        <label><input type="checkbox" name="interests" value="web"> Web Dev</label>
        <label><input type="checkbox" name="interests" value="ai"> AI / ML</label>
    </fieldset>

    <!-- Hidden field -->
    <input type="hidden" name="csrf_token" value="{{ token }}">

    <!-- Submit button -->
    <button type="submit">Create Account</button>
    <button type="reset">Clear Form</button>

</form>
```

## HTML5 built-in validation attributes

| Attribute | Purpose |
|-----------|---------|
| `required` | Field must not be empty |
| `minlength` / `maxlength` | String length bounds |
| `min` / `max` | Number / date bounds |
| `pattern` | Regex pattern match |
| `type="email"` | Valid email format |
| `type="url"` | Valid URL format |
| `step` | Allowed number increment |

## Datalist — searchable options

```html
<label for="course">Search for a course</label>
<input list="courses" id="course" name="course"
       placeholder="Type to search…">
<datalist id="courses">
    <option value="Python Programming">
    <option value="Web Development">
    <option value="Cybersecurity">
    <option value="Data Science">
</datalist>
```

## Accessible forms — best practices

1. **Always link `<label>` to input** using `for` / `id` pair
2. **Use `<fieldset>` + `<legend>`** for groups of related inputs
3. **Never use placeholder as a label** — placeholder disappears when typing
4. **Add `autocomplete`** — browsers can pre-fill known data
5. **Provide error messages** — not just red borders
""",
     "Build a registration form with: name, email, password (min 8 chars), country dropdown, profile picture upload, and a 'terms and conditions' checkbox. All fields required.",
     "Which HTML5 attribute makes a form field mandatory before submission?",
     "Build a fully-validated job application form: personal details, work experience (textarea), file CV upload, preferred salary (range), start date (date picker), and a submit button that shows a success message via JavaScript.",
     "Link every <input> to a <label> using the for/id pair. Without this, clicking the label text doesn't focus the input — a usability and accessibility failure.",
     45),

    (3, "HTML5 Tables, Lists & Media",
     "Organise data with tables, lists, and embed audio/video natively.",
     """## Tables — for tabular data only

```html
<table>
    <caption>CodeSavannah Course Fees 2025</caption>
    <thead>
        <tr>
            <th scope="col">Course</th>
            <th scope="col">Duration</th>
            <th scope="col">Level</th>
            <th scope="col">Fee (KES)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Python Programming</td>
            <td>8 weeks</td>
            <td>Beginner</td>
            <td>12,000</td>
        </tr>
        <tr>
            <td>Cybersecurity</td>
            <td>10 weeks</td>
            <td>Intermediate</td>
            <td>18,000</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td colspan="3">Total courses available</td>
            <td>12</td>
        </tr>
    </tfoot>
</table>
```

**Key table attributes:**
- `scope="col"` / `scope="row"` on `<th>` — required for accessibility
- `colspan` — merge columns horizontally
- `rowspan` — merge rows vertically
- `<caption>` — visible table title (good for accessibility)

## Lists

```html
<!-- Unordered list -->
<ul>
    <li>Python</li>
    <li>JavaScript</li>
    <li>CSS
        <ul>
            <li>Flexbox</li>
            <li>Grid</li>
        </ul>
    </li>
</ul>

<!-- Ordered list -->
<ol type="1" start="1">
    <li>Download VS Code</li>
    <li>Install Python</li>
    <li>Write your first program</li>
</ol>

<!-- ol type options: 1 (default), A, a, I (Roman), i -->

<!-- Description list — term + definition pairs -->
<dl>
    <dt>HTML</dt>
    <dd>HyperText Markup Language — the structure of web pages</dd>

    <dt>CSS</dt>
    <dd>Cascading Style Sheets — the styling of web pages</dd>

    <dt>JavaScript</dt>
    <dd>The programming language of the web</dd>
</dl>
```

## Native audio and video

```html
<!-- Audio player -->
<audio controls preload="metadata">
    <source src="lecture.mp3" type="audio/mpeg">
    <source src="lecture.ogg" type="audio/ogg">
    <p>Your browser doesn't support audio. <a href="lecture.mp3">Download it</a>.</p>
</audio>

<!-- Video player with poster image -->
<video
    controls
    width="854"
    height="480"
    poster="thumbnail.jpg"
    preload="metadata"
    muted
    playsinline
>
    <source src="intro.mp4" type="video/mp4">
    <source src="intro.webm" type="video/webm">
    <track kind="subtitles" src="captions.vtt" srclang="en" label="English">
    <p>Video not supported. <a href="intro.mp4">Download instead</a>.</p>
</video>
```

## Iframes — embed external content

```html
<!-- Embed a YouTube video -->
<iframe
    width="854" height="480"
    src="https://www.youtube.com/embed/VIDEO_ID"
    title="Video title"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media"
    allowfullscreen
    loading="lazy"
></iframe>

<!-- Embed a Google Map -->
<iframe
    src="https://maps.google.com/maps?q=Nairobi&output=embed"
    width="600" height="450"
    loading="lazy"
    title="Our location in Nairobi"
></iframe>
```

## Canvas — draw with JavaScript

```html
<canvas id="myCanvas" width="400" height="300">
    Your browser does not support the canvas element.
</canvas>

<script>
const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');

ctx.fillStyle = '#1341a8';
ctx.fillRect(10, 10, 150, 100);

ctx.strokeStyle = '#00d4f5';
ctx.lineWidth = 3;
ctx.beginPath();
ctx.arc(200, 150, 60, 0, Math.PI * 2);
ctx.stroke();
</script>
```
""",
     "Build an HTML page with a table showing a weekly timetable (Monday–Friday, 8am–4pm lessons), an ordered list of steps to install Python, and an embedded YouTube video of your choice.",
     "Which HTML5 element pair is used for a term and its definition in a description list?",
     "Build a course catalog page using a table with 8 courses, sortable columns (JavaScript), a filter input, and embedded video previews for each course.",
     "Never use tables for page layout — use CSS Flexbox or Grid instead. Tables are only for data with rows and columns of related information.",
     40),

    (4, "HTML5 Accessibility & SEO",
     "Write HTML that search engines rank highly and that everyone can use.",
     """## Why accessibility matters

- 1 billion people worldwide have a disability
- Many use screen readers (NVDA, JAWS, VoiceOver) to browse the web
- WCAG 2.1 (Web Content Accessibility Guidelines) is the international standard
- In many countries, inaccessible websites are illegal

## ARIA — Accessible Rich Internet Applications

ARIA attributes add semantic meaning where native HTML isn't enough:

```html
<!-- Roles -->
<div role="button" tabindex="0" aria-label="Close menu"
     onclick="closeMenu()" onkeydown="if(e.key==='Enter')closeMenu()">✕</div>

<!-- States -->
<button aria-expanded="false" aria-controls="menu" id="menu-btn">
    Menu
</button>
<ul id="menu" aria-labelledby="menu-btn" hidden>
    <li><a href="/">Home</a></li>
</ul>

<!-- Live regions — announce dynamic changes to screen readers -->
<div aria-live="polite" id="status"></div>
<script>
    document.getElementById('status').textContent = 'Form submitted successfully!';
</script>

<!-- Images -->
<img src="chart.png" alt="Bar chart showing 40% increase in enrolments from 2024 to 2025">
<!-- Decorative images get empty alt -->
<img src="divider.png" alt="">

<!-- Skip navigation link — first element on page -->
<a class="skip-link" href="#main-content">Skip to main content</a>
```

## Semantic HTML is accessible HTML

```html
<!-- Bad: div soup — screen reader can't understand this -->
<div class="header">
    <div class="nav">
        <div class="nav-item" onclick="go('/')">Home</div>
    </div>
</div>

<!-- Good: semantic HTML — meaning is clear -->
<header>
    <nav aria-label="Main navigation">
        <a href="/">Home</a>
    </nav>
</header>
```

## Keyboard navigation

All interactive elements must be reachable by Tab key:

```html
<!-- Native HTML elements are keyboard-accessible by default -->
<button>Submit</button>      ✓ focusable
<a href="...">Link</a>       ✓ focusable
<input type="text">          ✓ focusable

<!-- Custom elements need tabindex -->
<div tabindex="0" role="button">Custom button</div>  ✓ focusable
<div tabindex="-1" id="modal">Modal (focus via JS)</div>
```

## SEO — Search Engine Optimisation fundamentals

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Title: 50–60 characters, include target keyword -->
    <title>Python Programming Course | CodeSavannah Academy</title>

    <!-- Meta description: 150–160 chars, compelling summary -->
    <meta name="description" content="Learn Python from scratch in 8 weeks. Hands-on projects, expert mentorship, and a certificate. Join 5,000+ students across East Africa.">

    <!-- Canonical — prevents duplicate content penalty -->
    <link rel="canonical" href="https://codesavannah.ac/courses/python/">

    <!-- Open Graph — controls how page looks when shared on social media -->
    <meta property="og:title" content="Python Programming Course | CodeSavannah">
    <meta property="og:description" content="Go from zero to Python developer in 8 weeks.">
    <meta property="og:image" content="https://codesavannah.ac/img/python-og.jpg">
    <meta property="og:url" content="https://codesavannah.ac/courses/python/">
    <meta property="og:type" content="website">

    <!-- Twitter card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Python Programming Course">
</head>

<body>
    <!-- Structured data (JSON-LD) — helps Google understand your content -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": "Python Programming",
        "description": "Learn Python from scratch in 8 weeks.",
        "provider": {
            "@type": "Organization",
            "name": "CodeSavannah Academy"
        }
    }
    </script>
</body>
</html>
```

## SEO checklist

- One `<h1>` per page containing the primary keyword
- All images have descriptive `alt` text
- All links have meaningful text (not "click here")
- Page loads in under 3 seconds
- HTTPS enabled
- Sitemap.xml submitted to Google Search Console
""",
     "Audit an existing HTML page you've built: add proper ARIA labels, skip navigation link, structured data JSON-LD, and complete Open Graph meta tags.",
     "What ARIA attribute announces dynamic content changes to screen reader users?",
     "Build an SEO-optimised landing page for a fictional Nairobi tech bootcamp: proper meta tags, Open Graph, schema.org JSON-LD, semantic HTML, skip link, and pass WAVE accessibility checker with 0 errors.",
     "Run your page through Google Lighthouse (free in Chrome DevTools). Aim for 90+ on Accessibility, SEO, and Performance before you consider a page production-ready.",
     45),

    (5, "HTML5 Best Practices & Interview Prep",
     "Write clean, maintainable HTML and answer every HTML interview question confidently.",
     """## HTML5 vs HTML4 — what changed

| Feature | HTML4 | HTML5 |
|---------|-------|-------|
| Doctype | Long, complex | `<!DOCTYPE html>` |
| Semantic elements | None | header, nav, main, article, aside, footer, section |
| Multimedia | Required Flash/plugins | Native audio, video, canvas |
| Form inputs | Limited | email, tel, date, range, color, search, url |
| Storage | Cookies only | localStorage, sessionStorage, IndexedDB |
| APIs | None | Geolocation, Web Workers, WebSockets, Drag & Drop |

## The DOM — Document Object Model

When a browser reads HTML, it builds a tree of objects called the DOM:

```
Document
└── html
    ├── head
    │   ├── meta
    │   └── title
    └── body
        ├── header
        │   └── nav
        ├── main
        │   ├── h1
        │   └── p
        └── footer
```

JavaScript reads and modifies this tree in real time.

## Common interview questions

**Q: What is the difference between `<div>` and `<section>`?**
A: `<div>` is a generic container with no semantic meaning. `<section>` means "a thematic grouping of content" — it implies the content has a heading and belongs together. Use section for meaningful groups, div for layout grouping only.

**Q: What is the difference between `id` and `class`?**
A: `id` must be unique on a page — one element only. `class` can be shared by many elements. Use `id` for unique landmarks (main, sidebar), `class` for reusable styles.

**Q: What does `<!DOCTYPE html>` do?**
A: It tells the browser to render the page in standards mode (not quirks mode). Without it, browsers may render pages incorrectly.

**Q: What is the difference between `<script>` placement in head vs body?**
A: Scripts in `<head>` without `defer` or `async` block parsing. Best practice: put scripts at end of `<body>` OR use `<script defer>` in `<head>`.

**Q: What are data attributes?**
```html
<div data-user-id="42" data-role="admin" data-theme="dark">
    User profile
</div>

<script>
    const div = document.querySelector('div');
    console.log(div.dataset.userId);  // "42"
    console.log(div.dataset.role);    // "admin"
</script>
```
Data attributes store custom data on elements without misusing class or id.

## HTML best practices checklist

```html
✓ <!DOCTYPE html> on line 1
✓ <html lang="en"> with correct language
✓ <meta charset="UTF-8"> in head
✓ <meta name="viewport"> for mobile
✓ Meaningful <title>
✓ Semantic elements (not div soup)
✓ One <h1> per page
✓ All <img> have alt attributes
✓ All <a> have descriptive text
✓ All form inputs linked to labels
✓ No inline styles (use CSS files)
✓ External scripts have defer or async
✓ Valid HTML (run through validator.w3.org)
```

## HTML5 Web Storage

```javascript
// localStorage — persists forever until cleared
localStorage.setItem('username', 'grace_codes');
const name = localStorage.getItem('username');
localStorage.removeItem('username');
localStorage.clear();

// sessionStorage — cleared when tab closes
sessionStorage.setItem('draft', 'My blog post...');

// Store objects (must stringify)
const user = { name: 'Grace', gpa: 3.9 };
localStorage.setItem('user', JSON.stringify(user));
const user2 = JSON.parse(localStorage.getItem('user'));
```

## HTML5 Geolocation API

```javascript
if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(
        position => {
            const { latitude, longitude } = position.coords;
            console.log(`Lat: ${latitude}, Lng: ${longitude}`);
        },
        error => console.error('Location error:', error.message),
        { enableHighAccuracy: true, timeout: 5000 }
    );
}
```
""",
     "Answer these HTML questions in writing: (1) difference between semantic and non-semantic elements, (2) when to use id vs class, (3) how defer and async differ for script loading, (4) what ARIA is and name 3 ARIA roles.",
     "What HTML5 feature allows storing data in the browser that persists between page loads, without cookies?",
     "Build a complete multi-page HTML5 website for CodeSavannah Academy: Home (hero, features, testimonials), Courses (table of courses), About (team cards), Contact (form). Validate all pages with W3C Validator. Score 90+ on Lighthouse accessibility.",
     "Always validate your HTML at validator.w3.org before deploying. Invalid HTML can cause cross-browser rendering bugs that are very hard to debug.",
     50),
]

CSS3_LESSONS = [
    (1, "CSS3 Fundamentals — Selectors, Properties & the Box Model",
     "Write CSS rules, target elements precisely, and understand how every element is a box.",
     """## What is CSS3?

CSS (Cascading Style Sheets) controls the visual presentation of HTML. CSS3 is the current major version, introducing animations, gradients, flexbox, grid, and much more.

## Adding CSS to a page

```html
<!-- 1. External stylesheet — recommended -->
<link rel="stylesheet" href="styles.css">

<!-- 2. Internal style block -->
<style>
    body { font-family: sans-serif; }
</style>

<!-- 3. Inline style — avoid for maintainability -->
<p style="color: red; font-size: 18px;">Text</p>
```

## CSS syntax

```css
selector {
    property: value;
    property: value;
}
```

## Selectors — targeting HTML elements

```css
/* Type — all elements of that tag */
p { color: #333; }
h1, h2, h3 { font-weight: 900; }

/* Class — any element with class="card" */
.card { background: white; border-radius: 8px; }

/* ID — unique element with id="hero" */
#hero { height: 100vh; }

/* Attribute */
input[type="email"] { border: 2px solid blue; }
a[href^="https"] { color: green; }    /* starts with */
a[href$=".pdf"]  { color: red; }      /* ends with */
a[href*="google"] { color: orange; }  /* contains */

/* Descendant */
nav a { text-decoration: none; }      /* any <a> inside <nav> */

/* Direct child */
ul > li { list-style: none; }         /* only direct <li> children */

/* Adjacent sibling */
h2 + p { font-size: 1.1rem; }        /* <p> immediately after <h2> */

/* General sibling */
h2 ~ p { color: var(--muted); }

/* Pseudo-classes */
a:hover        { color: var(--accent); }
button:active  { transform: scale(0.98); }
input:focus    { outline: 2px solid blue; }
li:first-child { font-weight: bold; }
li:last-child  { border-bottom: none; }
li:nth-child(odd)  { background: #f5f5f5; }
li:nth-child(3n+1) { color: blue; }
p:not(.lead)   { font-size: .9rem; }
input:required { border-left: 4px solid red; }
input:valid    { border-color: green; }

/* Pseudo-elements */
p::first-line  { font-weight: bold; }
p::first-letter { font-size: 3rem; float: left; }
h2::before     { content: "→ "; color: var(--accent); }
h2::after      { content: ""; display: block; height: 2px; background: var(--primary); }
input::placeholder { color: #999; font-style: italic; }
::selection    { background: yellow; color: black; }
```

## The Box Model

Every HTML element is a rectangular box:

```
┌──────────────────── MARGIN ─────────────────────┐
│  ┌────────────────── BORDER ──────────────────┐  │
│  │  ┌─────────────── PADDING ──────────────┐  │  │
│  │  │                                      │  │  │
│  │  │              CONTENT                 │  │  │
│  │  │         (width × height)             │  │  │
│  │  │                                      │  │  │
│  │  └──────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

```css
/* Without box-sizing, padding adds to declared width */
.box-default {
    width: 200px;
    padding: 20px;
    /* actual rendered width = 200 + 20 + 20 = 240px */
}

/* box-sizing: border-box — padding is INSIDE the width */
*, *::before, *::after {
    box-sizing: border-box;  /* Include this in every project's reset */
}
.box-border {
    width: 200px;
    padding: 20px;
    /* actual rendered width = 200px (padding inside) */
}

/* Full box model example */
.card {
    width: 320px;
    padding: 24px;
    margin: 16px auto;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    background: white;
    box-shadow: 0 4px 16px rgba(0,0,0,.1);
}
```

## CSS Variables (Custom Properties)

```css
:root {
    /* Define globally */
    --primary:    #1341a8;
    --accent:     #00d4f5;
    --text:       #0f172a;
    --muted:      #64748b;
    --bg:         #f8fafc;
    --surface:    #ffffff;
    --radius:     8px;
    --radius-lg:  16px;
    --shadow:     0 4px 16px rgba(0,0,0,.08);
    --font-main:  'Inter', 'Segoe UI', sans-serif;
}

/* Use anywhere */
.btn-primary {
    background: var(--primary);
    color: white;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
}

/* Override in component scope */
.dark-card {
    --surface: #1e293b;
    --text: #f1f5f9;
    background: var(--surface);
    color: var(--text);
}
```

## Cascade & Specificity

When multiple rules target the same element, the most **specific** rule wins:

```
Inline style      1000  (highest)
ID selector       100
Class / attribute 10
Type selector     1     (lowest)

!important overrides all — use sparingly
```

```css
/* Specificity: 0,0,1 — type */
p { color: blue; }

/* Specificity: 0,1,0 — class — WINS */
.lead { color: green; }

/* Specificity: 1,0,0 — ID — WINS over class */
#intro { color: red; }
```
""",
     "Write CSS rules to style a card component: 320px wide, white background, rounded corners (12px), box shadow, 24px padding, centered on page, hover effect that lifts the card 4px upward.",
     "In CSS specificity, which selector type has the highest weight: type, class, or ID?",
     "Build a full CSS design system for CodeSavannah Academy: CSS variables for colors/spacing/typography, base reset, typography scale (h1–h6), button variants (primary, secondary, ghost, danger), and card component — all from scratch, no frameworks.",
     "Set box-sizing: border-box on * at the top of every project. It makes sizing predictable — padding no longer inflates element widths unexpectedly.",
     50),

    (2, "CSS3 Flexbox — One-Dimensional Layouts",
     "Use Flexbox to build navbars, card rows, centred elements, and any one-dimensional layout.",
     """## What is Flexbox?

Flexbox (Flexible Box Layout) is a one-dimensional layout system — it lays items out in a **row** or **column**. It makes alignment and distribution trivial.

## Container vs Items

```css
/* The PARENT becomes the flex container */
.container {
    display: flex;
}

/* All direct CHILDREN become flex items */
.item { /* flex item properties here */ }
```

## Flex direction

```css
.row     { flex-direction: row; }           /* default — left to right */
.row-rev { flex-direction: row-reverse; }   /* right to left */
.col     { flex-direction: column; }        /* top to bottom */
.col-rev { flex-direction: column-reverse; }
```

## Alignment — the two axes

```
flex-direction: row
                  ←──── MAIN AXIS ────→
                  ↑
                CROSS
                 AXIS
                  ↓

flex-direction: column
   MAIN AXIS runs top → bottom
   CROSS AXIS runs left → right
```

```css
/* MAIN AXIS — justify-content */
.container {
    justify-content: flex-start;   /* default */
    justify-content: flex-end;
    justify-content: center;
    justify-content: space-between; /* items spread, no outer gap */
    justify-content: space-around;  /* equal space around each item */
    justify-content: space-evenly;  /* equal space between all items */
}

/* CROSS AXIS — align-items */
.container {
    align-items: stretch;     /* default — items fill cross axis */
    align-items: flex-start;
    align-items: flex-end;
    align-items: center;
    align-items: baseline;    /* align text baselines */
}
```

## Wrapping

```css
.container {
    flex-wrap: nowrap;    /* default — all on one line, may overflow */
    flex-wrap: wrap;      /* wrap to next line when needed */
    flex-wrap: wrap-reverse;
}

/* shorthand: flex-flow = direction + wrap */
.container { flex-flow: row wrap; }
```

## Flex item properties

```css
.item {
    /* flex-grow — how much extra space does this item take?
       0 = take no extra space (default)
       1 = take equal share of extra space */
    flex-grow: 1;

    /* flex-shrink — can this item shrink if needed?
       1 = yes, shrink (default)
       0 = no, never shrink */
    flex-shrink: 0;

    /* flex-basis — starting size before grow/shrink */
    flex-basis: 200px;

    /* shorthand: grow shrink basis */
    flex: 1 1 200px;
    flex: 1;          /* = 1 1 0% */
    flex: auto;       /* = 1 1 auto */
    flex: none;       /* = 0 0 auto */
}

/* Override alignment for ONE item */
.special { align-self: flex-end; }

/* Order — reorder items visually (not in DOM) */
.first { order: -1; }
.last  { order: 1; }
```

## Real-world patterns

```css
/* 1. Centred hero section */
.hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    text-align: center;
}

/* 2. Navbar — logo left, links right */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    height: 72px;
}

/* 3. Card grid that wraps */
.card-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
}
.card { flex: 1 1 280px; max-width: 400px; }

/* 4. Sticky footer — push footer to bottom */
body {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}
main { flex: 1; }

/* 5. Equal-width columns */
.columns { display: flex; gap: 24px; }
.col     { flex: 1; }
```

## gap — the modern way to add spacing

```css
.container {
    display: flex;
    gap: 24px;        /* all directions */
    row-gap: 16px;    /* between rows only */
    column-gap: 24px; /* between columns only */
}
```
""",
     "Build a navigation bar using Flexbox: logo on the left, nav links in the centre, login/signup buttons on the right. Make it collapse vertically on screens under 600px.",
     "Which Flexbox property distributes extra space along the main axis between flex items?",
     "Build a responsive course card grid using Flexbox: each card has an image, category tag, title, description, instructor name, and enroll button. Cards wrap to new rows and stretch to equal height. Works on mobile, tablet, and desktop.",
     "Use gap instead of margin for spacing between flex items — gap is flex-container-aware so it never creates unwanted outer margins.",
     50),

    (3, "CSS3 Grid — Two-Dimensional Layouts",
     "Build magazine-style page layouts, dashboards, and complex grids with CSS Grid.",
     """## What is CSS Grid?

CSS Grid is a two-dimensional layout system — it works in both rows AND columns simultaneously. Use Grid for overall page layout; use Flexbox for components inside grid areas.

## Grid container

```css
.container {
    display: grid;

    /* Define columns */
    grid-template-columns: 200px 1fr 1fr;
    /* = sidebar 200px wide, then 2 equal columns */

    /* fr = fraction of available space */
    grid-template-columns: 1fr 2fr 1fr;
    /* = 25% | 50% | 25% */

    /* repeat() shorthand */
    grid-template-columns: repeat(4, 1fr);
    /* = 4 equal columns */

    /* auto-fill — as many as fit */
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    /* = responsive grid, no media queries needed */

    /* Define rows */
    grid-template-rows: 72px 1fr auto;
    /* = fixed header, flexible main, auto footer */

    /* Gaps */
    gap: 24px;
    row-gap: 16px;
    column-gap: 24px;
}
```

## Placing items

```css
/* By line numbers (1-based) */
.header {
    grid-column: 1 / 4;   /* start at line 1, end at line 4 (spans all 3 cols) */
    grid-row: 1 / 2;
}

/* Shorthand */
.sidebar {
    grid-column: 1;        /* = 1 / 2 */
    grid-row: 2 / 4;
}

/* span keyword */
.feature {
    grid-column: span 2;   /* span 2 columns from auto placement */
}

/* Named areas — most readable */
.layout {
    display: grid;
    grid-template-areas:
        "header  header  header"
        "sidebar main    main  "
        "footer  footer  footer";
    grid-template-columns: 240px 1fr 1fr;
    grid-template-rows: 72px 1fr auto;
    min-height: 100vh;
}

.site-header  { grid-area: header; }
.site-sidebar { grid-area: sidebar; }
.site-main    { grid-area: main; }
.site-footer  { grid-area: footer; }
```

## Alignment in Grid

```css
.container {
    /* Align ALL items */
    justify-items: stretch;  /* horizontal within cell */
    align-items:   stretch;  /* vertical within cell */

    /* Align the GRID TRACKS within the container */
    justify-content: center;
    align-content: center;
}

/* Individual item alignment */
.item {
    justify-self: end;
    align-self: center;
    place-self: center end; /* shorthand: align-self justify-self */
}
```

## Real-world layouts

```css
/* Dashboard layout */
.dashboard {
    display: grid;
    grid-template-columns: 260px 1fr;
    grid-template-rows: 72px 1fr;
    min-height: 100vh;
}

/* Responsive card grid — no media queries */
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 24px;
}

/* Magazine layout */
.magazine {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 24px;
}
.featured { grid-column: span 8; }
.sidebar  { grid-column: span 4; }
.article  { grid-column: span 4; }
```

## Grid vs Flexbox — when to use which

| Use Case | Best Tool |
|----------|-----------|
| Page-level layout | Grid |
| Component internal layout | Flexbox |
| 2D (rows AND columns) | Grid |
| 1D (row OR column) | Flexbox |
| Items that should align across rows | Grid |
| Items that should grow/shrink freely | Flexbox |
""",
     "Build a dashboard layout with CSS Grid: fixed sidebar (260px), top navbar (72px), main content area, and a footer. The main content area contains a 3-column stats grid.",
     "In CSS Grid, what unit represents a fraction of the remaining available space?",
     "Build a responsive news website layout using CSS Grid: full-width header, 12-column grid system, featured article spanning 8 columns, sidebar spanning 4, three equal article cards below, and footer. Collapse to single column on mobile.",
     "Use grid-template-areas for complex layouts — it makes the structure readable and maintainable compared to line numbers.",
     55),

    (4, "CSS3 Animations, Transitions & Responsive Design",
     "Add motion to interfaces and make layouts work on every screen size.",
     """## CSS Transitions — smooth state changes

```css
/* Basic transition: property duration timing delay */
.btn {
    background: var(--primary);
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
    transition: background 200ms ease, transform 200ms ease, box-shadow 200ms ease;
}
.btn:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(19,65,168,.35);
}

/* Transition all properties (careful — can be slow) */
.card { transition: all 300ms ease; }

/* Timing functions */
.ease        { transition-timing-function: ease; }
.ease-in     { transition-timing-function: ease-in; }
.ease-out    { transition-timing-function: ease-out; }
.ease-in-out { transition-timing-function: ease-in-out; }
.linear      { transition-timing-function: linear; }
.bounce      { transition-timing-function: cubic-bezier(0.34, 1.56, 0.64, 1); }
```

## CSS Animations — keyframe sequences

```css
/* Define the animation */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50%       { transform: scale(1.05); }
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* Apply animation */
.hero-title {
    animation: fadeInUp 600ms ease-out both;
}

.cta-button {
    animation: pulse 2s ease-in-out infinite;
}

.loader {
    animation: spin 1s linear infinite;
}

/* Stagger: delay each card */
.card:nth-child(1) { animation: fadeInUp 500ms 0ms   ease both; }
.card:nth-child(2) { animation: fadeInUp 500ms 100ms ease both; }
.card:nth-child(3) { animation: fadeInUp 500ms 200ms ease both; }

/* Skeleton loading */
.skeleton {
    background: linear-gradient(
        90deg,
        #f0f0f0 25%,
        #e0e0e0 50%,
        #f0f0f0 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
}
```

## Responsive Design — Mobile First

**Mobile first:** write base styles for mobile, then use `min-width` media queries to add desktop styles.

```css
/* Base — mobile (320px+) */
.card-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
}

/* Tablet (600px+) */
@media (min-width: 600px) {
    .card-grid { grid-template-columns: 1fr 1fr; gap: 20px; }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
    .card-grid { grid-template-columns: repeat(3, 1fr); gap: 24px; }
}

/* Large desktop (1280px+) */
@media (min-width: 1280px) {
    .card-grid { grid-template-columns: repeat(4, 1fr); }
}
```

## Common breakpoints (Bootstrap 5 inspired)

```css
/* Mobile:  < 576px  — no media query (base) */
/* SM:     ≥ 576px  */  @media (min-width: 576px)  { }
/* MD:     ≥ 768px  */  @media (min-width: 768px)  { }
/* LG:     ≥ 992px  */  @media (min-width: 992px)  { }
/* XL:     ≥ 1200px */  @media (min-width: 1200px) { }
/* XXL:    ≥ 1400px */  @media (min-width: 1400px) { }
```

## Viewport units & modern responsive units

```css
.hero      { height: 100vh; }   /* full viewport height */
.sidebar   { width: 25vw; }    /* 25% viewport width */
.text      { font-size: 4vw; } /* scales with viewport */

/* clamp(min, preferred, max) — fluid values */
.heading   { font-size: clamp(1.5rem, 4vw, 3rem); }
.container { width: clamp(300px, 90%, 1200px); }
.gap       { gap: clamp(12px, 2vw, 32px); }
```

## Dark mode with CSS

```css
/* Automatic — follows OS setting */
@media (prefers-color-scheme: dark) {
    :root {
        --bg: #0f172a;
        --surface: #1e293b;
        --text: #f1f5f9;
        --border: rgba(255,255,255,.1);
    }
}

/* Manual toggle with data attribute */
[data-theme="dark"] {
    --bg: #0f172a;
    --text: #f1f5f9;
}
```
""",
     "Add a staggered fade-in-up animation to a card grid (each card animates in 100ms after the previous), plus a hover lift transition and a CSS skeleton loading state.",
     "Which CSS media query type is considered best practice — mobile-first (min-width) or desktop-first (max-width)?",
     "Build an animated landing page: hero with fade-in text, animated gradient background, card grid with stagger entrance, and a dark/light mode toggle. All animations respect `prefers-reduced-motion`.",
     "Always add @media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } } — users with vestibular disorders can be seriously harmed by excessive motion.",
     55),
]

# ─────────────────────────────────────────────────────────────────────────────
# BATCH 2 — JAVASCRIPT & TYPESCRIPT
# ─────────────────────────────────────────────────────────────────────────────

JS_EXTRA_LESSONS = [
    (8, "JavaScript Async Programming — Promises, Async/Await & Fetch",
     "Write non-blocking code and call APIs using modern JavaScript async patterns.",
     """## Why async matters

JavaScript runs on a single thread. If you block it (e.g., waiting for a file or API), the entire page freezes. Async patterns let the browser handle waiting in the background while JavaScript keeps running.

## Callbacks — the original pattern (avoid for complex flows)

```javascript
function fetchUser(id, callback) {
    setTimeout(() => {
        if (id <= 0) {
            callback(new Error('Invalid ID'), null);
        } else {
            callback(null, { id, name: 'Grace', role: 'student' });
        }
    }, 1000);
}

fetchUser(1, (err, user) => {
    if (err) return console.error(err.message);
    console.log(user.name);
    fetchUser(2, (err, user2) => {   // callback hell begins
        // ...
    });
});
```

## Promises — chainable, cleaner

```javascript
function fetchUser(id) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (id <= 0) reject(new Error('Invalid ID'));
            else resolve({ id, name: 'Grace', role: 'student' });
        }, 1000);
    });
}

fetchUser(1)
    .then(user => {
        console.log(user.name);
        return fetchUser(2);
    })
    .then(user2 => console.log(user2.name))
    .catch(err => console.error(err.message))
    .finally(() => console.log('Done'));

// Run multiple promises in parallel
Promise.all([fetchUser(1), fetchUser(2), fetchUser(3)])
    .then(([u1, u2, u3]) => console.log(u1, u2, u3));

// First one to resolve wins
Promise.race([fetchUser(1), fetchUser(2)])
    .then(first => console.log('First:', first.name));

// All settle (even if some fail)
Promise.allSettled([fetchUser(1), fetchUser(-1)])
    .then(results => results.forEach(r => console.log(r.status, r.value || r.reason)));
```

## Async / Await — the modern standard

```javascript
async function loadDashboard(userId) {
    try {
        const user    = await fetchUser(userId);
        const courses = await fetchCourses(user.id);
        const grades  = await fetchGrades(user.id);

        return { user, courses, grades };
    } catch (err) {
        console.error('Dashboard load failed:', err.message);
        throw err;
    }
}

// Top-level await (ES2022 modules)
const data = await loadDashboard(1);
```

## Fetch API — making HTTP requests

```javascript
// GET request
async function getCourses() {
    const response = await fetch('/api/courses/');

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
}

// POST request
async function createEnrolment(courseId) {
    const response = await fetch('/api/enrolments/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ course: courseId }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Enrolment failed');
    }

    return response.json();
}

// Full CRUD helper
const api = {
    async get(url)         { return (await fetch(url)).json(); },
    async post(url, data)  { return (await fetch(url, { method:'POST',  headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) })).json(); },
    async put(url, data)   { return (await fetch(url, { method:'PUT',   headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) })).json(); },
    async delete(url)      { return (await fetch(url, { method:'DELETE' })).json(); },
};
```

## Error handling patterns

```javascript
// Custom error class
class APIError extends Error {
    constructor(message, status, data) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.data = data;
    }
}

async function safeFetch(url, options = {}) {
    try {
        const res = await fetch(url, options);
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new APIError(`${res.status} ${res.statusText}`, res.status, data);
        }
        return await res.json();
    } catch (err) {
        if (err instanceof APIError) throw err;
        throw new APIError('Network error — check your connection', 0, {});
    }
}
```
""",
     "Build a course search feature: fetch courses from an API on input (debounced 300ms), display results with loading spinner, handle errors with user-friendly messages, and cache results in a Map to avoid duplicate requests.",
     "What JavaScript keyword pauses an async function until a Promise resolves, without blocking the main thread?",
     "Build a full data dashboard: fetch user profile, enrolled courses, and recent grades in parallel (Promise.all), render the data, handle loading/error states, and add a 'retry' button on failure.",
     "Always handle the catch case in every async function. Unhandled promise rejections crash Node.js and show confusing errors in the browser console.",
     55),
]

TS_LESSONS = [
    (1, "TypeScript Introduction — Types, Interfaces & Setup",
     "Set up TypeScript and understand how static types prevent runtime errors.",
     """## What is TypeScript?

TypeScript is JavaScript with static types — developed and maintained by Microsoft. It compiles to plain JavaScript, runs everywhere JS runs, and catches entire categories of bugs before your code ever executes.

```
TypeScript (.ts) → compile → JavaScript (.js) → run in browser/Node
```

**Why TypeScript?**
- Catch typos and type errors at compile time, not in production
- Better IDE autocomplete and refactoring tools
- Self-documenting code — types are living documentation
- Scales better for large codebases and teams

## Setup

```bash
# Install TypeScript globally
npm install -g typescript

# Check version
tsc --version

# Initialise tsconfig in a project
tsc --init

# Compile a file
tsc app.ts

# Watch mode — recompile on save
tsc --watch

# With a project (recommended)
npm init -y
npm install --save-dev typescript ts-node @types/node
```

## tsconfig.json key options

```json
{
    "compilerOptions": {
        "target": "ES2022",
        "module": "commonjs",
        "strict": true,
        "outDir": "./dist",
        "rootDir": "./src",
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules", "dist"]
}
```

## Primitive types

```typescript
// Type annotations (explicit)
let name:    string  = 'Grace';
let age:     number  = 17;
let isActive: boolean = true;
let score:   null    = null;
let value:   undefined = undefined;

// TypeScript INFERS types when you assign immediately
let city    = 'Nairobi';   // inferred: string
let count   = 0;           // inferred: number
let passing = true;        // inferred: boolean

// These will now cause compile errors:
city  = 42;      // ✗ Error: number not assignable to string
count = 'hello'; // ✗ Error: string not assignable to number
```

## Arrays and Tuples

```typescript
// Arrays
let courses: string[]       = ['Python', 'Web Dev', 'Cybersecurity'];
let scores:  number[]       = [85, 92, 78];
let flags:   Array<boolean> = [true, false, true]; // generic syntax

// Tuple — fixed-length, mixed-type array
let student: [string, number, boolean] = ['Grace', 17, true];
// student[0] is string, student[1] is number, student[2] is boolean
student[1] = 'wrong'; // ✗ Error: string not assignable to number
```

## Interfaces — describe object shapes

```typescript
interface Student {
    id:        number;
    name:      string;
    grade:     string;
    gpa:       number;
    email?:    string;    // optional property
    readonly joinDate: Date; // cannot change after creation
}

// Usage
const grace: Student = {
    id: 1,
    name: 'Grace Adhiambo',
    grade: 'Form 3',
    gpa: 3.9,
    joinDate: new Date('2024-01-15'),
};

grace.name = 'Grace Odhiambo'; // ✓ mutable
grace.joinDate = new Date();   // ✗ Error: readonly

// Extending interfaces
interface Trainer extends Student {
    expertise:  string[];
    yearsExp:   number;
}
```

## Type aliases

```typescript
type ID         = number | string;
type Grade      = 'Form 1' | 'Form 2' | 'Form 3' | 'Form 4';
type Status     = 'active' | 'inactive' | 'suspended';
type Callback   = (error: Error | null, data: unknown) => void;

// Object type alias
type Course = {
    id:       number;
    title:    string;
    level:    'beginner' | 'intermediate' | 'advanced';
    price:    number;
};
```

## Union and Intersection types

```typescript
// Union — can be one of several types
type Input = string | number;
function display(value: Input): string {
    return typeof value === 'string' ? value : value.toString();
}

// Intersection — has properties of ALL types
type AdminStudent = Student & { permissions: string[] };
```

## Functions with types

```typescript
// Typed parameters and return
function addScores(a: number, b: number): number {
    return a + b;
}

// Optional and default parameters
function greet(name: string, lang: string = 'en', greeting?: string): string {
    if (greeting) return `${greeting}, ${name}!`;
    return lang === 'sw' ? `Habari, ${name}!` : `Hello, ${name}!`;
}

// Arrow function
const multiply = (x: number, y: number): number => x * y;

// void return — no meaningful return value
function logError(msg: string): void {
    console.error(`[ERROR] ${msg}`);
}

// never — function never returns (throws or infinite loop)
function fail(msg: string): never {
    throw new Error(msg);
}
```
""",
     "Convert a plain JavaScript student management object (add, remove, find student functions) into TypeScript with proper interfaces, type aliases, and strict null handling.",
     "In TypeScript, what is the difference between an interface and a type alias?",
     "Build a fully typed REST API client library in TypeScript: interfaces for User, Course, Enrolment, typed fetch wrappers for CRUD operations, and custom error types. Zero 'any' types allowed.",
     "Enable 'strict: true' in tsconfig.json from day one. It activates strictNullChecks, noImplicitAny, and other guards that prevent the most common TypeScript bugs.",
     50),

    (2, "TypeScript Generics & Advanced Types",
     "Write reusable, type-safe code with generics, mapped types, and utility types.",
     """## Generics — reusable code for any type

Without generics, you'd need separate functions for every type:

```typescript
function getFirstString(arr: string[]): string  { return arr[0]; }
function getFirstNumber(arr: number[]): number  { return arr[0]; }
// ... for every type — terrible!

// With generics: one function, works for ANY type
function getFirst<T>(arr: T[]): T {
    return arr[0];
}

getFirst<string>(['a', 'b', 'c']);   // returns string
getFirst<number>([1, 2, 3]);         // returns number
getFirst(['Grace', 'Brian']);        // inferred: string
```

## Generic constraints

```typescript
// T must have a 'length' property
function logLength<T extends { length: number }>(value: T): T {
    console.log(`Length: ${value.length}`);
    return value;
}
logLength('hello');        // ✓
logLength([1, 2, 3]);      // ✓
logLength({ length: 5 }); // ✓
logLength(42);             // ✗ Error: no length property

// Multiple type parameters
function merge<T extends object, U extends object>(a: T, b: U): T & U {
    return { ...a, ...b };
}
```

## Generic interfaces and classes

```typescript
interface Repository<T> {
    findById(id: number): T | null;
    findAll(): T[];
    create(item: Omit<T, 'id'>): T;
    update(id: number, changes: Partial<T>): T | null;
    delete(id: number): boolean;
}

class StudentRepository implements Repository<Student> {
    private students: Student[] = [];

    findById(id: number): Student | null {
        return this.students.find(s => s.id === id) ?? null;
    }
    findAll(): Student[] { return [...this.students]; }
    create(item: Omit<Student, 'id'>): Student {
        const student = { ...item, id: Date.now() };
        this.students.push(student);
        return student;
    }
    update(id: number, changes: Partial<Student>): Student | null {
        const idx = this.students.findIndex(s => s.id === id);
        if (idx === -1) return null;
        this.students[idx] = { ...this.students[idx], ...changes };
        return this.students[idx];
    }
    delete(id: number): boolean {
        const len = this.students.length;
        this.students = this.students.filter(s => s.id !== id);
        return this.students.length < len;
    }
}
```

## Built-in utility types

```typescript
interface User {
    id:       number;
    name:     string;
    email:    string;
    role:     'admin' | 'student' | 'trainer';
    password: string;
}

// Partial<T> — all properties optional
type UserUpdate = Partial<User>;
// { id?: number; name?: string; email?: string; ... }

// Required<T> — all properties required
type FullUser = Required<UserUpdate>;

// Readonly<T> — no mutation
type ImmutableUser = Readonly<User>;
const u: ImmutableUser = { id:1, name:'Grace', email:'', role:'student', password:'' };
u.name = 'X'; // ✗ Error: cannot assign to readonly

// Pick<T, Keys> — select specific fields
type PublicUser = Pick<User, 'id' | 'name' | 'email' | 'role'>;

// Omit<T, Keys> — exclude specific fields
type CreateUser = Omit<User, 'id'>;
type SafeUser   = Omit<User, 'password'>;

// Record<Keys, Type> — dictionary / map
type RolePermissions = Record<User['role'], string[]>;
const perms: RolePermissions = {
    admin:   ['read', 'write', 'delete', 'manage-users'],
    student: ['read'],
    trainer: ['read', 'write', 'grade'],
};

// ReturnType<T> — infer return type of a function
type ApiResult = ReturnType<typeof loadDashboard>;

// Parameters<T> — infer parameter types
type FetchArgs = Parameters<typeof fetch>;
```

## Conditional types and Template Literal types

```typescript
// Conditional type
type IsString<T> = T extends string ? 'yes' : 'no';
type R1 = IsString<string>;  // 'yes'
type R2 = IsString<number>;  // 'no'

// Template literal types
type Event = 'click' | 'focus' | 'blur';
type Handler = `on${Capitalize<Event>}`;
// 'onClick' | 'onFocus' | 'onBlur'

type CSSProperty = `--${string}`;
const color: CSSProperty = '--primary'; // ✓
const bad: CSSProperty   = 'primary';   // ✗
```
""",
     "Build a generic Stack<T> class with push, pop, peek, isEmpty, and size methods. Then create typed stacks for strings, numbers, and Student objects.",
     "Which TypeScript utility type creates a new type with all properties of T made optional?",
     "Build a type-safe event system: an EventEmitter<Events> generic class where Events is a Record mapping event names to their payload types. emit() and on() are fully typed.",
     "Avoid using 'any' — it defeats the purpose of TypeScript. Use 'unknown' when the type is genuinely unknown, then narrow it with typeof or instanceof guards.",
     55),

    (3, "TypeScript with React & Node.js",
     "Apply TypeScript in real-world React components and Express APIs.",
     """## TypeScript + React

```bash
# Create a typed React project
npx create-react-app my-app --template typescript
# or with Vite:
npm create vite@latest my-app -- --template react-ts
```

## Typing React components

```typescript
import React, { useState, useEffect, FC, ReactNode } from 'react';

// Props interface
interface CourseCardProps {
    course:    Course;
    onEnroll:  (id: number) => void;
    featured?: boolean;
    children?: ReactNode;
}

// Function component with typed props
const CourseCard: FC<CourseCardProps> = ({ course, onEnroll, featured = false, children }) => {
    const [enrolled, setEnrolled] = useState<boolean>(false);

    const handleEnroll = (): void => {
        setEnrolled(true);
        onEnroll(course.id);
    };

    return (
        <article className={`card ${featured ? 'card-featured' : ''}`}>
            <span className={`tag tag-${course.level}`}>{course.level}</span>
            <h2>{course.title}</h2>
            <p>{course.description}</p>
            {children}
            <button
                onClick={handleEnroll}
                disabled={enrolled}
                className={`btn ${enrolled ? 'btn-success' : 'btn-primary'}`}
            >
                {enrolled ? '✓ Enrolled' : 'Enrol Now'}
            </button>
        </article>
    );
};

// Typing useEffect and async data fetching
interface APIState<T> {
    data:    T | null;
    loading: boolean;
    error:   string | null;
}

function useFetch<T>(url: string): APIState<T> {
    const [state, setState] = useState<APIState<T>>({
        data: null, loading: true, error: null
    });

    useEffect(() => {
        let cancelled = false;
        async function load() {
            try {
                const res = await fetch(url);
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                const data: T = await res.json();
                if (!cancelled) setState({ data, loading: false, error: null });
            } catch (err) {
                if (!cancelled) setState({ data: null, loading: false, error: (err as Error).message });
            }
        }
        load();
        return () => { cancelled = true; };
    }, [url]);

    return state;
}

// Usage
const CoursesPage: FC = () => {
    const { data: courses, loading, error } = useFetch<Course[]>('/api/courses/');

    if (loading) return <div>Loading…</div>;
    if (error)   return <div>Error: {error}</div>;
    if (!courses) return null;

    return (
        <div className="card-grid">
            {courses.map(course => (
                <CourseCard
                    key={course.id}
                    course={course}
                    onEnroll={(id) => console.log('Enrolling in', id)}
                />
            ))}
        </div>
    );
};
```

## TypeScript + Express (Node.js)

```typescript
// types.ts — shared types
export interface Student {
    id:    number;
    name:  string;
    email: string;
    gpa:   number;
}

export interface APIResponse<T> {
    success: boolean;
    data?:   T;
    error?:  string;
}
```

```typescript
// app.ts
import express, { Request, Response, NextFunction } from 'express';
import { Student, APIResponse } from './types';

const app = express();
app.use(express.json());

// Typed route handler
app.get('/students', async (
    req: Request,
    res: Response<APIResponse<Student[]>>
) => {
    try {
        const students = await StudentService.findAll();
        res.json({ success: true, data: students });
    } catch (err) {
        res.status(500).json({ success: false, error: (err as Error).message });
    }
});

// Typed params
app.get('/students/:id', async (
    req: Request<{ id: string }>,
    res: Response<APIResponse<Student>>
) => {
    const student = await StudentService.findById(parseInt(req.params.id));
    if (!student) return res.status(404).json({ success: false, error: 'Not found' });
    res.json({ success: true, data: student });
});

// Typed body
app.post('/students', async (
    req: Request<{}, {}, Omit<Student, 'id'>>,
    res: Response<APIResponse<Student>>
) => {
    const student = await StudentService.create(req.body);
    res.status(201).json({ success: true, data: student });
});
```
""",
     "Build a typed React component: CourseFilter with search input (debounced), category dropdown, and level filter. Props and state all fully typed. Display filtered results from a typed API response.",
     "In a typed React component, what TypeScript type is used for the return type of a component that renders JSX?",
     "Build a full-stack TypeScript application: Express REST API with typed routes, request/response types, and a React frontend that consumes the API with a custom useFetch hook. Share types between frontend and backend via a shared types package.",
     "Create a types/ folder with shared interfaces used by both the API and the frontend. This single-source-of-truth prevents frontend/backend type drift.",
     65),
]

# ─────────────────────────────────────────────────────────────────────────────
# BATCH 3 — JAVA
# ─────────────────────────────────────────────────────────────────────────────

JAVA_LESSONS = [
    (1, "Java Introduction — Syntax, Types & Variables",
     "Write and run your first Java programs, understand the JVM, and use Java's type system.",
     """## What is Java?

Java is a compiled, object-oriented, platform-independent programming language created by James Gosling at Sun Microsystems in 1995. It powers Android apps, enterprise systems, web backends, and big data tools.

**Write Once, Run Anywhere (WORA):** Java compiles to bytecode that runs on the Java Virtual Machine (JVM) — the same code runs on Windows, macOS, Linux, and Android.

```
Java source (.java) → javac compiler → Bytecode (.class) → JVM → runs anywhere
```

## Setup

```bash
# Install JDK (Java Development Kit)
# Download from adoptium.net or use:
# Windows: winget install EclipseAdoptium.Temurin.21.JDK
# macOS:   brew install temurin@21

# Verify
java -version
javac -version

# Compile and run
javac HelloWorld.java
java HelloWorld

# Build tool — Maven
mvn archetype:generate -DarchetypeArtifactId=maven-archetype-quickstart
mvn compile
mvn exec:java -Dexec.mainClass="com.codesavannah.App"
```

## First Java program

```java
// File: HelloWorld.java
// Class name MUST match filename
public class HelloWorld {

    // Entry point — every Java program starts here
    public static void main(String[] args) {
        System.out.println("Hello, CodeSavannah!");
        System.out.print("No newline at end");
        System.out.printf("Formatted: %s is %d years old%n", "Grace", 17);
    }
}
```

## Data types

Java has **primitive types** (stored directly) and **reference types** (objects):

```java
// ── PRIMITIVE TYPES ──────────────────────────
// Integer types
byte   b = 127;              // 8-bit,  -128 to 127
short  s = 32767;            // 16-bit
int    i = 2_147_483_647;    // 32-bit (most common)
long   l = 9_223_372_036_854_775_807L; // 64-bit, suffix L

// Floating point
float  f = 3.14f;            // 32-bit, suffix f
double d = 3.141592653589793; // 64-bit (most common)

// Other
char   c  = 'A';             // 16-bit Unicode character
boolean ok = true;           // true or false

// ── REFERENCE TYPES ──────────────────────────
String  name = "Grace";                // String is an object
int[]   arr  = {1, 2, 3, 4, 5};       // Array
```

## Variables and constants

```java
// Local variable
int age = 17;

// Constant — SCREAMING_SNAKE_CASE by convention
final double PI = 3.14159265358979;
final int MAX_STUDENTS = 100;

// Type inference with var (Java 10+)
var message = "Hello, World!"; // inferred: String
var count   = 42;               // inferred: int
var courses = new ArrayList<String>(); // inferred: ArrayList<String>
```

## Operators

```java
int a = 10, b = 3;

// Arithmetic
a + b   // 13
a - b   // 7
a * b   // 30
a / b   // 3  (integer division — truncates)
a % b   // 1  (remainder)

// Comparison
a == b  // false
a != b  // true
a >  b  // true
a >= b  // true

// Logical
true && false  // false (AND — both must be true)
true || false  // true  (OR — either can be true)
!true          // false (NOT)

// Increment / decrement
int x = 5;
x++;  // x becomes 6  (post-increment)
++x;  // x becomes 7  (pre-increment)
x--;  // x becomes 6

// Compound assignment
x += 3;  // x = x + 3
x *= 2;  // x = x * 2

// Ternary
String grade = (score >= 50) ? "Pass" : "Fail";
```

## Strings

```java
String name = "Grace Adhiambo";

// Common methods
name.length()              // 14
name.toUpperCase()         // "GRACE ADHIAMBO"
name.toLowerCase()         // "grace adhiambo"
name.charAt(0)             // 'G'
name.substring(0, 5)       // "Grace"
name.contains("Adh")       // true
name.startsWith("Grace")   // true
name.endsWith("ambo")      // true
name.replace("Grace", "Brian") // "Brian Adhiambo"
name.trim()                // removes whitespace
name.split(" ")            // ["Grace", "Adhiambo"]
name.indexOf("A")          // 6
name.isEmpty()             // false
name.isBlank()             // false (also checks whitespace-only)

// String formatting
String msg = String.format("Name: %s, Age: %d, GPA: %.2f", name, 17, 3.9);
String msg2 = "Name: " + name + ", Age: " + 17; // concatenation

// StringBuilder — efficient when building strings in loops
StringBuilder sb = new StringBuilder();
for (int i = 1; i <= 5; i++) {
    sb.append("Item ").append(i).append("\\n");
}
String result = sb.toString();

// Comparison — ALWAYS use .equals(), never ==
String a = "hello";
String b = new String("hello");
a == b          // false — compares references
a.equals(b)     // true  — compares content
a.equalsIgnoreCase(b) // case-insensitive comparison
```
""",
     "Write a Java program that: declares variables of every primitive type, prints them formatted with printf, concatenates strings with StringBuilder, and tests string methods (contains, replace, split).",
     "Which Java method compares String content correctly — == or .equals()?",
     "Build a Student Report Card program in Java: prompt for name, 5 subject scores, calculate average, determine letter grade (A/B/C/D/F), and print a formatted report card using printf.",
     "Java uses == to compare primitive values (int, char, etc.) but reference equality for objects. Always use .equals() for String comparison, or you will get subtle bugs that only appear with certain JVM optimisations.",
     45),

    (2, "Java Control Flow — Conditionals, Loops & Methods",
     "Control program logic with conditionals, loops, and reusable methods.",
     """## Conditional statements

```java
// if / else if / else
int score = 87;

if (score >= 90) {
    System.out.println("Grade A — Excellent!");
} else if (score >= 80) {
    System.out.println("Grade B — Very Good");
} else if (score >= 70) {
    System.out.println("Grade C — Good");
} else if (score >= 60) {
    System.out.println("Grade D — Pass");
} else {
    System.out.println("Grade F — Retake Required");
}

// Switch statement
String day = "MONDAY";
switch (day) {
    case "MONDAY":
    case "TUESDAY":
    case "WEDNESDAY":
    case "THURSDAY":
    case "FRIDAY":
        System.out.println("Weekday");
        break;
    case "SATURDAY":
    case "SUNDAY":
        System.out.println("Weekend");
        break;
    default:
        System.out.println("Invalid day");
}

// Switch expression (Java 14+) — cleaner
String type = switch (day) {
    case "SATURDAY", "SUNDAY" -> "Weekend";
    default                   -> "Weekday";
};

// Ternary
String result = (score >= 50) ? "Pass" : "Fail";
```

## Loops

```java
// for loop
for (int i = 1; i <= 10; i++) {
    System.out.printf("%d x 7 = %d%n", i, i * 7);
}

// while loop
int attempts = 3;
Scanner scanner = new Scanner(System.in);
while (attempts > 0) {
    System.out.print("Enter password: ");
    String input = scanner.nextLine();
    if (input.equals("secret123")) {
        System.out.println("Access granted!");
        break;
    }
    attempts--;
    System.out.printf("%d attempt(s) remaining%n", attempts);
}

// do-while — always executes at least once
int choice;
do {
    System.out.println("1. View courses  2. Enroll  3. Exit");
    System.out.print("Choice: ");
    choice = scanner.nextInt();
} while (choice < 1 || choice > 3);

// Enhanced for (for-each)
String[] courses = {"Python", "Web Dev", "Java", "Cybersecurity"};
for (String course : courses) {
    System.out.println("Course: " + course);
}

// Loop control
for (int i = 0; i < 100; i++) {
    if (i % 2 == 0) continue; // skip even numbers
    if (i > 15)     break;    // stop at 15
    System.out.println(i);
}

// Nested loops with labels (rare but useful)
outer:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (i == 1 && j == 1) break outer; // break both loops
        System.out.printf("[%d][%d] ", i, j);
    }
}
```

## Methods

```java
public class Calculator {

    // Method: returnType methodName(parameters)
    public static int add(int a, int b) {
        return a + b;
    }

    // Void method — no return value
    public static void printDivider(int length) {
        System.out.println("=".repeat(length));
    }

    // Method overloading — same name, different parameters
    public static double power(double base, int exponent) {
        double result = 1.0;
        for (int i = 0; i < exponent; i++) result *= base;
        return result;
    }

    public static double power(double base, double exponent) {
        return Math.pow(base, exponent);
    }

    // Varargs — variable number of arguments
    public static int sum(int... numbers) {
        int total = 0;
        for (int n : numbers) total += n;
        return total;
    }

    // Recursive method
    public static long factorial(int n) {
        if (n <= 1) return 1;           // base case
        return n * factorial(n - 1);   // recursive case
    }

    public static void main(String[] args) {
        System.out.println(add(5, 3));           // 8
        System.out.println(power(2, 10));         // 1024.0
        System.out.println(sum(1, 2, 3, 4, 5));  // 15
        System.out.println(factorial(10));        // 3628800
        printDivider(30);
    }
}
```

## Variable scope

```java
public class ScopeDemo {
    static int classVar = 100;  // class-level (static field)

    public static void main(String[] args) {
        int localVar = 200;     // method-level

        for (int i = 0; i < 3; i++) {
            int loopVar = i * 2; // block-level
            System.out.println(classVar + localVar + loopVar);
        }
        // System.out.println(loopVar); // ERROR: out of scope
    }
}
```
""",
     "Write a Java program that implements FizzBuzz (1–100), a multiplication table printer, a simple menu-driven calculator using do-while, and a recursive Fibonacci sequence generator.",
     "What Java keyword skips the rest of the current loop iteration and continues to the next?",
     "Build a Java console-based quiz game: 10 multiple-choice questions stored in arrays, shuffled using Collections.shuffle, timer per question, score tracking, and final grade display.",
     "Use enhanced for loops (for-each) whenever you're iterating over a collection without needing the index. It's cleaner and prevents off-by-one errors.",
     50),

    (3, "Java OOP — Classes, Objects & Inheritance",
     "Model real-world systems using classes, inheritance, interfaces, and encapsulation.",
     """## Classes and Objects

```java
// Class definition
public class Student {

    // Instance variables (fields)
    private int    id;
    private String name;
    private String grade;
    private double gpa;

    // Constructor
    public Student(int id, String name, String grade, double gpa) {
        this.id    = id;
        this.name  = name;
        this.grade = grade;
        this.gpa   = gpa;
    }

    // Default constructor
    public Student() {
        this(0, "Unknown", "Form 1", 0.0);
    }

    // Getters (accessors)
    public int    getId()    { return id; }
    public String getName()  { return name; }
    public String getGrade() { return grade; }
    public double getGpa()   { return gpa; }

    // Setters (mutators) with validation
    public void setName(String name) {
        if (name == null || name.isBlank()) throw new IllegalArgumentException("Name cannot be empty");
        this.name = name.trim();
    }

    public void setGpa(double gpa) {
        if (gpa < 0.0 || gpa > 4.0) throw new IllegalArgumentException("GPA must be 0.0–4.0");
        this.gpa = gpa;
    }

    // Business logic
    public String getLetterGrade() {
        if (gpa >= 3.7) return "A";
        if (gpa >= 3.0) return "B";
        if (gpa >= 2.0) return "C";
        if (gpa >= 1.0) return "D";
        return "F";
    }

    // Override Object.toString()
    @Override
    public String toString() {
        return String.format("Student{id=%d, name='%s', grade='%s', gpa=%.2f (%s)}",
                id, name, grade, gpa, getLetterGrade());
    }

    // Override equals and hashCode
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Student s)) return false;
        return id == s.id;
    }

    @Override
    public int hashCode() { return Integer.hashCode(id); }
}
```

## Inheritance

```java
// Parent class
public class Person {
    protected String name;
    protected int    age;

    public Person(String name, int age) {
        this.name = name;
        this.age  = age;
    }

    public void introduce() {
        System.out.printf("Hi, I'm %s, age %d%n", name, age);
    }
}

// Child class — inherits Person
public class Trainer extends Person {
    private String expertise;
    private int    yearsExp;

    public Trainer(String name, int age, String expertise, int yearsExp) {
        super(name, age);  // call parent constructor
        this.expertise = expertise;
        this.yearsExp  = yearsExp;
    }

    // Method overriding
    @Override
    public void introduce() {
        super.introduce();  // call parent's version first
        System.out.printf("I teach %s with %d years experience%n", expertise, yearsExp);
    }

    public void teach(Student student) {
        System.out.printf("Teaching %s to %s%n", expertise, student.getName());
    }
}
```

## Interfaces

```java
// Interface — contract of what a class CAN DO
public interface Gradeable {
    String getLetterGrade();         // abstract method (no body)

    default String getDescription() { // default method (Java 8+)
        return "Grade: " + getLetterGrade();
    }

    static boolean isPassing(double gpa) { // static method
        return gpa >= 2.0;
    }
}

public interface Serializable {
    String toCSV();
    String toJSON();
}

// A class can implement multiple interfaces
public class Student extends Person implements Gradeable, Serializable {

    @Override
    public String getLetterGrade() { /* ... */ }

    @Override
    public String toCSV() {
        return String.format("%d,%s,%s,%.2f", id, name, grade, gpa);
    }

    @Override
    public String toJSON() {
        return String.format("{\"id\": %d, \"name\": \"%s\", \"grade\": \"%s\", \"gpa\": %.2f}",
            id, name, grade, gpa);
    }
}
```

## Abstract classes

```java
// Abstract — cannot be instantiated, provides template
public abstract class Shape {
    protected String color;

    public Shape(String color) { this.color = color; }

    // Abstract — subclasses MUST implement
    public abstract double area();
    public abstract double perimeter();

    // Concrete method — inherited as-is
    public void describe() {
        System.out.printf("%s %s: area=%.2f, perimeter=%.2f%n",
                color, getClass().getSimpleName(), area(), perimeter());
    }
}

public class Circle extends Shape {
    private double radius;
    public Circle(String color, double radius) { super(color); this.radius = radius; }
    @Override public double area()      { return Math.PI * radius * radius; }
    @Override public double perimeter() { return 2 * Math.PI * radius; }
}

public class Rectangle extends Shape {
    private double width, height;
    public Rectangle(String color, double w, double h) { super(color); width=w; height=h; }
    @Override public double area()      { return width * height; }
    @Override public double perimeter() { return 2 * (width + height); }
}
```

## Polymorphism

```java
List<Shape> shapes = List.of(
    new Circle("red", 5),
    new Rectangle("blue", 4, 6),
    new Circle("green", 3)
);

for (Shape s : shapes) {
    s.describe();  // correct method called for each actual type
}

// Total area — polymorphic
double totalArea = shapes.stream()
    .mapToDouble(Shape::area)
    .sum();
```
""",
     "Build a Library system in Java: abstract class LibraryItem with title, author, year; subclasses Book and Magazine; interface Borrowable with borrow() and return() methods; Library class with add, search, and display-all methods.",
     "In Java, what keyword is used in a subclass constructor to call the parent class constructor?",
     "Build a fully OOP Bank Management System: abstract Account class; SavingsAccount and CurrentAccount subclasses; Transaction record class; Bank class managing accounts; full CRUD operations with exception handling.",
     "Always override equals() and hashCode() together. If two objects are equal (equals() returns true), their hashCode() values must be identical — breaking this contract breaks HashMap and HashSet.",
     55),

    (4, "Java Collections, Generics & Exception Handling",
     "Use Java's collections framework, write generic code, and handle errors gracefully.",
     """## Collections Framework

```java
import java.util.*;

// ArrayList — ordered, allows duplicates, fast random access
List<String> courses = new ArrayList<>();
courses.add("Python");
courses.add("Web Dev");
courses.add("Java");
courses.add(1, "CSS");              // insert at index
courses.set(0, "Python 3");         // replace
courses.remove("CSS");              // remove by value
courses.remove(0);                  // remove by index
System.out.println(courses.get(0)); // get by index
System.out.println(courses.size()); // size
System.out.println(courses.contains("Java")); // contains?
courses.sort(Comparator.naturalOrder()); // sort
Collections.shuffle(courses);       // random shuffle

// LinkedList — fast insert/delete at ends, slow random access
Deque<String> queue = new LinkedList<>();
queue.offer("First");  // add to tail
queue.offer("Second");
queue.poll();          // remove from head — "First"

// Stack (LIFO) — use Deque
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1); stack.push(2); stack.push(3);
stack.pop();   // 3 — last in, first out
stack.peek();  // 2 — view top without removing

// HashSet — no duplicates, no order
Set<String> skills = new HashSet<>();
skills.add("Python"); skills.add("Java"); skills.add("Python"); // duplicate ignored
System.out.println(skills.size()); // 2

// TreeSet — sorted, no duplicates
Set<String> sorted = new TreeSet<>(skills);

// HashMap — key-value pairs, O(1) lookup
Map<String, Integer> grades = new HashMap<>();
grades.put("Grace",  92);
grades.put("Brian",  78);
grades.put("Amara",  88);
grades.get("Grace");          // 92
grades.getOrDefault("Zara", 0); // 0 if not found
grades.containsKey("Brian"); // true
grades.remove("Brian");

for (Map.Entry<String, Integer> entry : grades.entrySet()) {
    System.out.printf("%s: %d%n", entry.getKey(), entry.getValue());
}

// TreeMap — sorted by key
Map<String, Integer> sortedGrades = new TreeMap<>(grades);
```

## Generics

```java
// Generic class
public class Pair<A, B> {
    private final A first;
    private final B second;

    public Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }

    public A getFirst()  { return first; }
    public B getSecond() { return second; }

    @Override
    public String toString() {
        return "(" + first + ", " + second + ")";
    }
}

Pair<String, Integer> nameAge = new Pair<>("Grace", 17);
Pair<Course, Trainer> assignment = new Pair<>(pythonCourse, mrKamau);

// Generic method
public static <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}

System.out.println(max(3, 7));         // 7
System.out.println(max("Apple", "Mango")); // Mango
```

## Exception Handling

```java
// checked vs unchecked exceptions
// Checked — must be caught or declared (e.g., IOException, SQLException)
// Unchecked — runtime errors (e.g., NullPointerException, ArrayIndexOutOfBoundsException)

public static double divide(int a, int b) {
    if (b == 0) throw new ArithmeticException("Cannot divide by zero");
    return (double) a / b;
}

// try-catch-finally
try {
    double result = divide(10, 0);
    System.out.println(result);
} catch (ArithmeticException e) {
    System.err.println("Math error: " + e.getMessage());
} catch (Exception e) {
    System.err.println("Unexpected: " + e.getMessage());
} finally {
    System.out.println("This always runs — cleanup here");
}

// Multi-catch
try {
    int[] arr = {1, 2, 3};
    System.out.println(arr[10]); // ArrayIndexOutOfBoundsException
    String s = null;
    s.length();                  // NullPointerException
} catch (ArrayIndexOutOfBoundsException | NullPointerException e) {
    System.err.println("Array or null error: " + e.getClass().getSimpleName());
}

// Custom exception
public class InsufficientFundsException extends Exception {
    private final double amount;

    public InsufficientFundsException(double amount) {
        super(String.format("Insufficient funds. Shortfall: KES %.2f", amount));
        this.amount = amount;
    }

    public double getAmount() { return amount; }
}

// try-with-resources — auto-closes Closeable objects
try (FileReader fr = new FileReader("students.txt");
     BufferedReader br = new BufferedReader(fr)) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    System.err.println("File error: " + e.getMessage());
} // fr and br automatically closed — even if exception occurs
```
""",
     "Build a StudentDatabase using a HashMap<Integer, Student>. Implement: add, find by ID, find by name (partial match), update GPA, delete, list all sorted by name, and export to CSV string.",
     "Which Java collection maintains key-value pairs and provides O(1) average-time lookup by key?",
     "Build a School Management System with: Student, Trainer, Course, Enrolment classes; HashMap-backed repositories; custom exceptions (CourseFullException, AlreadyEnrolledException); full CLI menu with try-catch-finally.",
     "Always close resources (files, database connections, streams) using try-with-resources. It guarantees cleanup even when exceptions occur, preventing resource leaks.",
     60),

    (5, "Java Streams, Lambdas & Modern Java",
     "Write concise, functional-style Java with streams and lambda expressions.",
     """## Lambda Expressions (Java 8+)

A lambda is a short anonymous function:

```java
// Old way — anonymous class
Comparator<String> old = new Comparator<String>() {
    @Override
    public int compare(String a, String b) { return a.compareTo(b); }
};

// Lambda — much shorter
Comparator<String> lambda = (a, b) -> a.compareTo(b);
Comparator<String> ref    = String::compareTo; // method reference

// Common functional interfaces
Predicate<Integer>  isEven    = n -> n % 2 == 0;
Function<String, Integer> len = String::length;
Consumer<String>    print     = System.out::println;
Supplier<String>    greeting  = () -> "Hello!";
BinaryOperator<Integer> sum   = (a, b) -> a + b;

// Using them
System.out.println(isEven.test(4));  // true
System.out.println(len.apply("Hi")); // 2
print.accept("World");              // World
System.out.println(greeting.get()); // Hello!
```

## Streams API

```java
List<Student> students = List.of(
    new Student(1, "Grace",  "Form 3", 3.9),
    new Student(2, "Brian",  "Form 2", 2.8),
    new Student(3, "Amara",  "Form 4", 3.5),
    new Student(4, "Kofi",   "Form 3", 1.9),
    new Student(5, "Zara",   "Form 1", 4.0)
);

// filter — keep only passing students
List<Student> passing = students.stream()
    .filter(s -> s.getGpa() >= 2.0)
    .collect(Collectors.toList());

// map — transform each element
List<String> names = students.stream()
    .map(Student::getName)
    .sorted()
    .collect(Collectors.toList());

// reduce — combine to single value
double totalGpa = students.stream()
    .mapToDouble(Student::getGpa)
    .sum();

double avgGpa = students.stream()
    .mapToDouble(Student::getGpa)
    .average()
    .orElse(0.0);

// Chaining operations
String topStudents = students.stream()
    .filter(s -> s.getGpa() >= 3.5)
    .sorted(Comparator.comparing(Student::getGpa).reversed())
    .map(s -> s.getName() + " (" + s.getGpa() + ")")
    .collect(Collectors.joining(", "));
System.out.println("Top students: " + topStudents);

// groupingBy
Map<String, List<Student>> byGrade = students.stream()
    .collect(Collectors.groupingBy(Student::getGrade));

// count, min, max
long count = students.stream().filter(s -> s.getGpa() >= 3.0).count();
Optional<Student> best = students.stream()
    .max(Comparator.comparing(Student::getGpa));
best.ifPresent(s -> System.out.println("Top: " + s.getName()));

// anyMatch, allMatch, noneMatch
boolean anyHonours = students.stream().anyMatch(s -> s.getGpa() >= 3.7);
boolean allPassing = students.stream().allMatch(s -> s.getGpa() >= 2.0);
```

## Optional — null-safe values

```java
Optional<Student> found = students.stream()
    .filter(s -> s.getName().equals("Grace"))
    .findFirst();

// Never call .get() without checking
found.ifPresent(s -> System.out.println(s));
String name = found.map(Student::getName).orElse("Not found");
Student student = found.orElseThrow(() -> new RuntimeException("Student not found"));
```

## Records (Java 16+)

```java
// Immutable data class — no boilerplate
public record Course(int id, String title, String level, double price) {}

// Usage
Course python = new Course(1, "Python Programming", "beginner", 12000.0);
System.out.println(python.title()); // accessor, no "get" prefix
System.out.println(python);         // auto toString
```

## Sealed classes (Java 17+)

```java
public sealed interface Shape permits Circle, Rectangle, Triangle {}
public record Circle(double radius) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}

// Pattern matching switch (Java 21)
double area = switch (shape) {
    case Circle c       -> Math.PI * c.radius() * c.radius();
    case Rectangle r    -> r.width() * r.height();
    case Triangle t     -> 0.5 * t.base() * t.height();
};
```
""",
     "Given a List<Student> with 20 students, use Streams to: (1) find top 5 by GPA, (2) group by grade level, (3) calculate average GPA per grade, (4) find all students with names starting with 'A', (5) collect all emails to a comma-separated string.",
     "What Java Streams terminal operation collects stream elements into a List?",
     "Build a course analytics tool: load a CSV of 100 student enrolments, use Streams to compute: pass rate per course, average GPA per course, top 10 students overall, dropout risk (GPA < 2.0), and export a summary report.",
     "Streams are lazy — intermediate operations (filter, map) do nothing until a terminal operation (collect, count, forEach) is called. This means you can chain many operations with zero extra passes through the data.",
     60),
]

# ─────────────────────────────────────────────────────────────────────────────
# COMMAND
# ─────────────────────────────────────────────────────────────────────────────

BATCH_1 = [
    ('html5', 'HTML5', 'web', 'beginner', '4 weeks',
     'HTML5, Semantic Elements, Accessibility, SEO, Forms',
     'Master the language of the web — build structured, accessible, SEO-ready pages.', HTML5_LESSONS),

    ('css3-design', 'CSS3 Design', 'web', 'beginner', '5 weeks',
     'CSS3, Flexbox, Grid, Animations, Responsive Design',
     'Style beautiful, responsive interfaces from scratch using pure CSS3.', CSS3_LESSONS),

    ('typescript', 'TypeScript', 'web', 'intermediate', '6 weeks',
     'TypeScript, Generics, Interfaces, React, Node.js',
     'Add static types to JavaScript and build large, maintainable applications.', TS_LESSONS),

    ('java', 'Java', 'programming', 'beginner', '10 weeks',
     'Java, OOP, Collections, Streams, Lambdas, Maven',
     'Learn one of the world\'s most used languages — from syntax to enterprise patterns.', JAVA_LESSONS),
]


class Command(BaseCommand):
    help = 'Generate batch 1 of full curriculum: HTML5, CSS3, TypeScript, Java'

    def handle(self, *args, **options):
        total_created = total_updated = 0

        for (slug, title, category, level, duration, skills, summary, lessons) in BATCH_1:
            path, p_created = LearningPath.objects.get_or_create(
                slug=slug,
                defaults=dict(title=title, category=category, level=level,
                              duration=duration, skill_stack=skills,
                              summary=summary, is_featured=True)
            )
            if not p_created:
                path.title = title; path.category = category; path.level = level
                path.duration = duration; path.skill_stack = skills
                path.summary = summary; path.is_featured = True
                path.save()

            for lesson_data in lessons:
                created = upsert(path, *lesson_data)
                if created: total_created += 1
                else:       total_updated += 1

            self.stdout.write(f'  {"+" if p_created else "~"} {title}: {len(lessons)} lessons')

        self.stdout.write(self.style.SUCCESS(
            f'\nBatch 1 done — {total_created} lessons created, {total_updated} updated.'
        ))
