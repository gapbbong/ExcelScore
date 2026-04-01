import win32com.client
from PIL import ImageGrab
import os
import time
import pythoncom
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def capture_excel_screenshots(file_path: str, output_dir: str):
    """
    엑셀 파일을 열어 주 시트들의 스크린샷을 찍어 저장합니다.
    pywin32와 Pillow(ImageGrab)를 사용합니다.
    """
    # COM 초기화 (멀티스레딩 환경 대비)
    pythoncom.CoInitialize()
    
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        logger.error(f"File not found: {abs_path}")
        return {}

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    excel = None
    wb = None
    screenshots = {}

    try:
        # Excel 어플리케이션 실행
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False  # 쥐도 새도 모르게 (백그라운드 실행)
        excel.DisplayAlerts = False
        excel.ScreenUpdating = False # 화면 갱신 억제

        wb = excel.Workbooks.Open(abs_path)
        
        # ITQ 엑셀에서 필요한 시트들
        target_sheets = ["제1작업", "제2작업", "제3작업", "제4작업"]
        
        for sheet_name in target_sheets:
            try:
                ws = wb.Worksheets(sheet_name)
                ws.Activate()
                
                # 시트 전체 영역 또는 필요한 데이터 영역 복사
                # xlScreen = 1, xlPicture = 2
                ws.UsedRange.CopyPicture(1, 2)
                time.sleep(1.0)  # 클립보드 복사 대기
                
                img = ImageGrab.grabclipboard()
                if img:
                    img_path = os.path.join(output_dir, f"{sheet_name}.png")
                    img.convert("RGB").save(img_path, "PNG")
                    screenshots[sheet_name] = img_path
                    logger.info(f"Screenshot saved: {img_path}")
                else:
                    logger.warning(f"Failed to grab clipboard for {sheet_name}")
            except Exception as e:
                logger.error(f"Error capturing {sheet_name}: {e}")

    except Exception as e:
        logger.error(f"Excel automation error: {e}")
    finally:
        if wb:
            wb.Close(False)
        if excel:
            excel.Quit()
        pythoncom.CoUninitialize()

    return screenshots

if __name__ == "__main__":
    # 간단한 테스트용
    import sys
    if len(sys.argv) > 1:
        capture_excel_screenshots(sys.argv[1], "screenshots_test")
