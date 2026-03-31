import re
from typing import List
from models import CheckResult

def check_sheet2(ws, wb) -> List[CheckResult]:
    results = []
    
    # 1. B2 데이터 붙여넣기
    b2_has_data = ws['B2'].value is not None
    results.append(
        CheckResult(
            item_name="제1작업 데이터 복사 위치 (B2)",
            passed=b2_has_data,
            score_earned=3 if b2_has_data else 0,
            max_score=3,
            feedback="" if b2_has_data else "[제2작업 감점] B2 영역부터 데이터가 시작되지 않습니다."
        )
    )

    # 2. 고급 필터 조건 위치 검사 (B14)
    has_condition = ws['B14'].value is not None or ws['C14'].value is not None
    results.append(
        CheckResult(
            item_name="고급 필터 조건 위치 (B14)",
            passed=has_condition,
            score_earned=7 if has_condition else 0,
            max_score=7,
            feedback="" if has_condition else "[제2작업 감점] B14 셀에 고급 필터 조건이 기입되지 않았습니다."
        )
    )

    # 3. 고급 필터 결과 위치 검사 (B18)
    has_result = ws['B18'].value is not None
    results.append(
        CheckResult(
            item_name="고급 필터 결과 위치 (B18)",
            passed=has_result,
            score_earned=5 if has_result else 0,
            max_score=5,
            feedback="" if has_result else "[제2작업 감점] B18 셀에 고급 필터 결과가 추출되지 않았습니다."
        )
    )

    # 4. 표 서식 (보통 6번)
    has_table_format = False
    if hasattr(ws, 'tables') and ws.tables:
        for table in ws.tables.values():
            if table.tableStyleInfo and table.tableStyleInfo.name == "TableStyleMedium6":
                has_table_format = True

    results.append(
        CheckResult(
            item_name="표 스타일 '보통 6번' 적용 여부",
            passed=has_table_format,
            score_earned=5 if has_table_format else 0,
            max_score=5,
            feedback="" if has_table_format else "[제2작업 감점] 결과 셀의 채우기가 '없음'으로 설정되거나 표 스타일 '보통 6번'이 적용되지 않았습니다."
        )
    )

    return results
