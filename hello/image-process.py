# -*- coding: utf-8 -*-
import argparse
import random
import string
import textwrap

from PIL import Image, ImageDraw, ImageFont, ImageFilter

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filter', action="store_true")
args = parser.parse_args()

fileName = 'owu_randomCode'
fontPath = 'D:/tmp/my-font/'

font_colors = [(11, 11, 11), (28, 27, 22), (36, 36, 38), (45, 45, 53), (67, 65, 70), (99, 99, 99)]
bg_color = (207, 172, 140)
line_colors = [(99, 99, 99), (153, 153, 153), (180, 180, 180)]


def getRandomChar():
    return [random.choice(string.ascii_letters) for i in range(4)]


def getRandomColor():
    return font_colors[random.randint(0, len(font_colors) - 1)]


def getRandomLineColor():
    return line_colors[random.randint(0, len(line_colors) - 1)]


tail = u'由某图片输入法生成-柳公权版'


def getCodePicture():
    width = 720
    height = 1280
    # get verification text
    # text = getRandomChar()
    input = open('D:/tmp//sample_text.txt', 'r')
    readlines = input.readlines()
    print len(readlines)
    # font = ImageFont.truetype(fontPath + 'fznht.ttf', 48)
    font = ImageFont.truetype(fontPath + 'liugongquant.ttf', 48)
    w, h = font.getsize(u'柳')
    count = width / w - 1
    y_text = 40

    # compute image height
    img_ht = y_text
    for text in readlines:
        lines = textwrap.wrap(text.decode('utf-8'), width=count)
        img_ht += len(lines) * (h + 10) + 20
    img_ht += h * 3
    print img_ht
    height = img_ht

    # create canvas
    image = Image.new('RGB', (width, img_ht), bg_color)
    draw = ImageDraw.Draw(image)

    for text in readlines:
        lines = textwrap.wrap(text.decode('utf-8'), width=count)
        # write to canvas
        # y_text = 40
        for line in lines:
            ww, hh = font.getsize(line)
            x_text = 20
            for i in range(len(line)):
                draw.text((x_text, y_text), line[i], font=font, fill=getRandomColor())
                x_text += w
            y_text += hh
            y_text += 10
        y_text += 20

    # tail
    font = ImageFont.truetype(fontPath + 'liugongquant.ttf', 32)
    w, h = font.getsize(tail)
    draw.text((width - w - 40, img_ht - h * 2), tail, font=font, fill=getRandomColor())
    # fill noise
    for x in range(random.randint(1000, 2000)):
        draw.point((random.randint(0, width), random.randint(0, height)), fill=getRandomColor())
    for x in range(random.randint(500, 1000)):
        c1 = random.randint(0, width)
        c2 = random.randint(0, height)
        cord = (c1, c2, c1 + random.randint(20, 80), c2 + random.randint(20, 80))
        start = random.randint(0, 360)
        draw.arc(cord, start, start + random.randint(20, 60), fill=getRandomLineColor())
    if args.filter:
        # blur
        image = image.filter(ImageFilter.BLUR)
    image.show()
    # save to image
    image.save(fileName + '.jpg', 'jpeg')


if __name__ == '__main__':
    getCodePicture()
    print 'image saved'
    print getRandomColor()
