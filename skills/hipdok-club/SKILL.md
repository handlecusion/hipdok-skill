---
name: hipdok-club
description: Operate Seoul Outdoor Library Hipdok Club (힙독클럽) in Safari with agent-safari. Use when the user asks in natural language to do Hipdok Club tasks such as daily attendance/출석체크, book registration/도서등록 in 나의 서재, reading records/독서기록, completion certification/완독인증, transcription certification/필사인증, activity reviews/활동후기, checking mileage/grade/activity status, or navigating Hipdok community pages on seouloutdoorlibrary.kr.
---

# Hipdok Club

Use agent-safari MCP operations, or the equivalent `agent-safari` CLI commands when the MCP tool surface is not exposed, to operate the live Hipdok Club site for the user. The main entry point is:

`https://seouloutdoorlibrary.kr/user/hipdok/mypage/myInfo.do`

## Operating Rules

1. Treat the site as a live account. Do not log out, change profile data, delete records, request rewards, or submit public posts unless the user asked for that action and the final content is clear.
2. If Safari lands on `로그인 | 서울야외도서관`, use the site's `네이버로 로그인` link first. Do not ask for passwords or type credentials; if Naver asks for ID/password, passkeys, phone verification, or extra consent that is not clearly routine, stop and ask the user to complete that step in Safari.
3. Before submitting public content (`완독인증`, `필사인증`, `활동후기`, comments, likes), show a short confirmation summary unless the user explicitly asked to submit immediately.
4. Prefer visible labels and page text over brittle selectors. Use MCP equivalents of `snapshot`, `text`, and compact `evaluate` queries to confirm controls.
5. After any successful action, verify by returning to `나의 힙독클럽` or the relevant list page and checking status, mileage, progress, or the newly created item.
6. If the account is not eligible for a task, explain the exact blocker and the next required action. Common blockers: completion certification requires 100% reading progress; activity review requires an eligible completed program/event; online attendance may already show `출석완료`.

For exact observed screens, field names, URLs, and limits, read `references/hipdok-workflows.md`.
For natural-language examples and coverage expectations, read `references/use-cases.md`.

## Quick Workflow

1. Start or check Safari automation:

```bash
agent-safari doctor
agent-safari daemon
```

2. Open the Hipdok my page and confirm login:

```bash
agent-safari navigate https://seouloutdoorlibrary.kr/user/hipdok/mypage/myInfo.do
agent-safari wait-for-idle --timeout 15000
agent-safari text
```

If this shows the login page, click the visible `네이버로 로그인` link or navigate to `/user/login/naver.do`, wait for redirects, then re-open the Hipdok my page. Login is successful only when the page shows `나의 힙독클럽` and `로그아웃`.

3. Classify the user's intent:

- `출석`, `출첵`, `attendance`: attendance check.
- `책 등록`, `도서등록`, `나의 서재`: register a book.
- `읽은 페이지`, `독서기록`, `진행률`: record reading progress.
- `완독`, `별점`, `독서 소감`: completion certification.
- `필사`, `문장`, `필사 사진`: transcription certification.
- `후기`, `프로그램 후기`, `활동후기`: activity review.
- `마일리지`, `등급`, `활동현황`: status lookup.

4. Gather missing task inputs only when needed. Examples: book title/ISBN, page number, reading date/time, rating, review text, image file path, public/private setting, or program name.

5. Execute through the UI with agent-safari; use JavaScript evaluation only to inspect forms or fill obvious fields. Do not bypass the site's normal validation or confirmation dialogs.

6. Verify and report concise evidence: current page, visible success text, updated progress/mileage, or the blocker encountered.

## Task Notes

### Attendance

Use `나의 힙독클럽` or `출석체크`. If the page shows `출석완료`, report that attendance is already complete. Online attendance is once per day; offline visit certification is separate and uses `방문인증`.

### Book Registration

Go to `힙독클럽 > 독서활동`, then `도서등록`.

- Search registration uses Aladin book DB results. Search by title, author, or ISBN; pick the result that matches the user's request.
- Direct registration is for missing books. Required fields include title, author, publisher, total page count, and subject category. Direct registrations require admin approval before reading records can proceed.
- Avoid duplicate registration by searching the user's library first.

### Reading Records

From `독서활동`, choose a book and open `독서 기록`.

Required fields: read page count, read date, read time. The page validates numeric pages, at least 1 page, not more than total pages, greater than the previous last page, and no future dates.

### Completion Certification

Open `완독 인증` for a book only after reading progress is 100%. If the page says `독서기록 100% 달성 후 등록가능합니다`, first add the reading record that reaches the total page count. Completion certification requires a rating and at least 100 characters of quote/impression according to the site policy.

### Transcription Certification

Open `필사 인증` from a registered book. Required fields: public/private, image upload, and content. The observed form requires an image file, content, and limits content to 300 characters; images are limited to 5 MB by site notice.

### Activity Reviews

Use `힙독 커뮤니티 > 활동후기` for browsing. To write a review, first inspect `마이페이지 > 프로그램 신청현황` or any eligible event-specific review button. If the account has no eligible completed program/event, report that an activity review cannot be posted yet.

### Community Safety

Follow the site's moderation policy: no abusive content, hate/discrimination, spam, illegal promotion, privacy leaks, copyright-infringing material, sexual content, self-harm encouragement, impersonation, malware, or repeated duplicate posts. Keep user-submitted text original and appropriate.
