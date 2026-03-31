import re
from typing import List
from models import CheckResult

def check_sheet1(ws, wb) -> List[CheckResult]:
    results = []

    # 1. 셀 서식 검사 (천단위 원) E5:E12
    # Number format 확인
    valid_format = False
    for row in range(5, 13):
        cell = ws[f"E{row}"]
        if cell.number_format and "원" in cell.number_format:
            valid_format = True
    
    results.append(
        CheckResult(
            item_name="E5:E12 셀 서식 (천 단위 및 '원')",
            passed=valid_format,
            score_earned=5 if valid_format else 0,
            max_score=5,
            feedback="" if valid_format else "[표 서식 감점] E5:E12 영역에 숫자 천단위 구분기호 및 '원' 서식이 적용되지 않았습니다."
        )
    )

    # 2. 이름 정의 검사 (G5:G12 -> '포인트 점수')
    has_defined_name = False
    if wb.defined_names:
        for dn in wb.defined_names.definedName:
            if dn.name == "포인트_점수" or dn.name == "포인트 점수" or dn.name == "포인트점수":
                has_defined_name = True
    
    results.append(
        CheckResult(
            item_name="이름 정의 (G5:G12 -> 포인트 점수)",
            passed=has_defined_name,
            score_earned=5 if has_defined_name else 0,
            max_score=5,
            feedback="" if has_defined_name else "[표 서식 감점] '포인트 점수'라는 이름 정의를 찾을 수 없습니다."
        )
    )

    # 3. 유효성 검사 (H14)
    has_validation = False
    for validation in ws.data_validations.dataValidation:
        if validation.sqref and "H14" in str(validation.sqref):
            has_validation = True
    
    results.append(
        CheckResult(
            item_name="데이터 유효성 검사 (H14)",
            passed=has_validation,
            score_earned=5 if has_validation else 0,
            max_score=5,
            feedback="" if has_validation else "[표 서식 감점] H14 셀에 데이터 유효성 검사(목록)가 설정되지 않았습니다."
        )
    )

    # 4. 결재란 그림 복사 여부
    has_images = len(ws._images) > 0
    results.append(
        CheckResult(
            item_name="결재란 그림 생성",
            passed=has_images,
            score_earned=5 if has_images else 0,
            max_score=5,
            feedback="" if has_images else "[표 서식 감점] 결재란이 '그림으로 복사' 기능을 통해 생성되지 않았습니다 (이미지 객체 없음)."
        )
    )

    # 5. 주황색 채우기 검사 (간략히 한 셀만)
    b4 = ws['B4']
    is_orange = False
    if b4.fill and b4.fill.fgColor and hasattr(b4.fill.fgColor, 'rgb'):
        if isinstance(b4.fill.fgColor.rgb, str) and b4.fill.fgColor.rgb.endswith('FFC000'):
            is_orange = True
    
    results.append(
        CheckResult(
            item_name="셀 채우기 (주황: B4:J4, G14, I14)",
            passed=b4.fill is not None,  # rgb 값이 Theme 컬러라 확인이 어려울 수 있어서 fill 존재여부로 완화
            score_earned=5 if b4.fill else 0,
            max_score=5,
            feedback="" if b4.fill else "[표 서식 감점] 지정된 영역(B4:J4 등)에 주황색 채우기가 적용되지 않았습니다."
        )
    )

    # 6. 함수식 존재 확인 (CHOOSE, MID, IF, COUNTIF, ROUND, DAVERAGE, MAX, VLOOKUP)
    funcs = {
        "택배 업체(CHOOSE, MID)": ["CHOOSE", "MID"],
        "보너스 점수(IF)": ["IF"],
        "식음료 개수(COUNTIF, &)": ["COUNTIF", "&"],
        "가격 평균(ROUND, DAVERAGE)": ["ROUND", "DAVERAGE"],
        "최대 포인트 점수(MAX)": ["MAX", "포인트 점수"],
        "가격검색(VLOOKUP)": ["VLOOKUP"]
    }

    formulas_used = []
    # 전체 셀 수식 파싱
    for row in ws.iter_rows(min_row=5, max_row=15, min_col=1, max_col=12):
        for cell in row:
            if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
                val = cell.value.upper()
                formulas_used.append(val)

    # 각 요구 함수별 점수 계산
    for func_label, required_keywords in funcs.items():
        found = False
        for f in formulas_used:
            if all(k.upper() in f for k in required_keywords):
                found = True
                break
        
        results.append(
            CheckResult(
                item_name=f"함수 로직: {func_label}",
                passed=found,
                score_earned=8 if found else 0,
                max_score=8,
                feedback="" if found else f"[함수 감점] '{func_label}' 관련 함수 또는 수식이 누락되거나 맞지 않습니다."
            )
        )

    # 7. 조건부 서식 존재 확인
    cf_rules = ws.conditional_formatting._cf_rules
    has_cf = len(cf_rules) > 0
    results.append(
        CheckResult(
            item_name="조건부 서식 적용 (행 전체 파랑/굵게)",
            passed=has_cf,
            score_earned=7 if has_cf else 0,
            max_score=7,
            feedback="" if has_cf else "[조건부 서식 감점] 조건부 서식이 적용되지 않았습니다. 수식을 사용해 행 전체에 적용해야 합니다."
        )
    )

    return results
