import sys

from pathlib import Path
import pymupdf

if len(sys.argv) != 2:
    raise SystemExit("변환할 파일 경로를 인자로 전달해주세요.")

input_path = Path(sys.argv[1]).expanduser().resolve()

# 문서 이름과 확장자로 결과 폴더 구분
extension = input_path.suffix.lower().lstrip(".")

output_dir = (
    Path(__file__).resolve().parent
    / "html_output"
    / f"{input_path.stem}_{extension}"
)

output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "index.html"

image_dir = output_dir / "images"
image_dir.mkdir(parents=True, exist_ok=True)

if not input_path.is_file():
    raise FileNotFoundError(f"파일을 찾을 수 없습니다: {input_path}")

image_dir.mkdir(parents=True, exist_ok=True)

# 일반 문자열이므로 CSS 중괄호를 한 개씩 사용
html_header = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>PDF 변환 결과</title>
    <style>
        body {
            margin: 0;
            padding: 24px;
            background: #eeeeee;
            font-family: "맑은 고딕", sans-serif;
        }
        section {
            margin-bottom: 32px;
        }
        h2 {
            font-size: 16px;
            color: #555555;
        }
        .page {
            position: relative;
            background: white;
            overflow: hidden;
        }
        .page-image {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            user-select: none;
        }
        .text-layer {
            position: absolute;
            inset: 0;
            user-select: text;
        }
        .text-layer > div {
            position: relative;
            background: transparent !important;
        }
        .text-layer p {
            position: absolute;
            white-space: pre;
            margin: 0;
            padding: 0;
        }
        .text-layer p,
        .text-layer span {
            color: transparent !important;
            background: transparent !important;
        }
        .text-layer ::selection {
            background: rgba(0, 120, 255, 0.3);
            color: transparent;
        }
    </style>
</head>
<body>
"""

print("PDF 전체 변환 시작", flush=True)

with pymupdf.open(input_path) as document:
    if document.needs_pass:
        raise RuntimeError("암호가 걸린 PDF입니다.")

    if len(document) == 0:
        raise RuntimeError("페이지가 없는 PDF입니다.")

    # 현재 버전은 회전되지 않은 페이지 기준
    rotated_pages = [
        i + 1
        for i, page in enumerate(document)
        if page.rotation != 0
    ]

    if rotated_pages:
        raise RuntimeError(
            f"회전된 페이지의 좌표 보정이 필요합니다: {rotated_pages}"
        )

    flags = pymupdf.TEXTFLAGS_HTML & ~pymupdf.TEXT_PRESERVE_IMAGES

    # 페이지별로 바로 기록하여 HTML 전체를 메모리에 쌓지 않음
    with output_path.open("w", encoding="utf-8") as html_file:
        html_file.write(html_header)

        for page_number, page in enumerate(document, start=1):
            width = page.rect.width
            height = page.rect.height

            # 1. 페이지 이미지를 PNG 파일로 저장
            image_name = f"page_{page_number:04d}.png"
            image_path = image_dir / image_name

            pixmap = page.get_pixmap(dpi=144, alpha=False)
            pixmap.save(image_path)
            del pixmap

            # 2. 선택·복사용 텍스트 추출
            text_html = page.get_text("html", flags=flags)

            # 3. 이미지와 투명 텍스트를 겹쳐서 HTML에 추가
            page_html = f"""
<section>
    <h2>{page_number} / {len(document)}페이지</h2>
    <div class="page"
         style="width: {width}pt; height: {height}pt;">
        <img
            class="page-image"
            src="images/{image_name}"
            alt="{page_number}페이지"
            loading="lazy"
            draggable="false"
        >
        <div class="text-layer">
            {text_html}
        </div>
    </div>
</section>
"""
            html_file.write(page_html)

            print(
                f"{page_number}/{len(document)}페이지 처리 완료",
                flush=True,
            )

        html_file.write("</body></html>")

print(f"변환 완료: {output_path}")