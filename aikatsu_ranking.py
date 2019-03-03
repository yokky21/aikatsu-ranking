#!/usr/bin/env python3.6
# vim: ts=4 sw=4

import requests, lxml.html, json, sys, os, configparser
from datetime import datetime
from mastodon import *

## Initializing
host         = 'https://bpnavi.jp'
ua           = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1'
url_main     = host + '/s/elec/aikatsu_p5/ranking'
url_ajax     = host + '/s/elec/aikatsu_p5/item_rankings/more'
rank         = []
name         = []
post_summary = datetime.now().strftime("%Y-%m-%d %H:%M") + ' 現在のランキング'
post_data    = post_summary + "\n"
conf_select  = 'aikatsu8'
inifile      = configparser.ConfigParser()
inifile.read(os.path.dirname(os.path.abspath(__file__)) + '/mastodon.ini', 'UTF-8')

## Getting main page (CSRF Token)
headers   = {'User-Agent': ua}
resp      = requests.get(url_main, timeout=30, headers=headers)
main_html = resp.text
cookies   = resp.cookies

root = lxml.html.fromstring(main_html)
csrf_token_data = root.xpath('/html/head/meta[@name="csrf-token"]')
csrf_token = csrf_token_data[0].attrib['content']

## Getting ranking data
headers = {'User-Agent': ua,
           'Accept': '*/*',
           'Origin': host,
           'Referer': host + '/s/elec/aikatsu_p5/item_rankings',
           'X-CSRF-Token': csrf_token,
           'X-Requested-With': 'XMLHttpRequest'}

for page in range(4):
    obj     = {'page': str(page+1)}
    resp    = requests.post(url_ajax, timeout=30,
                            headers=headers, cookies=cookies, data=obj)
    if resp.status_code != 200:
        sys.exit()
    data = json.loads(resp.text)
    rank_html = data['attachmentPartial']
    root = lxml.html.fromstring(rank_html)

    for row in range(3):
        for col in range(3):
            rank_data = root.xpath('//tr['+ str(row+1) +']/td['+ str(col+1) +']/p["rank"]/font[1]')
            name_data = root.xpath('//tr['+ str(row+1) +']/td['+ str(col+1) +']/p["name_vote"]/a[1]')
            try:
                rank.append(rank_data[0].text.strip())
                name.append(name_data[0].text.strip())
            except IndexError:
                break
        else:
            continue
        break

for num in range(len(rank)):
    post_data += rank[num] + name[num] + "\n"

# print(post_data)
# print(post_summary)
# sys.exit()

## Posting to Mastodon
mastodon = Mastodon(client_id     = inifile.get(conf_select, 'id'),
                    client_secret = inifile.get(conf_select, 'secret'),
                    access_token  = inifile.get(conf_select, 'token'),
                    api_base_url  = inifile.get(conf_select, 'url'))

# mastodon.toot(post_data)
mastodon.status_post(
        post_data,
        spoiler_text=post_summary)

