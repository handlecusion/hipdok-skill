# Hipdok Workflow Reference

Observed with `agent-safari` on 2026-05-25 against `https://seouloutdoorlibrary.kr`.

## Login And Entry

Primary entry:

`/user/hipdok/mypage/myInfo.do`

Logged-in indicators:

- Header links show `나의 힙독클럽`, `마이페이지`, `로그아웃`.
- My page shows nickname, club term, attendance status, grade, mileage, and activity counts.

If unauthenticated, the site redirects to `/user/loginUserForm.do`.

Observed login controls:

- Local ID/password form: `#userId`, `#userPw`, submit via `/user/loginUserForm.do`.
- Naver social login link: `/user/login/naver.do`, visible text `네이버로 로그인`.
- Kakao social login link: `/user/login/kakao.do`, visible text `카카오로 로그인`.

Preferred login fallback:

1. If the page text is `로그인 | 서울야외도서관` or includes `서비스 이용을 위해 로그인해 주세요`, click the visible `네이버로 로그인` link, or navigate directly to `/user/login/naver.do`.
2. Wait for redirects and then navigate back to `/user/hipdok/mypage/myInfo.do`.
3. Treat login as complete only when `나의 힙독클럽`, `마이페이지`, and `로그아웃` are visible.
4. If Naver shows an ID/password, passkey, phone verification, CAPTCHA, or non-routine consent page, do not enter secrets. Ask the user to complete that step in Safari, then retry the Hipdok my page.
5. If the session is already authenticated, navigating to `/user/loginUserForm.do` may redirect to `/user/main/mainIndex.do`; in that case skip Naver login and continue.

## Status Page

URL:

`/user/hipdok/mypage/myInfo.do`

Useful links and controls:

- `출석체크`: `/user/hipdok/mypage/attend/hipdokAttendCaledar.do`
- `나의게시글`: `/user/hipdok/mypage/hipdokReviewReadCertifyAllList.do`
- `나의댓글`: `/user/hipdok/comment/mypage/hipdokMyCommentList.do`
- `정보수정`: `/user/hipdok/member/mypage/hipdokMemberUpdate.do`
- `방문인증`: opens `/user/hipdok/attend/hipdokAttendQrPop.do`
- `마일리지내역`: `/user/hipdok/mileage/mypage/hipdokMileageList.do`

Observed status text includes the next grade requirement, e.g. `다음 등급으로 마일리지298점, 독서기록 3회 더 필요합니다.`

## Attendance

URL:

`/user/hipdok/mypage/attend/hipdokAttendCaledar.do`

Observed text:

- Monthly attendance count.
- Cumulative mileage.
- `출석완료` when online attendance is already done.
- Notice: online attendance and visit attendance are each possible once per day.

Policy summary:

- Online attendance: once per day, 2 mileage.
- Offline visit attendance: once per day, 10 mileage.

When asked to check attendance:

1. Open my page or attendance calendar.
2. If `출석완료` is visible, report already complete.
3. If a check-in button is visible, click it, accept site confirmation if the user requested attendance, then verify `출석완료`.
4. For offline visit certification, open `방문인증`; do not invent QR or location proof.

## Book Registration And Library

Main library URL:

`/user/hipdok/book/mypage/hipdokBookList.do`

Observed page text:

- `도서등록`
- Search filters and keyword field.
- Book cards with progress percent and buttons: `독서 기록`, `완독 인증`, `필사 인증`.

### Register By Search

Open `도서등록`; it loads:

`/user/hipdok/book/mypage/hipdokBookPop.do`

Observed controls:

- `searchCondition`
- `searchKeyword` placeholder: `도서명, 저자, ISBN 으로 검색하세요`
- `검색`
- `바코드 읽기`
- `도서정보 직접 등록하기`

Search results come from Aladin DB and include hidden values:

- `title`
- `author`
- `publisher`
- `pubYear`
- `isbn`
- `ageLimit`

Selecting a result runs `fnRegist(idx)`, confirms `선택하시겠습니까?`, then posts to:

`/user/hipdok/book/mypage/hipdokBookSearchRegistProc.do`

### Direct Registration

Direct URL:

`/user/hipdok/book/mypage/hipdokBookRegistPop.do`

Observed required fields:

- `title`: 도서명
- `author`: 저자
- `publisher`: 출판사
- `totalPageCnt`: 총 페이지 수
- `classNo1`: 주제분류 radio. Values 0-9 correspond to 총류, 철학, 종교, 사회과학, 자연과학, 기술과학, 예술, 언어, 문학, 역사.

Observed optional fields:

- `pubYear`: 발행연도
- `isbn`: ISBN
- `upload`: 도서표지

Hidden default:

- `ageLimit=0`

Validation:

- Title, author, publisher, total pages, and subject category are required.
- Year and total pages must be numeric.
- Direct registration posts to `/user/hipdok/book/mypage/hipdokBookDirectRegistProc.do`.
- Direct registrations require admin approval before reading records can proceed.

## Reading Record

Open from a book card: `독서 기록`.

Direct observed URL shape:

