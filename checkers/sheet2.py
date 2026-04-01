from typing import List, Dict
from models import CheckResult

def check_sheet2(ws, wb) -> List[CheckResult]:
    results = []
    
    # 1. 제1작업 B4:H12 -> 제2작업 B2 복사
    ws1 = wb["제1작업"]
    copy_passed = False
    if ws['B2'].value == ws1['B4'].value and ws['H10'].value == ws1['H12'].value:
        copy_passed = True

    results.append(
        CheckResult(
            item_name="데이터 복사 (B4:H12 -> B2)",
            passed=copy_passed,
            score_earned=20 if copy_passed else 0,
            max_score=20,
            feedback="" if copy_passed else "[필터 감점] 제1작업의 데이터가 제2작업 B2 셀에 정확히 복사되지 않았습니다."
        )
    )

    # 2. 고급 필터 (B18부터 결과)
    # 조건: 구분 <> "스킨케어" AND 예약고객수 >= 90
    filter_passed = False
    if ws['B18'].value == ws1['B4'].value: # 헤더 일치 확인
        filter_passed = True
    
    results.append(
        CheckResult(
            item_name="고급 필터 (구분<>스킨케어, 예약고객수>=90)",
            passed=filter_passed,
            score_earned=40 if filter_passed else 0,
            max_score=40,
            feedback="" if filter_passed else "[필터 감점] 고급 필터 조건이 맞지 않거나 결과 위치(B18)가 틀립니다."
        )
    )

    # 3. 표 서식 (표 스타일 보통 6, 머리글/줄무늬 행)
    table_passed = False
    if hasattr(ws, 'tables') and ws.tables:
        for table in ws.tables.values():
            if table.tableStyleInfo and table.tableStyleInfo.name == "TableStyleMedium6":
                if table.headerRow and table.showRowStripes:
                    table_passed = True
                    break

    results.append(
        CheckResult(
            item_name="표 서식 (스타일 보통 6, 머리글/줄무늬 행)",
            passed=table_passed,
            score_earned=20 if table_passed else 0,
            max_score=20,
            feedback="" if table_passed else "[표서식 감점] 표 스타일(보통 6) 또는 옵션(머리글/줄무늬 행)이 올바르지 않습니다."
        )
    )

    return results
