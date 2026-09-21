import sys

from pathlib import Path
import win32com.client

if len(sys.argv) != 2:
    raise SystemExit("변환할 파일 경로를 인자로 전달해주세요.")

input_path = Path(sys.argv[1]).expanduser().resolve()

# .py 파일이 있는 main 폴더의 상위 폴더 = to_html
project_dir = Path(__file__).resolve().parent.parent

# 변환 결과를 to_html/test_html 아래에 저장
extension = input_path.suffix.lower().lstrip(".")

output_dir = (
    project_dir
    / "test_html"
    / f"{input_path.stem}_{extension}"
)

output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "index.html"

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
    raise

finally:
    hwp.Quit()