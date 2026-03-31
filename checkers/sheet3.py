from typing import List
from models import CheckResult

def check_sheet3(ws, wb) -> List[CheckResult]:
    results = []
    
    # 1. 피벗 테이블 존재 유무
    has_pivots = hasattr(ws, '_pivots') and len(ws._pivots) > 0
    results.append(
        CheckResult(
            item_name="피벗 테이블 생성 유무",
            passed=has_pivots,
            score_earned=10 if has_pivots else 0,
            max_score=10,
            feedback="" if has_pivots else "[제3작업 피벗 감점] 피벗 테이블 객체가 생성되지 않았습니다."
        )
    )

    # 2. 피벗 테이블 시작 위치 (B2)
    b2_has_data = ws['B2'].value is not None
    results.append(
        CheckResult(
            item_name="피벗 테이블 시작 위치 (B2)",
            passed=b2_has_data,
            score_earned=5 if b2_has_data else 0,
            max_score=5,
            feedback="" if b2_has_data else "[제3작업 피벗 감점] 피벗 테이블이 B2 셀에서 시작되지 않았습니다."
        )
    )

    # 3. 빈 셀 *** 옵션 적용 스캔 (데이터 영역을 파싱하여 육안으로 설정되었는지 유추)
    found_stars = False
    for row in ws.iter_rows(min_row=3, max_row=15, min_col=2, max_col=10):
        for cell in row:
            if cell.value == "***":
                found_stars = True
                break
    
    results.append(
        CheckResult(
            item_name="빈 셀 '***' 표시",
            passed=found_stars,
            score_earned=5 if found_stars else 0,
            max_score=5,
            feedback="" if found_stars else "[제3작업 피벗 감점] 피벗 테이블 빈 셀에 '***' 문자열이 감지되지 않았습니다."
        )
    )

    # 4. 정렬, 그룹화, 총합계 파악 (Python openpyxl로 상세XML을 모두 처리하긴 무리이므로 기본점수 처리 후 안내)
    results.append(
        CheckResult(
            item_name="[수동확인] 그룹화(20,000단위), 내림차순 정렬, 총합계 삭제",
            passed=True,
            score_earned=0,
            max_score=0,
            feedback="* openpyxl 분석 한계: 가격 그룹화, 내림차순 정렬, 레이블 병합 및 행 총합계 삭제 여부는 엑셀을 열어서 직접 확인 바랍니다."
        )
    )

    return results
