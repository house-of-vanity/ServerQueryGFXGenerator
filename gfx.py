# -*- coding: utf-8 -*-
import StringIO
#import sys
import urllib
import json
from flask import Flask, render_template, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont


app = Flask(__name__)


def serve_pil_image(pil_img):
    img_io = StringIO.StringIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


def get_gfx():
    base = Image.open('tuxlgbt.jpg').convert('RGBA')
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
    fnt = ImageFont.truetype('clacon.ttf', 28)
    fnt_small = ImageFont.truetype('clacon.ttf', 41)
    fnt_xsmall = ImageFont.truetype('clacon.ttf', 21)
    d = ImageDraw.Draw(txt)
    kernel_version = get_kernel()
    d.text((10, 10), "Linux kernel versions", font=fnt_small,
           fill=(37, 0, 117, 255))
    d.text((10, 60), "Mainline " + kernel_version['mainline'], font=fnt_small,
           fill=(37, 0, 117, 255))
    d.text((10, 120), "Stable . " + kernel_version['stable'], font=fnt_small,
           fill=(37, 0, 117, 255))
    d.text((10, 190), "LTS ... " + kernel_version['longterm'], font=fnt_small,
           fill=(37, 0, 117, 255))
    out = Image.alpha_composite(base, txt)
    return out


def get_kernel():
    url = "https://www.kernel.org/releases.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    out = {
        "mainline": data['releases'][0]['version'] + ' @' 
            + data['releases'][0]['released']['isodate'],
        "stable": data['releases'][1]['version'] + ' @' 
            + data['releases'][1]['released']['isodate'],
        "longterm": data['releases'][2]['version'] + ' @' 
            + data['releases'][2]['released']['isodate']
    }
    return out


@app.route("/")
def index():
    return serve_pil_image(get_gfx())


if __name__ == "__main__":
    app.run()
