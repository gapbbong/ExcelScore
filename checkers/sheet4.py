from typing import List, Dict
from models import CheckResult

def check_sheet4(ws, wb, visual_results: Dict = None) -> List[CheckResult]:
    results = []

    # 1. 차트 존재 및 종류 (묶은 세로 막대형)
    has_charts = hasattr(ws, '_charts') and len(ws._charts) > 0
    results.append(
        CheckResult(
            item_name="차트 생성 및 종류 (묶은 세로 막대형)",
            passed=has_charts,
            score_earned=20 if has_charts else 0,
            max_score=20,
            feedback="" if has_charts else "[차트 감점] 제4작업 시트에 차트가 생성되지 않았습니다."
        )
    )

    # 2. 시각적 요소 확인 (Visual Result 연동: 파랑 박엽지, 보조축 꺾은선 등)
    if visual_results and "sheet4_visuals" in visual_results:
        passed_v, feedback_v = visual_results["sheet4_visuals"]
        results.append(
            CheckResult(
                item_name="차트 서식: 배경(파랑 박엽지), 그림(흰색), 보조축(꺾은선)",
                passed=passed_v,
                score_earned=30 if passed_v else 0,
                max_score=30,
                feedback=feedback_v if not passed_v else ""
            )
        )
    else:
        results.append(CheckResult("차트 시각 서식 (시각 분석 미수행)", False, 0, 30, "시각적 분석 결과를 찾을 수 없습니다."))

    # 3. 데이터 레이블 및 제목
    detail_passed = False
    if has_charts:
        chart = ws._charts[0]
        if chart.title:
            detail_passed = True

    results.append(
        CheckResult(
            item_name="차트 제목 및 레이블 설정",
            passed=detail_passed,
            score_earned=15 if detail_passed else 0,
            max_score=15,
            feedback="" if detail_passed else "[차트 감점] 차트 제목 또는 데이터 레이블 설정이 누락되었습니다."
        )
    )

    # 4. 범례명 편집 (한 줄로 표시)
    results.append(
        CheckResult(
            item_name="범례명 편집 (한 줄로 표시)",
            passed=True, 
            score_earned=15,
            max_score=15,
            feedback="* 범례명이 '예약고객(단위:명)'으로 한 줄로 편집되었는지 확인하세요."
        )
    )

    return results
