from bs4 import BeautifulSoup
import urllib.request
import json


def checkModes(url):
    link_s = url.split('/')
    link_s = link_s[0:5]
    url = '/'.join(link_s)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    content = soup.select('#json-beatmapset')[0].text
    raw_data = json.loads(content)
    title = raw_data['artist']+' - '+raw_data['title'] + ' by '+raw_data['creator']
    mode_data = 0
    # std=1 taiko=2 ctb=4 mania=8
    mode_osu = False
    mode_taiko = False
    mode_ctb = False
    mode_mania = False
    for diff in raw_data['beatmaps']:
        if diff['convert'] == True:
            continue
        if diff['mode'] == 'osu':
            mode_osu = True
        if diff['mode'] == 'taiko':
            mode_taiko = True
        if diff['mode'] == 'fruits':
            mode_ctb = True
        if diff['mode'] == 'mania':
            mode_mania = True
    if mode_osu:
        mode_data += 1
    if mode_taiko:
        mode_data += 2
    if mode_ctb:
        mode_data += 4
    if mode_mania:
        mode_data += 8
    return title, mode_data


def get_nominate_data():
    url = "https://osu.ppy.sh/beatmapsets/events?user=&types%5B%5D=nominate&types%5B%5D=qualify&types%5B%5D=nomination_reset&types%5B%5D=disqualify&min_date=&max_date="
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    content = soup.select(".beatmapset-event")
    nominate_data = []
    for n in content:
        # print(n)
        mapinfo = n.select('a')
        mapurl = mapinfo[0].get('href')
        mapstatus = "null"
        if len(n.select('.beatmapset-event__icon--qualify')) == 1:
            mapstatus = "qualify"
        if len(n.select('.beatmapset-event__icon--nominate')) == 1:
            mapstatus = "nominate"
        if len(n.select('.beatmapset-event__icon--nomination-reset')) == 1:
            mapstatus = "nomination-reset"
        if len(n.select('.beatmapset-event__icon--disqualify')) == 1:
            mapstatus = "disqualify"

        imgurl = n.select('.beatmapset-activities__beatmapset-cover')[0].get('srcset').split(',')[1][1:-3]
        time = n.select('.timeago')[0].get('datetime')

        info = n.select('.beatmapset-event__content')[0].text.replace("                ","").replace("            ","").replace("\n", "")

        data = {}
        data["mapurl"] = mapurl
        data["maptitle"], data["mode"] = checkModes(mapurl)
        data["mapstatus"] = mapstatus
        data["imgurl"] = imgurl
        data["time"] = time
        data["info"] = info
        data["hash"] = hash(time)
        nominate_data.append(data)
    nominate_data.reverse()
    return nominate_data

if __name__ == '__main__':
    d = get_nominate_data()
    print(d)