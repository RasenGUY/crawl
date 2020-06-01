
from bs4 import BeautifulSoup
import requests
from tests_parser import *
from helpers import *
import re
from schemes import *


# Links to extract
    # test with textbox 
        # https://test-english.com/grammar-points/b2/generic-pronouns/3/
    # test with example 
        # https://test-english.com/grammar-points/a2/asking-questions-in-english/4/

    # forms with multiple and single gaps
        # single gaps single options
            # https://test-english.com/grammar-points/a2/infinitives-and-gerunds/3/
        # multiple gaps single options
            # https://test-english.com/grammar-points/b1-b2/review-verb-tenses-b1-b2/3/
        # single gaps multiple options
            # https://test-english.com/grammar-points/a2/however-although-time-connectors/
        # multiple gaps multiple options
            # https://test-english.com/grammar-points/b1-b2/review-verb-tenses-b1-b2/

    # form with multiple choice
        # options
            # https://test-english.com/listening/b1-b2/actors-talk-acting/
        # bullets 
            # https://test-english.com/grammar-points/a2/however-although-time-connectors/2/
        # boxes
            # https://test-english.com/writing/b1-b2/narrative-writing-step-by-step/
    # text 
        # gaps with single options
            # https://test-english.com/grammar-points/a2/however-although-time-connectors/3/

        # gaps with multiple options
            # https://test-english.com/grammar-points/a2/present-continuous-future-arrangements/
            # https://test-english.com/grammar-points/b1-b2/present-perfect-simple-continuous/
    
    # dialogue
        # https://test-english.com/grammar-points/a2/present-continuous-future-arrangements/3/


# https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/2/
# https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/3/
# special pages
    # writing (special cases)(done)
        # https://test-english.com/writing/b1-b2/for-against-essay-argumentative-writing/2/
        # note (does not contain correct answers)
    
    # not done completely
        # https://test-english.com/writing/b1-b2/narrative-writing-step-by-step/2/ 
        # https://test-english.com/writing/b1-b2/formal-email-letter-asking-information/4/
        # https://test-english.com/reading/b1/ebay-tips-selling-successfully/
        # https://test-english.com/grammar-points/a2/present-continuous-future-arrangements/3/
            # check correct answers 
        # https://test-english.com/grammar-points/a2/however-although-time-connectors/3/
            # check correct answers 
# some notes for parsing answers
    # forms of feedback
        # bullet form 
        #     


headers = [
    {"User-Agent": "Mozilla/75.0"}, 
    [
        {"User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0 Chrome/73.0.3683.103", "X-Requested-With": "XMLHttpRequest"}, {"action": "watupro_submit", "quiz_id": "258"}
    ]
] 

req = requests.get('https://test-english.com/use-of-english/a2/a2-english-test-1-text-multiple-choice-gaps/', headers=headers[0])

q_page = BeautifulSoup(req.text, 'html.parser')


# get quiz id
q_id = retr_q_id(q_page.select('.quiz-form')[0])
headers[-1][-1]['quiz_id'] = q_id
payload = headers[-1][-1]


post_link = 'https://test-english.com/staging01/wp-admin/admin-ajax.php'
req = requests.post(post_link, data=payload, headers=headers[0])

ca_page = BeautifulSoup(req.text, 'lxml')

content = parse_tests_content(q_page, ca_page, general_scheme)
# print(content['passage'])



# post_link = 'https://www.easymp3converter.com/models/convertProcess.php'
# audio_link = get_audio_link(q_page, listening_scheme)

# payload = {'search_txt': audio_link}

# hdrs = {'User-Agent': 'Mozilla/75.0'}
# req = requests.post(post_link, data=payload, headers=headers[-1][0])

# ad_page = BeautifulSoup(req.text, 'lxml')
 
# d_links = ad_page.find_all('option')
# d_link = None

# for link in d_links:
    
#     if  link.get_text() == 'mp3\xa0128kbps':
#         d_link = 'https:' + link.attrs['data-link']

# print(d_link)


# print(len(page.select('.quiz-form .watu-question')))
# parse answers

# print()
# print(content['title'])
# print(content['sub_title'])
# print()
# for i in range(len(content['content']['questions'])):
#     q_num = content['content']['questions'][i][0]
#     q_body = content['content']['questions'][i][-1]

#     print('{} {}'.format(q_num, q_body))
    
#     for j in range(len(content['content']['options'][i])):

#         o_num = content['content']['options'][i][j][0]
#         o_body = content['content']['options'][i][j][-1]
        
#         print('\t {} {}'.format(o_num, o_body))
    
#     print()
# ils = feed_crawler_links('eng_test_links.txt')
# ins = find_pattern_inst(re.compile(rf'https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/4.*'), ils)
# print(ins)

# write parsed questions
print('\n'*2)
print("Test: {}".format(content['test_title']))
print('\n')

