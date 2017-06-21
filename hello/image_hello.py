from PIL import Image, ImageDraw, ImageFont

# get an image
base = Image.open('D:/tmp/nihao.PNG').convert('RGBA')

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

# get a font
fnt = ImageFont.truetype('C:\\Windows\\Fonts\\simsun.ttc', 40)
# get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((10, 10), "Hello", font=fnt, fill=(0, 255, 255, 128))
# draw text, full opacity
d.text((10, 60), "World", font=fnt, fill=(255, 0, 255, 255))

# d.line((15, 20, 50, 90), fill="red", width=5)
d.arc((100, 0, 100, 100), 90, 180, fill="red")
# d.rectangle((10, 40, 90, 90), outline="red")
# d.ellipse((15, 20, 50, 90), outline="red")

out = Image.alpha_composite(base, txt)

out.show()