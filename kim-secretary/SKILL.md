---
name: kim-secretary
description: "Run `/김비서` to get a daily briefing and update your dashboard. This command reads all data from the 김비서-데이터 folder (업무목록, 주간일정, 프로젝트현황, 매출데이터, 회의록), analyzes what needs to be done today, and updates your dashboard with the latest information. Use this whenever you want to start your workday, get a quick status update on tasks and projects, or sync the dashboard with current data. The briefing will show high-priority tasks due soon, upcoming meetings, project progress, and today's sales metrics."
compatibility: ""
---

## Purpose

The `/김비서` (Kim Secretary) skill reads all data from your 김비서-데이터 folder and provides:
1. **Daily Briefing**: A prioritized summary of tasks, meetings, and deadlines for today and upcoming days
2. **Dashboard Update**: Synced dashboard showing latest task status, projects, schedule, and sales data
3. **Quick Status**: Key metrics and urgent action items at a glance

## How to Use

Simply type `/김비서` to trigger this workflow:
1. Read and analyze all data files from the 김비서-데이터 folder
2. Identify tasks with today's date or that are overdue
3. Extract today's schedule and meetings
4. Calculate key metrics (sales, project progress, completion rate)
5. Provide a formatted briefing with priorities
6. Update the dashboard with current data

## Workflow Implementation

When `/김비서` is invoked, perform these steps:

### Step 1: Read Data Files
Read all files from 김비서-데이터 folder:
- **업무목록.csv**: Parse task list with columns (업무, 우선순위, 상태, 담당자, 마감일, 카테고리)
- **주간일정.txt**: Extract schedule information
- **프로젝트현황.csv**: Review project status and progress (진행률, 상태, 예산)
- **매출데이터.csv**: Analyze sales data
- **회의록.txt**: Reference recent decisions and action items

### Step 2: Analyze Today's Tasks
- Filter tasks where 마감일 (deadline) is today or in the past
- Exclude tasks with 상태 = "완료" (completed)
- Prioritize by 우선순위 (높음 → 보통 → 낮음)
- Identify urgent items (high priority + near deadline)

### Step 3: Extract Today's Schedule
- Parse 주간일정.txt to find entries for today
- List all meetings and events
- Note any deadlines mentioned in schedule

### Step 4: Calculate Key Metrics
- **오늘 매출 (Today's Sales)**: Sum 매출액 from 매출데이터.csv for today's date
- **활성 프로젝트 (Active Projects)**: Count projects with 상태 = "진행중" or "마무리"
- **작업 완료율 (Completion Rate)**: (completed tasks / total tasks) * 100%
- **긴급 항목 (Urgent Items)**: High priority tasks due soon

### Step 5: Format and Present Briefing

Generate output in this format:

```
================================================================
📋 오늘의 브리핑 - [Today's Date]
================================================================

⚠️  긴급 확인 (높은 우선순위 + 마감 임박)
  • [높음] Task Name
    마감: YYYY-MM-DD | 담당: Name
    상태: Status

📌 오늘의 할 일
  • [우선순위] Task Name
    마감: YYYY-MM-DD | 담당: Name | 상태: Status
  
  [List all non-completed tasks due today, sorted by priority]

📅 오늘의 일정
  [List today's meetings and schedule items]
  [If no schedule for today, indicate this]

📊 핵심 지표
  • 오늘 매출: [Sales Amount]
  • 판매 수량: [Unit Count]
  • 진행 중인 프로젝트: [Active Count]/[Total Count]
  • 작업 완료율: [Percentage]%

================================================================
```

### Step 6: Update Dashboard
- Read 대시보드.html
- Update task sections with latest 업무목록.csv data
- Refresh project progress display with 프로젝트현황.csv
- Update sales chart with latest 매출데이터.csv
- Refresh schedule section with 주간일정.txt
- Save updated dashboard

## Data Format Reference

### 업무목록.csv Columns
- 업무: Task name
- 우선순위: "높음" (high), "보통" (medium), "낮음" (low)
- 상태: "대기" (waiting), "진행중" (in progress), "완료" (completed)
- 담당자: Assigned person name
- 마감일: Deadline in format YYYY-MM-DD
- 카테고리: Category (마케팅, 콘텐츠, 리서치, 운영, 보고)

### 프로젝트현황.csv Columns
- 프로젝트명: Project name
- 진행률: Progress percentage (0-100)
- 상태: "기획중" (planning), "준비중" (preparation), "진행중" (in progress), "마무리" (finishing)
- 담당자: Project lead
- 시작일/마감일: YYYY-MM-DD format
- 예산(만원)/집행(만원): Budget and spending in units of 10,000 won

### 매출데이터.csv Columns
- 날짜: Date in YYYY-MM-DD format
- 제품: Product name
- 카테고리: Product category
- 수량: Quantity sold
- 단가: Unit price
- 매출액: Sales amount
- 지역: Region/Area

## Output Priority

1. **Urgent Items**: Always show high-priority tasks due today/overdue first
2. **Today's Tasks**: Show all tasks due today, sorted by priority
3. **Key Metrics**: Display sales, projects, and completion rate
4. **Schedule**: Show today's meetings and events
5. **Dashboard**: Update all visual elements with latest data

## Notes

- Today's date is determined by the current system date when the command runs
- Tasks are considered "due today" if 마감일 matches today's date or is earlier
- The briefing focuses on actionable items for the current day
- All data is read fresh from files each time the command runs (always current)
- Previous briefings are not cached - always generates latest version
