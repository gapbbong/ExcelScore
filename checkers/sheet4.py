from typing import List
from models import CheckResult

def check_sheet4(ws, wb) -> List[CheckResult]:
    results = []
    
    # 1. 차트 존재 유무
    has_charts = hasattr(ws, '_charts') and getattr(ws, '_charts', [])
    num_charts = len(ws._charts) if has_charts else 0
    results.append(
        CheckResult(
            item_name="제4작업 차트 생성 유무",
            passed=num_charts > 0,
            score_earned=10 if num_charts > 0 else 0,
            max_score=10,
            feedback="" if num_charts > 0 else "[제4작업 차트 감점] 제4작업 시트에 차트 객체가 생성되지 않았습니다."
        )
    )

    if num_charts > 0:
        chart = ws._charts[0]
        # openpyxl의 chart.type을 가져와 묶은 세로 막대형 계열인지 파악
        chart_type = type(chart).__name__
        is_bar = "BarChart" in chart_type or "Bar" in chart_type
        
        results.append(
            CheckResult(
                item_name="묶은 세로 막대형 차트 생성",
                passed=is_bar,
                score_earned=5 if is_bar else 0,
                max_score=5,
                feedback="" if is_bar else f"[제4작업 차트 감점] 기본 바탕 차트가 묶은 세로 막대형이 아닙니다. (발견된 차트: {chart_type})"
            )
        )
    else:
        results.append(
            CheckResult(
                item_name="묶은 세로 막대형 차트 생성",
                passed=False,
                score_earned=0,
                max_score=5,
                feedback="[제4작업 차트 감점] 차트가 없습니다."
            )
        )

    # 파이썬으로 평가하기 어려운 상세 UI (보조 축, 데이터 범위 6개, 도형 삽입, 범례 1줄 지정, 축 서식 등) 안내
    results.append(
        CheckResult(
            item_name="[수동확인] 혼합 차트(보조 축), 데이터 레이블, 설명선 도형, 축 눈금 등",
            passed=True,
            score_earned=0,
            max_score=0,
            feedback="* openpyxl 분석 한계: 보조 축 선, 꺾은선형 마름모 표식, 설명선 도형, 범례 1줄 수정, 눈금선(파선) 등 세부 디자인 요소는 엑셀 파일을 직접 열어서 확인해주세요."
        )
    )

    return results
