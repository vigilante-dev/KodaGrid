# KodaGrid original technology curriculum

This curriculum is original instructional material. It uses public language concepts and links to primary specifications or official documentation for reference; those references are not copied lesson text.

## Import contract

Each Markdown file describes one learning path with YAML front matter. Import `title`, `slug`, `category`, `level`, `duration`, `skill_stack`, and `summary` as `LearningPath` fields. The six `stages` entries supply lesson order, display stage, slug, and estimated time. The matching `##` sections in the Markdown body are the six lesson bodies; an importer can split them by heading and derive `objective`, `exercise_prompt`, `quiz_question`, and `project_prompt` from their labeled subsections, while retaining the full section as `content`. Content uses plain Markdown and fenced code. Slugs are unique within each path.

## Paths

| Technology | File |
|---|---|
| HTML | [html.md](html.md) |
| CSS | [css.md](css.md) |
| JavaScript | [javascript.md](javascript.md) |
| TypeScript | [typescript.md](typescript.md) |
| Python | [python.md](python.md) |
| React | [react.md](react.md) |
| Next.js | [nextjs.md](nextjs.md) |
| Node.js | [nodejs.md](nodejs.md) |
| SQL | [sql.md](sql.md) |
| Git & GitHub | [git-github.md](git-github.md) |

Every path follows Beginner → Intermediate → Advanced → Projects → Challenges → Final Assessment. Examples use contexts such as school clubs, local markets, community events, water access, transport, and mobile-first services. Learners should substitute their own community context and avoid putting real personal information in practice apps.
