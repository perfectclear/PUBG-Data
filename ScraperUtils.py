# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 20:50:13 2018

@author: Michael
"""

from lxml import html
import requests
from urllib import request
import json
from time import sleep
from contextlib import closing


def scrape_user_id(name):
    page = requests.get('https://pubg.op.gg/user/{}?server=na'.format(name))
    tree = html.fromstring(page.content)
    user_id = tree.xpath('/descendant::div[@data-p-user_id]')[0].attrib['data-p-user_id']
    return user_id


def scrape_match_list(user_id):
    offset = ''
    match_ids = set()
    n = 0
    while n < 5:
        if offset == '':
            with closing(request.urlopen(
                    'https://pubg.op.gg/api/users/{}/matches/recent?server=na&queue_size=4&mode=fpp'
                    .format(user_id, offset))) as url:
                data = json.loads(url.read().decode())
        else:
            with closing(request.urlopen(
                    'https://pubg.op.gg/api/users/{}/matches/recent?server=na&queue_size=4&mode=fpp&after={}'
                    .format(user_id, offset))) as url:
                data = json.loads(url.read().decode())
        for j in range(0, len(data['matches']['items'])):
            offset = data['matches']['items'][j]['offset']
            match_id = data['matches']['items'][j]['match_id']
            match_ids.add(match_id)
        sleep(0.5)
        n = n + 1
    return match_ids


def scrape_match_data(match_id):
    name_id_set = set()
    with closing(request.urlopen('https://pubg.op.gg/api/matches/{}/deaths'.format(match_id))) as url:
        data = json.loads(url.read().decode())
    for j in range(0, len(data['deaths'])):
        victim_id = data['deaths'][j]['victim']['participant_id']
        victim_name = data['deaths'][j]['victim']['user']['nickname']
        name_id_set.add((victim_name, victim_id))
        if data['deaths'][j]['killer']:
            killer_name = data['deaths'][j]['killer']['user']['nickname']
            killer_id = data['deaths'][j]['killer']['participant_id']
            name_id_set.add((killer_name, killer_id))
    sleep(0.5)
    return name_id_set, data
