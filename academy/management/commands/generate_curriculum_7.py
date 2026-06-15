"""
Batch 7: CSS, JavaScript for Web, NextJS
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


class Command(BaseCommand):
    help = 'Batch 7: CSS, JavaScript for Web, NextJS'

    def handle(self, *args, **options):
        created = updated = 0

        # ── CSS ──────────────────────────────────────────────────────────────
        p = LearningPath.objects.get(slug='css')

        r = upsert(p, 1, 'CSS Fundamentals: Selectors and the Box Model',
            'Select HTML elements with CSS selectors and control spacing with the box model.',
            '''## CSS: Styling the Web

CSS (Cascading Style Sheets) controls the **visual appearance** of HTML.

### Linking CSS to HTML

```html
<!-- External (recommended) -->
<link rel="stylesheet" href="styles.css">

<!-- Internal (small pages) -->
<style>
  p { color: navy; }
</style>

<!-- Inline (avoid for maintainability) -->
<p style="color: red;">Avoid this pattern.</p>
```

### Selectors

```css
/* Element selector */
p { color: #334155; }

/* Class selector */
.card { background: white; border-radius: 12px; }

/* ID selector (use sparingly) */
#hero { min-height: 80vh; }

/* Descendant */
nav a { text-decoration: none; }

/* Child (direct only) */
ul > li { list-style: none; }

/* Pseudo-class */
a:hover    { color: #6366f1; }
a:focus    { outline: 2px solid #6366f1; }
li:first-child { font-weight: bold; }
li:nth-child(2n) { background: #f8fafc; }  /* even rows */

/* Pseudo-element */
p::first-line { font-variant: small-caps; }
.card::before { content: "NEW "; color: #f59e0b; }

/* Attribute selectors */
input[type="email"] { border-color: #6366f1; }
a[href^="https"]    { color: green; }   /* starts with https */
```

### Specificity (who wins conflicts)

```
Inline style:     1000 points (highest)
ID:               100 points
Class/attribute:  10 points
Element:          1 point

#nav .link a {}  = 100 + 10 + 1 = 111 points
```

### The Box Model

Every HTML element is a rectangular box:

```
┌─────────────────────────────────┐  ← margin
│  ┌───────────────────────────┐  │
│  │  ┌─────────────────────┐  │  │  ← border
│  │  │  ┌───────────────┐  │  │  │
│  │  │  │   CONTENT    │  │  │  │  ← padding
│  │  │  └───────────────┘  │  │  │
│  │  └─────────────────────┘  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

```css
.card {
    /* Content */
    width: 300px;
    height: 200px;

    /* Padding (inside border) */
    padding: 20px;         /* all sides */
    padding: 16px 24px;    /* top/bottom left/right */
    padding: 8px 12px 16px 12px; /* top right bottom left */

    /* Border */
    border: 2px solid #e2e8f0;
    border-radius: 12px;

    /* Margin (outside border) */
    margin: 0 auto;       /* center horizontally */
    margin-bottom: 24px;
}

/* box-sizing: border-box — width INCLUDES padding+border */
* {
    box-sizing: border-box;
}
```

### Colors and Typography

```css
body {
    font-family: Inter, system-ui, -apple-system, sans-serif;
    font-size: 16px;          /* base */
    line-height: 1.6;         /* comfortable reading */
    color: #1e293b;
    background-color: #f8fafc;
}

h1 {
    font-size: clamp(1.8rem, 5vw, 3rem);  /* responsive font size */
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0f172a;
}

.accent { color: #6366f1; }

/* CSS Custom Properties (variables) */
:root {
    --primary:  #6366f1;
    --success:  #22c55e;
    --text:     #1e293b;
    --muted:    #64748b;
    --surface:  #ffffff;
    --border:   #e2e8f0;
    --radius:   12px;
}

.btn {
    background: var(--primary);
    border-radius: var(--radius);
    color: white;
    padding: 10px 20px;
}
```''',
            'Style the HTML profile page you built in the HTML lesson. Add: a color scheme using CSS variables, a different font from Google Fonts, box model spacing on all elements, and hover effects on the links and skills list.',
            'What does `box-sizing: border-box` change about how width and height are calculated? A) Excludes margin from width  B) Width includes padding and border  C) Doubles the padding  D) Removes the border',
            'Build a complete CSS style guide: create an HTML page that demonstrates all color variables, typography scale (h1-h6, p, small), button variants (primary, secondary, ghost, danger), form element styles, and card/badge components. Use only CSS custom properties for colors.',
            'Google Fonts can be loaded with `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">`. The `display=swap` parameter prevents invisible text while the font loads.',
            50)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 2, 'CSS Layout: Flexbox and Grid',
            'Build complex, responsive page layouts using CSS Flexbox and CSS Grid.',
            '''## CSS Flexbox

Flexbox is a one-dimensional layout system (row OR column).

```css
.container {
    display: flex;
    flex-direction: row;        /* row | column */
    justify-content: space-between; /* main axis */
    align-items: center;        /* cross axis */
    flex-wrap: wrap;            /* allow wrapping */
    gap: 16px;                  /* space between items */
}

/* Flex children */
.item {
    flex: 1;            /* grow equally */
    flex: 0 0 200px;    /* fixed 200px, no grow/shrink */
    align-self: flex-start;  /* override align-items */
}
```

### Flexbox Navbar

```css
nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    height: 64px;
    background: #1e293b;
}

.nav-links {
    display: flex;
    gap: 28px;
    list-style: none;
    margin: 0;
    padding: 0;
}

@media (max-width: 768px) {
    .nav-links {
        display: none;  /* hide on mobile */
    }
}
```

### CSS Grid

Grid is a two-dimensional layout system (rows AND columns).

```css
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* 3 equal columns */
    grid-template-rows: auto;
    gap: 24px;
}

/* Different column sizes */
.layout {
    display: grid;
    grid-template-columns: 250px 1fr;  /* sidebar + main */
    grid-template-areas:
        "header  header"
        "sidebar main  "
        "footer  footer";
    min-height: 100vh;
}

header { grid-area: header; }
aside  { grid-area: sidebar; }
main   { grid-area: main; }
footer { grid-area: footer; }
```

### Responsive Design with Media Queries

```css
/* Mobile first: default styles = mobile */
.card-grid {
    display: grid;
    grid-template-columns: 1fr;   /* 1 column */
    gap: 16px;
}

/* Tablet */
@media (min-width: 640px) {
    .card-grid { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop */
@media (min-width: 1024px) {
    .card-grid { grid-template-columns: repeat(3, 1fr); }
}

/* Large desktop */
@media (min-width: 1280px) {
    .card-grid { grid-template-columns: repeat(4, 1fr); }
}
```

### CSS Transitions and Animations

```css
/* Smooth transitions */
.btn {
    background: #6366f1;
    transform: translateY(0);
    transition: background 200ms ease, transform 200ms ease, box-shadow 200ms ease;
}
.btn:hover {
    background: #4f46e5;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(99, 102, 241, .3);
}

/* Keyframe animation */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-text {
    animation: fadeInUp 0.6s ease forwards;
}

/* Spinning loader */
@keyframes spin {
    to { transform: rotate(360deg); }
}
.loader {
    width: 40px; height: 40px;
    border: 4px solid #e2e8f0;
    border-top-color: #6366f1;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}
```''',
            'Build a dashboard layout with CSS Grid: a fixed sidebar (250px) and main content area. Inside the main area, use Flexbox to create a stats row (4 equal cards) and a responsive card grid below it.',
            'In CSS Flexbox, which property controls the alignment of items along the main (primary) axis? A) align-items  B) align-content  C) justify-content  D) flex-direction',
            'Build a complete responsive portfolio page using CSS Grid and Flexbox: header/nav, a hero section (full viewport height), a 3-column project grid (1 column on mobile), a skills section, and a footer. No CSS framework — pure CSS only.',
            'CSS Grid and Flexbox complement each other. Use Grid for the overall page structure (rows and columns together) and Flexbox for components within those grid areas (single-direction alignment).',
            60)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 3, 'CSS Project: Design System',
            'Build a complete, reusable CSS design system with tokens, components, and dark mode.',
            '''## Project: CSS Design System

### Folder Structure

```
css/
├── tokens.css        ← variables (colors, spacing, type)
├── reset.css         ← normalize browser defaults
├── base.css          ← global element styles
├── components/
│   ├── buttons.css
│   ├── cards.css
│   ├── forms.css
│   ├── nav.css
│   └── badges.css
└── utilities.css     ← helper classes
```

### tokens.css

```css
:root {
    /* Colors */
    --color-primary-50:  #eef2ff;
    --color-primary-500: #6366f1;
    --color-primary-600: #4f46e5;
    --color-primary-900: #1e1b4b;

    --color-success: #22c55e;
    --color-warning: #f59e0b;
    --color-danger:  #ef4444;

    --color-text:    #1e293b;
    --color-muted:   #64748b;
    --color-surface: #ffffff;
    --color-border:  #e2e8f0;

    /* Spacing scale */
    --space-1:  4px;
    --space-2:  8px;
    --space-3:  12px;
    --space-4:  16px;
    --space-6:  24px;
    --space-8:  32px;
    --space-12: 48px;
    --space-16: 64px;

    /* Typography */
    --font-sans:    Inter, system-ui, sans-serif;
    --font-mono:    'Fira Code', monospace;
    --text-sm:      0.875rem;
    --text-base:    1rem;
    --text-lg:      1.125rem;
    --text-xl:      1.25rem;
    --text-2xl:     1.5rem;
    --text-4xl:     2.25rem;

    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0,0,0,.06);
    --shadow-md: 0 4px 12px rgba(0,0,0,.08);
    --shadow-lg: 0 8px 32px rgba(0,0,0,.1);

    /* Borders */
    --radius-sm:  6px;
    --radius-md:  10px;
    --radius-lg:  16px;
    --radius-full: 9999px;
}

/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
    :root {
        --color-text:    #f1f5f9;
        --color-muted:   #94a3b8;
        --color-surface: #1e293b;
        --color-border:  #334155;
    }
}
[data-theme="dark"] {
    --color-text:    #f1f5f9;
    --color-surface: #1e293b;
    --color-border:  #334155;
}
```

### components/buttons.css

```css
.btn {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-4);
    border: 2px solid transparent;
    border-radius: var(--radius-md);
    font-family: var(--font-sans);
    font-size: var(--text-sm);
    font-weight: 600;
    cursor: pointer;
    transition: all 150ms ease;
    text-decoration: none;
}

.btn-primary { background: var(--color-primary-500); color: #fff; }
.btn-primary:hover { background: var(--color-primary-600); transform: translateY(-1px); }

.btn-ghost { background: transparent; border-color: var(--color-border); color: var(--color-text); }
.btn-ghost:hover { border-color: var(--color-primary-500); color: var(--color-primary-500); }

.btn-danger { background: var(--color-danger); color: #fff; }

.btn-sm { padding: var(--space-1) var(--space-3); font-size: .75rem; }
.btn-lg { padding: var(--space-3) var(--space-8); font-size: var(--text-base); }
```

### Deliverables
1. All CSS files above, fully implemented
2. A demo HTML page showing ALL components
3. Dark mode toggle working
4. All buttons, cards, form fields, badges, and nav
5. Documented with comments explaining each design decision''',
            'Add a `.prose` component class that styles any block of HTML text content: headings, paragraphs, code blocks, blockquotes, and lists — with sensible typography for long-form reading.',
            'What CSS feature allows you to define reusable values (colors, spacing) that can be referenced throughout the stylesheet? A) SASS mixins  B) CSS variables (custom properties)  C) @import  D) !important',
            'Extend the design system with a grid utilities file: `.container` (max-width centered), `.grid-2`, `.grid-3`, `.grid-4` (responsive column grids), `.flex`, `.flex-col`, `.items-center`, `.justify-between`. Then use it to build a 3-page website without any HTML framework.',
            'CSS custom properties cascade and inherit like other CSS properties. Defining them on `:root` makes them global. Redefining on a specific selector overrides for that element and all its descendants.',
            75)
        if r: created += 1
        else: updated += 1

        # ── JAVASCRIPT FOR WEB ───────────────────────────────────────────────
        p = LearningPath.objects.get(slug='javascript-for-web')

        r = upsert(p, 1, 'JavaScript DOM Manipulation',
            'Select, modify, and create HTML elements dynamically using the DOM API.',
            '''## JavaScript in the Browser

### How JavaScript Connects to HTML

```html
<!-- At end of body (best practice) -->
<script src="app.js"></script>

<!-- Or with defer: loads in parallel, executes after HTML parsed -->
<script src="app.js" defer></script>
```

### Selecting Elements

```javascript
// Single element
const heading = document.querySelector('h1');
const btn     = document.querySelector('#submit-btn');
const card    = document.querySelector('.card');

// Multiple elements (NodeList)
const items   = document.querySelectorAll('li');
const buttons = document.querySelectorAll('.btn');

// Old-style (still common)
const el = document.getElementById('myId');
```

### Reading and Modifying Elements

```javascript
// Read content
console.log(heading.textContent);   // plain text
console.log(heading.innerHTML);      // includes HTML tags

// Change content
heading.textContent = 'Welcome, Alice!';
heading.innerHTML   = 'Welcome, <strong>Alice!</strong>';

// Change style
heading.style.color       = '#6366f1';
heading.style.fontSize    = '2rem';
heading.style.display     = 'none';    // hide
heading.style.display     = '';        // show (reset)

// Add/remove CSS classes (preferred over inline style)
btn.classList.add('active');
btn.classList.remove('active');
btn.classList.toggle('active');       // on/off
btn.classList.contains('active');     // true/false
```

### Reading Form Values

```javascript
const nameInput  = document.querySelector('#name');
const levelSelect = document.querySelector('#level');

const name  = nameInput.value;
const level = levelSelect.value;

// Checkboxes
const agreed = document.querySelector('#agree').checked; // true/false
```

### Creating and Inserting Elements

```javascript
// Create a new element
const card = document.createElement('article');
card.className = 'card';
card.innerHTML = `
    <h3>Python Course</h3>
    <p>Learn Python from scratch.</p>
    <a href="/python" class="btn">Enroll</a>
`;

// Insert into the page
document.querySelector('.courses-grid').appendChild(card);

// Insert before another element
const grid = document.querySelector('.courses-grid');
const firstCard = grid.firstElementChild;
grid.insertBefore(card, firstCard);

// Remove an element
card.remove();
```

### Event Listeners

```javascript
const btn = document.querySelector('#search-btn');

btn.addEventListener('click', function(event) {
    event.preventDefault();    // stop form submission
    const query = document.querySelector('#search-input').value;
    console.log('Searching for:', query);
    doSearch(query);
});

// Arrow function style
btn.addEventListener('click', (e) => {
    e.stopPropagation();    // don't bubble up to parent
    handleClick(e.target);
});

// Common events
// click, dblclick, mouseenter, mouseleave
// keydown, keyup, keypress
// submit, change, input, focus, blur
// scroll, resize, load

// Listen for Enter key on input
document.querySelector('#search-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') doSearch(e.target.value);
});
```

### Traversing the DOM

```javascript
const item = document.querySelector('.selected');

item.parentElement          // parent node
item.children               // child elements
item.nextElementSibling     // next sibling
item.previousElementSibling // previous sibling
item.closest('.card')       // nearest ancestor matching selector
```''',
            'Build a dynamic to-do list: an input + button that appends new list items when clicked, and a delete button on each item that removes it. Style the completed items differently when clicked.',
            'Which DOM method returns the FIRST element matching a CSS selector? A) getElementById  B) querySelector  C) getElementsByClassName  D) querySelectorAll',
            'Build an interactive quiz app: display one question at a time from an array of 5 question objects, highlight the chosen answer (green correct, red wrong), show a score tracker, and display the final score with a restart button at the end.',
            'Event delegation: instead of adding listeners to each list item, add ONE listener to the parent. Use `event.target.closest(".item")` to check what was clicked. This works for dynamically added elements and is more efficient.',
            55)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 2, 'JavaScript Fetch API and Async',
            'Make HTTP requests with the Fetch API and write clean async/await code.',
            '''## Asynchronous JavaScript

### Callbacks (old way)

```javascript
setTimeout(() => {
    console.log('After 2 seconds');
}, 2000);

// Callback hell — hard to read
fetchUser(id, (user) => {
    fetchCourses(user.id, (courses) => {
        fetchProgress(courses[0].id, (progress) => {
            console.log(progress); // deeply nested!
        });
    });
});
```

### Promises

```javascript
fetch('https://api.example.com/courses')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
```

### Async/Await (modern, recommended)

```javascript
async function loadCourses() {
    try {
        const response = await fetch('https://api.example.com/courses');

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const courses = await response.json();
        return courses;
    } catch (error) {
        console.error('Failed to load courses:', error);
        return [];
    }
}

// Call it
const courses = await loadCourses();
renderCourses(courses);
```

### GET Request

```javascript
async function searchCourses(query) {
    const url = new URL('/api/courses/', window.location.origin);
    url.searchParams.set('q', query);
    url.searchParams.set('limit', 10);

    const resp = await fetch(url);
    return resp.json();
}
```

### POST Request (Submit a Form)

```javascript
async function enrollInCourse(formData) {
    const resp = await fetch('/api/enroll/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),     // Django CSRF
        },
        body: JSON.stringify({
            course_id:  formData.course_id,
            student_id: formData.student_id,
        }),
    });

    if (!resp.ok) {
        const error = await resp.json();
        throw new Error(error.detail || 'Enrollment failed');
    }
    return resp.json();
}

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
```

### Rendering Fetched Data

```javascript
async function renderCourses() {
    const grid = document.querySelector('#courses-grid');
    grid.innerHTML = '<p class="loading">Loading courses...</p>';

    try {
        const courses = await loadCourses();

        grid.innerHTML = courses.map(course => `
            <article class="card">
                <span class="tag">${course.category}</span>
                <h3>${escapeHtml(course.title)}</h3>
                <p>${escapeHtml(course.description)}</p>
                <a href="/courses/${course.slug}/" class="btn">View Course</a>
            </article>
        `).join('');

    } catch (err) {
        grid.innerHTML = `<p class="error">Failed to load: ${err.message}</p>`;
    }
}

function escapeHtml(str) {
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
}

renderCourses();
```

### Parallel Requests

```javascript
// Run both at once (faster than sequential)
const [user, courses] = await Promise.all([
    fetch('/api/user/').then(r => r.json()),
    fetch('/api/courses/').then(r => r.json()),
]);
```''',
            'Build a course search page: a text input that calls a /api/courses/?q=... endpoint as you type (debounce to 300ms). Display results in a grid with loading and error states.',
            'Which async keyword pair should you use to wait for a fetch() response in modern JavaScript? A) then/catch  B) async/await  C) setTimeout/Promise  D) yield/next',
            'Build a full CRUD interface for a notes app: load all notes on page load, create a new note via POST, update note title via PUT on blur, and delete via DELETE with a confirmation. All changes persist to a Django API backend.',
            'Always escape user-generated content before inserting into innerHTML to prevent XSS. Use `element.textContent = userText` for plain text, or a function that creates a text node. Never use `innerHTML = untrustedInput` directly.',
            60)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 3, 'JavaScript Project: Interactive Web App',
            'Build a complete single-page web application with state management, routing, and API integration.',
            '''## Project: Flashcard Study App

### Features
- Create, edit, and delete flashcard decks
- Flip cards to reveal answer
- Score tracking (got it / missed)
- LocalStorage persistence

### Application State

```javascript
// state.js — single source of truth
const state = {
    decks: [],
    activeDeckId: null,
    currentCardIndex: 0,
    score: { correct: 0, total: 0 },
    isFlipped: false,
};

function getActiveDeck() {
    return state.decks.find(d => d.id === state.activeDeckId);
}

function getCurrentCard() {
    const deck = getActiveDeck();
    return deck?.cards[state.currentCardIndex] ?? null;
}
```

### Rendering Functions

```javascript
function renderDeckList() {
    const container = document.querySelector('#deck-list');
    container.innerHTML = state.decks.map(deck => `
        <div class="deck-card ${deck.id === state.activeDeckId ? 'active' : ''}"
             data-id="${deck.id}">
            <h3>${escapeHtml(deck.title)}</h3>
            <p>${deck.cards.length} cards</p>
            <div class="deck-actions">
                <button class="btn-study" data-id="${deck.id}">Study</button>
                <button class="btn-delete" data-id="${deck.id}">Delete</button>
            </div>
        </div>
    `).join('');
}

function renderFlashcard() {
    const card = getCurrentCard();
    if (!card) { showComplete(); return; }

    const el = document.querySelector('#flashcard');
    el.innerHTML = `
        <div class="card-inner ${state.isFlipped ? 'flipped' : ''}">
            <div class="card-front">
                <p class="card-label">Question ${state.currentCardIndex + 1} / ${getActiveDeck().cards.length}</p>
                <h2>${escapeHtml(card.question)}</h2>
                <p class="hint">Click to reveal answer</p>
            </div>
            <div class="card-back">
                <p class="card-label">Answer</p>
                <h2>${escapeHtml(card.answer)}</h2>
                <div class="score-btns">
                    <button id="got-it">Got it!</button>
                    <button id="missed">Missed</button>
                </div>
            </div>
        </div>
    `;
}
```

### Event Handling

```javascript
// Delegate events from container
document.querySelector('#deck-list').addEventListener('click', (e) => {
    const id = Number(e.target.dataset.id);
    if (e.target.matches('.btn-study'))  startStudy(id);
    if (e.target.matches('.btn-delete')) deleteDeck(id);
});

document.querySelector('#flashcard')?.addEventListener('click', (e) => {
    if (e.target.matches('#flashcard, .card-inner, .card-front')) {
        state.isFlipped = !state.isFlipped;
        renderFlashcard();
    }
    if (e.target.id === 'got-it')  recordAnswer(true);
    if (e.target.id === 'missed')  recordAnswer(false);
});

function recordAnswer(correct) {
    state.score.total++;
    if (correct) state.score.correct++;
    state.currentCardIndex++;
    state.isFlipped = false;
    renderFlashcard();
    renderScoreBar();
}
```

### LocalStorage Persistence

```javascript
function saveState() {
    localStorage.setItem('flashcards', JSON.stringify(state.decks));
}

function loadState() {
    const saved = localStorage.getItem('flashcards');
    if (saved) state.decks = JSON.parse(saved);
}

// Call after every mutation
function addDeck(title) {
    state.decks.push({ id: Date.now(), title, cards: [] });
    saveState();
    renderDeckList();
}
```

### CSS: Card Flip Effect

```css
.card-inner {
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.5s ease;
    cursor: pointer;
}
.card-inner.flipped { transform: rotateY(180deg); }

.card-front, .card-back {
    position: absolute; inset: 0;
    backface-visibility: hidden;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 40px; border-radius: 20px;
}
.card-back { transform: rotateY(180deg); background: var(--primary); color: white; }
```

### Deliverables
1. Create/delete decks and add/remove cards
2. Study mode with card flip animation
3. Score tracking (% correct)
4. LocalStorage persistence
5. Keyboard shortcuts (Space to flip, Left arrow missed, Right arrow got it)''',
            'Add keyboard shortcuts: Space to flip the card, ArrowRight for "Got it", ArrowLeft for "Missed". Use document.addEventListener("keydown") and check e.key.',
            'Which Web API allows JavaScript to persist data in the user\'s browser without a server? A) IndexedDB  B) localStorage  C) sessionStorage  D) cookies',
            'Add a "shuffle" feature that randomizes card order, and a "spaced repetition" mode that shows missed cards more frequently. Track per-card accuracy in state and use it to weight which cards appear next.',
            'The `data-*` HTML attribute pattern lets you attach arbitrary data to elements without polluting the JS global scope. Use `element.dataset.id` to read `data-id`, etc. This is better than looking up indices or global maps.',
            90)
        if r: created += 1
        else: updated += 1

        # ── NEXTJS ───────────────────────────────────────────────────────────
        p = LearningPath.objects.get(slug='nextjs')

        r = upsert(p, 1, 'Next.js Fundamentals: App Router and Components',
            'Understand the Next.js App Router, file-based routing, and React Server Components.',
            '''## Why Next.js?

Next.js adds production features on top of React:
- **File-based routing** (no need for react-router)
- **Server-Side Rendering (SSR)** and **Static Site Generation (SSG)**
- **API Routes** (full-stack in one project)
- **Image optimization, fonts, metadata** built-in

### Create a Next.js App

```bash
npx create-next-app@latest my-app
# Choose: TypeScript? Yes  |  ESLint? Yes  |  Tailwind? Yes  |  App Router? Yes
cd my-app && npm run dev
```

### App Router Folder Structure

```
app/
├── layout.tsx          ← Root layout (wraps all pages)
├── page.tsx            ← Home page: /
├── about/
│   └── page.tsx        ← About page: /about
├── courses/
│   ├── page.tsx        ← Courses list: /courses
│   └── [slug]/
│       └── page.tsx    ← Course detail: /courses/python-programming
└── api/
    └── courses/
        └── route.ts    ← API endpoint: /api/courses
```

### Root Layout

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: { default: 'CodeSavannah', template: '%s | CodeSavannah' },
  description: "Africa's premier coding academy",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <header className="sticky top-0 z-50 bg-white border-b">
          {/* Navigation */}
        </header>
        <main>{children}</main>
        <footer className="bg-slate-900 text-white py-12">
          {/* Footer */}
        </footer>
      </body>
    </html>
  )
}
```

### Server Components (default in App Router)

```tsx
// app/courses/page.tsx — runs on server, can fetch directly
import { getCourses } from '@/lib/data'

export const metadata = { title: 'Courses' }

export default async function CoursesPage() {
  // This runs on the server — no useEffect needed!
  const courses = await getCourses()

  return (
    <section className="container mx-auto py-12">
      <h1 className="text-4xl font-bold mb-8">Our Courses</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {courses.map(course => (
          <CourseCard key={course.slug} course={course} />
        ))}
      </div>
    </section>
  )
}
```

### Dynamic Routes

```tsx
// app/courses/[slug]/page.tsx
import { getCourseBySlug } from '@/lib/data'
import { notFound } from 'next/navigation'

interface Props {
  params: { slug: string }
}

export async function generateMetadata({ params }: Props) {
  const course = await getCourseBySlug(params.slug)
  return { title: course?.title ?? 'Course Not Found' }
}

export default async function CourseDetailPage({ params }: Props) {
  const course = await getCourseBySlug(params.slug)
  if (!course) notFound()

  return (
    <article>
      <h1>{course.title}</h1>
      <p>{course.description}</p>
    </article>
  )
}
```

### Client Components

```tsx
// components/SearchBar.tsx
'use client'  // ← this directive makes it a Client Component
import { useState } from 'react'
import { useRouter } from 'next/navigation'

export function SearchBar() {
  const [query, setQuery] = useState('')
  const router = useRouter()

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    router.push(`/courses?q=${encodeURIComponent(query)}`)
  }

  return (
    <form onSubmit={handleSearch} className="flex gap-2">
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search courses..."
        className="border rounded px-3 py-2 flex-1"
      />
      <button type="submit" className="btn-primary">Search</button>
    </form>
  )
}
```''',
            'Create a Next.js app with 3 pages: home (/), courses list (/courses), and a dynamic course detail (/courses/[slug]). Use hardcoded data arrays for now. Add proper metadata for each page.',
            'In Next.js App Router, which directive makes a component run in the browser (enabling hooks and event handlers)? A) "use server"  B) "use client"  C) "client: true"  D) @client',
            'Build a blog with Next.js App Router: fetch posts from a free API (jsonplaceholder.typicode.com/posts), render a paginated list, and dynamic detail pages. Use generateStaticParams() to pre-render the first 10 posts at build time.',
            'Server Components run on the server and send HTML to the browser — no JavaScript bundle is shipped for them. Client Components ship JavaScript and enable interactivity. Keep interactive parts as leaf nodes to minimize client JS.',
            65)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 2, 'Next.js Data Fetching and API Routes',
            'Fetch data with Server Components, build API routes, and implement Static and Dynamic rendering.',
            '''## Data Fetching in Next.js

### Fetch in Server Components

```tsx
// app/courses/page.tsx
async function getCourses(query = '') {
  const url = `https://api.codesavannah.com/courses?q=${query}`
  const res = await fetch(url, {
    next: { revalidate: 3600 }  // cache for 1 hour (ISR)
  })
  if (!res.ok) throw new Error('Failed to fetch courses')
  return res.json()
}

// No cache (always fresh)
const fresh = await fetch(url, { cache: 'no-store' })

// Cache forever (static)
const cached = await fetch(url, { cache: 'force-cache' })
```

### API Route (App Router)

```typescript
// app/api/courses/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/lib/db'

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const query = searchParams.get('q') ?? ''

  const courses = await db.course.findMany({
    where: { title: { contains: query, mode: 'insensitive' } },
    orderBy: { title: 'asc' },
    take: 20,
  })

  return NextResponse.json(courses)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  // Validate
  if (!body.title) {
    return NextResponse.json({ error: 'Title required' }, { status: 400 })
  }
  const course = await db.course.create({ data: body })
  return NextResponse.json(course, { status: 201 })
}
```

### Dynamic API Segment

```typescript
// app/api/courses/[slug]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { slug: string } }
) {
  const course = await db.course.findUnique({ where: { slug: params.slug } })
  if (!course) return NextResponse.json({ error: 'Not found' }, { status: 404 })
  return NextResponse.json(course)
}
```

### Prisma ORM Setup

```bash
npm install prisma @prisma/client
npx prisma init

# prisma/schema.prisma
model Course {
  id          Int      @id @default(autoincrement())
  slug        String   @unique
  title       String
  description String
  level       String   @default("beginner")
  createdAt   DateTime @default(now())
}
```

### Suspense and Loading States

```tsx
// app/courses/loading.tsx — automatic loading UI
export default function CoursesLoading() {
  return (
    <div className="grid grid-cols-3 gap-6">
      {[...Array(6)].map((_, i) => (
        <div key={i} className="h-48 bg-slate-200 rounded-xl animate-pulse" />
      ))}
    </div>
  )
}

// Or use Suspense manually
import { Suspense } from 'react'
import { CoursesList } from './CoursesList'

export default function Page() {
  return (
    <Suspense fallback={<CoursesLoading />}>
      <CoursesList />
    </Suspense>
  )
}
```

### Error Handling

```tsx
// app/courses/error.tsx — catches errors in the subtree
'use client'
export default function Error({ error, reset }: { error: Error, reset: () => void }) {
  return (
    <div className="text-center py-12">
      <h2>Something went wrong</h2>
      <p className="text-slate-500">{error.message}</p>
      <button onClick={reset} className="btn mt-4">Try again</button>
    </div>
  )
}
```''',
            'Build 3 API routes: GET /api/courses (list all), GET /api/courses/[slug] (single), POST /api/courses (create). Test with curl or the browser. Add request validation for the POST route.',
            'Which Next.js fetch option caches the response and revalidates it every hour (ISR)? A) cache: "force-cache"  B) next: { revalidate: 3600 }  C) cache: "no-store"  D) next: { static: true }',
            'Build a full-stack Next.js blog: API routes for CRUD, Server Components that fetch from the API, and a Client Component for the create/edit form. Use Prisma with SQLite for the database. Deploy to Vercel.',
            'Next.js collocates your API and frontend in one project, making it easy to share TypeScript types between them. Define your data types in a shared `types/` folder and import them in both API routes and components.',
            65)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 3, 'Next.js Project: Full-Stack Academy Platform',
            'Build and deploy a complete Next.js full-stack web application with authentication, database, and deployment.',
            '''## Project: Course Platform with Next.js + Prisma + Auth

### Tech Stack
- Next.js 14 App Router
- Prisma + SQLite (switch to PostgreSQL for production)
- NextAuth.js for authentication
- TailwindCSS for styling
- Vercel for deployment

### Authentication Setup

```bash
npm install next-auth @prisma/client prisma
```

```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth'
import GithubProvider from 'next-auth/providers/github'
import CredentialsProvider from 'next-auth/providers/credentials'

const handler = NextAuth({
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
    CredentialsProvider({
      name: 'Email',
      credentials: {
        email:    { label: 'Email',    type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        const user = await db.user.findUnique({
          where: { email: credentials?.email }
        })
        if (!user) return null
        const valid = await bcrypt.compare(credentials!.password, user.password)
        return valid ? user : null
      }
    }),
  ],
  callbacks: {
    session: ({ session, token }) => ({
      ...session,
      user: { ...session.user, id: token.sub }
    })
  }
})

export { handler as GET, handler as POST }
```

### Protected Pages

```tsx
// app/dashboard/page.tsx
import { getServerSession } from 'next-auth'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const session = await getServerSession()
  if (!session) redirect('/login')

  const enrollments = await db.enrollment.findMany({
    where: { userId: session.user.id },
    include: { course: true }
  })

  return (
    <div>
      <h1>Welcome, {session.user.name}!</h1>
      <h2>Your Courses</h2>
      {enrollments.map(e => (
        <CourseCard key={e.id} course={e.course} />
      ))}
    </div>
  )
}
```

### Database Schema

```prisma
// prisma/schema.prisma
model User {
  id          String       @id @default(cuid())
  name        String?
  email       String       @unique
  password    String
  enrollments Enrollment[]
  createdAt   DateTime     @default(now())
}

model Course {
  id          String       @id @default(cuid())
  slug        String       @unique
  title       String
  description String
  level       String       @default("beginner")
  enrollments Enrollment[]
}

model Enrollment {
  id        String   @id @default(cuid())
  user      User     @relation(fields: [userId], references: [id])
  userId    String
  course    Course   @relation(fields: [courseId], references: [id])
  courseId  String
  createdAt DateTime @default(now())
  @@unique([userId, courseId])
}
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard:
# DATABASE_URL, NEXTAUTH_SECRET, GITHUB_ID, GITHUB_SECRET
```

### Deliverables
1. Working authentication (email + GitHub OAuth)
2. Course list and detail pages (Server Components)
3. Enrollment system (Client Component + API route)
4. User dashboard showing enrolled courses
5. Deployed and publicly accessible on Vercel''',
            'Set up NextAuth.js with the Credentials provider. Create a registration page that hashes passwords with bcrypt and saves to the database. Test that login/logout works.',
            'In Next.js, where should you check authentication in a Server Component to protect a page? A) useEffect  B) getServerSession() at the top of the component  C) middleware.ts  D) Both B and C',
            'Add course progress tracking: when a user views a lesson page, record it in the database. Show a progress bar on the course detail page and dashboard. Add a "Complete Course" button that sends a completion event.',
            'Vercel auto-deploys on every git push to main. Set up branch previews to get a unique URL for each pull request — invaluable for testing before merging to production.',
            90)
        if r: created += 1
        else: updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Batch 7 complete: {created} created, {updated} updated'
        ))
