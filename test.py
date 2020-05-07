from bs4 import BeautifulSoup
import requests
from schemes import *
import re
 
headers = {"User-Agent": "Mozilla/75.0"}
req = requests.get('https://test-english.com/level-test/', headers=headers)
soup = BeautifulSoup(req.text, 'lxml')
pattern = re.compile(r'(\b\d+|\b[a-zA-Z]\.)')
scheme = level_test_tags_scheme
content = dict()

# level test scheme
for s_key in scheme.keys():
    
    if s_key == 'title' or s_key == 'sub_title':
        
        content[s_key] = soup.select(scheme[s_key])[0].get_text().strip()
    
    elif s_key == 'content': 
        
        content[s_key] = {}
        for c_key in scheme[s_key].keys(): 
            
            if c_key == 'questions':
                content[s_key][c_key] = [
                    [   #convert string to tuple vale
                        ''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())[0]+"."),
                        # remove number from string
                        tag.get_text().encode('ascii', 'ignore').decode().strip().strip(''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())))
                    ] 
                    for tag in soup.select(scheme[s_key][c_key])
                    ]
            
            elif c_key == 'options':
                content[s_key][c_key] = [
                                    [
                                [   
                                    ''.join(pattern.findall(option.get_text().encode('ascii', 'ignore').decode().strip())[0]),
                                    ''.join(option.get_text().encode('ascii', 'ignore').decode().split(''.join(pattern.findall(option.get_text().encode('ascii', 'ignore').decode().strip()))+''))
                                ]
                                for option in options.select(scheme[s_key][c_key][-1])
                            ]

                            for options in soup.select(scheme[s_key][c_key][0])
                            ]
                    
print()
print(content['title'])
print(content['sub_title'])
print()
for i in range(len(content['content']['questions'])):
    q_num = content['content']['questions'][i][0]
    q_body = content['content']['questions'][i][-1]

    print('{} {}'.format(q_num, q_body))
    
    for j in range(len(content['content']['options'][i])):

        o_num = content['content']['options'][i][j][0]
        o_body = content['content']['options'][i][j][-1]
        
        print('\t {} {}'.format(o_num, o_body))
    
    print()


