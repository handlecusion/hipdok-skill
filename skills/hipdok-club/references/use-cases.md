# Hipdok Natural-Language Use Cases

Use these cases to validate that the skill covers the requested Hipdok Club tasks. Each case is phrased like a user request and maps to the workflow that should be exercised.

## Coverage Matrix

| # | Natural-language request | Covered workflow |
|---|---|---|
| 1 | `오늘 힙독 출석체크 해줘.` | Online attendance |
| 2 | `이번 달 출석현황이랑 현재 마일리지, 다음 등급까지 필요한 조건 알려줘.` | Status, mileage, grade |
| 3 | `나의 서재에 데미안 등록해줘. 민음사 판이면 좋아.` | Book search registration |
| 4 | `검색에 안 나오는 책을 직접 등록해줘. 제목/저자/출판사/페이지는 내가 줄게.` | Direct book registration |
| 5 | `제로 투 원 오늘 120쪽까지 읽은 걸로 독서기록 남겨줘.` | Reading record |
| 6 | `이 책을 다 읽은 걸로 마지막 페이지까지 기록하고 완독인증도 이어서 작성해줘.` | Reading record to 100%, completion certification |
| 7 | `완독인증 가능한 책이 있는지 확인하고, 없으면 왜 안 되는지 알려줘.` | Completion eligibility/blocker |
| 8 | `필사 사진 올리고 문장은 비공개로 등록해줘.` | Transcription certification |
| 9 | `지난 프로그램 활동후기 쓸 수 있는지 확인하고 가능하면 후기 초안으로 등록해줘.` | Activity review eligibility and submission |
| 10 | `내가 쓴 힙독 게시글이랑 댓글 목록 확인해줘.` | My posts/comments |

## Expected Handling

1. Attendance: open my page or attendance calendar. If `출석완료` is visible, report completion instead of clicking repeatedly.
2. Status: read current mileage, grade, required next-grade mileage, and required activities from `나의 힙독클럽`.
3. Book search registration: search existing library first, open `도서등록`, search title/author/ISBN, disambiguate if multiple editions match, then confirm before selecting.
4. Direct book registration: collect required fields: title, author, publisher, total page count, subject category. Explain that admin approval is required.
5. Reading record: select the correct book, enter page count, read date, and read time. Validate that page count is increasing and not over total pages.
6. Completion after final reading record: first make progress 100%, then open completion certification. Collect rating and at least 100 characters of quote/impression.
7. Completion eligibility: if the site alerts that 100% reading progress is required, report that exact blocker and the remaining action.
8. Transcription: collect image path, contents, and public/private choice. Confirm the post summary before submit because it can become public and may not be deletable after mileage is credited.
9. Activity review: check `프로그램 신청현황` for eligible completed programs. If none exists, say no eligible activity review is available yet.
10. My posts/comments: use `나의게시글` and `나의댓글`, summarize counts and visible items without modifying anything.

## Full-Coverage Checklist

Use this checklist before claiming the skill can handle the user's requested scope:

- [x] Login detection, Naver social-login fallback, and safe handoff for Naver credential/verification steps.
- [x] My Hipdok status and grade/mileage reading.
- [x] Online attendance detection and completed-state handling.
- [x] Offline visit certification entry point.
- [x] Book search registration route and submit endpoint.
- [x] Direct book registration route, required fields, and approval caveat.
- [x] Reading record route, fields, validation rules, and submit endpoint.
- [x] Completion certification eligibility and policy requirements.
- [x] Transcription certification route, fields, validation rules, and submit endpoint.
- [x] Activity review list, eligibility rule, and no-eligible-program handling.
- [x] My posts and comments routes.
- [x] Community comment/like endpoint behavior.

## Known Live-Test Limits

The initial exploration intentionally avoided creating public posts or altering the user's account beyond read-only navigation. The observed account also had no completed 100% book and no eligible program application, so completion certification and activity review were covered by the live blocker states plus the site's published policy. When those states become eligible, inspect the live form dynamically before submitting.
