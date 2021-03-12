from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from templates import templates


def measure_font_size(text):
    L = len(text)
    if L < 5:
        return 60
    elif L < 10:
        return 45
    elif L < 20:
        return 30
    else:
        return 20


def make_meme(template_id, text):
    template_info = templates[template_id]
    coordinates = template_info["position"]
    color = template_info["color"]
    with Image.open("templates/%s.png" % template_id) as template:
        draw = ImageDraw.Draw(template)
        for i in range(min(len(coordinates), len(text))):
            font = ImageFont.truetype("fonts/impact.ttf", measure_font_size(text[i]))
            width, _ = draw.textsize(text[i], font)
            x = coordinates[i][0] - (width / 2)
            y = coordinates[i][1]
            draw.text((x, y), text[i].upper(), font=font, fill=color)
        f = BytesIO()
        template.save(f, "PNG")
        return f.getvalue()
        
