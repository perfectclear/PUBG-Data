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
    try:
        user_id = tree.xpath('/descendant::div[@data-p-user_id]')[0].attrib['data-p-user_id']
        return user_id
    except IndexError:
        return None


def scrape_match_list(user_id):
    if user_id:
        offset = ''
        match_ids = set()
        n = 0
        while n < 5:
            if offset == '':
                with closing(request.urlopen(
                        'https://pubg.op.gg/api/users/{}/matches/recent?server=na&queue_size=4&mode=fpp'
                        .format(user_id))) as url:
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
            sleep(0)
            n = n + 1
        return match_ids
    else:
        return None


def scrape_match_data(match_id):
    if match_id:
        name_set = set()
        with closing(request.urlopen('https://pubg.op.gg/api/matches/{}/deaths'.format(match_id))) as url:
            data = json.loads(url.read().decode())
        for j in range(0, len(data['deaths'])):
            victim_name = data['deaths'][j]['victim']['user']['nickname']
            name_set.add(victim_name)
            if data['deaths'][j]['killer']:
                killer_name = data['deaths'][j]['killer']['user']['nickname']
                name_set.add(killer_name)
        sleep(0)
        return name_set, data
    else:
        return None
