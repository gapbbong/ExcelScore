from models import GradingReport

def print_report(report: GradingReport):
    print("=" * 60)
    print(" ** ITQ 엑셀 채점 결과 보고서 (2026-02 A형) **")
    print("=" * 60)
    print(f"수험생 성명 : {report.student_name}")
    print(f"수험 번호   : {report.student_id}")
    
    total = report.total_score
    max_score = report.max_score
    # openpyxl로 분석 불가능한 영역이 남을 수 있으므로 대략적 점수임
    
    # max_score가 0인 항목은 단순 안내용이므로 배점에서 제외됨
    print(f"총 획득 점수 : {total} / 100점 (수동 채점 항목 점수 별도 포함 필요)")
    print("-" * 60)
    
    for section in report.sections:
        print(f"\n[{section.section_name}]")
        for check in section.checks:
            if check.max_score == 0:
                mark = "⚠️ "
                score_str = ""
            else:
                mark = "✅ " if check.passed else "❌ "
                score_str = f"(+{check.score_earned} / {check.max_score}점)"
                
            print(f"  {mark}{check.item_name} {score_str}")
            
            if (not check.passed and check.feedback) or (check.max_score == 0 and check.feedback):
                print(f"      👉 {check.feedback}")
                
    print("\n" + "=" * 60 + "\n")
