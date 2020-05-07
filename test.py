from bs4 import BeautifulSoup
import requests
from schemes import *
 
headers = {"User-Agent": "Mozilla/75.0"}
req = requests.get('https://test-english.com/level-test/', headers=headers)
soup = BeautifulSoup(req.text, 'lxml')
scheme = level_test_tags_scheme
content = dict()
# content['questions'] = [tag.select('i') for tag in soup.select('.question-choices')]
# print(content['questions'])

for s_key in scheme.keys():
    
    if s_key == 'title' or s_key == 'sub_title':
        
        content[s_key] = soup.select(scheme[s_key])[0].get_text().strip()
    
    elif s_key == 'content': 
        
        content[s_key] = {}
        for c_key in scheme[s_key].keys(): 
            
            if c_key == 'questions':
                content[s_key][c_key] = [tag.get_text().encode('ascii', 'ignore').decode().strip() for tag in soup.select(scheme[s_key][c_key])]
            
            elif c_key == 'options':

                content[s_key][c_key] = {}
                for o_key in scheme[s_key][c_key].keys():
                    
                    content[s_key][c_key][o_key] = [ [ info.get_text().encode('ascii', 'ignore').decode().strip() for info in tag.select(scheme[s_key][c_key][o_key][-1])] 
                    for tag in soup.select(scheme[s_key][c_key][o_key][0])]
                    
print(content)