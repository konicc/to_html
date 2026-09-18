from pathlib import Path
import win32com.client

# 변환할 HWP 파일 — 실제 파일 경로로 수정
input_path = Path(r"C:\Users\Cotax\Desktop\k\to_html\text_hwpx.hwpx")

# 원본 옆의 html_output 폴더에 저장
output_dir = input_path.parent / "html_output"
output_path = output_dir / f"{input_path.stem}.html"

if not input_path.is_file():
    raise FileNotFoundError(f"파일을 찾을 수 없습니다: {input_path}")

output_dir.mkdir(parents=True, exist_ok=True)

# 기존 결과를 실수로 덮어쓰지 않도록 확인
if output_path.exists():
    raise FileExistsError(f"이미 결과 파일이 있습니다: {output_path}")

hwp = win32com.client.DispatchEx("HWPFrame.HwpObject")

try:
    hwp.XHwpWindows.Item(0).Visible = True

    print("1. 문서 열기 시작")
    opened = hwp.Open(str(input_path.resolve()), "", "")
    print("2. 문서 열기 결과:", opened)

    if not opened:
        raise RuntimeError("문서를 열지 못했습니다.")

    print("3. HTML 저장 시작")
    print("저장 경로:", output_path.resolve())

    saved = hwp.SaveAs(str(output_path.resolve()), "HTML", "")
    print("4. 저장 결과:", saved)
    print("5. 실제 파일 존재:", output_path.exists())

except Exception as e:
    print("오류 종류:", type(e).__name__)
    print("오류 내용:", e)

finally:
    input("결과를 확인한 뒤 Enter를 누르면 한글을 종료합니다.")
    hwp.Quit()