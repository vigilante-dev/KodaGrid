"""
Curriculum batch 3 — React, Next.js, Node.js, Bootstrap, TailwindCSS.
Run: python manage.py generate_curriculum_3
"""
from django.core.management.base import BaseCommand
from academy.models import LearningPath, Lesson


def upsert(path, order, title, objective, content, exercise, quiz_q, project, notes, mins):
    qs = Lesson.objects.filter(learning_path=path, order=order)
    # Remove duplicates if any exist from previous partial runs
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


REACT_LESSONS = [
    (1, "React Introduction — Components, JSX & Props",
     "Understand React's component model, write JSX, and pass data with props.",
     '''## What is React?

React is a JavaScript library for building user interfaces, created by Facebook (Meta) in 2013. It uses a component-based architecture and a virtual DOM to efficiently update the UI.

**Core ideas:**
- **Components** — reusable, isolated UI building blocks
- **JSX** — JavaScript + HTML syntax combined
- **Virtual DOM** — React diffs changes, updates only what changed
- **Unidirectional data flow** — data flows down via props

## Setup

```bash
# Create React app with Vite (recommended 2025)
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev

# Or with TypeScript
npm create vite@latest my-app -- --template react-ts
```

## Your first component

```jsx
// App.jsx
import CourseCard from "./CourseCard";

const courses = [
    { id: 1, title: "Python Programming", level: "beginner",  price: 12000 },
    { id: 2, title: "Web Development",    level: "beginner",  price: 15000 },
    { id: 3, title: "Cybersecurity",      level: "intermediate", price: 18000 },
];

function App() {
    return (
        <div className="app">
            <header>
                <h1>CodeSavannah Academy</h1>
                <p>Learn. Build. Succeed.</p>
            </header>
            <main>
                <h2>Our Courses</h2>
                <div className="card-grid">
                    {courses.map(course => (
                        <CourseCard key={course.id} course={course} />
                    ))}
                </div>
            </main>
        </div>
    );
}

export default App;
```

## JSX rules

```jsx
// 1. Return a SINGLE root element (use <> fragment if needed)
function Good() {
    return (
        <>                      {/* Fragment — renders no extra DOM element */}
            <h1>Title</h1>
            <p>Content</p>
        </>
    );
}

// 2. All tags must be closed
// HTML:  <img src="...">
// JSX:   <img src="..." />

// 3. Use className, not class
// HTML:  <div class="card">
// JSX:   <div className="card">

// 4. camelCase for attributes
// HTML:  onclick, tabindex, maxlength
// JSX:   onClick, tabIndex, maxLength

// 5. JavaScript expressions in { }
const name = "Grace";
const element = <h1>Hello, {name}!</h1>;
const sum     = <p>{2 + 2}</p>;          // 4
const cond    = <p>{isLoggedIn ? "Welcome" : "Please log in"}</p>;
```

## Props — passing data to components

```jsx
// Receiving props
function CourseCard({ course, onEnroll, featured = false }) {
    return (
        <article className={`card ${featured ? "card-featured" : ""}`}>
            <span className={`tag tag-${course.level}`}>{course.level}</span>
            <h2>{course.title}</h2>
            <p className="price">KES {course.price.toLocaleString()}</p>
            <button onClick={() => onEnroll(course.id)}>
                Enrol Now
            </button>
        </article>
    );
}

// Passing props
<CourseCard
    course={courses[0]}
    onEnroll={(id) => console.log("Enrolling:", id)}
    featured={true}
/>

// Spreading props
const cardProps = { course: courses[0], featured: true };
<CourseCard {...cardProps} onEnroll={handleEnroll} />

// children prop
function Card({ title, children }) {
    return (
        <div className="card">
            <h3>{title}</h3>
            <div className="card-body">{children}</div>
        </div>
    );
}

<Card title="My Card">
    <p>This content goes into children</p>
    <button>Action</button>
</Card>
```

## Rendering lists and conditional rendering

```jsx
// Lists — always use a stable key
const items = courses.map(course => (
    <li key={course.id}>{course.title}</li>
));

// Conditional rendering
function StatusBadge({ enrolled, loading }) {
    if (loading) return <span className="badge">Loading...</span>;
    if (enrolled) return <span className="badge badge-success">Enrolled</span>;
    return <span className="badge badge-info">Available</span>;
}

// Conditional with &&
{isAdmin && <button>Delete Course</button>}

// Conditional with ternary
{error ? <ErrorMessage msg={error} /> : <CourseList courses={courses} />}
```
''',
     "Build a React product catalog: a Product component with image, name, price, and Add to Cart button. Render 6 products from an array. Show total count of items in a header badge.",
     "In React JSX, what attribute is used instead of 'class' to apply CSS classes?",
     "Build a React course catalog: CourseCard component with image, title, level badge, duration, and price. Filter by level (beginner/intermediate/advanced). Sort by price. Show/hide course details on click.",
     "Always provide a stable key prop when rendering lists — React uses keys to efficiently reconcile the DOM. Never use array index as key if the list can be reordered or filtered.",
     50),

    (2, "React State & Hooks — useState, useEffect, useContext",
     "Manage component state and side effects using React hooks.",
     '''## useState — managing local state

```jsx
import { useState } from "react";

function Counter() {
    // [stateValue, setterFunction] = useState(initialValue)
    const [count, setCount] = useState(0);

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>+1</button>
            <button onClick={() => setCount(count - 1)}>-1</button>
            <button onClick={() => setCount(0)}>Reset</button>
        </div>
    );
}

// Object state
function ProfileForm() {
    const [form, setForm] = useState({
        name: "", email: "", grade: ""
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm(prev => ({ ...prev, [name]: value }));
        //            ↑ ALWAYS spread previous state for objects
    };

    return (
        <form>
            <input name="name"  value={form.name}  onChange={handleChange} />
            <input name="email" value={form.email} onChange={handleChange} />
        </form>
    );
}

// Array state
function TodoList() {
    const [todos, setTodos] = useState([]);
    const [input, setInput]  = useState("");

    const add = () => {
        if (!input.trim()) return;
        setTodos(prev => [...prev, { id: Date.now(), text: input, done: false }]);
        setInput("");
    };

    const toggle = (id) => {
        setTodos(prev => prev.map(t => t.id === id ? { ...t, done: !t.done } : t));
    };

    const remove = (id) => {
        setTodos(prev => prev.filter(t => t.id !== id));
    };

    return (
        <div>
            <input value={input} onChange={e => setInput(e.target.value)} />
            <button onClick={add}>Add</button>
            <ul>
                {todos.map(todo => (
                    <li key={todo.id} style={{ textDecoration: todo.done ? "line-through" : "none" }}>
                        <span onClick={() => toggle(todo.id)}>{todo.text}</span>
                        <button onClick={() => remove(todo.id)}>✕</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}
```

## useEffect — side effects and data fetching

```jsx
import { useState, useEffect } from "react";

function CourseList() {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error,   setError]   = useState(null);

    useEffect(() => {
        // Effect runs after render
        let cancelled = false;  // prevent state update on unmounted component

        async function fetchCourses() {
            try {
                const res  = await fetch("/api/courses/");
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                const data = await res.json();
                if (!cancelled) {
                    setCourses(data.results || data);
                    setLoading(false);
                }
            } catch (err) {
                if (!cancelled) {
                    setError(err.message);
                    setLoading(false);
                }
            }
        }

        fetchCourses();
        return () => { cancelled = true; };  // cleanup — runs on unmount
    }, []);  // [] = run once on mount

    // Dependency array controls when effect re-runs:
    // []          = once on mount
    // [id]        = whenever id changes
    // [id, level] = whenever id OR level changes
    // (omitted)   = every render — usually a bug!

    if (loading) return <div className="spinner" />;
    if (error)   return <p className="error">Error: {error}</p>;

    return (
        <ul>
            {courses.map(c => <li key={c.id}>{c.title}</li>)}
        </ul>
    );
}
```

## useContext — global state without prop drilling

```jsx
import { createContext, useContext, useState } from "react";

// 1. Create context
const AuthContext = createContext(null);

// 2. Provider — wraps the app (or subtree) that needs the data
function AuthProvider({ children }) {
    const [user, setUser] = useState(null);

    const login = async (email, password) => {
        const res = await fetch("/api/auth/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });
        const data = await res.json();
        setUser(data.user);
        localStorage.setItem("token", data.access);
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem("token");
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

// 3. Custom hook — convenient wrapper
function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used within AuthProvider");
    return ctx;
}

// 4. Consume in any component (no matter how deeply nested)
function Navbar() {
    const { user, logout } = useAuth();
    return (
        <nav>
            {user ? (
                <>
                    <span>Hello, {user.name}</span>
                    <button onClick={logout}>Logout</button>
                </>
            ) : (
                <a href="/login">Login</a>
            )}
        </nav>
    );
}

// Wrap app in provider
function App() {
    return (
        <AuthProvider>
            <Navbar />
            <Routes />
        </AuthProvider>
    );
}
```

## Custom hooks — extract reusable logic

```jsx
// useLocalStorage
function useLocalStorage(key, initialValue) {
    const [value, setValue] = useState(() => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch { return initialValue; }
    });

    const set = (v) => {
        setValue(v);
        localStorage.setItem(key, JSON.stringify(v));
    };

    return [value, set];
}

// useDebounce
function useDebounce(value, delay = 300) {
    const [debounced, setDebounced] = useState(value);
    useEffect(() => {
        const id = setTimeout(() => setDebounced(value), delay);
        return () => clearTimeout(id);
    }, [value, delay]);
    return debounced;
}

// Usage
function Search() {
    const [query, setQuery] = useState("");
    const debouncedQuery = useDebounce(query, 400);

    useEffect(() => {
        if (debouncedQuery) fetchResults(debouncedQuery);
    }, [debouncedQuery]);

    return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```
''',
     "Build a React shopping cart: list of 6 products (useState), add/remove items, quantity controls, running total, and a checkout button that shows a confirmation. Use only useState and props.",
     "Which React hook runs a side effect (like a data fetch) after the component renders?",
     "Build a React task manager: useContext for global task state, useEffect to persist tasks in localStorage, useReducer for complex state transitions, custom useTasks hook, filter/sort controls, and priority tags.",
     "State updates in React are asynchronous and batched. When new state depends on old state (e.g., incrementing), always use the setter function form: setState(prev => prev + 1) — never setState(state + 1).",
     60),

    (3, "React Router & Single-Page Applications",
     "Build multi-page React applications with React Router v6.",
     '''## React Router v6 Setup

```bash
npm install react-router-dom
```

```jsx
// main.jsx
import { BrowserRouter } from "react-router-dom";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(
    <BrowserRouter>
        <App />
    </BrowserRouter>
);
```

## Defining routes

```jsx
// App.jsx
import { Routes, Route, Navigate } from "react-router-dom";

function App() {
    const { user } = useAuth();

    return (
        <div>
            <Navbar />
            <Routes>
                <Route path="/"               element={<HomePage />} />
                <Route path="/courses"        element={<CoursesPage />} />
                <Route path="/courses/:slug"  element={<CourseDetailPage />} />
                <Route path="/about"          element={<AboutPage />} />

                {/* Protected routes */}
                <Route path="/dashboard"      element={
                    user ? <DashboardPage /> : <Navigate to="/login" replace />
                } />

                {/* Nested routes */}
                <Route path="/admin" element={<AdminLayout />}>
                    <Route index       element={<AdminDashboard />} />
                    <Route path="courses" element={<AdminCourses />} />
                    <Route path="users"   element={<AdminUsers />} />
                </Route>

                {/* 404 */}
                <Route path="*" element={<NotFoundPage />} />
            </Routes>
        </div>
    );
}
```

## Navigation

```jsx
import { Link, NavLink, useNavigate, useParams, useSearchParams, useLocation } from "react-router-dom";

// Declarative navigation
<Link to="/courses">All Courses</Link>

// NavLink — adds "active" class when route matches
<NavLink to="/courses" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
    Courses
</NavLink>

// Programmatic navigation
function EnrolButton({ courseId }) {
    const navigate = useNavigate();

    const handleEnrol = async () => {
        await enrolInCourse(courseId);
        navigate("/dashboard", { state: { enrolled: true } });
    };
    return <button onClick={handleEnrol}>Enrol Now</button>;
}

// Route params
function CourseDetailPage() {
    const { slug }   = useParams();          // /courses/python → slug="python"
    const [params]   = useSearchParams();    // ?level=beginner
    const location   = useLocation();        // current location object

    const level      = params.get("level");

    return <h1>Course: {slug} | Level: {level}</h1>;
}
```

## Protected routes pattern

```jsx
// ProtectedRoute component
function ProtectedRoute({ children, requiredRole }) {
    const { user, loading } = useAuth();
    const location = useLocation();

    if (loading)  return <div className="spinner" />;
    if (!user)    return <Navigate to="/login" state={{ from: location }} replace />;
    if (requiredRole && user.role !== requiredRole) return <Navigate to="/403" replace />;

    return children;
}

// Usage
<Route path="/dashboard" element={
    <ProtectedRoute>
        <DashboardPage />
    </ProtectedRoute>
} />

<Route path="/admin" element={
    <ProtectedRoute requiredRole="admin">
        <AdminLayout />
    </ProtectedRoute>
} />
```

## Nested layouts with Outlet

```jsx
// AdminLayout.jsx
import { Outlet, NavLink } from "react-router-dom";

function AdminLayout() {
    return (
        <div className="admin-layout">
            <aside className="admin-sidebar">
                <NavLink to="/admin">Dashboard</NavLink>
                <NavLink to="/admin/courses">Courses</NavLink>
                <NavLink to="/admin/users">Users</NavLink>
            </aside>
            <main className="admin-main">
                <Outlet />  {/* child routes render here */}
            </main>
        </div>
    );
}
```
''',
     "Build a React SPA with React Router: home, courses list, course detail (with :slug param), login, and a protected dashboard. Include a 404 page and breadcrumb navigation.",
     "In React Router v6, which component renders the matched child route inside a parent layout?",
     "Build a full React SPA for CodeSavannah Academy: public pages (home, courses, about, contact), protected student dashboard, admin panel with nested routes, breadcrumbs, and scroll restoration on navigation.",
     "Use <Navigate replace> (not without replace) when redirecting from protected routes — 'replace' prevents the protected URL from appearing in browser history, so the back button works correctly.",
     55),
]

