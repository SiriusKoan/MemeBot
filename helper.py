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