for key in content.keys():

    # handle passage
    if key == 'passage':
        
        if content['q_struct'] == 'dialogue' and content[key] != None:
            
            counter = 0 
            for question in content[key]:

                if counter+1 != len(content[key]):
                    
                    # new line if Dialogue substring
                    if question.rfind('Dialogue') != -1 or content[key][counter+1].rfind('Dialogue') != -1:
                        
                        print(question + '\n')
                    
                    else:

                        print(question)
                else:

                    print(question)

                counter += 1

            print('\n')

        else:

            if isinstance(content[key], list):
                
                counter = 0
                for line in content[key]: 
                    
                    if line == '\n':
                        pass 
                    elif line == '':
                        pass
                    else:
                        print(line, end='\n')
                    
                    # print every two lines
                    if counter % 2 == 0: 
                        print('\n')
                
                    # increment counter with one
                    counter+= 1

                print('\n')
                
    # handle questions
    elif key == 'questions':
        
        # write answers of options
        if content['q_struct'] == 'dialogue':

            if content[key][-1] != None: 
            
                d_counter = 0
                a_counter = 0
                
                # loop through dialogue
                for dialogue in content[key][-1]:

                    # loop through p_answers
                    for p_as in dialogue:

                        a_counter += 1
                        
                        print(str(a_counter) + '. ' + '_'*10 + '\n')

                        for i in range(len(p_as)):
                            
                            p_a = '\t' + chr(ord('a') + i) + '.' + p_as[i]
                            
                            print(p_a)
                        
                        print('\n')
                        
                    d_counter += 1
            else:

                pass  


        elif content['q_struct'] == 'form':
        
            counter = 0
            for question in content[key][0]:
        
                print(str(counter+1)+ '. ' + question, end='\n')
                
                # if questions multiple choice 
                if len(content[key][-1]) != 0:
                    
                    p_as = content[key][-1][counter] 
                    for i in range(len(p_as)): 
                        
                        if isinstance(p_as, list):
                            
                            p_a = chr(ord('a') + i) + '. ' + p_as[i]
                            
                            print('\t' + p_a, end='\n')
                    
                        else:

                            print(p_as)
                else:

                    pass
            
            print('\n')
            
            counter+= 1

        # handle texts                      
        elif content['q_struct'] == 'text' or content['q_struct'] == 'special': 
            
            for paragraph in content[key][0]:

                print(paragraph)
            
            print('\n')

            if len(content[key][-1]) > 0:
                
                a_counter = 0
                for p_as in content[key][-1]:

                    if isinstance(p_as, list):

                        for i in range(len(p_as)):

                            p_a = p_as[i]
                            
                            print(str(a_counter+1) + '. ' + '_'*10)

                            for j in range(len(p_a)):
                                
                                print('\t' + chr(ord('a') + j) + '.' + p_a[j])
                            
                            print('\n')

                            a_counter += 1
                    else:
                        
                        print('\t' + str(a_counter+1) + '. ' + p_as)
                        a_counter += 1        
            else:

                pass
            

    elif key == 'sub_title' or key == 'test_title' or key == 'instructions' or key == 'words':

        # don't print test title
        if key == 'test_title':

            pass

        # print sub title instructions and text_box
        elif content[key] != None: 

            print(key + ': ' + content[key], end='\n')
            print('\n')

    
    # pass parsed answers
    else:

        pass

# write parsed answers
print('\n'*2)
print("Answers for the test: {}".format(content['test_title']))
print('\n')

for key in content.keys():

    if key == 'c_answers':
        
        counter = 0
        for c_answer in content[key][0]:

            if content['q_struct'] == 'dialogue':        

                # print each line in dialogue
                for line in c_answer:

                    if line[0:2].isdigit():
                    
                        print('{}.{}'.format(line[0:2], line[2:len(line)]))
                    
                    elif line[0].isdigit():
                        
                        print('{}.{}'.format(line[0], line[1:len(line)]))
                    
                    else:

                        print(line)

            # store single answers 
            elif content['ca_fb_sct'] == 'ca_multiple_bullets_wf':

                # store multiple correct answers  with feedback multiple
                if isinstance(content[key][-1][0], list) != True:
                    
                    c_a = ''
                    if isinstance(c_answer, list):
                    
                        for answer in c_answer:
                                
                            c_a += answer[3:len(answer)] + ', '

                    else:

                        c_a = c_answer[3:len(c_answer)] 
                    
                    print(str(counter + 1) + '. ' + c_a) 
                            
                # store single correct answers 
                else:

                    c_a = str(counter + 1) + '. ' + c_answer
                    
                    print(c_a)
                
                                
                # write if feedback is a list
                if isinstance(content[key][-1][counter], list):
                    
                    for line in content[key][-1][counter]:

                        print('\t' + line)
                
                # write feedback is not list   
                else: 

                    print('\t' + content[key][-1][counter])

                print('\n')

                counter += 1
                        
        
            elif content['ca_fb_sct'] == 'ca_multiple_normal':
                
                if c_answer[0:1] == '\n':

                    print(str(counter+1) + '. ' + c_answer[1:-1])
                
                else:
                    print(str(counter+1) + '. ' + c_answer)
                
                if c_answer[-1] != '\n':
                    
                    print('\n')
                
                counter+= 1
            
            elif content['ca_fb_sct'] == 'ca_multiple_bullets_wof':
                
                if c_answer[-1] == '\n':

                    print(str(counter + 1) + '. '+ c_answer)

                else:
                    
                    print(str(counter + 1) + '. '+ c_answer + '\n')

                counter += 1
            
            elif content['ca_fb_sct'] == 'ca_single':

                p_a = c_answer

                print(p_a)

            elif content['ca_fb_sct'] == 'ca_single_bullets':

                for num in range(len(content[key][0])):
                    
                    print('Question {}.'.format(num+1))
                    
                    for answer in content[key][0][num]:

                        print('\t' + answer + '\n')
            
    elif key == 'sub_title' or key == 'test_title' or key == 'instructions' or key == 'words':

        # don't print test title
        if key == 'test_title':

            pass

        # print sub title instructions and text_box
        elif content[key] != None: 

            print(key + ': ' + content[key], end='\n')
            print('\n')
    else:
        pass

print('\n'*2)
print("Explanations for the test: {}".format(content['test_title']))
print('\n')

expl = False

for key in content.keys():
    
    if key == 'expl':

        expl = True

if expl == True:

    for line in content['expl']:

        
        if isinstance(line, list):
            
            print(line[0], line[-1], '\n') 
        
        else:
            
            print(line)

else: 

    print("No Explanations")


print(content)