from string import printable
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from templates import templates


def measure_font_size(text, language):
    L = len(text)
    if language == "en":
        if L < 5:
            return 60
        elif L < 10:
            return 45
        elif L < 20:
            return 30
        else:
            return 20
    elif language == "zh-TW":
        if L < 3:
            return 60
        elif L < 10:
            return 45
        elif L < 20:
            return 30
        else:
            return 20


def multiple_lines(text, language):
    if language == "en":
        split_text = []
        length = 0
        line = []
        for t in text.split():
            line.append(t)
            length += len(t)
            if length >= 8:
                split_text.append(line)
                length = 0
                line = []
            if t == text.split()[-1] and line != []:    # add last word
                split_text.append(line)
        split_text = [" ".join(t) for t in split_text]
        return split_text
    if language == "zh-TW":
        split_text = []
        for i in range(0, len(text), 5):
            split_text.append(text[i:i+5])
        return split_text


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
                font = ImageFont.truetype("fonts/impact.ttf", measure_font_size(text[i], "en"))
                _, height = draw.textsize(text[i], font)
                result_text = multiple_lines(text[i], "en")
            else:
                font = ImageFont.truetype("fonts/jf.ttf", measure_font_size(text[i], "zh-TW"))
                _, height = draw.textsize(text[i], font)
                result_text = multiple_lines(text[i], "zh-TW")
            lines = len(result_text)
            for j, line in enumerate(result_text):
                width, _ = draw.textsize(line, font)
                x = coordinates[i][0] - (width / 2)
                y = coordinates[i][1] + (j - (lines / 2)) * height
                draw.text((x-2, y-2), line.upper(), font=font, fill=shadowcolor)
                draw.text((x+2, y-2), line.upper(), font=font, fill=shadowcolor)
                draw.text((x-2, y+2), line.upper(), font=font, fill=shadowcolor)
                draw.text((x+2, y+2), line.upper(), font=font, fill=shadowcolor)
                draw.text((x, y), line.upper(), font=font, fill=color)
                
        f = BytesIO()
        template.save(f, "PNG")
        return f.getvalue()
