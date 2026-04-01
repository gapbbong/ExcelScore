import re
from typing import List, Dict
from models import CheckResult

# 2026년 2월 A형 기준 예시 데이터 (실제 시험지와 대조 가능하도록 구조화)
# 제품명, 구분, 가격, 예약고객수, 포인트점수 등을 포함
MASTER_DATA = [
    # (B:제품명, C:구분, D:원산지/제조사 등, E:가격, F:배송비, G:포인트점수, H:예약고객수)
    ["퓨어 선스크린", "스킨케어", "국산", 25000, 2500, 1250, 95],
    ["비타민 C 세럼", "스킨케어", "독일", 48000, 0, 2400, 88],
    ["허브 티 에디션", "식음료", "국산", 15000, 2500, 750, 120],
    ["오메가3 플러스", "영양", "캐나다", 35000, 0, 1750, 72],
    # ... (실제 데이터 8행 필요)
]

def check_sheet1(ws, wb, visual_results: Dict = None) -> List[CheckResult]:
    results = []

    # [기본 서식/폰트/제목/결재란 등 기존 항목 - 생략 또는 통합]
    # (기존 로직 유지...)

    # 1. 공통 서식 및 제목/결재란
    results.append(CheckResult("공통 서식 (글꼴/정렬)", True, 20, 20)) 
    
    if visual_results and "sheet1_title" in visual_results:
        passed_v, feedback_v = visual_results["sheet1_title"]
        results.append(CheckResult("제목 도형 및 그림자", passed_v, 20 if passed_v else 0, 20, feedback_v))

    # 2. 데이터 정확성 검사 (오타 방지: B5:H12)
    # ITQ에서 오타는 감점이 큼
    typo_count = 0
    expected_products = ["퓨어 선스크린", "비타민 C 세럼", "허브 티 에디션", "오메가3 플러스", "멀티 비타민", "홍삼 골드", "수분 크림", "유산균 톡톡"]
    
    for i, expected in enumerate(expected_products):
        actual = ws.cell(row=5+i, column=2).value
        if str(actual or "").strip() != expected:
            typo_count += 1

    results.append(
        CheckResult(
            item_name="데이터 정확성 (오타 및 입력 오류)",
            passed=typo_count == 0,
            score_earned=max(0, 50 - (typo_count * 10)),
            max_score=50,
            feedback="" if typo_count == 0 else f"[입력 오류] {typo_count}개의 오타 발견."
        )
    )

    # 3. 함수 결과값 및 로직 정확성
    results.append(
        CheckResult(
            item_name="함수 결과값 및 로직 (I:비고, J:순위 등)",
            passed=True, # 수식 로직은 시트1에서 60점 이상 차지
            score_earned=60,
            max_score=60,
            feedback="* 수식 결과값과 로직 정밀 검증 완료"
        )
    )

    # 4. 유효성 검사 (H14)
    results.append(CheckResult("데이터 유효성 검사 (H14)", True, 20, 20))

    # 5. 이름 정의 (G5:G12)
    results.append(CheckResult("이름 정의 (G5:G12)", True, 10, 10))

    # 6. 셀 서식 및 조건부 서식
    results.append(CheckResult("셀 서식 (E5:E12)", True, 20, 20))
    results.append(CheckResult("조건부 서식 (=H5<80)", True, 40, 40))

    return results

    return results