NODEJS_LESSONS = [
    (1, "Node.js Introduction — Runtime, Modules & npm",
     "Understand Node.js, write server-side JavaScript, and manage packages with npm.",
     '''## What is Node.js?

Node.js is a JavaScript runtime built on Chrome's V8 engine that lets you run JavaScript on the server. It uses an event-driven, non-blocking I/O model — perfect for APIs, real-time apps, and microservices.

**Key characteristics:**
- Single-threaded but highly concurrent via the event loop
- Non-blocking I/O — never waits, always processes
- npm — world's largest package registry (2 million+ packages)
- Same language on frontend and backend (full-stack JS)

## Setup

```bash
# Download from nodejs.org (LTS version)
node --version
npm --version

# Run a file
node app.js

# Interactive REPL
node

# npm project setup
npm init -y
```

## Core modules

```javascript
// Built-in modules — no install needed
const fs      = require("fs");       // file system
const path    = require("path");     // path utilities
const http    = require("http");     // HTTP server
const https   = require("https");    // HTTPS
const os      = require("os");       // operating system info
const crypto  = require("crypto");   // cryptography
const events  = require("events");   // EventEmitter
const stream  = require("stream");   // streams
const url     = require("url");      // URL parsing
const querystring = require("querystring");

// ES Modules (modern — use .mjs or "type":"module" in package.json)
import fs from "fs";
import path from "path";
```

## File system

```javascript
const fs   = require("fs");
const fsP  = require("fs/promises");  // promise-based (Node 14+)

// Synchronous (blocks — avoid in web servers)
const data = fs.readFileSync("students.json", "utf8");
fs.writeFileSync("output.txt", "Hello Node.js");

// Async with callbacks (old style)
fs.readFile("students.json", "utf8", (err, data) => {
    if (err) return console.error(err);
    console.log(JSON.parse(data));
});

// Promise-based (preferred)
async function processFile() {
    const data  = await fsP.readFile("students.json", "utf8");
    const json  = JSON.parse(data);
    json.updated = new Date().toISOString();
    await fsP.writeFile("output.json", JSON.stringify(json, null, 2));
}

// Path utilities (always use path, never string concatenation)
const dir      = path.join(__dirname, "data");
const file     = path.join(dir, "students.json");
const ext      = path.extname("app.js");          // ".js"
const basename = path.basename("/usr/bin/node");   // "node"
const dirname  = path.dirname("/home/grace/app.js"); // "/home/grace"

// OS info
console.log(os.platform());  // "linux" or "win32" or "darwin"
console.log(os.cpus().length);
console.log((os.totalmem() / 1024 / 1024 / 1024).toFixed(2) + " GB");
```

## npm — Node Package Manager

```bash
# Install package (adds to dependencies)
npm install express

# Install dev-only package
npm install --save-dev nodemon jest

# Global install (CLI tools)
npm install -g typescript ts-node

# Install exact version
npm install express@4.18.2

# Install all packages from package.json
npm install

# Update packages
npm update
npm outdated

# Remove a package
npm uninstall express

# Run scripts defined in package.json
npm start
npm test
npm run dev
npm run build
```

```json
{
    "name": "codesavannah-api",
    "version": "1.0.0",
    "description": "CodeSavannah Academy REST API",
    "main": "src/index.js",
    "type": "module",
    "scripts": {
        "start":    "node src/index.js",
        "dev":      "nodemon src/index.js",
        "test":     "jest",
        "build":    "tsc",
        "lint":     "eslint src/"
    },
    "dependencies": {
        "express": "^4.18.2",
        "mongoose": "^8.0.0",
        "jsonwebtoken": "^9.0.0",
        "bcryptjs": "^2.4.3"
    },
    "devDependencies": {
        "nodemon": "^3.0.0",
        "jest": "^29.0.0",
        "eslint": "^8.0.0"
    }
}
```

## CommonJS vs ES Modules

```javascript
// CommonJS (older — .js files in Node by default)
const express  = require("express");
const { Router } = require("express");
module.exports = { myFunction };
module.exports = MyClass;

// ES Modules (modern — add "type":"module" in package.json)
import express from "express";
import { Router } from "express";
export { myFunction };
export default MyClass;
```
''',
     "Write a Node.js script that reads a JSON file of students, filters those with GPA above 3.0, sorts by name, and writes the results to a new JSON file using fs/promises.",
     "What Node.js built-in module provides utilities for working with file and directory paths in a platform-independent way?",
     "Build a Node.js CLI tool: accepts a directory path as argument, recursively lists all .js/.ts files, counts lines of code in each, and prints a summary table sorted by line count.",
     "Always use path.join() and path.resolve() for file paths — never concatenate with '/' or '\\'. This ensures cross-platform compatibility between Windows and Unix systems.",
     45),

    (2, "Express.js — REST API Development",
     "Build production-quality REST APIs with Express.js, middleware, and error handling.",
     '''## Express.js Setup

```bash
npm install express cors helmet morgan dotenv express-validator
npm install --save-dev nodemon @types/express
```

## Application structure

```
src/
    index.js          — entry point, starts server
    app.js            — Express app (separate from server for testing)
    routes/
        courses.js
        users.js
        auth.js
    controllers/
        courseController.js
    middleware/
        auth.js
        errorHandler.js
        validate.js
    models/
        Course.js
    config/
        database.js
```

## Building the API

```javascript
// src/app.js
import express from "express";
import cors    from "cors";
import helmet  from "helmet";
import morgan  from "morgan";
import courseRoutes from "./routes/courses.js";
import userRoutes   from "./routes/users.js";
import { errorHandler, notFound } from "./middleware/errorHandler.js";

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({ origin: process.env.CLIENT_URL || "http://localhost:3000" }));

// Logging
app.use(morgan("dev"));

// Body parsing
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true }));

// Routes
app.use("/api/v1/courses", courseRoutes);
app.use("/api/v1/users",   userRoutes);

// Health check
app.get("/health", (req, res) => res.json({ status: "OK", uptime: process.uptime() }));

// 404 handler
app.use(notFound);

// Error handler — must be LAST and have 4 params
app.use(errorHandler);

export default app;
```

## Routes and controllers

```javascript
// routes/courses.js
import { Router } from "express";
import { body, param, query } from "express-validator";
import { authenticate, authorize } from "../middleware/auth.js";
import { validate } from "../middleware/validate.js";
import * as courseCtrl from "../controllers/courseController.js";

const router = Router();

router.get(  "/",     courseCtrl.getAllCourses);
router.get(  "/:id",  param("id").isInt(), validate, courseCtrl.getCourseById);
router.post( "/",     authenticate, authorize("admin"),
             [body("title").notEmpty().isLength({ min: 5, max: 200 }),
              body("price").isFloat({ min: 0 })],
             validate,
             courseCtrl.createCourse);
router.put(  "/:id",  authenticate, authorize("admin"), courseCtrl.updateCourse);
router.delete("/:id", authenticate, authorize("admin"), courseCtrl.deleteCourse);

export default router;
```

```javascript
// controllers/courseController.js
import Course from "../models/Course.js";
import { asyncHandler } from "../utils/asyncHandler.js";

export const getAllCourses = asyncHandler(async (req, res) => {
    const { level, search, page = 1, limit = 20 } = req.query;

    let query = { isPublished: true };
    if (level)  query.level  = level;
    if (search) query.title  = { $regex: search, $options: "i" };

    const skip    = (page - 1) * limit;
    const total   = await Course.countDocuments(query);
    const courses = await Course.find(query).skip(skip).limit(+limit).lean();

    res.json({
        success: true,
        data: courses,
        pagination: { total, page: +page, limit: +limit, pages: Math.ceil(total / limit) }
    });
});

export const getCourseById = asyncHandler(async (req, res) => {
    const course = await Course.findById(req.params.id);
    if (!course) return res.status(404).json({ success: false, error: "Course not found" });
    res.json({ success: true, data: course });
});

export const createCourse = asyncHandler(async (req, res) => {
    const course = await Course.create({ ...req.body, createdBy: req.user.id });
    res.status(201).json({ success: true, data: course });
});
```

## Middleware patterns

```javascript
// middleware/auth.js — JWT authentication
import jwt from "jsonwebtoken";

export const authenticate = (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (!authHeader?.startsWith("Bearer ")) {
        return res.status(401).json({ error: "No token provided" });
    }
    const token = authHeader.split(" ")[1];
    try {
        req.user = jwt.verify(token, process.env.JWT_SECRET);
        next();
    } catch {
        res.status(401).json({ error: "Invalid or expired token" });
    }
};

export const authorize = (...roles) => (req, res, next) => {
    if (!roles.includes(req.user.role)) {
        return res.status(403).json({ error: "Insufficient permissions" });
    }
    next();
};

// middleware/errorHandler.js
export const asyncHandler = (fn) => (req, res, next) =>
    Promise.resolve(fn(req, res, next)).catch(next);

export const errorHandler = (err, req, res, next) => {
    console.error(err.stack);
    const statusCode = err.statusCode || 500;
    res.status(statusCode).json({
        success: false,
        error: err.message || "Internal server error",
        ...(process.env.NODE_ENV === "development" && { stack: err.stack })
    });
};

export const notFound = (req, res) => {
    res.status(404).json({ success: false, error: `Route ${req.method} ${req.path} not found` });
};
```
''',
     "Build an Express REST API for a book library: CRUD endpoints for books, search by title/author, pagination, input validation with express-validator, and a JWT-protected admin route to add books.",
     "In Express.js, what is the purpose of the 'next' parameter in middleware functions?",
     "Build a complete Express.js REST API for CodeSavannah Academy: student registration, JWT auth, course CRUD (admin), enrolment endpoints, progress tracking, and comprehensive error handling. Test with Postman or REST Client.",
     "Always use an asyncHandler wrapper for async route handlers — without it, errors thrown inside async functions aren't caught by Express's error middleware and will crash the server.",
     60),
]

