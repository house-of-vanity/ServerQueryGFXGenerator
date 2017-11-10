# -*- coding: utf-8 -*-
import socket
import sys
import json
import yaml
def get_status():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('77.220.180.27', 27015)
    #server_address = ('cs.hexor.ru', 27015)
    request = ''.join(
        chr(x) for x in [0xFF, 0xFF, 0xFF, 0xFF, 0x54, 0x53, 0x6F,
            0x75, 0x72, 0x63, 0x65, 0x20, 0x45, 0x6E, 0x67, 0x69,
            0x6E, 0x65, 0x20, 0x51, 0x75, 0x65, 0x72, 0x79, 0x00])

    assertion = ''.join(
        chr(x) for x in [0xFF, 0xFF, 0xFF, 0xFF, 0x55, 0xFF, 0xFF, 0xFF, 0xFF])

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

print(get_status())
