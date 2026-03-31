import os
import re
import math
from typing import List
from models import CheckResult

def check_base_structure(file_path: str, wb) -> List[CheckResult]:
    results = []
    # 1. 파일명 검사
    filename = os.path.basename(file_path)
    pattern = r'^\d+-[가-힣]+\.xlsx$'
    is_valid_name = bool(re.match(pattern, filename))
    results.append(
        CheckResult(
            item_name="파일명 규칙",
            passed=is_valid_name,
            score_earned=10 if is_valid_name else 0,
            max_score=10,
            feedback="" if is_valid_name else f"[파일명 감점] 작성 파일명: '{filename}'. 올바른 형식은 '수험번호-이름.xlsx' 입니다."
        )
    )
    
    # 2. 시트 구성 및 순서 검사
    expected_sheets = ["제1작업", "제2작업", "제3작업", "제4작업"]
    actual_sheets = wb.sheetnames
    
    extra_sheets = [s for s in actual_sheets if s not in expected_sheets]
    has_extra = len(extra_sheets) > 0
    results.append(
        CheckResult(
            item_name="불필요한 시트 검사",
            passed=not has_extra,
            score_earned=5 if not has_extra else 0,
            max_score=5,
            feedback="" if not has_extra else f"[시트 감점] 남아있는 불필요한 시트: {', '.join(extra_sheets)}"
        )
    )
    
    # 앞쪽 4개 시트가 제1~제4 순서인지 확인
    is_ordered = actual_sheets[:min(4, len(actual_sheets))] == expected_sheets[:min(4, len(actual_sheets))]
    # 모든 시트가 존재하는지 확인
    all_exist = all(s in actual_sheets for s in expected_sheets)
    passed_order = (is_ordered and all_exist)

    results.append(
        CheckResult(
            item_name="시트 순서 검사",
            passed=passed_order,
            score_earned=5 if passed_order else 0,
            max_score=5,
            feedback="" if passed_order else "[시트 감점] 시트 순서가 올바르지 않거나 누락된 시트가 있습니다. (제1작업~제4작업 순서)"
        )
    )
    
    # 3. 열 너비 검사
    for sheet_name in ["제1작업", "제2작업", "제3작업"]:
        if sheet_name in actual_sheets:
            ws = wb[sheet_name]
            col_a = ws.column_dimensions['A']
            width = col_a.width if col_a else None
            # 열 너비가 1 언저리로 설정되었는지 확인
            # openpyxl에서 1 이면 대략 1.x 언저리로 표시되기도 함
            is_valid_width = width is not None and width < 2.0
            results.append(
                CheckResult(
                    item_name=f"{sheet_name} A열 너비",
                    passed=is_valid_width,
                    score_earned=5 if is_valid_width else 0,
                    max_score=5,
                    feedback="" if is_valid_width else f"[열너비 감점] {sheet_name}의 A열 너비가 1이 아닙니다."
                )
            )

    return results