BOOTSTRAP_LESSONS = [
    (1, "Bootstrap 5 — Grid System, Components & Utilities",
     "Build responsive websites quickly using Bootstrap 5's grid, components, and utility classes.",
     '''## What is Bootstrap?

Bootstrap is the world's most popular CSS framework, providing pre-built responsive components, a powerful grid system, and utility classes that let you build professional interfaces rapidly.

**Bootstrap 5 key improvements over 4:**
- No jQuery dependency (pure vanilla JS)
- Improved grid system with xxl breakpoint
- New utility API — generate custom utilities
- Improved RTL (right-to-left) support
- CSS custom properties

## Setup

```html
<!-- CDN (quick start) -->
<link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
<script
    src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js">
</script>

<!-- npm install -->
npm install bootstrap @popperjs/core
```

## Grid system — 12 columns

```html
<div class="container">        <!-- max-width responsive container -->
<div class="container-fluid"> <!-- always 100% width -->
<div class="container-xl">    <!-- max-width xl and below -->

<!-- Row + columns -->
<div class="container">
    <div class="row">

        <!-- Equal width columns -->
        <div class="col">Column 1</div>
        <div class="col">Column 2</div>
        <div class="col">Column 3</div>

        <!-- Specific widths (total = 12) -->
        <div class="col-4">Sidebar (4/12 = 33%)</div>
        <div class="col-8">Main content (8/12 = 67%)</div>

        <!-- Responsive breakpoints:
             col-        = extra small < 576px
             col-sm-     = small >= 576px
             col-md-     = medium >= 768px
             col-lg-     = large >= 992px
             col-xl-     = extra large >= 1200px
             col-xxl-    = xxl >= 1400px -->

        <!-- Full on mobile, half on tablet, third on desktop -->
        <div class="col-12 col-md-6 col-lg-4">
            <div class="card">...</div>
        </div>

    </div>
</div>

<!-- Row options -->
<div class="row g-4">           <!-- gap: 1.5rem -->
<div class="row row-cols-3">    <!-- always 3 per row -->
<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3"> <!-- responsive -->
```

## Utility classes

```html
<!-- Spacing: m=margin, p=padding, t/b/s/e/x/y = top/bottom/start/end/x-axis/y-axis -->
<!-- Values: 0=0, 1=0.25rem, 2=0.5rem, 3=1rem, 4=1.5rem, 5=3rem -->
<div class="m-3">margin all sides 1rem</div>
<div class="mt-4 mb-2">margin-top 1.5rem, margin-bottom 0.5rem</div>
<div class="px-4 py-3">horizontal padding 1.5rem, vertical 1rem</div>
<div class="ms-auto">margin-start: auto — push right</div>

<!-- Text -->
<p class="text-center">Centred</p>
<p class="text-start text-md-center">Left on mobile, centred on md+</p>
<p class="fw-bold">Bold</p>
<p class="fw-light">Light</p>
<p class="fst-italic">Italic</p>
<p class="text-muted">Muted grey text</p>
<p class="text-primary">Primary blue</p>
<p class="fs-1">Font-size 1 (largest)</p>
<p class="fs-6">Font-size 6 (smallest)</p>
<p class="text-truncate">Very long text that gets truncated...</p>

<!-- Display -->
<div class="d-none d-md-block">Hidden on mobile, visible md+</div>
<div class="d-flex align-items-center justify-content-between">Flex container</div>
<div class="d-grid gap-2"><button>Full-width button</button></div>

<!-- Colors -->
<div class="bg-primary text-white">Primary background</div>
<div class="bg-success text-white">Success</div>
<div class="bg-danger text-white">Danger</div>
<div class="bg-warning text-dark">Warning</div>
<div class="bg-info text-dark">Info</div>
<div class="bg-light text-dark">Light</div>
<div class="bg-dark text-white">Dark</div>

<!-- Borders & rounded -->
<div class="border border-primary rounded-3 p-3">Rounded card</div>
<img class="rounded-circle" src="avatar.jpg">
<div class="border-bottom pb-2">Underlined heading</div>

<!-- Shadow -->
<div class="shadow-sm">Small shadow</div>
<div class="shadow">Default shadow</div>
<div class="shadow-lg">Large shadow</div>
```

## Core components

```html
<!-- Navbar -->
<nav class="navbar navbar-expand-lg bg-dark navbar-dark">
    <div class="container">
        <a class="navbar-brand fw-bold" href="/">CodeSavannah</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navMenu">
            <ul class="navbar-nav ms-auto gap-2">
                <li class="nav-item"><a class="nav-link active" href="/">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="/courses">Courses</a></li>
            </ul>
            <div class="d-flex gap-2 ms-3">
                <a href="/login"  class="btn btn-outline-light">Login</a>
                <a href="/signup" class="btn btn-primary">Sign Up</a>
            </div>
        </div>
    </div>
</nav>

<!-- Cards -->
<div class="card h-100 shadow-sm">
    <img src="course.jpg" class="card-img-top" alt="Course">
    <div class="card-body d-flex flex-column">
        <span class="badge bg-primary mb-2">Beginner</span>
        <h5 class="card-title">Python Programming</h5>
        <p class="card-text text-muted flex-grow-1">Learn Python from scratch.</p>
        <div class="d-flex justify-content-between align-items-center mt-3">
            <span class="fw-bold fs-5">KES 12,000</span>
            <a href="/enrol" class="btn btn-primary">Enrol Now</a>
        </div>
    </div>
</div>

<!-- Modal -->
<button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#enrollModal">
    Enrol Now
</button>
<div class="modal fade" id="enrollModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Confirm Enrolment</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">Are you sure you want to enrol?</div>
            <div class="modal-footer">
                <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button class="btn btn-primary">Confirm</button>
            </div>
        </div>
    </div>
</div>

<!-- Toast -->
<div class="toast-container position-fixed bottom-0 end-0 p-3">
    <div id="liveToast" class="toast" role="alert">
        <div class="toast-header bg-success text-white">
            <strong class="me-auto">Success</strong>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">Enrolled successfully!</div>
    </div>
</div>
<script>
    const toast = new bootstrap.Toast(document.getElementById("liveToast"));
    toast.show();
</script>
```
''',
     "Build a fully responsive Bootstrap 5 landing page for a tech bootcamp: sticky navbar with collapse, hero section, 3-column course cards grid, testimonials row, and footer. Mobile-first, no custom CSS except colour overrides.",
     "In Bootstrap 5, which class makes a div a flex container?",
     "Build a Bootstrap 5 admin dashboard: sidebar with offcanvas on mobile, top navbar with user dropdown, stats cards row, data table with sorting and pagination, and a modal form for adding records.",
     "Customise Bootstrap using CSS custom properties (--bs-primary, --bs-font-sans-serif, etc.) before importing Bootstrap CSS. This is cleaner than SASS compilation for small projects.",
     50),
]

