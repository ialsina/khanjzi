import requests
from bs4 import BeautifulSoup
from tqdm import tqdm 

file_simp = open('hanzi_simplified.txt','w')
file_trad = open('hanzi_traditional.txt','w')
file_url = open('url.txt','r')
# file_html = open('hanzi01.html','w', encoding='utf-8')

urls = [line.replace('\n','') for line in file_url.readlines()]

url_han = urls[0]
url_han2 = urls[2]

table = []

session = requests.Session()
session.mount('http://', requests.adapters.HTTPAdapter(max_retries = 2))
session.mount('https://', requests.adapters.HTTPAdapter(max_retries = 2))


for i in tqdm(range(1,83)):

    response = session.get(url_han.format(i))
    response.encoding = 'utf-8'
    #print(response.text)

    #file_html.write(response.text)

    html = BeautifulSoup(response.text, features='lxml')

    htable = html.find_all('div')[-2].find_next('table')

    for hrow in htable.find_all('tr'):
        row = []
        for hcol in hrow.find_all('td'):
            col = hcol.text
            row.append(col)
        if row != []:
            table.append(row)

file_simp.write('\n'.join([row[0] for row in table]))

file_url.close()
file_simp.close()
file_trad.close()
# file_html.close()

input(f"""
    1. Copy characters from 'hanzi_simplified.txt' into
    '{url_han2}'
    2. Paste traditional versions into 'hanzi_traditional.txt'
    3. Hit [ENTER]. Waiting...
    """)

file_chn = open('hanzi.txt','w')
file_trad = open('hanzi_traditional.txt','r')
file_simp = open('hanzi_simplified.txt','r')

lines_trad = [l.replace('\n','') for l in file_trad.readlines()]
lines_simp = [l.replace('\n','') for l in file_simp.readlines()]


table_full = []

for (i, (row, simp, trad)) in enumerate(zip(table, lines_simp, lines_trad)):
    assert row[0] == simp
    table_full.append([str(i+1), simp, trad] + row[1:])


file_chn.write(f"""# SOURCE:
# {url_han}
# {url_han2}
# 
# Id\tSimp.\tTrad.\tPinyin\tDefinition\tRadical\tStroke count\tHSK level\tGeneral Standard#\tFrequency rank
""")
file_chn.write('\n'.join(['\t'.join(row) for row in table_full]))

file_chn.close()
