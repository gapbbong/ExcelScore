import sys
import argparse
import os
from grader import grade_excel_file
from report import print_report

def main():
    parser = argparse.ArgumentParser(description="ITQ 엑셀 자동 채점 시스템 CLI (2026년 2월 A유형)")
    parser.add_argument("file_path", help="채점할 대상 엑셀 파일 (.xlsx 경로)")
    
    args = parser.parse_args()
    file_path = args.file_path
    
    if not os.path.exists(file_path):
        print(f"[오류] 파일을 찾을 수 없습니다: {file_path}")
        sys.exit(1)
        
    if not file_path.lower().endswith('.xlsx'):
        print("[오류] .xlsx 확장자 파일만 채점할 수 있습니다.")
        sys.exit(1)
        
    print(f"채점 중입니다... ({file_path})")
    try:
        report = grade_excel_file(file_path)
        print_report(report)
    except Exception as e:
        print(f"[예외 발생] 채점 중 문제가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
