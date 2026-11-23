---
kind: learning_path
title: SQL: Ask Questions of Data
slug: sql-foundations
category: databases
level: beginner
duration: 6 stages · self-paced
skill_stack: SQL, relational modeling, joins, transactions, security
summary: Query and update relational data accurately, use constraints and transactions, and protect database access.
language: en
stages:
  - {order: 1, stage: Beginner, slug: beginner-sql, estimated_minutes: 45}
  - {order: 2, stage: Intermediate, slug: intermediate-sql, estimated_minutes: 50}
  - {order: 3, stage: Advanced, slug: advanced-sql, estimated_minutes: 55}
  - {order: 4, stage: Projects, slug: sql-projects, estimated_minutes: 70}
  - {order: 5, stage: Challenges, slug: sql-challenges, estimated_minutes: 40}
  - {order: 6, stage: Final Assessment, slug: sql-assessment, estimated_minutes: 50}
references:
  - https://www.postgresql.org/docs/current/tutorial.html
  - https://www.postgresql.org/docs/current/ddl.html
originality: Original KodaGrid instructional content; references identify official documentation. Examples use broadly supported SQL with PostgreSQL named as the reference dialect.
---

# SQL · Ask Questions of Data

SQL is a language for defining, querying, and changing relational data. Dialects differ in details; examples use common SQL and point to PostgreSQL documentation. A relational database organizes data into tables with rows and columns and uses keys to express relationships.

## Beginner

**Objectives:** read a table, select columns, filter rows, sort results, and limit output.

```sql
SELECT name, category, price_ksh
FROM market_items
WHERE price_ksh < 500
ORDER BY price_ksh ASC
LIMIT 10;
```

`SELECT` chooses columns, `FROM` names a table, `WHERE` filters rows, and `ORDER BY` sorts. `ASC` is ascending. The semicolon ends a statement in many SQL tools.

**Try it:** using fictional library data, list titles published after 2020, ordered newest first. Select only the columns needed.

**Practice / answers:** Which clause filters rows? `WHERE`. How do you sort high to low? `ORDER BY column DESC`. Is `NULL = NULL` true? No; use `IS NULL` to test missing values.

**Mistakes / habits:** forgetting quotes around text values, using `= NULL`, and omitting a filter on an update. Preview query results before changing data.

## Intermediate

**Objectives:** aggregate rows, group summaries, join related tables, and understand constraints.

```sql
SELECT category, COUNT(*) AS item_count, AVG(price_ksh) AS mean_price
FROM market_items
GROUP BY category
HAVING COUNT(*) >= 2
ORDER BY item_count DESC;
```

`GROUP BY` forms groups; aggregate functions summarize each group; `HAVING` filters groups after aggregation. A `JOIN` combines related rows using a meaningful key. A primary key identifies a row; a foreign key helps enforce a relationship.

**Exercise:** create fictional `learners` and `enrolments` tables and join them to count learners per course. Include a course with no enrolments and decide whether `LEFT JOIN` is appropriate.

**Questions:** `WHERE` or `HAVING` for aggregate condition? `HAVING`. Why define a primary key? Reliable row identity. What does `LEFT JOIN` preserve? Every row on the left, with nulls where no right match exists.

**Mini project:** create a small community library schema for books, borrowers (fictional), and loans. Add keys and query overdue counts using sample dates.

**Habits:** use explicit join conditions, name columns, and qualify ambiguous names. Avoid storing multiple values in one column when they need independent querying.

## Advanced

**Objectives:** use subqueries/CTEs, transactions, indexes, and safe parameterized access.

```sql
BEGIN;
UPDATE stock
SET quantity = quantity - 2
WHERE item_id = 17 AND quantity >= 2;
-- Application checks affected row count before COMMIT.
COMMIT;
```

Transactions group changes so they can succeed or be rolled back as a unit. This sample alone does not prove a reservation succeeded; the application must check affected rows and handle failures. Use parameterized statements in application code, never concatenate user input into SQL. Indexes can speed reads but cost space and may slow writes; inspect query plans before adding them.

**Challenge:** model transfers between two fictional inventory locations so both sides update atomically. Include constraints against negative stock and explain rollback behaviour.

**Best practices:** least-privilege database accounts, parameterized queries, constraints for important invariants, backups, and explicit transaction boundaries. Avoid displaying private records just because a query can retrieve them.

**Quiz / answers:** What protects a multi-step change from partial completion? Transaction. What is an index trade-off? Faster some reads with storage/write costs. How prevent SQL injection? Parameterized queries and least privilege.

## Projects

Build **Community Learning Centre Database** using fictional course, session, and attendance data. Create tables with appropriate types and keys; insert sample records; write queries for attendance rate, busiest session, and learners with no attendance. Include a parameterized query example in the application layer or pseudocode.

**Review:** are relationships normalized sensibly? Are missing values distinguished from zero? Do joins duplicate counts? Are changes transactional and input parameters bound safely?

## Challenges

1. Rewrite a query that uses `= NULL`.
2. Find why a join multiplies totals.
3. Use a `LEFT JOIN` to include categories without rows.
4. Inspect a slow query and justify an index from its plan.

**Hint:** check key uniqueness and row counts before and after each join; aggregate at the intended grain.

## Final Assessment

Given a small library schema, query titles, borrowers, and loans and propose safe updates.

1. Which clause groups rows? `GROUP BY`.
2. Which clause filters groups? `HAVING`.
3. How do you test missing data? `IS NULL` / `IS NOT NULL`.
4. What does a foreign key help ensure? A reference points to an allowed related row.
5. How should a web app pass a search term into SQL? As a bound parameter.

**Rubric (20):** query correctness 5; joins and aggregation 5; schema constraints 3; transaction/security reasoning 5; readable explanation 2.
