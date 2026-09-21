import argparse
import subprocess
import sys
from pathlib import Path

# main.py가 있는 폴더
BASE_DIR = Path(__file__).resolve().parent

# 확장자별 변환 코드
CONVERTERS = {
    ".hwp": "02_hwp_to_html.py",
    ".hwpx": "02_hwp_to_html.py",
    ".docx": "03_docx_to_html.py",
    ".xlsx": "04_xlsx_to_html.py",
    ".pdf": "07_pdf_all_pages.py",
    ".pptx": "11_pptx_all_slides.py",
}


def main():
    # 실행 명령에서 파일 경로 받기
    parser = argparse.ArgumentParser(
        description="문서 파일을 HTML로 변환합니다."
    )
    parser.add_argument(
        "file",
        help="변환할 문서 파일 경로",
    )
    args = parser.parse_args()

    input_path = Path(args.file).expanduser().resolve()

    # 입력 파일 확인
    if not input_path.is_file():
        print(f"파일을 찾을 수 없습니다: {input_path}")
        return 1

    # 대문자 확장자도 처리: .PDF → .pdf
    extension = input_path.suffix.lower()
    script_name = CONVERTERS.get(extension)

    if script_name is None:
        print(f"지원하지 않는 확장자입니다: {extension or '(없음)'}")
        print("지원 형식:", ", ".join(CONVERTERS))
        return 1

    script_path = BASE_DIR / script_name

    if not script_path.is_file():
        print(f"변환 코드를 찾을 수 없습니다: {script_path}")
        return 1

    print(f"입력 파일: {input_path.name}", flush=True)
    print(f"파일 형식: {extension}", flush=True)
    print(f"실행 코드: {script_name}", flush=True)

    try:
        # 현재 Python 환경으로 해당 변환 코드 실행
        # 변환 코드의 출력은 터미널에 그대로 표시
        subprocess.run(
            [
                sys.executable,
                "-u",
                str(script_path),
                str(input_path),
            ],
            check=True,
        )

    except subprocess.CalledProcessError as error:
        print(f"\n변환 실패: 종료 코드 {error.returncode}")
        print("위에 출력된 오류 내용을 확인해주세요.")
        return 1

    print("\n변환 프로그램 실행이 종료됐습니다.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())