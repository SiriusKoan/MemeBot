from string import printable
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
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


def generate_example_text(template_id):
    template_info = templates[template_id]
    text_fields = len(template_info["position"]) + 1
    return list("text%d" % i for i in range(1, text_fields))


def make_meme(template_id, text):
    template_info = templates[template_id]
    coordinates = template_info["position"]
    color = "#FFFFFF"
    shadowcolor = "#000000"
    text = [t for t in text if t is not None]
    with Image.open("templates/%s.png" % template_id) as template:
        draw = ImageDraw.Draw(template)
        for i in range(min(len(coordinates), len(text))):
            if all(c in printable for c in text[i]):
                font = ImageFont.truetype("fonts/impact.ttf", measure_font_size(text[i]))
            else:
                font = ImageFont.truetype("fonts/jf.ttf", measure_font_size(text[i]))
            width, _ = draw.textsize(text[i], font)
            x = coordinates[i][0] - (width / 2)
            y = coordinates[i][1]
            draw.text((x-2, y-2), text[i].upper(), font=font, fill=shadowcolor)
            draw.text((x+2, y-2), text[i].upper(), font=font, fill=shadowcolor)
            draw.text((x-2, y+2), text[i].upper(), font=font, fill=shadowcolor)
            draw.text((x+2, y+2), text[i].upper(), font=font, fill=shadowcolor)
            draw.text((x, y), text[i].upper(), font=font, fill=color)
        f = BytesIO()
        template.save(f, "PNG")
        return f.getvalue()
