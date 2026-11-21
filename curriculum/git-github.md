---
kind: learning_path
title: Git & GitHub: Collaborate with Confidence
slug: git-github-foundations
category: programming
level: beginner
duration: 6 stages · self-paced
skill_stack: Git, GitHub, version control, collaboration, code review
summary: Track project history with Git and collaborate through clear branches, commits, pull requests, and reviews.
language: en
stages:
  - {order: 1, stage: Beginner, slug: beginner-git, estimated_minutes: 40}
  - {order: 2, stage: Intermediate, slug: intermediate-git, estimated_minutes: 45}
  - {order: 3, stage: Advanced, slug: advanced-git, estimated_minutes: 50}
  - {order: 4, stage: Projects, slug: git-projects, estimated_minutes: 60}
  - {order: 5, stage: Challenges, slug: git-challenges, estimated_minutes: 35}
  - {order: 6, stage: Final Assessment, slug: git-assessment, estimated_minutes: 45}
references:
  - https://git-scm.com/docs
  - https://docs.github.com/en/get-started
  - https://docs.github.com/en/pull-requests
originality: Original CoderGrid instructional content; references identify official documentation.
---

# Git & GitHub · Collaborate with Confidence

Git records project history on your computer. GitHub hosts repositories and adds collaboration features such as issues and pull requests. Git can be used with other hosting services; GitHub is not Git itself. Practise with a folder of non-sensitive files.

## Beginner

**Objectives:** initialize a repository, inspect changes, stage selected files, commit, and read history.

```bash
git init
git status
git add index.html styles.css
git commit -m "Add community notice page"
git log --oneline
```

The working tree contains current files; staging selects the next commit's changes; a commit records a snapshot and message. `git status` is a safe first diagnostic. Set `user.name` and `user.email` for commit attribution; use an address suitable for public history.

**Try it:** create a README, commit it, edit one line, inspect the difference with `git diff`, and commit the focused change.

**Practice / answers:** Which command shows changed files? `git status`. Does `git add` publish to GitHub? No, it stages locally. What should a commit message say? The purpose of the change.

**Mistakes / habits:** committing generated secrets, staging everything without review, or vague messages. Inspect staged changes with `git diff --cached`; add sensitive files to `.gitignore` before they are tracked.

## Intermediate

**Objectives:** branch for isolated work, integrate changes, and collaborate through a pull request.

```bash
git switch -c add-event-schedule
# edit and commit work
git push -u origin add-event-schedule
```

A branch is a movable name for a line of development. A pull request on GitHub asks collaborators to review and integrate proposed commits; it is not a Git command. Small PRs with context, screenshots when useful, and test notes are easier to review.

**Exercise:** create a branch to add a fictional event schedule. Open a pull request against a practice repository, write a summary and test plan, then respond to one review comment.

**Practice:** Why branch? Isolate related work. What is a pull request for? Propose and discuss changes before integration. When do conflicts happen? Concurrent changes overlap in a way Git cannot automatically combine.

**Mini project:** collaborate in pairs on a README for a community coding event. Divide sections, use branches, review each other's change, and merge after approval.

**Habits:** pull before starting when appropriate, commit coherent changes, explain decisions in PRs, and keep credentials out of commits.

## Advanced

**Objectives:** resolve conflicts, recover carefully, and understand shared versus local history.

```bash
git fetch origin
git log --oneline --graph --decorate --all
git revert <commit-id>
```

`fetch` updates remote-tracking references without merging. The graph helps inspect history. `revert` creates a new commit that reverses an earlier commit and is often appropriate for shared history. Rewriting tools such as reset/rebase can change commit history; coordinate before force-pushing shared branches. Confirm the target and working tree before recovery actions.

**Challenge:** resolve a conflict in a practice branch, explain which lines were retained, and verify the resulting file before committing. Then revert a deliberately harmless change.

**Best practices:** protect main branches, review diffs, use least-privilege access, enable secret scanning where available, and rotate any credential accidentally exposed. `.gitignore` does not remove files already tracked.

**Quiz / answers:** Does `fetch` merge? No. What does `revert` do? Adds a new commit undoing a selected change. Does `.gitignore` untrack a committed file? No; remove it from tracking separately and address exposed secrets.

## Projects

Build **Open Community Workshop Handbook** in a shared repository. Add setup instructions, schedule, code of conduct, and contribution guide. Work in short-lived branches; use descriptive commits and pull requests; review for clarity and accessibility. Use only fictional contact details and no credentials.

**Deliverables:** repository link or exported history, one merged pull request per contributor, and a short reflection on one review improvement. **Review:** can a new contributor follow setup? Are commits focused? Was shared history rewritten without agreement?

## Challenges

1. Identify unstaged versus staged changes from `git status`.
2. Find a committed secret in a toy repository and explain safe remediation.
3. Resolve a same-line conflict without discarding either intended change.
4. Choose between `revert` and history rewriting for a published commit.

**Hint:** inspect `git diff` and `git diff --cached` before acting. Never paste a real secret into an exercise or public issue.

## Final Assessment

Submit a small change through a reviewable branch and explain the history.

1. What is the staging area? Selection of changes for the next commit.
2. What does `git status` show? Repository state and changed/untracked files.
3. What feature supports code review on GitHub? Pull requests.
4. What is safer for shared history when undoing a published commit? Revert.
5. Can `.gitignore` erase a leaked credential from history? No; revoke/rotate it and follow repository cleanup procedures.

**Rubric (20):** clean focused commits 4; branch/PR communication 5; conflict handling 4; safe secret practices 4; reflection and instructions 3.
