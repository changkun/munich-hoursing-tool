# -- encoding: utf-8 --
from bs4 import BeautifulSoup
import requests
import csv
import time
import geocoder

# studentenwerk rent url
base_url = "http://www.studentenwerk-muenchen.de"
offers_uri = "/wohnen/privatzimmervermittlung/angebote/"

illustrate_de = [
    'Länge',
    'Breite',
    'Stadtteil',
    'Straße',
    'Art des Zimmers',
    'Möblierung',
    'Größe',
    'Anzahl Zimmer',
    'Kaltmiete',
    'Nebenkosten',
    'Gesamtmiete',
    'Kaution',
    'möglich ab',
    'Befristung',
    'Nebenleistung',
    'Weitere Nebenleistungen',
    'Besonderheiten',
    'Verkehrsmittel',
    'Entfernung',
    'Bemerkung',
    'url'
]
illustrate_en = [
    'longitude',
    'latitude',
    'District',
    'Road',
    'Type of room',
    'Furnishing',
    'Size',
    'Number of Rooms',
    'Cold rent',
    'Additional costs',
    'Total rent',
    'Deposit',
    'Possible ab',
    'Time limit',
    'Ancillary service',
    'Other ancillary services',
    'Particularities',
    'Transport',
    'Distance',
    'Remark'
    'Url'
]
illustrate_cn = [
    '经度',
    '纬度',
    '区',
    '街道',
    '房屋类型',
    '家具',
    '房屋大小',
    '房屋数量',
    '基本租金',
    '费用',
    '总租金',
    '押金',
    '开始时间',
    '结束时间',
    '辅助设施',
    '其他设施',
    '特殊设施',
    '交通',
    '距离',
    '备注',
    'URL'
]

print "fetch infomations..."
response = requests.get(base_url+offers_uri)
html = BeautifulSoup(response.text, "html.parser")

# data container
offers = {
    'muenchen': [],
    'freising': [],
    'rosenheim':[]
}

# parse infos
tables = html.find_all('table', attrs = {
    'class': 'tx_stwmprivatzimmervermittlung'
})

# fetch muenchen offers
table_body = tables[0].find('tbody')
rows = table_body.find_all('tr')

for i, row in enumerate(rows):

    offer = [col.text.strip() for col in row.find_all('td')]
    offer = [col.encode('utf-8') for col in offer if col]

    uris = [uri['href'] for uri in row.find_all('a')]
    uris  = [col for col in uris if col]
    offer_response = requests.get(base_url+uris[0])
    offer_details = BeautifulSoup(offer_response.text, "html.parser")
    uls = offer_details.find('ul', attrs = {
        'class': '[ o-list-ui o-list-ui--flush ]'
    })


    infos = []
    for li in uls.find_all('li', {'class': 'o-media'}):
        info = li.find('span', {'class': 'o-media__body'}).string
        if info is not None:
            info = unicode(info)
        else: # TODO: here should be the size of room
            info = 'Nothing'
        info = info.replace('\n', ' ').replace('\t', '').replace('  ', '').strip(' ')
        infos.append(info.encode('utf-8'))

    # server side geocoding
    pos = geocoder.google(infos[1]+' munich').latlng
    print pos

    offers['muenchen'].append(pos+infos+uris)

(year, mon, day, hour, _, _, _, _, _) = time.localtime()
filename = str(year)+'-'+str(mon)+'-'+str(day)+'-'+str(hour)+'.csv'
with open(filename, 'wb') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(illustrate_cn)
    csv_writer.writerows(offers['muenchen'])