`/user/hipdok/book/mypage/hipdokReadHistoryRegistPop.do?bookNo=<bookNo>`

Observed fields:

- `bookNo`: hidden
- `readPageCnt`: read page count
- `readYmd`: read date
- `readHm`: read time

Observed validation:

- `readPageCnt` is required.
- Page count must be numeric.
- Page count must be at least 1.
- Page count must not exceed total pages.
- Page count must be greater than the previously registered last page.
- `readYmd` is required and cannot be a future date.
- `readHm` is required.

Submit endpoint:

`/user/hipdok/book/mypage/hipdokReadHistoryRegistProc.do`

Delete endpoint:

`/user/hipdok/book/mypage/hipdokReadHistoryDeleteProc.do`

Policy summary:

- Reading record is a required activity for grade progression.
- Mileage limit: per book once per day, up to two books per day, up to three mileage-credit records per book.

## Completion Certification

Open from a book card: `완독 인증`.

Direct observed URL shape:

`/user/hipdok/book/mypage/hipdokReadCompleteRegistPop.do?bookNo=<bookNo>`

Observed blocker:

- If reading progress is not 100%, the page alerts `독서기록 100% 달성 후 등록가능합니다.`

Policy requirements:

- The book must be registered in `나의 서재`.
- Reading progress must be 100%.
- Add a rating.
- Write at least 100 characters of meaningful quote or reading impression.
- Mileage-credit limit: once per day.

Because the observed account had no 100% book during exploration, inspect the live form dynamically when it becomes available. Do not hard-code selectors beyond visible labels.

## Transcription Certification

Direct observed URL shape:

`/user/hipdok/bookcopy/mypage/hipdokBookCopyRegistPop.do?bookNo=<bookNo>`

Observed fields:

- `bookNo`: hidden
- `openYn`: public/private radio, values `Y` and `N`
- `upload`: required image file
- `contents`: required text

Observed validation and notices:

- Content is required.
- Content maximum is 300 characters.
- Image upload is required.
- Image files are limited to 5 MB by page notice.
- Copyright-infringing, defamatory, abusive, or improper content can be deleted and mileage can be canceled.
- Once mileage is credited, the post cannot be deleted; only editing and public/private switching are available.
- Age-restricted books are blocked for transcription certification.

Submit endpoint:

`/user/hipdok/bookcopy/mypage/hipdokBookCopyRegistProc.do`

Policy summary:

- Mileage-credit limit: once per day.

## Activity Review

Community review list:

`/user/hipdok/review/hipdokReviewList.do`

Observed page text:

- `활동후기`
- Reviews for online/offline programs.
- Search/sort controls.
- Likes use table `HD_REVIEW`.

Observed account state:

- `마이페이지 > 프로그램 신청현황` had `전체 0건`, so no eligible review button was available.

Policy requirements:

- The user must participate in a Hipdok online/offline event and complete participation proof.
- Then write a text or photo review.
- Mileage-credit limit: once per program.

Execution rule:

1. Check `마이페이지 > 프로그램 신청현황`.
2. Find an eligible completed event/program and its review/write button.
3. If none exists, report that activity review cannot be posted yet.
4. If a review form appears, inspect its fields dynamically and confirm the final public content before submit.

## Community Pages

Useful routes:

- Completion community: `/user/hipdok/book/hipdokReadCompleteList.do`
- Book recommendation: `/user/hipdok/book/hipdokRecommendList.do`
- Reading proof photos: `/user/hipdok/readcertify/hipdokReadCertifyList.do`
- Transcription community: `/user/hipdok/bookcopy/hipdokBookCopyList.do`
- Activity reviews: `/user/hipdok/review/hipdokReviewList.do`
- Free board: `/user/hipdok/freeboard/hipdokFreeBoardList.do`

Comment JavaScript posts to:

- `/user/hipdok/comment/hipdokCommentRegistProc.do`
- `/user/hipdok/comment/hipdokCommentDeleteProc.do`

Like JavaScript posts to:

- `/hipdok/like/hipdokLikeRegistProc.do`
- `/hipdok/like/hipdokLikeDeleteProc.do`
- `/hipdok/like/hipdokLikeCnt.do`

If like/comment responses redirect to `/user/hipdok/recruit/hipdokRecruitLogin.do` or `/user/hipdok/recruit/hipdokRecruitIntro.do`, the account is either not logged in or not a Hipdok member.

## Mileage And Grade Policy Snapshot

Observed 2026 policy summary:

- Online attendance: 2 mileage, once daily.
- Offline attendance: 10 mileage, once daily.
- Reading record: 5 mileage, limited by book/day and per-book count.
- Completion certification: 30 mileage, once daily.
- Transcription certification: 15 mileage, once daily.
- Activity review: 10 mileage, once per program.
- Comment: 5 mileage, up to two daily mileage-credit comments.

Grade levels:

- 0 `힙독이`
- 1 `현무`
- 2 `청룡`
- 3 `백호`
- 4 `주작`
- 5 `해치`

Grade progression requires both mileage and required activities. Do not promise grade changes unless the page confirms them.
