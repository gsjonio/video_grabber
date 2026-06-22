# Enable GitHub Discussions

## Quick Setup

2 minutes:

1. Go to your repo → **Settings** → **Features**
2. Check the box: ✅ **Discussions**
3. Click **Save** (if prompted)
4. Discussions tab appears in repo navigation

---

## What Goes Where

### 📢 Discussions (Q&A, Ideas)

- "How do I configure X?"
- "Can we support feature Y?"
- "Best practices for Z?"
- Feature requests and discussions

### 🐛 Issues (Bugs, Tasks)

- Broken behavior
- Crashes / errors
- Feature implementation tasks
- PRs and code review

---

## Discussion Categories (Optional)

After enabling, customize categories:

1. **Announcements** — New releases, breaking changes
2. **Q&A** — Usage questions, troubleshooting
3. **Ideas** — Feature proposals, RFCs
4. **Show and Tell** — Community projects, tips

---

## How to Link in README

Add a section:

```markdown
## Questions?

Have a question about vidgrab? Use [GitHub Discussions](https://github.com/gsjonio/video_grabber/discussions) — no need to open an issue!
```

---

## Auto-Reply (Optional)

Add issue template to suggest Discussions for Q&A:

**`.github/ISSUE_TEMPLATE/question.md`**:

```markdown
---
name: Question
about: Ask a question about vidgrab
title: "[QUESTION] "
labels: question
---

> **Note:** Questions belong in [GitHub Discussions](https://github.com/gsjonio/video_grabber/discussions), not Issues. Issues are for bugs and feature requests. Please move this question there!
```

---

## Done ✓

Once enabled, your repo has a community hub separate from issues. Clean, organized, and collaborative!