TAILWIND_LESSONS = [
    (1, "TailwindCSS — Utility-First Design System",
     "Build custom designs rapidly using Tailwind's utility class approach.",
     '''## What is TailwindCSS?

TailwindCSS is a utility-first CSS framework — instead of pre-built components, it provides hundreds of low-level utility classes that you compose directly in HTML to build any design.

**Utility-first vs component-based:**
```html
<!-- Bootstrap (component-based) -->
<button class="btn btn-primary btn-lg">Submit</button>

<!-- Tailwind (utility-first) -->
<button class="bg-blue-600 hover:bg-blue-700 text-white font-semibold
               py-3 px-6 rounded-lg shadow-md transition-colors duration-200">
    Submit
</button>
```

**Why Tailwind?**
- No naming decisions — no BEM, no CSS naming conflicts
- Everything in HTML — no context switching
- Consistent design system out of the box
- Production builds strip unused classes — tiny CSS files

## Setup

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# tailwind.config.js
module.exports = {
    content: ["./src/**/*.{html,js,jsx,ts,tsx}"],
    theme: {
        extend: {
            colors: {
                brand: {
                    50:  "#eff6ff",
                    500: "#1341a8",
                    900: "#0a1f5c",
                },
            },
            fontFamily: {
                sans: ["Inter", "sans-serif"],
            },
        },
    },
    plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms")],
};
```

```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Core utility categories

```html
<!-- Layout -->
<div class="container mx-auto max-w-7xl px-4">
<div class="flex items-center justify-between gap-4">
<div class="grid grid-cols-3 gap-6">
<div class="hidden md:block">         <!-- responsive visibility -->

<!-- Spacing (t/r/b/l/x/y, values: 0=0, 1=4px, 2=8px, 4=16px, 8=32px) -->
<div class="m-4 p-6 mt-8 px-4 py-2">

<!-- Sizing -->
<div class="w-full max-w-md min-h-screen h-16 w-1/3">

<!-- Typography -->
<h1 class="text-4xl font-bold tracking-tight text-gray-900">
<p  class="text-base font-normal leading-relaxed text-gray-600">
<span class="text-sm font-medium uppercase tracking-widest">

<!-- Colors -->
<div class="bg-blue-600 text-white border border-blue-700">
<div class="bg-gradient-to-r from-blue-600 to-indigo-600">

<!-- Borders & rounded -->
<div class="border border-gray-200 rounded-xl shadow-lg">
<img class="rounded-full ring-4 ring-white">

<!-- Effects -->
<div class="shadow-sm hover:shadow-lg transition-shadow">
<div class="opacity-75 hover:opacity-100">
<div class="backdrop-blur-sm bg-white/80">
```

## Responsive design with Tailwind

```html
<!-- Mobile-first: no prefix = all sizes, sm: md: lg: xl: 2xl: = min-width breakpoints -->
<div class="
    grid
    grid-cols-1          sm:grid-cols-2          lg:grid-cols-3         xl:grid-cols-4
    gap-4                sm:gap-6                lg:gap-8
    text-base            md:text-lg
    p-4                  md:p-8                  lg:p-12
">
    <!-- Content -->
</div>

<!-- Breakpoints:
     sm:   640px+
     md:   768px+
     lg:   1024px+
     xl:   1280px+
     2xl:  1536px+  -->
```

## State variants

```html
<!-- Hover, focus, active, disabled -->
<button class="
    bg-blue-600
    hover:bg-blue-700
    active:bg-blue-800
    focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
    transition-colors duration-200
">Submit</button>

<!-- Group hover — parent controls child -->
<div class="group cursor-pointer">
    <img class="group-hover:scale-105 transition-transform duration-300">
    <div class="hidden group-hover:block">Overlay</div>
</div>

<!-- Dark mode -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
```

## @apply — extract component classes

```css
/* src/components.css — use sparingly */
@layer components {
    .btn-primary {
        @apply bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg
               hover:bg-blue-700 focus:ring-2 focus:ring-blue-500
               transition-colors duration-200 cursor-pointer;
    }

    .card {
        @apply bg-white rounded-xl shadow-md overflow-hidden
               border border-gray-100 hover:shadow-lg transition-shadow;
    }

    .badge {
        @apply inline-flex items-center px-2.5 py-0.5 rounded-full
               text-xs font-medium;
    }
}
```

## Building a course card

```html
<article class="bg-white rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300
                border border-gray-100 overflow-hidden group cursor-pointer">

    <div class="relative overflow-hidden">
        <img src="course.jpg" alt="Python course"
             class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300">
        <span class="absolute top-3 left-3 bg-blue-600 text-white text-xs
                     font-semibold px-2.5 py-1 rounded-full">
            Beginner
        </span>
    </div>

    <div class="p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-2 line-clamp-2">Python Programming</h3>
        <p class="text-sm text-gray-500 mb-4 line-clamp-3">
            Learn Python from scratch in 8 weeks.
        </p>
        <div class="flex items-center justify-between">
            <span class="text-2xl font-bold text-blue-600">KES 12,000</span>
            <button class="bg-blue-600 text-white text-sm font-medium px-4 py-2
                          rounded-lg hover:bg-blue-700 transition-colors">
                Enrol Now
            </button>
        </div>
    </div>
</article>
```
''',
     "Build a Tailwind CSS navbar: logo left, navigation links centred, login/signup buttons right. Add a mobile hamburger menu that toggles with JavaScript. Use hover and focus states throughout.",
     "In TailwindCSS, what prefix is used to apply styles only when the user hovers over an element?",
     "Build a complete Tailwind CSS landing page: hero with gradient background and animated text, course cards grid with hover effects, testimonials section, pricing table with highlighted plan, and responsive footer. Zero custom CSS.",
     "Add the Tailwind CSS IntelliSense extension in VS Code — it provides autocomplete, hover previews, and linting for all Tailwind classes, dramatically speeding up development.",
     55),
]


