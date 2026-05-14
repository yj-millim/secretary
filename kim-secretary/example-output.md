# Kim Secretary (/김비서) - Example Output

## Example 1: Daily Briefing Based on March 10, 2026 Data

```
================================================================
📋 오늘의 브리핑 - 2026-03-10
================================================================

⚠️  긴급 확인 (높은 우선순위 + 마감 임박)
  • [높음] 3월 프로모션 기획안 작성
    마감: 2026-03-12 | 담당: 김대리
    상태: 진행중

  • [높음] 파트너사 계약서 검토
    마감: 2026-03-11 | 담당: 정팀장
    상태: 대기

  • [높음] 월간 마케팅 보고서 작성
    마감: 2026-03-31 | 담당: 김대리
    상태: 대기

📌 오늘의 할 일
  • [높음] 3월 프로모션 기획안 작성
    마감: 2026-03-12 | 담당: 김대리 | 상태: 진행중

  • [높음] 파트너사 계약서 검토
    마감: 2026-03-11 | 담당: 정팀장 | 상태: 대기

  • [높음] 월간 마케팅 보고서 작성
    마감: 2026-03-31 | 담당: 김대리 | 상태: 대기

  • [높음] 4월 신제품 티저 콘텐츠 기획
    마감: 2026-03-21 | 담당: 정팀장 | 상태: 대기

  • [보통] 인플루언서 미팅 일정 잡기
    마감: 2026-03-14 | 담당: 이과장 | 상태: 대기

  • [보통] 영상 광고 3개 추가 제작
    마감: 2026-03-14 | 담당: 박사원 | 상태: 진행중

📅 오늘의 일정 (3월 10일 월요일)
  • 10:00  마케팅팀 주간회의
  • 14:00  신제품 런칭 킥오프 미팅

📊 핵심 지표
  • 진행 중인 프로젝트: 6/7
  • 작업 완료율: 9%
  • 마감 임박 항목: 3건
  • 오늘의 회의: 2건

================================================================

💡 최근 회의 내용 요약
- SNS 광고 A/B 테스트: B안(영상형)이 A안(이미지형) 대비 클릭률 2.3배 높음
- B안 기반으로 영상 광고 3개 추가 제작 진행
- 인플루언서 협업: 푸드스타일리 김OO와 진행
- 3월 넷째 주부터 신제품 티저 시작
- 영상 제작비 200만원 추가 예산 필요
```

## Example 2: Dashboard Update Content

The skill will update the dashboard.html with:

- **Task Status Section**: Latest data from 업무목록.csv showing tasks grouped by status
  - 진행중 (In Progress)
  - 대기 (Waiting)
  - 완료 (Completed)

- **Project Progress Section**: From 프로젝트현황.csv
  - 봄맞이 프로모션: 65% 진행중
  - 신제품 런칭 캠페인: 20% 준비중
  - 인플루언서 협업: 35% 진행중
  - 유튜브 채널 리뉴얼: 80% 마무리
  - 고객 리텐션 프로그램: 10% 기획중
  - 홈페이지 리뉴얼: 45% 진행중

- **Schedule Section**: From 주간일정.txt
  - Formatted view of this week's meetings
  - Today's specific schedule highlighted

- **Sales Section**: From 매출데이터.csv
  - Today's sales total
  - Sales by region
  - Product category breakdown
  - Sales trend chart

## Integration Notes

When the user runs `/김비서`:

1. ✅ The skill reads all files from 김비서-데이터 folder
2. ✅ Parses CSV and TXT files
3. ✅ Filters data for today's date
4. ✅ Generates prioritized briefing
5. ✅ Updates dashboard.html with fresh data
6. ✅ Displays key metrics and urgent items
7. ✅ References recent meeting notes for context

All data is fresh from files - no caching, always current!
