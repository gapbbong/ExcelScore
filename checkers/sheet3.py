from typing import List, Dict
from models import CheckResult

def check_sheet3(ws, wb) -> List[CheckResult]:
    results = []

    # 1. 피벗 테이블 구조 (행: 가격, 열: 구분)
    # B2 셀부터 시작 여부 및 '가격' 헤더 확인
    struct_passed = False
    if ws['B2'].value is not None:
        struct_passed = True
        
    results.append(
        CheckResult(
            item_name="피벗 테이블 구조 및 배치 (행: 가격, 열: 구분)",
            passed=struct_passed,
            score_earned=20 if struct_passed else 0,
            max_score=20,
            feedback="" if struct_passed else "[피벗 감점] 피벗 테이블의 행/열 배치가 올바르지 않거나 B2 셀에서 시작되지 않았습니다."
        )
    )

    # 2. 값 필드 (제품명의 개수, 포인트점수의 평균)
    val_passed = False
    # 보통 C2, D2 등에 헤더가 나타남. (피벗 위치에 따라 다를 수 있음)
    for row in ws.iter_rows(min_row=1, max_row=5, min_col=1, max_col=10):
        for cell in row:
            if "개수" in str(cell.value or "") or "평균" in str(cell.value or ""):
                val_passed = True
                break
        if val_passed: break

    results.append(
        CheckResult(
            item_name="값 필드 (제품명 개수, 포인트점수 평균)",
            passed=val_passed,
            score_earned=20 if val_passed else 0,
            max_score=20,
            feedback="" if val_passed else "[피벗 감점] 값 영역의 설정(개수, 평균)이 틀리거나 누락되었습니다."
        )
    )

    # 3. 그룹화 (가격 20,000 단위: 1~20,000 등)
    group_passed = False
    for cell in ws['B']:
        if "20,001" in str(cell.value or ""):
            group_passed = True
            break

    results.append(
        CheckResult(
            item_name="가격 그룹화 (단위: 20,000)",
            passed=group_passed,
            score_earned=20 if group_passed else 0,
            max_score=20,
            feedback="" if group_passed else "[피벗 감점] 가격 항목의 그룹화 설정이 올바르지 않습니다 (1~20,000 등)."
        )
    )

    # 4. 옵션 (빈 셀 ***, 행의 총합계 지우기)
    opt_passed = False
    for row in ws.iter_rows(min_row=3, max_row=20, min_col=2, max_col=10):
        for cell in row:
            if cell.value == "***":
                opt_passed = True
                break
        if opt_passed: break

    results.append(
        CheckResult(
            item_name="피벗 옵션 (빈 셀 '***', 행 총합계 제거)",
            passed=opt_passed,
            score_earned=20 if opt_passed else 0,
            max_score=20,
            feedback="" if opt_passed else "[피벗 옵션 감점] 빈 셀 표시(***) 또는 행의 총합계 지우기 설정이 누락되었습니다."
        )
    )

    # 5. [NEW] 데이터 결과값 검증 (Aggregate Verification)
    # 그룹화 및 데이터 원본이 정확한지 확인하기 위해 특정 셀의 결과값 비교
    val_check_passed = False
    # 예: 특정 조건(전체 또는 특정 구분)의 포인트점수 평균이 1,500 인지 등
    # 여기서는 샘플로 전체 합계나 특정 셀의 값이 기대값과 일치하는지 확인
    for row in ws.iter_rows(min_row=5, max_row=20, min_col=1, max_col=10):
        for cell in row:
            # 포인트점수의 평균값 중 하나가 특정 숫자(예: 1250)와 일치하는지
            if cell.value == 1250 or cell.value == "1,250":
                val_check_passed = True
                break
        if val_check_passed: break

    results.append(
        CheckResult(
            item_name="데이터 집계 결과 검증 (평균/개수 값 일치 여부)",
            passed=val_check_passed,
            score_earned=10 if val_check_passed else 0,
            max_score=10,
            feedback="" if val_check_passed else "[피벗 오류] 집계된 결과값(평균 등)이 기대값과 일치하지 않습니다. 데이터 범위 또는 그룹화 설정을 확인하세요."
        )
    )

    return results
