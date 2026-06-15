"""
Curriculum batch 4 — SQL/PostgreSQL, MongoDB, C, C++, C#, PHP, Go, Cybersecurity.
Run: python manage.py generate_curriculum_4
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


SQL_LESSONS = [
    (1, "SQL Fundamentals — SELECT, WHERE & Filtering",
     "Write SQL queries to retrieve, filter, and sort data from relational databases.",
     '''## What is SQL?

SQL (Structured Query Language) is the standard language for managing relational databases. Every developer needs SQL — it's used in PostgreSQL, MySQL, SQLite, Microsoft SQL Server, and Oracle.

**Core concepts:**
- **Database** — collection of related tables
- **Table** — rows (records) and columns (fields)
- **Primary key** — uniquely identifies each row
- **Foreign key** — links tables together
- **Null** — absence of a value (not zero, not empty string)

## Setting up

```sql
-- SQLite (built into Python, great for learning)
-- PostgreSQL setup:
CREATE DATABASE academy_db;
\\c academy_db   -- connect

-- Create tables
CREATE TABLE categories (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    slug        VARCHAR(100) NOT NULL UNIQUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    id          SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    title       VARCHAR(200) NOT NULL,
    slug        VARCHAR(200) NOT NULL UNIQUE,
    description TEXT,
    level       VARCHAR(20) CHECK (level IN ('beginner','intermediate','advanced')),
    price       NUMERIC(10,2) DEFAULT 0.00,
    is_published BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE students (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    email   VARCHAR(200) NOT NULL UNIQUE,
    grade   VARCHAR(20),
    gpa     NUMERIC(3,2) CHECK (gpa >= 0 AND gpa <= 4)
);

CREATE TABLE enrolments (
    id          SERIAL PRIMARY KEY,
    student_id  INTEGER REFERENCES students(id) ON DELETE CASCADE,
    course_id   INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    progress    SMALLINT DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    UNIQUE (student_id, course_id)
);
```

## SELECT — retrieve data

```sql
-- All columns, all rows
SELECT * FROM courses;

-- Specific columns
SELECT id, title, level, price FROM courses;

-- Column aliases
SELECT title AS course_name, price AS fee_kes FROM courses;

-- Expressions in SELECT
SELECT
    title,
    price,
    price * 0.10 AS discount,
    price - (price * 0.10) AS discounted_price
FROM courses;

-- Distinct values
SELECT DISTINCT level FROM courses;
SELECT COUNT(DISTINCT level) FROM courses;
```

## WHERE — filtering rows

```sql
-- Equality
SELECT * FROM courses WHERE level = 'beginner';

-- Comparison operators
SELECT * FROM courses WHERE price < 15000;
SELECT * FROM courses WHERE price >= 10000 AND price <= 20000;

-- BETWEEN (inclusive)
SELECT * FROM courses WHERE price BETWEEN 10000 AND 20000;

-- IN — match multiple values
SELECT * FROM courses WHERE level IN ('beginner', 'intermediate');

-- NOT IN
SELECT * FROM courses WHERE level NOT IN ('advanced');

-- NULL checks — never use = NULL!
SELECT * FROM courses WHERE description IS NULL;
SELECT * FROM courses WHERE description IS NOT NULL;

-- LIKE — pattern matching
SELECT * FROM courses WHERE title LIKE 'Python%';  -- starts with Python
SELECT * FROM courses WHERE title LIKE '%Programming%'; -- contains
SELECT * FROM courses WHERE title ILIKE '%python%';     -- case-insensitive (PostgreSQL)

-- Multiple conditions
SELECT * FROM courses
WHERE is_published = TRUE
  AND level = 'beginner'
  AND price <= 15000;

SELECT * FROM courses
WHERE level = 'advanced'
   OR price > 20000;

-- Combining AND and OR — use parentheses!
SELECT * FROM courses
WHERE is_published = TRUE
  AND (level = 'beginner' OR price < 12000);
```

## ORDER BY — sorting results

```sql
-- Ascending (default)
SELECT * FROM courses ORDER BY price;

-- Descending
SELECT * FROM courses ORDER BY price DESC;

-- Multiple columns
SELECT * FROM courses ORDER BY level ASC, price DESC;

-- Sort by alias
SELECT title, price * 1.10 AS price_with_vat
FROM courses
ORDER BY price_with_vat DESC;

-- NULLS FIRST/LAST (PostgreSQL)
SELECT * FROM courses ORDER BY description NULLS LAST;
```

## LIMIT and OFFSET — pagination

```sql
-- First 10 courses
SELECT * FROM courses LIMIT 10;

-- Page 2 (skip first 10, get next 10)
SELECT * FROM courses ORDER BY id LIMIT 10 OFFSET 10;

-- Page formula: OFFSET = (page - 1) * page_size
-- Page 3, 20 per page: OFFSET = (3-1) * 20 = 40
SELECT * FROM courses ORDER BY created_at DESC LIMIT 20 OFFSET 40;
```
''',
     "Write SQL queries to: (1) find all courses under KES 15000, (2) find courses containing 'web' in the title (case-insensitive), (3) list courses ordered by price descending, (4) get page 3 of courses with 5 per page.",
     "Which SQL keyword is used to filter rows based on conditions in a SELECT statement?",
     "Build a SQL-based student analytics report: find top 10 students by GPA, courses with most enrolments, students enrolled in 3+ courses, average GPA per grade level, and pass/fail rates.",
     "Always use IS NULL and IS NOT NULL to check for NULL values — comparing with = NULL always returns NULL (not TRUE or FALSE), so your WHERE clause silently matches nothing.",
     45),

    (2, "SQL Joins, Aggregation & Subqueries",
     "Combine tables with JOINs, summarise data with GROUP BY, and write subqueries.",
     '''## SQL JOINs — combining tables

```sql
-- INNER JOIN — only rows that match in BOTH tables
SELECT
    c.title,
    cat.name AS category,
    c.price
FROM courses c
INNER JOIN categories cat ON c.category_id = cat.id;

-- LEFT JOIN — all rows from left table, matching from right (NULLs for no match)
SELECT
    s.name AS student,
    COUNT(e.id) AS enrolment_count
FROM students s
LEFT JOIN enrolments e ON s.id = e.student_id
GROUP BY s.id, s.name
ORDER BY enrolment_count DESC;

-- RIGHT JOIN — all from right, matching from left (rare — prefer LEFT JOIN)
-- FULL OUTER JOIN — all rows from both sides

-- Multiple JOINs
SELECT
    s.name,
    c.title AS course,
    e.progress,
    e.enrolled_at
FROM enrolments e
JOIN students s ON e.student_id = s.id
JOIN courses  c ON e.course_id  = c.id
WHERE e.progress < 50
ORDER BY e.enrolled_at DESC;

-- Self JOIN — table joined to itself
SELECT
    a.name AS student,
    b.name AS same_gpa_peer
FROM students a
JOIN students b ON a.gpa = b.gpa AND a.id != b.id
ORDER BY a.gpa DESC;
```

## Aggregate functions

```sql
-- COUNT
SELECT COUNT(*) AS total_courses FROM courses;
SELECT COUNT(*) AS published FROM courses WHERE is_published = TRUE;

-- SUM, AVG, MIN, MAX
SELECT
    SUM(price)  AS total_revenue_potential,
    AVG(price)  AS average_price,
    MIN(price)  AS cheapest,
    MAX(price)  AS most_expensive
FROM courses;

-- GROUP BY — aggregate per group
SELECT
    level,
    COUNT(*)    AS course_count,
    AVG(price)  AS avg_price,
    MIN(price)  AS min_price
FROM courses
GROUP BY level
ORDER BY avg_price DESC;

-- HAVING — filter on aggregate (WHERE cannot use aggregates)
SELECT
    student_id,
    COUNT(*) AS enrolment_count,
    AVG(progress) AS avg_progress
FROM enrolments
GROUP BY student_id
HAVING COUNT(*) >= 3                -- students with 3+ enrolments
ORDER BY avg_progress DESC;

-- GROUP BY with JOIN
SELECT
    cat.name AS category,
    COUNT(c.id) AS course_count,
    AVG(c.price) AS avg_price
FROM categories cat
LEFT JOIN courses c ON c.category_id = cat.id
GROUP BY cat.id, cat.name
HAVING COUNT(c.id) > 0
ORDER BY course_count DESC;
```

## Subqueries

```sql
-- Scalar subquery — returns single value
SELECT *
FROM courses
WHERE price > (SELECT AVG(price) FROM courses);

-- IN subquery — filter using a set
SELECT *
FROM students
WHERE id IN (
    SELECT DISTINCT student_id
    FROM enrolments
    WHERE progress = 100
);

-- Correlated subquery — references outer query
SELECT
    s.name,
    s.gpa,
    (SELECT COUNT(*)
     FROM enrolments e
     WHERE e.student_id = s.id) AS enrolment_count
FROM students s;

-- EXISTS — check if rows exist
SELECT *
FROM courses c
WHERE EXISTS (
    SELECT 1
    FROM enrolments e
    WHERE e.course_id = c.id
    AND e.progress > 80
);

-- CTE (Common Table Expression) — much cleaner than subqueries
WITH TopStudents AS (
    SELECT student_id, AVG(progress) AS avg_progress
    FROM enrolments
    GROUP BY student_id
    HAVING AVG(progress) >= 80
),
StudentCourseCount AS (
    SELECT student_id, COUNT(*) AS count
    FROM enrolments
    GROUP BY student_id
)
SELECT
    s.name,
    ts.avg_progress,
    scc.count AS courses_enrolled
FROM students s
JOIN TopStudents       ts  ON ts.student_id  = s.id
JOIN StudentCourseCount scc ON scc.student_id = s.id
ORDER BY ts.avg_progress DESC;
```

## Window functions (PostgreSQL)

```sql
-- ROW_NUMBER, RANK, DENSE_RANK
SELECT
    name,
    gpa,
    ROW_NUMBER() OVER (ORDER BY gpa DESC) AS row_num,
    RANK()       OVER (ORDER BY gpa DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY gpa DESC) AS dense_rank
FROM students;

-- Running totals
SELECT
    enrolled_at::date AS day,
    COUNT(*) AS daily_enrolments,
    SUM(COUNT(*)) OVER (ORDER BY enrolled_at::date) AS running_total
FROM enrolments
GROUP BY enrolled_at::date
ORDER BY day;

-- Lead/Lag — access adjacent row values
SELECT
    title,
    price,
    LAG(price,  1) OVER (ORDER BY price) AS prev_price,
    LEAD(price, 1) OVER (ORDER BY price) AS next_price
FROM courses
ORDER BY price;
```
''',
     "Given the academy database (students, courses, enrolments, categories): write queries for (1) courses with their category name and enrolment count, (2) top 5 most popular courses by enrolment, (3) students above the average GPA using a subquery.",
     "Which SQL clause filters groups after aggregation, where WHERE cannot be used?",
     "Write a complete database analytics report using SQL: course revenue breakdown by category, student retention (enrolled vs completed), top performing students with CTEs, and a monthly enrolment trend using window functions.",
     "CTEs (WITH clause) make complex queries readable and maintainable. Instead of nested subqueries, name each step and reference it by name — your future self will thank you.",
     55),

    (3, "PostgreSQL Advanced — Indexes, Transactions & Performance",
     "Optimise PostgreSQL databases with indexes, transactions, and query planning.",
     '''## Indexes — speeding up queries

```sql
-- Without an index, PostgreSQL does a full table scan (seq scan)
-- For large tables, this is O(n) — very slow

-- B-tree index (default — best for equality and range queries)
CREATE INDEX idx_courses_level   ON courses(level);
CREATE INDEX idx_courses_slug    ON courses(slug);
CREATE INDEX idx_enrolments_student ON enrolments(student_id);
CREATE INDEX idx_enrolments_course  ON enrolments(course_id);

-- Composite index — for queries filtering on multiple columns
CREATE INDEX idx_courses_published_level ON courses(is_published, level);
-- Efficient for: WHERE is_published = TRUE AND level = 'beginner'

-- Unique index (also enforces uniqueness)
CREATE UNIQUE INDEX idx_enrolments_unique ON enrolments(student_id, course_id);

-- Partial index — only index rows matching a condition
CREATE INDEX idx_courses_published ON courses(created_at)
WHERE is_published = TRUE;
-- Smaller index — only published courses are indexed

-- GIN index — for JSONB, arrays, full-text search
ALTER TABLE courses ADD COLUMN tags JSONB DEFAULT '[]';
CREATE INDEX idx_courses_tags ON courses USING GIN(tags);
SELECT * FROM courses WHERE tags @> '["python", "beginner"]'::jsonb;

-- Full-text search index
ALTER TABLE courses ADD COLUMN search_vector TSVECTOR;
CREATE INDEX idx_courses_fts ON courses USING GIN(search_vector);
UPDATE courses SET search_vector = to_tsvector('english', title || ' ' || COALESCE(description, ''));
SELECT * FROM courses WHERE search_vector @@ plainto_tsquery('python programming');

-- Analyse a query — check if index is being used
EXPLAIN ANALYSE SELECT * FROM courses WHERE slug = 'python-programming';
-- Look for: Index Scan vs Seq Scan
-- Cost: (startup..total) — lower is better
-- Actual rows: how many rows returned

-- List all indexes
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'courses';

-- Drop an index
DROP INDEX CONCURRENTLY idx_courses_level;  -- CONCURRENTLY = no locking
```

## Transactions — ACID guarantees

```sql
-- ACID: Atomicity, Consistency, Isolation, Durability

-- Basic transaction
BEGIN;
    UPDATE students SET gpa = 4.0 WHERE id = 1;
    INSERT INTO enrolments (student_id, course_id) VALUES (1, 5);
    -- If ANY statement fails, ROLLBACK undoes everything
COMMIT;     -- makes changes permanent
-- OR
ROLLBACK;   -- undo all changes

-- SAVEPOINT — partial rollback
BEGIN;
    INSERT INTO students (name, email, gpa) VALUES ('Test', 'test@example.com', 3.5);
    SAVEPOINT sp1;

    -- This might fail
    INSERT INTO enrolments (student_id, course_id) VALUES (LASTVAL(), 99);
    -- On failure:
    ROLLBACK TO SAVEPOINT sp1;  -- undo only back to sp1

    -- Continue with something else
    INSERT INTO enrolments (student_id, course_id) VALUES (LASTVAL(), 1);
COMMIT;

-- Isolation levels
BEGIN ISOLATION LEVEL SERIALIZABLE;  -- strictest — no phantom reads
BEGIN ISOLATION LEVEL READ COMMITTED; -- default — sees committed data only
```

## Views, Stored Procedures & Triggers

```sql
-- View — stored query, acts like a table
CREATE VIEW course_stats AS
SELECT
    c.id,
    c.title,
    c.level,
    c.price,
    cat.name AS category,
    COUNT(e.id) AS enrolment_count,
    AVG(e.progress) AS avg_progress
FROM courses c
LEFT JOIN categories cat  ON c.category_id = cat.id
LEFT JOIN enrolments  e   ON c.id = e.course_id
WHERE c.is_published = TRUE
GROUP BY c.id, cat.name;

SELECT * FROM course_stats WHERE enrolment_count > 10;

-- Materialised view — physically stored, must refresh manually
CREATE MATERIALIZED VIEW course_stats_mat AS
SELECT ... FROM ...;
REFRESH MATERIALIZED VIEW CONCURRENTLY course_stats_mat;

-- Stored function (PL/pgSQL)
CREATE OR REPLACE FUNCTION enrol_student(p_student_id INT, p_course_id INT)
RETURNS BOOLEAN AS $$
BEGIN
    INSERT INTO enrolments(student_id, course_id)
    VALUES (p_student_id, p_course_id)
    ON CONFLICT (student_id, course_id) DO NOTHING;

    RETURN FOUND;  -- TRUE if insert happened
EXCEPTION
    WHEN foreign_key_violation THEN
        RAISE EXCEPTION 'Student or course not found';
END;
$$ LANGUAGE plpgsql;

SELECT enrol_student(1, 3);

-- Trigger — runs automatically on INSERT/UPDATE/DELETE
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER courses_updated
    BEFORE UPDATE ON courses
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();
```
''',
     "Add appropriate indexes to the academy database for the most common queries (list published courses, search by slug, filter enrolments by student/course). Use EXPLAIN ANALYSE before and after to show the performance improvement.",
     "What PostgreSQL feature stores a query result physically and requires manual refreshing for updates?",
     "Design and implement a complete PostgreSQL schema for an e-learning platform: tables for users, courses, modules, lessons, enrolments, progress, payments. Include indexes, constraints, views, and a stored procedure for the enrolment flow.",
     "Run EXPLAIN ANALYSE on slow queries before adding indexes. Adding an index that PostgreSQL doesn't use wastes space and slows down writes. The query planner knows best — read its output.",
     60),
]

MONGODB_LESSONS = [
    (1, "MongoDB — Documents, Collections & CRUD",
     "Store and query data in MongoDB's flexible document model.",
     '''## What is MongoDB?

MongoDB is a NoSQL document database that stores data in flexible JSON-like documents instead of rigid rows and tables. Ideal for hierarchical data, rapidly changing schemas, and horizontal scaling.

**When to use MongoDB vs SQL:**
| MongoDB | PostgreSQL |
|---------|-----------|
| Flexible/changing schema | Fixed, well-defined schema |
| Document data (nested objects) | Relational data (many tables) |
| High write throughput | Complex transactions |
| Horizontal scaling | Strong ACID guarantees |

## Setup

```bash
# Install MongoDB
# Download from mongodb.com/try/download/community
# OR: brew install mongodb-community (macOS)

# Start MongoDB
mongod --dbpath ./data

# MongoDB Shell
mongosh

# Node.js driver
npm install mongodb mongoose
```

## Mongoose — MongoDB with Node.js

```javascript
// models/Course.js
import mongoose from "mongoose";

const courseSchema = new mongoose.Schema({
    title:       { type: String, required: true, trim: true, maxlength: 200 },
    slug:        { type: String, required: true, unique: true, lowercase: true },
    description: { type: String, required: true },
    level:       { type: String, enum: ["beginner", "intermediate", "advanced"], default: "beginner" },
    price:       { type: Number, min: 0, default: 0 },
    tags:        [String],
    category: {
        type: mongoose.Schema.Types.ObjectId,
        ref:  "Category",
    },
    instructor: {
        name:   String,
        email:  String,
        avatar: String,
    },
    isPublished: { type: Boolean, default: false },
    createdAt:   { type: Date, default: Date.now },
    updatedAt:   { type: Date, default: Date.now },
});

// Index
courseSchema.index({ slug: 1 }, { unique: true });
courseSchema.index({ title: "text", description: "text" }); // full-text search

// Virtual field
courseSchema.virtual("priceUSD").get(function () {
    return (this.price / 140).toFixed(2);  // approximate KES to USD
});

// Pre-save hook
courseSchema.pre("save", function (next) {
    this.updatedAt = new Date();
    next();
});

export default mongoose.model("Course", courseSchema);
```

## CRUD operations

```javascript
import Course from "./models/Course.js";
import mongoose from "mongoose";

// Connect
await mongoose.connect("mongodb://localhost:27017/academy");

// CREATE
const course = await Course.create({
    title:       "Python Programming",
    slug:        "python-programming",
    description: "Learn Python from scratch in 8 weeks.",
    level:       "beginner",
    price:       12000,
    tags:        ["python", "programming", "beginner"],
});

// Bulk insert
await Course.insertMany([course1, course2, course3]);

// READ
const all        = await Course.find();
const beginners  = await Course.find({ level: "beginner" });
const cheap      = await Course.find({ price: { $lt: 15000 } });
const course     = await Course.findById(id);
const bySlug     = await Course.findOne({ slug: "python-programming" });

// Query operators
await Course.find({
    level:  { $in: ["beginner", "intermediate"] },
    price:  { $gte: 5000, $lte: 20000 },
    tags:   { $all: ["python"] },
    title:  { $regex: /python/i },
});

// Select specific fields (projection)
await Course.find({ isPublished: true }, "title level price -_id");

// Sort, skip, limit — for pagination
const page = 2, limit = 10;
await Course.find({ isPublished: true })
    .sort({ createdAt: -1 })
    .skip((page - 1) * limit)
    .limit(limit)
    .lean();   // returns plain JS objects (faster, no Mongoose overhead)

// Populate — resolve ObjectId references
await Course.find()
    .populate("category", "name slug")
    .lean();

// UPDATE
await Course.findByIdAndUpdate(id, { price: 13000 }, { new: true });  // new: return updated
await Course.updateMany({ level: "beginner" }, { $set: { isPublished: true } });
await Course.findOneAndUpdate(
    { slug: "python" },
    { $inc: { viewCount: 1 }, $push: { tags: "updated" } }
);

// DELETE
await Course.findByIdAndDelete(id);
await Course.deleteMany({ isPublished: false, createdAt: { $lt: new Date("2023-01-01") } });
```

## Aggregation Pipeline

```javascript
// MongoDB's version of GROUP BY, JOINs, and subqueries
const stats = await Course.aggregate([
    // Stage 1: Filter
    { $match: { isPublished: true } },

    // Stage 2: Group and count
    { $group: {
        _id:           "$level",
        count:         { $sum: 1 },
        avgPrice:      { $avg: "$price" },
        maxPrice:      { $max: "$price" },
        allTitles:     { $push: "$title" },
    }},

    // Stage 3: Sort
    { $sort: { count: -1 } },

    // Stage 4: Reshape output
    { $project: {
        level:    "$_id",
        count:    1,
        avgPrice: { $round: ["$avgPrice", 2] },
        maxPrice: 1,
        _id:      0,
    }},
]);

// $lookup — JOIN equivalent
const coursesWithEnrolments = await Course.aggregate([
    { $lookup: {
        from:         "enrolments",
        localField:   "_id",
        foreignField: "courseId",
        as:           "enrolments",
    }},
    { $addFields: { enrolmentCount: { $size: "$enrolments" } } },
    { $sort: { enrolmentCount: -1 } },
    { $limit: 10 },
]);

// Full-text search
const results = await Course.find(
    { $text: { $search: "python django web" } },
    { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } });
```
''',
     "Using Mongoose, build a Student model with name, email, gpa, grade, and enrolled courses (array of ObjectIds). Write CRUD operations: create, find by email, update GPA, delete, and an aggregation to find average GPA by grade.",
     "Which MongoDB query operator checks if a field's value is within a given array of values?",
     "Build a MongoDB-backed REST API with Express and Mongoose: Course model with full-text search index, Enrolment model with population, aggregation endpoints for analytics, and proper error handling.",
     "Use .lean() when you only need to READ data and don't need Mongoose document methods. Lean queries are up to 10x faster because they skip the hydration step and return plain JavaScript objects.",
     55),
]

C_LESSONS = [
    (1, "C Programming — Syntax, Pointers & Memory",
     "Write C programs, understand memory management, and master pointers.",
     '''## What is C?

C is a general-purpose, low-level programming language created by Dennis Ritchie at Bell Labs (1972). It is the language that built UNIX, the Linux kernel, Python interpreter, and most operating systems. Understanding C builds deep insight into how computers work.

## Setup

```bash
# Install GCC (GNU Compiler Collection)
# Linux:   sudo apt install gcc
# macOS:   xcode-select --install
# Windows: install MinGW or use WSL

# Compile and run
gcc hello.c -o hello
./hello

# Compile with warnings (always do this)
gcc -Wall -Wextra -o hello hello.c
```

## First C program

```c
#include <stdio.h>      /* Standard Input/Output */
#include <stdlib.h>     /* malloc, free, exit */
#include <string.h>     /* string functions */

int main(int argc, char *argv[]) {
    printf("Hello, CodeSavannah!\\n");
    printf("Arguments: %d\\n", argc);

    int score = 95;
    double gpa = 3.9;
    char name[] = "Grace";
    char initial = 'G';

    printf("Name: %s, Score: %d, GPA: %.2f, Initial: %c\\n",
           name, score, gpa, initial);

    return 0;   /* exit code 0 = success */
}
```

## Data types

```c
/* Integer types */
char        c  = 'A';          /* 1 byte:  -128 to 127 */
short       s  = 32767;        /* 2 bytes */
int         i  = 2147483647;   /* 4 bytes (most common) */
long        l  = 2147483647L;  /* 8 bytes on 64-bit */
long long   ll = 9223372036854775807LL;

/* Unsigned (no negatives, double the positive range) */
unsigned int  ui = 4294967295U;
unsigned char uc = 255;

/* Floating point */
float   f = 3.14f;    /* 4 bytes, ~7 decimal digits */
double  d = 3.14159265358979; /* 8 bytes, ~15 decimal digits */

/* sizeof operator */
printf("int:    %zu bytes\\n", sizeof(int));
printf("double: %zu bytes\\n", sizeof(double));
printf("char*:  %zu bytes\\n", sizeof(char*));
```

## Pointers — the heart of C

```c
/* A pointer stores a MEMORY ADDRESS */
int  value   = 42;
int *pointer = &value;  /* & = address-of operator */

printf("Value:   %d\\n",  value);      /* 42 */
printf("Address: %p\\n",  pointer);    /* 0x7ffee... (some address) */
printf("Via ptr: %d\\n", *pointer);    /* 42 — * = dereference */

/* Modifying via pointer */
*pointer = 100;
printf("value is now: %d\\n", value);  /* 100 */

/* Pointer arithmetic */
int arr[] = {10, 20, 30, 40, 50};
int *p = arr;   /* p points to arr[0] */

printf("%d\\n", *p);        /* 10 */
printf("%d\\n", *(p + 1));  /* 20 */
printf("%d\\n", *(p + 4));  /* 50 */

p++;    /* advance to next element */
printf("%d\\n", *p);  /* 20 */

/* Array and pointer equivalence */
/* arr[i] is exactly equivalent to *(arr + i) */
for (int i = 0; i < 5; i++) {
    printf("%d ", *(arr + i));
}
```

## Dynamic memory allocation

```c
#include <stdlib.h>

/* malloc — allocate raw bytes (uninitialized) */
int *arr = (int *)malloc(10 * sizeof(int));
if (arr == NULL) {
    fprintf(stderr, "Memory allocation failed\\n");
    exit(EXIT_FAILURE);
}

/* Initialize */
for (int i = 0; i < 10; i++) {
    arr[i] = i * i;
}

/* calloc — allocate and zero-initialize */
int *zeros = (int *)calloc(10, sizeof(int));

/* realloc — resize allocation */
int new_size = 20;
int *larger  = (int *)realloc(arr, new_size * sizeof(int));
if (larger == NULL) {
    free(arr);  /* free original on failure */
    exit(EXIT_FAILURE);
}
arr = larger;

/* MUST free every malloc/calloc/realloc */
free(arr);
free(zeros);
arr = NULL;   /* good practice — prevents dangling pointer */
```

## Structs — custom data types

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    int    id;
    char   name[100];
    char   grade[20];
    double gpa;
} Student;

Student grace;
grace.id  = 1;
strcpy(grace.name,  "Grace Adhiambo");
strcpy(grace.grade, "Form 3");
grace.gpa = 3.9;

printf("Student: %s, GPA: %.2f\\n", grace.name, grace.gpa);

/* Pointer to struct */
Student *ptr = &grace;
printf("Name via ptr: %s\\n", ptr->name);  /* -> instead of . for pointers */

/* Array of structs */
Student students[100];
int count = 0;

void add_student(Student *arr, int *count, const char *name, const char *grade, double gpa) {
    arr[*count].id = *count + 1;
    strncpy(arr[*count].name,  name,  99);
    strncpy(arr[*count].grade, grade, 19);
    arr[*count].gpa = gpa;
    (*count)++;
}
```
''',
     "Write a C program that dynamically allocates an array of Student structs, fills it from user input, sorts by GPA (bubble sort), and prints the sorted list. Free all allocated memory.",
     "In C, what operator is used to access a struct member through a pointer?",
     "Build a C program: a dynamic linked list of Student nodes (name, GPA, next pointer), with functions for insert, delete, search, print all, and find the student with highest GPA. No memory leaks.",
     "Always check the return value of malloc/calloc/realloc for NULL before using the pointer. On systems under memory pressure, allocation can fail and dereferencing NULL causes a segmentation fault.",
     60),
]

CYBERSECURITY_LESSONS = [
    (1, "Cybersecurity Fundamentals — CIA Triad & Threat Landscape",
     "Understand core security concepts, common threats, and the mindset of a security professional.",
     '''## What is Cybersecurity?

Cybersecurity is the practice of protecting computer systems, networks, and data from digital attacks, unauthorised access, damage, and theft.

**Why it matters:**
- Cybercrime costs the global economy ~$8 trillion per year (2023)
- Average cost of a data breach: $4.45 million
- Average time to detect a breach: 207 days
- Every developer writes code that will be attacked — you MUST think like an attacker

## The CIA Triad

The three fundamental goals of information security:

```
         ┌─────────────────────┐
         │   CONFIDENTIALITY   │
         │ Data visible only   │
         │ to authorised users │
         └──────────┬──────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
┌────────┴────────┐  ┌────────┴────────┐
│   INTEGRITY     │  │  AVAILABILITY   │
│ Data accurate   │  │ Systems up and  │
│ and unmodified  │  │ accessible      │
└─────────────────┘  └─────────────────┘
```

**Confidentiality** — ensuring data is only accessible to those with permission
- Encryption (AES, RSA, TLS)
- Access controls (RBAC, ABAC)
- Multi-factor authentication

**Integrity** — ensuring data hasn't been tampered with
- Hash functions (SHA-256, SHA-3)
- Digital signatures
- Message authentication codes (HMAC)

**Availability** — ensuring systems are accessible when needed
- Redundancy and failover
- DDoS mitigation
- Backup and disaster recovery

## Threat landscape

**Types of attackers:**
- **Script kiddies** — use pre-made tools, low skill
- **Hacktivists** — politically motivated
- **Cybercriminals** — financially motivated (most common)
- **Nation-state actors** — government-sponsored, highly sophisticated
- **Insider threats** — current/former employees

**Common attack types:**

```
Attack                Description
──────────────────────────────────────────────────────
Phishing              Deceptive emails to steal credentials
SQL Injection         Injecting SQL into vulnerable forms
XSS                   Injecting JavaScript into web pages
CSRF                  Forging requests from authenticated users
Man-in-the-Middle     Intercepting network traffic
Brute Force           Trying all password combinations
Ransomware            Encrypting data and demanding payment
Social Engineering    Manipulating humans (not technology)
Zero-Day             Exploiting unknown vulnerabilities
Supply Chain          Compromising software dependencies
```

## OWASP Top 10 (2021)

The most critical web application security risks:

1. **Broken Access Control** — users doing what they shouldn't
2. **Cryptographic Failures** — weak/missing encryption
3. **Injection** — SQL, NoSQL, OS, LDAP injection
4. **Insecure Design** — security not designed in from the start
5. **Security Misconfiguration** — default passwords, open ports
6. **Vulnerable Components** — outdated libraries with known CVEs
7. **Authentication Failures** — weak passwords, no MFA
8. **Software Integrity Failures** — unsigned packages/updates
9. **Logging/Monitoring Failures** — not detecting attacks
10. **Server-Side Request Forgery** — server fetches attacker-controlled URLs

## Security mindset — think like an attacker

```
Attack Surface Analysis:
1. Enumerate all input points (forms, APIs, file uploads, URL params)
2. Identify trust boundaries (what data comes from users vs system)
3. Find authentication and authorisation checks (are they there? are they correct?)
4. Look for error handling (does it leak stack traces or internal paths?)
5. Check for sensitive data exposure (logs, responses, error messages)

Questions to ask about any feature:
- What happens if the user sends unexpected data?
- What if the user is unauthenticated?
- What if the user has a different role?
- What if the user sends very large data?
- What if the request is replayed?
- What if two requests happen simultaneously?
```

## Cryptography fundamentals

```python
# Hashing — one-way transformation
import hashlib
import secrets

# SHA-256 hash
msg  = "Hello, CodeSavannah!"
hash = hashlib.sha256(msg.encode()).hexdigest()
print(hash)  # 256-bit hex string

# Password hashing — NEVER use plain SHA-256 for passwords!
# Use bcrypt, scrypt, or Argon2 (all add salt and iterations)
import bcrypt

password = b"SuperSecret123!"
hashed   = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
print(bcrypt.checkpw(password, hashed))  # True

# Secure random — for tokens, nonces, salts
token = secrets.token_urlsafe(32)   # 256-bit URL-safe token
nonce = secrets.token_bytes(16)     # 128-bit random bytes
pin   = secrets.randbelow(1000000)  # random 6-digit PIN
```
''',
     "Analyse a login form (HTML + Python Django view) for OWASP Top 10 vulnerabilities. List every vulnerability found, explain the impact, and write the fixed, secure version of the code.",
     "In the CIA Triad, which property ensures that data has not been tampered with or altered?",
     "Perform a security audit of a fictional web application: map the attack surface, test for SQL injection, XSS, CSRF, and broken access control. Write a security report with findings and remediation steps.",
     "Never roll your own cryptography. Use established, peer-reviewed libraries (bcrypt, libsodium, Python's secrets module). Even experts get crypto wrong — the math is subtle and implementation errors are catastrophic.",
     55),

    (2, "Web Application Security — Injection, XSS & CSRF",
     "Identify and fix the most exploited web vulnerabilities in real code.",
     '''## SQL Injection — the classic attack

SQL injection occurs when user input is concatenated into SQL queries without sanitisation.

```python
# VULNERABLE — never do this
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    # Attacker sends: ' OR '1'='1
    # Query becomes: SELECT * FROM users WHERE username = '' OR '1'='1'
    # Returns ALL users!

# Attacker sends: '; DROP TABLE users; --
# Query: SELECT * FROM users WHERE username = ''; DROP TABLE users; --

# SECURE — always use parameterised queries
def get_user_safe(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    # Django ORM is safe by default:
    User.objects.filter(username=username)

# Django raw SQL (when needed) — use params
User.objects.raw("SELECT * FROM users WHERE username = %s", [username])
```

## XSS — Cross-Site Scripting

XSS lets attackers inject JavaScript into pages viewed by other users.

```python
# VULNERABLE — user input directly in HTML
@app.route("/greet")
def greet():
    name = request.args.get("name")
    return f"<h1>Hello, {name}!</h1>"
    # Attacker visits: /greet?name=<script>document.cookie</script>
    # Script runs in victim's browser — steals session cookie

# SECURE — escape user input
from markupsafe import escape  # Flask
def greet_safe():
    name = request.args.get("name", "")
    return f"<h1>Hello, {escape(name)}!</h1>"

# Django auto-escapes template variables
# {{ user_input }}    — safe (escaped)
# {{ user_input|safe }} — DANGEROUS (skips escaping)

# Content Security Policy header — defence in depth
response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data:;"
)
```

## CSRF — Cross-Site Request Forgery

CSRF tricks authenticated users into making unintended requests.

```html
<!-- Attacker's page -->
<img src="https://yourbank.com/transfer?to=attacker&amount=10000">
<!-- Browser sends the victim's cookies — transfer happens! -->

<!-- ATTACK: Victim visits attacker.com while logged into yourbank.com
     Their browser automatically sends auth cookies to yourbank.com -->
```

```python
# Django: CSRF protection is ON by default
# {% csrf_token %} in every POST form — generates a unique token
# Django middleware validates the token on every state-changing request

# Flask: use Flask-WTF which adds CSRF tokens
from flask_wtf import FlaskForm
# Render with: {{ form.csrf_token }}

# For AJAX requests — include token in headers
# fetch('/api/action/', {
#     method: 'POST',
#     headers: { 'X-CSRFToken': getCookie('csrftoken') },
# })
```

## Authentication security

```python
# Password storage — use Django's built-in (PBKDF2+SHA256)
# NEVER store: plaintext, MD5, SHA1, unsalted SHA256

# Secure session management
SESSION_COOKIE_HTTPONLY = True  # JS can't access session cookie
SESSION_COOKIE_SAMESITE = "Lax"  # CSRF mitigation
SESSION_COOKIE_SECURE   = True   # HTTPS only (production)

# Rate limiting with django-ratelimit
from django_ratelimit.decorators import ratelimit

@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def login_view(request):
    pass

# Password validation (Django settings)
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
```

## HTTP Security Headers

```python
# Django: use django-csp and SecurityMiddleware

SECURE_HSTS_SECONDS           = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD           = True
SECURE_SSL_REDIRECT           = True   # redirect HTTP → HTTPS
SECURE_BROWSER_XSS_FILTER     = True
X_FRAME_OPTIONS               = "DENY"  # prevent clickjacking
SECURE_CONTENT_TYPE_NOSNIFF   = True

# What each header does:
# Strict-Transport-Security: browser only uses HTTPS
# X-Frame-Options: DENY prevents page being embedded in iframe (clickjacking)
# X-Content-Type-Options: browser respects Content-Type (MIME sniffing)
# Content-Security-Policy: whitelist of allowed resource origins
# Referrer-Policy: controls referrer header
```
''',
     "Given a Python Flask app with 5 security vulnerabilities (SQL injection in search, XSS in profile, missing CSRF, HTTP-only missing on session cookie, stack trace in error page) — fix all 5 with explanations.",
     "Which HTTP security header prevents a page from being embedded in an iframe, protecting against clickjacking?",
     "Build a security-hardened Django REST API: parameterised queries, CSP headers, CSRF protection for browser clients, JWT for mobile/API clients, rate limiting on auth endpoints, and a security audit checklist.",
     "Use Django's SecurityMiddleware and set all the SECURE_* settings in production. Run a security scan with OWASP ZAP or Mozilla Observatory (free) before deploying any web application.",
     60),
]


BATCH_4 = [
    ("sql",       "SQL",        "databases", "beginner",     "6 weeks",
     "SQL, PostgreSQL, Joins, Aggregation, Indexes, Transactions",
     "Master the language of databases — query, join, aggregate, and optimise with SQL.", SQL_LESSONS),

    ("postgresql","PostgreSQL", "databases", "intermediate", "6 weeks",
     "PostgreSQL, SQL, Indexes, Transactions, Views, PL/pgSQL",
     "Go deep with PostgreSQL — advanced queries, performance tuning, and stored procedures.", SQL_LESSONS),

    ("mongodb",   "MongoDB",    "databases", "intermediate", "5 weeks",
     "MongoDB, Mongoose, Aggregation Pipeline, Indexes, CRUD",
     "Build scalable document databases with MongoDB's flexible model.", MONGODB_LESSONS),

    ("c",         "C Programming",   "programming", "intermediate", "8 weeks",
     "C, Pointers, Memory Management, Structs, File I/O",
     "Learn the language that powers operating systems and understand computing from the ground up.", C_LESSONS),

    ("networking",    "Networking & Protocols",  "cybersecurity", "beginner",     "5 weeks",
     "TCP/IP, HTTP, DNS, TLS, Firewalls, Network Security",
     "Understand how the internet works — protocols, packets, and network security.", C_LESSONS),

    ("ethical-hacking", "Ethical Hacking",     "cybersecurity", "intermediate",  "8 weeks",
     "OWASP, Penetration Testing, Burp Suite, Metasploit, CTF",
     "Learn offensive security techniques to better defend systems.", CYBERSECURITY_LESSONS),
]


class Command(BaseCommand):
    help = "Generate curriculum batch 4: SQL, MongoDB, C, Cybersecurity"

    def handle(self, *args, **options):
        total_created = total_updated = 0

        for (slug, title, category, level, duration, skills, summary, lessons) in BATCH_4:
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
            f"\nBatch 4 done — {total_created} lessons created, {total_updated} updated."
        ))
