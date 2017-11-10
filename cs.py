# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import socket
import sys
import StringIO
import yaml

app = Flask(__name__)

with open("servers.yaml", 'r') as config:
    try:
        config = yaml.load(config)
    except yaml.YAMLError as exc:
        print(exc)

def serve_pil_image(pil_img):
    img_io = StringIO.StringIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

def get_gfx(address, port):
    base = Image.open('banner.png').convert('RGBA')
    txt = Image.new('RGBA', base.size, (255,255,255,0))
    fnt = ImageFont.truetype('clacon.ttf', 28)
    fnt_small = ImageFont.truetype('clacon.ttf', 25)
    fnt_xsmall = ImageFont.truetype('clacon.ttf', 21)
    d = ImageDraw.Draw(txt)
    d.text((10,10), str(get_status(address, port)['name']), font=fnt_small, \
        fill=(37, 0, 117, 255))
    d.text((10,85), "Map: " + str(get_status(address, port)['map']), \
        font=fnt, fill=(37, 0, 117, 255))
    d.text((10,108), "Players: " + str(get_status(address, port)['players']) \
        + "/" + str(get_status(address, port)['max_players']), \
        font=fnt, fill=(37, 0, 117, 255))
    d.text((10,146), "Type: " + str(get_status(address, port)['server_type']), \
        font=fnt_xsmall, fill=(37, 0, 117, 255))
    d.text((10,161), "Platform: " + str(get_status(address, port)['platform']), \
        font=fnt_xsmall, fill=(37, 0, 117, 255))
    d.text((350,161), "UltraDesu", font=fnt_xsmall, fill=(232, 135, 219, 255))
    out = Image.alpha_composite(base, txt)
    return out

def get_status(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (address, port)
    request = ''.join(
        chr(x) for x in [0xFF, 0xFF, 0xFF, 0xFF, 0x54, 0x53, 0x6F,
            0x75, 0x72, 0x63, 0x65, 0x20, 0x45, 0x6E, 0x67, 0x69,
            0x6E, 0x65, 0x20, 0x51, 0x75, 0x65, 0x72, 0x79, 0x00])

    assertion = ''.join(
        chr(x) for x in [0xFF, 0xFF, 0xFF, 0xFF, 0x55, 0xFF, 
            0xFF, 0xFF, 0xFF])

    try:
        sock.sendto(request, server_address)
        a2s_info, server = sock.recvfrom(4096)
        a2s_info = filter(None, a2s_info.split(b'\x00'))

        head = '\xff\xff\xff\xff\x55'
        sock.sendto(assertion, server_address)
        assertion, server = sock.recvfrom(4096)
        sock.sendto((head + assertion[5:]), server_address)
        a2s_players, server = sock.recvfrom(4096)
        players = []
        i = 0
        user_count = int(a2s_players[5].encode('hex'), 16)

        if len(a2s_players) <= 6:
            players = []
        else:
            try:
                a2s_players = a2s_players[7:]
                while i < user_count:
                    a2s_players = a2s_players.split(b'\x00', 1)
                    players.append(a2s_players[0])
                    a2s_players = a2s_players[1][9:]
                    i = i + 1
            except:
                players = ['Invalid server response']

        if len(a2s_info[5]) == 2:
            players_count = int(a2s_info[5][0].encode('hex'), 16)
            max_players = int(a2s_info[5][1].encode('hex'), 16)
        else:
            players_count = '0'
            max_players = int(a2s_info[5].encode('hex'), 16)

        if a2s_info[6][1] == 'l':
            platform = 'linux'
        elif a2s_info[6][1] == 'w':
            platform = 'windows'
        else:
            platform = 'mac'

        if a2s_info[6][0] == 'd':
            server_type = 'dedicated'
        else:
            server_type = 'listing'
        
        response = {
            "name": a2s_info[0][6:],
            "map": a2s_info[1],
            "folder": a2s_info[2],
            "game": a2s_info[3],
            "players": players_count,
            "max_players": max_players,
            "platform": platform,
            "server_type": server_type,
            "player_list": players,
        }
        return response
    finally:
        sock.close()

@app.route("/")
def index():
    api = ['/status', ['/status/<server_name>'], '/gfx/<server_name>']
    return jsonify(api)

@app.route("/status")
def status():
    response = []
    for server in config['servers']:
        response.append(get_status(server['address'], server['port']))
    return jsonify(response)

@app.route("/gfx/<addr>")
def gfx(addr):
    for server in config['servers']:
        if server['address'] == addr:
            return serve_pil_image(get_gfx(server['address'], server['port']))

if __name__ == "__main__":
    app.run()