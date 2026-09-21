import sys

from pathlib import Path
import mammoth

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


if output_path.exists():
    raise FileExistsError(f"이미 결과 파일이 있습니다: {output_path}")

# DOCX를 읽어 HTML 본문으로 변환
with input_path.open("rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)

# 브라우저에서 열 수 있는 완전한 HTML 문서 구성
html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>DOCX 변환 결과</title>
    <style>
        body {
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 20px;
            font-family: "맑은 고딕", sans-serif;
            line-height: 1.7;
        }
        table {
            border-collapse: collapse;
            max-width: 100%;
        }
        td, th {
            border: 1px solid #aaa;
            padding: 8px;
        }
        img {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
""" + result.value + """
</body>
</html>
"""

output_path.write_text(html_content, encoding="utf-8")
print(f"변환 완료: {output_path}")

# 변환 중 발생한 주의 메시지 출력
for message in result.messages:
    print(f"[{message.type}] {message.message}")