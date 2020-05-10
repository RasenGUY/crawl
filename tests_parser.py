from helpers import *
from schemes import *  
import re

def parse_tests_content(page, scheme, test_structs):
    '''
    Function for parsing the content of tests from tests website
    '''
    
    # locals 
    test_content = dict()
    struct = find_page_struct(page, test_structs)
    pattern = re.compile(r'(\b\d+|\b[a-zA-Z]\.)')

    # find test structure and assign scheme to parser according to structure 
    if struct == 'g-w-o':
        scheme['content'] = test_structs[0][-1]
    elif struct == 'multiple-c':
        scheme['content'] = test_structs[1][-1]
    elif struct == 'g-w-s':
        scheme['content'] = test_structs[-1][-1]

    print(struct)
    
    # parse data according to keys in scheme 
    for s_key in scheme.keys():

        if s_key == 'title' or s_key == 'sub_title' or s_key == 'ex_title':
            test_content[s_key] = page.select(scheme[s_key])[0].get_text().strip()
        
        # parse test content
        elif s_key == 'content': 
            

            test_content[s_key] = {}
            for c_key in scheme[s_key].keys(): 

                # ------------------------- parse multiple choice questions tests-------------------------

                # parse questios
                if c_key == 'questions' and struct == 'multiple-c':
                    test_content[s_key][c_key] = [
                        [   # get question number
                            ''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())[0]+"."),
                            # get question content
                            tag.get_text().encode('ascii', 'ignore').decode().strip().strip(''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())))
                        ] 
                        for tag in page.select(scheme[s_key][c_key])
                        ]

                # parse possible answers 
                elif c_key == 'options' and struct == 'multiple-c':
                    test_content[s_key][c_key] = [
                                    [
                                        # get option content
                                        ''.join(option.get_text().encode('ascii', 'ignore').decode().split(pattern.findall(option.get_text().encode('ascii', 'ignore').decode().strip())[0]+''))

                                    for option in options.select(scheme[s_key][c_key][-1])
                                    ]

                                for options in page.select(scheme[s_key][c_key][0])
                                ]


                # --------------------- parse gap tests with options -----------------------

                # parse questions  
                elif c_key == 'questions' and struct == 'g-w-o':

                    test_content[s_key][c_key] = [
                                    [   # get question number
                                        ''.join(pattern.findall(questions.get_text().encode('ascii', 'ignore').decode().strip())[0]+"."),
                                        # join all options in the text into one string and remove them from the question and remove number
                                        questions.get_text().encode('ascii', 'ignore').decode().strip().replace(''.join([question.get_text() for question in questions.select(scheme['content']['options'][-1]) if question.get_text() != '']), '_'*5).strip(''.join(pattern.findall(questions.get_text().encode('ascii', 'ignore').decode().strip())))

                                    ]
                                        # parse questions from documents
                                        for questions in page.select(scheme[s_key][c_key])
                                ]

                # parse possible answers 
                elif c_key == 'options' and struct == 'g-w-o':
                    
                    test_content[s_key][c_key] = [
                                    [   # parse all option in column retrieve text 
                                        option.get_text() for option in column.select(scheme[s_key][c_key][-1]) if option.get_text() != ''
                                    ]
                                # parse all option columms
                                for column in page.select(scheme[s_key][c_key][0])
                                ]
                
                # --------------------- parse gap tests with single answers -----------------------
                # parse questions  
                elif c_key == 'questions' and struct == 'g-w-s':
                    
                    
                    test_content[s_key][c_key] = []
                        
                    for paragraph in page.select(scheme[s_key][c_key][0]):
                        
                        for numbox in paragraph.select('.numBox'):
                            
                            numbox.string.replace_with('___'+numbox.get_text()+'___')
                    
                        test_content[s_key][c_key].append(paragraph.get_text().encode('ascii', 'ignore').decode())        
                    
                # no options to parse
                elif c_key == 'options' and struct == 'g-w-s':
                    pass

    return test_content

def parse_tests_answers(page, scheme, test_structs):
    '''
    Function for parsing answers of tests from the tests website
    '''
    pass
