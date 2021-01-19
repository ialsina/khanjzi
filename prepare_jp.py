import requests
from bs4 import BeautifulSoup, element
from tqdm import tqdm

ALLOW = [' ', '-', ',', '.', '（', '）']

def syllabary(inp):
    def single(char):
        unicode = ord(char)
        if 12353 <= unicode <= 12440:
            return 1 # HIRAGANA
        elif 12449 <= unicode <= 12540:
            return 2 # KATAKANA
        elif 12288 <= unicode <= 12321:
            return 4 # PUNCTUATION
        elif char in ALLOW:
            return 5 # ALLOW
        else:
            return 0 # NOT ALLOW
    
    cum = []
    for char in inp:
        cum.append(single(char))
    
    cum = [el for el in cum if el < 4]
    
    if all(el==cum[0] for el in cum):
        return cum[0]
    else:
        return -1

def process_readings(i, hcol):
    read_parts = [str(el) for el in hcol.contents if isinstance(el, element.NavigableString)]

    if len(read_parts) == 2:
        kana, roma = read_parts
    else:
        print(i, read_parts)
        raise RuntimeError

    kana_list = kana.split('、')
    roma_list = roma.split(', ')

    kun, on, rkun, ron = [], [], [], []

    for (kk, rr) in zip(kana_list, roma_list):
        k = kk.replace('\n','')
        r = rr.replace('\n','')
        syl = syllabary(k)

        if syl == 1:
            kun.append(k)
            rkun.append(r)
        elif syl == 2:
            on.append(k)
            ron.append(r)
        else:
            print(k, syl)
            raise RuntimeError

    return '、'.join(kun), '、'.join(on), ', '.join(rkun), ', '.join(ron)


    print(kana, romaaji)


file_url = open('url.txt','r')

urls = [line.replace('\n','') for line in file_url.readlines()]

url_jap = urls[1]

table = []

session = requests.Session()
session.mount('http://', requests.adapters.HTTPAdapter(max_retries = 2))
session.mount('https://', requests.adapters.HTTPAdapter(max_retries = 2))


response = session.get(url_jap)
response.encoding = 'utf-8'

html = BeautifulSoup(response.text, features='lxml')


htable = html.find_all('table')[1]

for (j, hrow) in enumerate(htable.find_all('tr')):
    row = []
    for (i,hcol) in enumerate(hrow.find_all('td')):
        if i != 8:
            row.append(hcol.text)
        else:
            (kun, on, rkun, ron) = process_readings(j, hcol)
            row.extend([on, ron, kun, rkun])
    if row != []:
        table.append(row)

with open('kanji.txt','w') as f:
    f.write(f"""# SOURCE:
# {url_jap}
# 
# Id\tShin.\tKyuu.\tRadical\tStroke count\tGrade\tYear added\tEnglish meaning\tOn'yomi\t(Rōmaji)\tKun'yomi\t(Rōmaji)
""")
    f.write('\n'.join(['\t'.join(row) for row in table]))