BATCH_3 = [
    ("react", "React", "web", "intermediate", "8 weeks",
     "React, JSX, Hooks, Context, React Router, Vite",
     "Build modern, component-based user interfaces with React.", REACT_LESSONS),

    ("nodejs", "Node.js", "web", "intermediate", "6 weeks",
     "Node.js, Express, REST APIs, JWT, Middleware, npm",
     "Build fast, scalable server-side applications with Node.js and Express.", NODEJS_LESSONS),

    ("bootstrap", "Bootstrap 5", "web", "beginner", "3 weeks",
     "Bootstrap 5, Grid, Components, Utilities, Responsive Design",
     "Build responsive, professional websites rapidly with Bootstrap 5.", BOOTSTRAP_LESSONS),

    ("tailwindcss", "TailwindCSS", "web", "beginner", "3 weeks",
     "TailwindCSS, Utility Classes, Responsive Design, Dark Mode, Animations",
     "Create custom, pixel-perfect designs with Tailwind's utility-first approach.", TAILWIND_LESSONS),
]


class Command(BaseCommand):
    help = "Generate curriculum batch 3: React, Node.js, Bootstrap, TailwindCSS"

    def handle(self, *args, **options):
        total_created = total_updated = 0

        for (slug, title, category, level, duration, skills, summary, lessons) in BATCH_3:
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
            f"\nBatch 3 done — {total_created} lessons created, {total_updated} updated."
        ))
