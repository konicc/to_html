from pathlib import Path
from html import escape
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

# 방금 확인한 PPTX 파일 경로
input_path = Path(
    r"C:\Users\Cotax\Desktop\k\to_html\스마트물류 자원 및 예측 관리.pptx"
)

output_dir = (
    Path(__file__).resolve().parent
    / "html_output"
    / f"{input_path.stem}_pptx_all"
)
image_dir = output_dir / "images"
output_path = output_dir / "index.html"

if not input_path.is_file():
    raise FileNotFoundError(f"파일을 찾을 수 없습니다: {input_path}")

image_dir.mkdir(parents=True, exist_ok=True)

presentation = Presentation(str(input_path))

if len(presentation.slides) == 0:
    raise RuntimeError("슬라이드가 없습니다.")

# PPTX의 길이 단위 EMU를 CSS 픽셀로 변환
def to_px(value):
    return value / 9525

slide_width = to_px(presentation.slide_width)
slide_height = to_px(presentation.slide_height)

slides_html = []

for slide_number, slide in enumerate(presentation.slides, start=1):
    elements_html = []

    for number, shape in enumerate(slide.shapes, start=1):
        left = to_px(shape.left)
        top = to_px(shape.top)
        width = to_px(shape.width)
        height = to_px(shape.height)

        position_style = (
            f"position:absolute;"
            f"left:{left}px;top:{top}px;"
            f"width:{width}px;height:{height}px;"
        )

        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            image = shape.image

            # 슬라이드 번호를 넣어 이미지 이름 충돌 방지
            image_name = (
                f"slide_{slide_number:03d}"
                f"_image_{number}.{image.ext}"
            )

            (image_dir / image_name).write_bytes(image.blob)

            elements_html.append(
                f'<img src="images/{image_name}" '
                f'alt="{slide_number}번 슬라이드 그림 {number}" '
                f'loading="lazy" '
                f'style="{position_style}">'
            )

        elif shape.has_text_frame:
            text = escape(shape.text)

            elements_html.append(
                f'<div class="text-box" '
                f'style="{position_style}">{text}</div>'
            )

        else:
            print(
                f"미지원 요소: {slide_number}번 슬라이드"
                f" / {shape.name}"
            )

    slide_html = "\n".join(elements_html)

    slides_html.append(
        f'<section style="margin-bottom:32px;">'
        f"<h2>{slide_number} / {len(presentation.slides)}슬라이드</h2>"
        f'<div class="slide">{slide_html}</div>'
        f"</section>"
    )

    print(
        f"{slide_number}/{len(presentation.slides)}슬라이드 완료",
        flush=True,
    )

all_slides_html = "\n".join(slides_html)

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>PPTX 첫 슬라이드 테스트</title>
    <style>
        body {{
            margin: 0;
            padding: 24px;
            background: #eeeeee;
        }}
        .slide {{
            position: relative;
            width: {slide_width}px;
            height: {slide_height}px;
            background: white;
            overflow: hidden;
        }}
        .text-box {{
            font-family: "맑은 고딕", sans-serif;
            font-size: 24px;
            color: black;
            white-space: pre-wrap;
            overflow-wrap: break-word;
        }}
    </style>
</head>
<body>
    {all_slides_html}
</body>
</html>
"""

output_path.write_text(html_content, encoding="utf-8")
print(f"변환 완료: {output_path}")