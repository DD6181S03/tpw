import requests
import json
import time
from os import environ
from zbzh import transform

# 如果手动部署，需修改此处高德地图api key
amapkey = environ['AMAPKEY']
httpauth = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6Ik1qQXpZamxtWTJVdE1UVTRZaTAwTURVMUxXRTRaVEl0T1RObU5tUTFNamMyTmpRMyIsInJvbGUiOiJWaXNpdG9yIiwibmFtZWlkIjoiLTEyNzU2Mjc4NzEiLCJqdGkiOiJjZjYxYmFlZS0zYTBkLTQzMTctODEzYy0yNTczNDkzNmJiYjciLCJuYmYiOjE1Nzc2MjY4OTIsImV4cCI6MTczNTQ3OTY5MiwiaWF0IjoxNTc3NjI2ODkyLCJpc3MiOiJ3ZWIuMzY5Y3guY24iLCJhdWQiOiJhcGkud2ViLjM2OWN4LmNuIn0.ZQysaz6fEHRMLnHIQgfySpk6EtWTqE5puINlVq-RfA9u6DqzlcmH6kq7mTRSCz5k93fAR17Q-ya9kHJovLXe30-T254rK2L-XOnbiJLlX7z2ZjlzUrJJKXr78eKaJI-3mS370hoyTZMhGr6Ui41v1LaPvhrs7N-CD05NUDuP-RWrj3WyRpqM56SrN-WNfX0oU5RKOqYusou_lsPQXuIe450ti65Ajq0-GtKgEPa-bkpFYxC7OLaVfwo60upAgTP9AFk3vfnUCbVwNptG1dSNo1zPTQh2tfnmEK3bjnDuMXkfRKzxnjNEW7tmDiKCVwsGco0QfvFKZFuOav8AjZ2XgA'
headersold = {'version': 'ios-com.travelincity.WayBookJN-4392'}
headersget = {'authorization': httpauth, 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; samsung) Cx369Android/5200'}
headerspost = {'content-type': 'application/json; charset=UTF-8', 'authorization': httpauth}
urlsearch = 'https://api.369cx.cn/v2/Search'


def getlineid(line):
    lines = requests.post(urlsearch, headers=headerspost, data=json.dumps(
        {'keyword': line})).json()['result']['result']
    # 根据输入的线路名称查询上下行和相似线路
    ret = {}
    if lines:
        for line in lines:
            lineid = line['guid']  # 每条线路的独立id
            linename = line['text1']  # 线路名称
            startstn = line['text3'].replace('始发|', ' 从 ')  # 始发站
            endstn = line['text2'].replace('开往|', ' 开往 ')  # 终点站
            ret[lineid] = (linename + startstn + endstn)
    return ret


def getlineinfo(lineid):
    url2 = 'https://api.369cx.cn/v2/Line/GetRealTimeLineInfo/' + lineid
    rp = requests.get(url2, headers=headersget).json()
    r = rp['result']
    r2 = r['stations']
    r3 = r['busses']
    try:
        r4 = ' '.join((r['nextBus']['name'], r['nextBus']['planTime']))
    except:
        r4 = '没有数据'
    # 获取该线路所有站点，当前线上车辆，下一班车辆
    dplist = []
    for station in r2:
        stnid = station['stationNo'] + 1
        stnname = station['name']
        eachstnlist = [stnid, stnname]
        dplist.append(eachstnlist)
    for bus in r3:
        busid = bus['name']
        stnnum = bus['stationNo']
        dplist[stnnum].append(busid)
    extinfo = {'lineName': r['name'], 'nextBus': r4, 'startTime': r['firstDepartureTime'],
               'endTime': r['lastDepartureTime'], 'todayPlan': rp['status']['msg'].rstrip('|'),
               'revLine': r['backLineId']}
    dplist.append(extinfo)
    return dplist


def nbloc(busid, lineid):
    ret = {}
    busid = busid.lstrip('K')
    if len(busid) < 4:
        busid = busid.zfill(4)
    if lineid == -1:
        rid = requests.post(urlsearch, headers=headerspost, data=json.dumps({'keyword': busid})).json()['result']
        if rid:
            if not rid['result']:
                return {'message': '查不到'}
            lineid = rid['result'][0]['guid']
            ret = {'busid': rid['result'][0]['text1'], 'nextstn': '未上线运行',
                    'busline': rid['result'][0]['text3'].split('|')[1].split(' ')[0]}
        else:
            return {'message': '查不到'}
    urlbuses = 'http://iwaybook.369cx.cn/server-ue2/rest/buses/busline/370100/' + lineid
    urlstns = 'https://api.369cx.cn/v2/Line/GetRealTimeLineInfo/' + lineid
    rxl = requests.get(urlstns, headers=headersget).json()['result']
    rstns = rxl['stations']
    rc = rxl['busses']
    r = requests.get(urlbuses, headers=headersold).json()['result']
    for res in r:
        if res['busId'] == busid or res['busId'] == 'K'+busid:
            ret['busid'] = res['busId']
            ret['busline'] = rxl['name']
            ret['nextstn'] = rstns[res['stationSeqNum']]['name']
            for bus in rc:
                if bus['name'] == busid or bus['name'] == 'K'+busid:
                    ret['velocity'] = str(bus['velocity']) + ' km/h'
            wglng = res['lng']
            wglat = res['lat']
            gcjzb = transform(wglat, wglng)
            lng = str(round(gcjzb[1], 6))
            lat = str(round(gcjzb[0], 6))
            ret['amapurl'] = 'https://restapi.amap.com/v3/staticmap?markers=mid,,A:' + str(lng) + ',' + str(lat) + \
                '&traffic=1&zoom=14&size=200*200&scale=2&key=' + amapkey
    return ret


def getstnid(stninput):
    stns = requests.post(urlsearch, headers=headerspost, data=json.dumps(
        {'keyword': stninput})).json()['result']['tip']['tips']
    ret = []
    for stn in stns:
        if stn['type'] == 3:
            stnid = stn['innerText'].split(':')[1]
            stnname = stn['showText'].split(' ')[1]
            stndes = stn['address']
            ret.append([stnid, stnname, stndes])
    return ret


def getstninfo(stnid, det):
    lines = requests.post(urlsearch, headers=headerspost, data=json.dumps(
        {'keyword': 'stationId:' + stnid})).json()['result']['result']
    ret = []
    for line in lines:
        lineid = line['guid']
        linedesc = line['text1'] + ' ' + line['text2'].replace('|', ' ')
        ret.append([lineid, linedesc])
    return ret


def getnoticelist(pageid='0'):
    urlnotl = 'https://api.369cx.cn/v2/Notice/GetNoticeList/'
    notices = requests.get(urlnotl + pageid, headers=headersget).json()['result']
    ret = []
    for notice in notices:
        notid = notice['noticeId']
        nottime = time.strftime('%Y-%m-%d', time.localtime(notice['time']))
        nottit = notice['title']
        ret.append([notid, nottime, nottit])
    return ret


def getnoticedetail(noticeid):
    urlnotd = 'https://api.369cx.cn/v2/Notice/GetNoticeDetail/'
    notice = requests.get(urlnotd + noticeid, headers=headersget).json()['result']
    nottime = time.strftime('%Y-%m-%d', time.localtime(notice['time']))
    return [notice['title'], nottime, notice['content']]


def getroute():
    pass
