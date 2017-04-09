
import os
try:
    from PIL import Image, ImageDraw, ImageFont
except:
    import Image, ImageDraw, ImageFont

def draw_circle(image_draw, x, y, color, radius, thickness=1):
    # Draw inside and outside radius given
    start = radius - thickness//2
    for i in range(start, start+thickness):
        image_draw.ellipse((x-i, y-i, x+i, y+i), outline=color)

def draw_text(image_draw, text, x, y, fill_color, border_color=(0,0,0), border_thickness=0, font_size=12):
    # Load font, required for larger font size. Found here: https://www.fontsquirrel.com/fonts/open-sans
    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "OpenSans.ttf"), size=48)

    if border_thickness != 0:
        image_draw.text((x-border_thickness, y-border_thickness), text, font=font, fill=border_color)
        image_draw.text((x+border_thickness, y-border_thickness), text, font=font, fill=border_color)
        image_draw.text((x-border_thickness, y+border_thickness), text, font=font, fill=border_color)
        image_draw.text((x+border_thickness, y+border_thickness), text, font=font, fill=border_color)

    # now draw the text over it
    image_draw.text((x, y), text, font=font, fill=fill_color)
