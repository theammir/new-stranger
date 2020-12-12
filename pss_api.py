import urllib.parse
import urllib.request
import time
from xml.etree import ElementTree
from collections import defaultdict

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

def _receive_dict(data) -> dict:
    xmltree = ElementTree.fromstring(data)
    return etree_to_dict(xmltree)

def inspect_user(nickname: str):
    user_inspect = "https://api2.pixelstarships.com/UserService/SearchUsers?searchString="
    search = urllib.parse.quote(nickname)
    file = urllib.request.urlopen(user_inspect + search)
    info = _receive_dict(file.read())['UserService']["SearchUsers"]["Users"]
    if (info):
        info = info["User"]
        if (isinstance(info, list)):
            info = info[0]
    else:
        return None
    return info
    
def receive_top100():
    top100_receive = "https://api2.pixelstarships.com/AllianceService/ListAlliancesByRanking?take=100"
    file = urllib.request.urlopen(top100_receive)
    return _receive_dict(file.read())["AllianceService"]["ListAlliancesByRanking"]["Alliances"]["Alliance"]

def find_fleet_ranking(fleet: str):
    fleets = receive_top100()
    for fl_index in range(100):
        if (fleets[fl_index]["@AllianceName"] == fleet):
            return fl_index + 1
    return 101
