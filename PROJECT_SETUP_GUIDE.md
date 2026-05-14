# 프로젝트 셋업 및 GitHub 배포 완전 가이드

**작성일**: 2026-05-14  
**프로젝트**: 김비서 (Kim Secretary) - 업무 관리 대시보드 & AI 스킬

---

## 📑 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [1단계: 데이터 파일 준비](#1단계-데이터-파일-준비)
3. [2단계: 스킬 개발 (SKILL.md)](#2단계-스킬-개발-skillmd)
4. [3단계: 헬퍼 스크립트 작성](#3단계-헬퍼-스크립트-작성)
5. [4단계: 테스트 케이스 정의](#4단계-테스트-케이스-정의)
6. [5단계: 환경변수 설정 (.env.local)](#5단계-환경변수-설정-envlocal)
7. [6단계: .gitignore 설정](#6단계-gitignore-설정)
8. [7단계: Git 초기화 및 GitHub 배포](#7단계-git-초기화-및-github-배포)

---

## 프로젝트 개요

### 무엇인가?
- **목적**: 데이터 기반의 일일 업무 브리핑 및 대시보드 업데이트 자동화
- **구성**: HTML 대시보드 + CSV/TXT 데이터 파일 + Claude AI 스킬
- **주요 기능**:
  - 📋 일일 브리핑 (오늘의 할 일, 일정, 긴급 항목)
  - 📊 대시보드 업데이트 (실시간 데이터 반영)
  - 📈 핵심 지표 표시 (판매, 프로젝트 진행도)

### 프로젝트 구조
```
프로젝트폴더/
├── .env.local                 (GitHub 토큰 등 환경변수 - 커밋X)
├── .gitignore                 (Git 제외 파일 목록)
├── README.md                  (프로젝트 설명)
├── dashboard.html             (메인 대시보드)
├── chart.html                 (매출 차트)
├── report.html                (사이트 분석 보고서)
├── meeting-result.html        (회의록)
├── diagram.html               (업무 프로세스 다이어그램)
├── kim-secretary/             (Claude AI 스킬 디렉토리)
│   ├── SKILL.md              (스킬 정의 및 가이드)
│   ├── evals/
│   │   └── evals.json        (테스트 케이스)
│   ├── scripts/
│   │   └── briefing_generator.py  (헬퍼 스크립트)
│   └── example-output.md     (예제 출력)
└── 김비서-데이터/             (데이터 폴더)
    ├── 업무목록.csv          (작업 리스트)
    ├── 주간일정.txt          (주간 스케줄)
    ├── 프로젝트현황.csv      (프로젝트 진행도)
    ├── 매출데이터.csv        (판매 데이터)
    └── 회의록.txt            (회의 노트)
```

---

## 1단계: 데이터 파일 준비

### 1-1. 데이터 폴더 생성
```bash
mkdir 김비서-데이터
```

### 1-2. 필수 데이터 파일 5가지

#### (1) **업무목록.csv** - 작업 리스트
```csv
업무,우선순위,상태,담당자,마감일,카테고리
3월 프로모션 기획안 작성,높음,진행중,김대리,2026-03-12,마케팅
인플루언서 미팅 일정 잡기,높음,대기,이과장,2026-03-14,마케팅
```

**컬럼 설명**:
- `업무`: 작업 이름
- `우선순위`: "높음", "보통", "낮음"
- `상태`: "대기", "진행중", "완료"
- `담당자`: 담당자 이름
- `마감일`: YYYY-MM-DD 형식
- `카테고리`: 작업 분류 (마케팅, 콘텐츠, 리서치 등)

#### (2) **주간일정.txt** - 주간 스케줄
```
========================================
  2026년 3월 10일 ~ 14일 주간 일정
========================================

■ 월요일 (3/10)
- 10:00  마케팅팀 주간회의
- 14:00  신제품 런칭 킥오프 미팅
```

**형식**:
- 자유로운 텍스트 형식
- 날짜와 시간 명확히 표기
- 구분선으로 섹션 나누기

#### (3) **프로젝트현황.csv** - 프로젝트 진행도
```csv
프로젝트명,진행률,상태,담당자,시작일,마감일,예산(만원),집행(만원)
봄맞이 프로모션,65,진행중,김대리,2026-02-15,2026-03-31,500,325
신제품 런칭 캠페인,20,준비중,정팀장,2026-03-01,2026-04-30,1200,240
```

**컬럼 설명**:
- `진행률`: 0~100 (백분율)
- `상태`: "기획중", "준비중", "진행중", "마무리"
- `예산` / `집행`: 만원 단위

#### (4) **매출데이터.csv** - 판매 데이터
```csv
날짜,제품,카테고리,수량,단가,매출액,지역
2026-01-05,무선 이어폰,전자기기,45,89000,4005000,서울
2026-01-05,보조배터리,전자기기,32,35000,1120000,서울
```

**컬럼 설명**:
- `날짜`: YYYY-MM-DD 형식
- `단가`/`매출액`: 숫자 (쉼표 제거)
- `지역`: 판매 지역

#### (5) **회의록.txt** - 회의 노트
```
========================================
  마케팅팀 주간회의 - 2026년 3월 10일 (월)
========================================

참석: 김대리, 이과장, 박사원, 정팀장

■ 지난주 진행사항
- SNS 광고 캠페인 A/B 테스트 결과 나옴
```

---

## 2단계: 스킬 개발 (SKILL.md)

### 2-1. 디렉토리 구조
```bash
mkdir kim-secretary
mkdir kim-secretary/evals
mkdir kim-secretary/scripts
```

### 2-2. SKILL.md 작성

**파일 위치**: `kim-secretary/SKILL.md`

**필수 포함 사항**:
1. **YAML 프론트매터** - 스킬 메타데이터
   ```yaml
   ---
   name: kim-secretary
   description: "[스킬 설명]"
   compatibility: ""
   ---
   ```

2. **목적 섹션** - 스킬이 하는 일
3. **사용 방법** - 사용자가 호출하는 방식
4. **워크플로우** - 단계별 처리 방식
5. **데이터 포맷 참조** - 각 파일의 컬럼 설명
6. **출력 포맷** - 정해진 형식으로 결과 제공

**핵심 작성 팁**:
- 스킬은 `/명령어` 형식으로 호출 가능
- 설명은 구체적이고 명확하게
- 예상 동작과 출력 형식을 명시
- 데이터 파일 구조를 자세히 기록

### 2-3. 주요 내용 구성

**브리핑 출력 형식** (스킬이 생성할 결과):
```
================================================================
📋 오늘의 브리핑 - [날짜]
================================================================

⚠️  긴급 확인 (높은 우선순위 + 마감 임박)
📌 오늘의 할 일
📅 오늘의 일정
📊 핵심 지표

================================================================
```

---

## 3단계: 헬퍼 스크립트 작성

### 3-1. 목적
- 데이터 파일 읽기 및 파싱
- 오늘 날짜 기준 필터링
- 브리핑 포맷팅

### 3-2. 파일 위치
`kim-secretary/scripts/briefing_generator.py`

### 3-3. 기본 구조
```python
import csv
import json
from datetime import datetime
from pathlib import Path

def read_csv(file_path):
    """CSV 파일 읽기"""
    # 구현

def read_text(file_path):
    """텍스트 파일 읽기"""
    # 구현

def parse_date(date_str):
    """날짜 문자열 파싱 (YYYY-MM-DD)"""
    # 구현

def generate_briefing(data_folder):
    """브리핑 생성 메인 함수"""
    # 데이터 읽기
    # 오늘 날짜로 필터링
    # 우선순위 정렬
    # 브리핑 딕셔너리 반환

def format_briefing(briefing):
    """출력용 포맷팅"""
    # 마크다운 형식으로 변환
```

### 3-4. 핵심 기능
- 📅 오늘 날짜와 과제 마감일 비교
- 🎯 우선순위별 정렬 (높음 → 보통 → 낮음)
- 📊 통계 계산 (완료율, 활성 프로젝트 수)
- 💰 오늘의 매출 합계

---

## 4단계: 테스트 케이스 정의

### 4-1. 파일 위치
`kim-secretary/evals/evals.json`

### 4-2. 테스트 케이스 구조
```json
{
  "skill_name": "kim-secretary",
  "evals": [
    {
      "id": 1,
      "prompt": "사용자가 실제로 입력할 명령어/질문",
      "expected_output": "예상되는 결과 설명",
      "files": []
    }
  ]
}
```

### 4-3. 작성 예시

**테스트 1: 기본 브리핑**
```json
{
  "id": 1,
  "prompt": "/김비서 명령어를 실행해서 오늘의 브리핑을 받고 싶어.",
  "expected_output": "Today's briefing with tasks due today, schedule, and key metrics",
  "files": []
}
```

**테스트 2: 대시보드 업데이트**
```json
{
  "id": 2,
  "prompt": "/김비서를 실행해서 대시보드를 업데이트해줘.",
  "expected_output": "Dashboard update with latest sales data, project status",
  "files": []
}
```

**테스트 3: 긴급 항목 확인**
```json
{
  "id": 3,
  "prompt": "/김비서로 높은 우선순위의 긴급 항목들을 확인하고 싶어.",
  "expected_output": "Urgent items list with high priority tasks",
  "files": []
}
```

---

## 5단계: 환경변수 설정 (.env.local)

### 5-1. 파일 생성
```bash
# 프로젝트 루트에 생성
touch .env.local
```

### 5-2. 파일 내용
```env
# GitHub Token
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxx

# GitHub API Settings
GITHUB_API_URL=https://api.github.com
```

### 5-3. 주의사항
- ⚠️ **절대 GitHub에 업로드하지 말 것**
- 개인 토큰을 절대 다른 사람에게 공유 금지
- `.gitignore`에 반드시 포함시킬 것

### 5-4. 토큰 얻기
1. GitHub 계정 로그인
2. Settings → Developer settings → Personal access tokens
3. Generate new token
4. `repo` 권한 선택
5. 생성된 토큰을 `.env.local`에 저장

---

## 6단계: .gitignore 설정

### 6-1. 파일 생성
```bash
touch .gitignore
```

### 6-2. 필수 포함 항목
```gitignore
# 환경 변수 (가장 중요!)
.env
.env.local
.env.*.local

# Node 관련
node_modules/
npm-debug.log
yarn-error.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Python
__pycache__/
*.py[cod]
*$py.class
env/
venv/

# 빌드 결과물
dist/
build/
*.egg-info/
```

### 6-3. 검증
```bash
# .env.local이 제외되는지 확인
git status --ignored
```

---

## 7단계: Git 초기화 및 GitHub 배포

### 7-1. Git 저장소 생성
```bash
# 로컬 git 초기화
git init

# 사용자 설정 (처음 한 번만)
git config user.name "your-github-username"
git config user.email "your-email@example.com"

# 기본 브랜치 이름을 main으로 설정
git branch -M main
```

### 7-2. GitHub 원격 저장소 연결
```bash
# GitHub에서 빈 저장소 생성한 후
git remote add origin https://github.com/your-username/repository-name.git

# 원격 저장소 확인
git remote -v
```

### 7-3. 파일 추가 및 커밋
```bash
# 모든 파일 스테이징 (gitignore 제외됨)
git add .

# 상태 확인 (.env.local이 제외되었는지 확인)
git status

# .env.local 미포함 확인 (중요!)
# "nothing added to commit" 또는 무시된 파일 목록 확인

# 커밋 메시지와 함께 커밋
git commit -m "Initial commit: Add secretary project with dashboards, data files, and kim-secretary skill"
```

### 7-4. GitHub에 푸시
```bash
# 첫 푸시 (origin main 설정)
git push -u origin main

# 이후 푸시
git push
```

### 7-5. 검증
- GitHub 저장소 방문
- `.env.local` 파일이 **없는지** 확인
- 다른 모든 파일이 업로드되었는지 확인

---

## 📋 체크리스트

다음 프로젝트에서 이 가이드를 사용할 때 확인 항목:

### 데이터 준비 단계
- [ ] 데이터 폴더 생성 (예: `[project-name]-데이터`)
- [ ] 5가지 필수 파일 생성 (CSV 2개, TXT 2개)
- [ ] CSV 파일이 올바른 포맷인지 확인
- [ ] 날짜 형식이 YYYY-MM-DD인지 확인

### 스킬 개발 단계
- [ ] `[skill-name]/SKILL.md` 생성
- [ ] YAML 프론트매터 포함
- [ ] 목적, 사용법, 워크플로우 명확히 작성
- [ ] 데이터 포맷 참조 섹션 포함

### 테스트/배포 준비
- [ ] 헬퍼 스크립트 작성 (선택사항)
- [ ] 테스트 케이스 정의 (3~5개)
- [ ] `.env.local` 생성 및 토큰 입력
- [ ] `.gitignore` 생성 및 `.env.local` 포함

### Git 배포
- [ ] `git init`으로 로컬 저장소 초기화
- [ ] GitHub에 원격 저장소 생성
- [ ] `git remote add origin` 실행
- [ ] `.gitignore` 제대로 작동하는지 확인 (git status)
- [ ] `git add .` → `git commit` → `git push`
- [ ] GitHub에서 `.env.local` 미포함 확인

---

## 🔒 보안 주의사항

### 절대 하면 안 되는 것
❌ GitHub 토큰을 코드에 직접 포함  
❌ `.env.local` 파일을 커밋  
❌ 민감한 정보를 public 저장소에 업로드  
❌ 토큰을 다른 사람에게 공유  

### 안전한 방법
✅ `.env.local` 사용 (로컬에만 존재)  
✅ `.gitignore`에 환경 파일 등록  
✅ GitHub Actions 사용 시 Secrets 활용  
✅ 토큰 주기적 갱신  

---

## 🎯 다음 프로젝트에서 빠르게 시작하기

이 가이드를 참고하여:

1. **10분 안에**: 데이터 파일 5개 준비
2. **20분 안에**: SKILL.md 작성
3. **10분 안에**: 테스트 케이스 정의
4. **5분 안에**: 환경변수 및 gitignore 설정
5. **5분 안에**: GitHub 배포

**총 소요 시간**: 약 50분

---

## 참고사항

### 파일 인코딩
- CSV 파일: UTF-8 (BOM 없음)
- TXT 파일: UTF-8
- HTML 파일: UTF-8 + `<meta charset="UTF-8">`

### 디렉토리 이름
- 한글 폴더명 사용 가능 (UTF-8 인코딩)
- 공백 포함 가능
- 특수문자 제한 없음 (다만 일관성 유지)

### Git 커밋 메시지 규칙
```
feat: 새 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 추가
chore: 빌드, 의존성 등 관리
```

---

**이 가이드는 다른 프로젝트에서도 유사한 구조로 반복할 수 있습니다.**  
필요에 따라 수정하고, 프로젝트별 특성에 맞게 커스터마이징하세요.
