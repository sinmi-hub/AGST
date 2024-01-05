# this file will be used to generate images for each letter (A-Z) which will be used as default profile pictures. I will then store this locally in static directory to ensure that Flask can be served easily. 

from string import ascii_uppercase
from random import randint
from PIL import Image, ImageDraw, ImageFont

def generate_color_hex():
    return "#{:06x}".format(randint(0, 0xFFFFFF))

def default_picture(initial, size=(500, 500), bgcolor="red", textcolor="white"):
    img = Image.new('RGB', size, color=bgcolor)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(270)  

    # use textlength to calculate text width
    text_width = draw.textlength(initial, font=font)
    text_x = (size[0] - text_width) / 2.2 # horizontal alignment
    text_y = (size[1] - font.size) / 3  # vert alignment

    draw.text((text_x, text_y), initial, fill=textcolor, font=font)
    return img

# Now we will generate images from A to Z
for alphabet in ascii_uppercase:
    rand_color = generate_color_hex()
    img = default_picture(alphabet, bgcolor=rand_color)
    img.save(f"{alphabet}_image.jpg")  #  save the image

