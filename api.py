import requests
import json



key = '410346-ndim-7AYZMXFC'
movie = input('Enter the movie:')
payload = {'q': f'movie:{movie}', 'k': key, 'info':1}
r = requests.get('https://tastedive.com/api/similar?', params=payload)
txt = r.json()
res = json.dumps(txt, indent=4)

with open('books.json', 'w') as f:
    json.dump(txt, f, indent=4)

lst = []
for each in txt['Similar']['Results']:
    name = each['Name']
    type = each['Type']
    info_link = each['wUrl']
    row = (name, type, info_link)
    lst.append(row)

print(txt['Similar']['Info'][0]['wTeaser'])
for each in lst:
    print(each[0],each[2])



