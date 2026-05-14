#!/usr/bin/env python3
import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

def read_csv(file_path):
    """Read CSV file and return list of dictionaries"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def read_text(file_path):
    """Read text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def parse_date(date_str):
    """Parse date string in format YYYY-MM-DD"""
    try:
        return datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
    except:
        return None

def generate_briefing(data_folder):
    """Generate daily briefing from data files"""
    data_path = Path(data_folder)

    # Read all data files
    tasks = read_csv(data_path / '업무목록.csv')
    projects = read_csv(data_path / '프로젝트현황.csv')
    sales = read_csv(data_path / '매출데이터.csv')
    schedule = read_text(data_path / '주간일정.txt')
    meeting_notes = read_text(data_path / '회의록.txt')

    today = datetime.now().date()

    # Filter tasks for today or overdue
    today_tasks = []
    urgent_items = []

    for task in tasks:
        deadline_str = task.get('마감일', '').strip()
        deadline = parse_date(deadline_str)

        if deadline and deadline <= today:
            status = task.get('상태', '').strip()
            priority = task.get('우선순위', '').strip()

            task_item = {
                'name': task.get('업무', ''),
                'priority': priority,
                'status': status,
                'deadline': deadline_str,
                'assignee': task.get('담당자', ''),
                'category': task.get('카테고리', '')
            }

            if status != '완료':
                today_tasks.append(task_item)

                if priority == '높음':
                    urgent_items.append(task_item)

    # Sort by priority
    priority_order = {'높음': 0, '보통': 1, '낮음': 2}
    today_tasks.sort(key=lambda x: priority_order.get(x['priority'], 3))
    urgent_items.sort(key=lambda x: priority_order.get(x['priority'], 3))

    # Calculate sales for today
    today_sales = 0
    today_sales_count = 0

    for sale in sales:
        sale_date_str = sale.get('날짜', '').strip()
        sale_date = parse_date(sale_date_str)
        if sale_date == today:
            today_sales += int(sale.get('매출액', '0').replace(',', ''))
            today_sales_count += int(sale.get('수량', '0'))

    # Count active projects
    active_projects = [p for p in projects if p.get('상태', '').strip() in ['진행중', '마무리']]

    # Generate briefing summary
    briefing = {
        'date': today.strftime('%Y-%m-%d'),
        'today_tasks': today_tasks,
        'urgent_items': urgent_items,
        'today_sales': {
            'total': f"{today_sales:,}원" if today_sales > 0 else "0원",
            'quantity': today_sales_count,
            'has_data': today_sales > 0
        },
        'active_projects': len(active_projects),
        'total_projects': len(projects),
        'task_completion_rate': calculate_completion_rate(tasks),
        'schedule_snippet': schedule[:500] if schedule else "No schedule data"
    }

    return briefing

def calculate_completion_rate(tasks):
    """Calculate task completion rate"""
    if not tasks:
        return 0
    completed = sum(1 for t in tasks if t.get('상태', '').strip() == '완료')
    return f"{int(completed / len(tasks) * 100)}%"

def format_briefing(briefing):
    """Format briefing for display"""
    output = []
    output.append("=" * 60)
    output.append(f"📋 오늘의 브리핑 - {briefing['date']}")
    output.append("=" * 60)
    output.append("")

    # Urgent items
    if briefing['urgent_items']:
        output.append("⚠️  긴급 확인 (높은 우선순위 + 마감 임박)")
        for item in briefing['urgent_items'][:3]:  # Show top 3
            output.append(f"  • [{item['priority']}] {item['name']}")
            output.append(f"    마감: {item['deadline']} | 담당: {item['assignee']}")
            output.append(f"    상태: {item['status']}")
        output.append("")

    # Today's tasks
    if briefing['today_tasks']:
        output.append("📌 오늘의 할 일")
        for item in briefing['today_tasks']:
            output.append(f"  • [{item['priority']}] {item['name']}")
            output.append(f"    마감: {item['deadline']} | 담당: {item['assignee']} | 상태: {item['status']}")
        output.append("")
    else:
        output.append("📌 오늘의 할 일: 없음 ✓")
        output.append("")

    # Key metrics
    output.append("📊 핵심 지표")
    output.append(f"  • 오늘 매출: {briefing['today_sales']['total']}")
    if briefing['today_sales']['has_data']:
        output.append(f"  • 판매 수량: {briefing['today_sales']['quantity']}개")
    output.append(f"  • 진행 중인 프로젝트: {briefing['active_projects']}/{briefing['total_projects']}")
    output.append(f"  • 작업 완료율: {briefing['task_completion_rate']}")
    output.append("")
    output.append("=" * 60)

    return "\n".join(output)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        data_folder = sys.argv[1]
    else:
        data_folder = "김비서-데이터"

    briefing = generate_briefing(data_folder)
    print(format_briefing(briefing))

    # Also output JSON for programmatic use
    print("\n\n📦 Raw Data (JSON):")
    print(json.dumps(briefing, indent=2, ensure_ascii=False))
