import re
from bs4 import BeautifulSoup

def feed_crawler_links(file):
    '''
    helper function which loads already surfed llinks to the crawler returns a list of of links
    '''
    # read links from file into list and return it
    link_list = []
    with open(file, 'r') as link_file:
        lines = link_file.readlines()
        
        for link in lines:
            link_list.append(link.rstrip())
    
    return link_list

def find_pattern_inst(pattern, list):
    '''
    helper function which finds instances of a list item for a given regular expression pattern  
    ''' 

    # find instances of pattern in given list and return it
    return len([list_item for list_item in list if pattern.match(list_item)])

def rem_soup_ins_re(targets, soup, repl_str, parser='lxml'):
    '''
    helper function for removing target instances in a list from a bsoup string utilizing the targets as the pattern instances
    '''

    # remove target instances from string 
    elem = str(soup)
    for target in targets:
        
        pattern = re.compile(r''+str(target))
        match = pattern.search(elem)

        if match != None:

            new = elem.replace(elem[match.start():match.end()], repl_str)

            elem = new 
    
    return BeautifulSoup(elem, parser) 


def find_q_struct(selector, page):
    '''
    Helper function that finds the question structure of the test
    there are two structures:
        - forms -> these contain more then one watu-question
        - texts -> these contain just one watu-question 
    '''
    # test type
    q_struct = None
    
    if len(page.select(selector)) > 1:

        q_struct = 'form'
    
        # tag to retreive questins or questions
        q_tag = '.question-content p'

    elif len(page.select(selector)) == 1:
        
        q_struct = 'text'

        # tag to retreive questins or questions
        q_tag = '.question-content p'
    
    if len(page.find_all(string=re.compile(r'Dialogue \d+'))) > 0:

        q_struct = 'dialogue'
        q_tag = '.question-content'
    
    else:

        q_struct = 'special'
        q_tag = '.question-content'

    return (q_struct, q_tag)

def find_a_struct(q_struct, sels, q_sel, page):
    '''
    Helper function that finds the structure for possible test answers
    there are different structures:
        - single gaps with no options -> these contain just one input.watupro-gap in .question-content p
        - multiple gaps with no options -> these contain more then one input.watupro-gap in the .question-content p
        - single gaps with multiple options -> these contain just one select tag in question-content p
        - multiple gaps with multiple options -> these contain more the one select tags in question-content p
            - note that a text will have either have multiple gaps with no-options or multiple gaps with multiple options in the paragraphs represented by p, therefore look for both, if you can't find one look for the other. 
        - multiple choices (questions in text form will NEVER have multiple choice options)
            - multiple choice questions can either be with bullets (label), boxes(ul li) or options
    '''
    
    a_struct = None
    a_tag = None

    # loop through selectors
    for sel in sels:

        # find answer structure in a form
        if q_struct == 'form':

            # is the a_struct of the first question a multiple c?
            if sel[-1] == 'multiple_c':
                
                if len(page.select(q_sel)[0].select(sel[0])) != 0:
                    
                    # is the multiple choice as option 
                    if len(page.select(q_sel)[0].select(sel[0])[0].select('select')) != 0:
                        
                        a_struct = sel[-1] + '_options'
                        a_tag = sel[0] + ' ' + 'select option'        
                    
                    # is the multiple choice as bullets
                    elif len(page.select(q_sel)[0].select(sel[0])[0].select('label')) != 0:

                        a_struct = sel[-1] + '_bullets'
                        a_tag = sel[0] + ' ' + 'label'       
                    
                    # is the multiple choice as box
                    elif len(page.select(q_sel)[0].select(sel[0])[0].select('ul')) != 0:
                
                        a_struct = sel[-1] + '_boxes'
                        a_tag = sel[0] + ' ' + 'ul li'        
        
            # is the a_struct a gap_option or a gap_options?             
            else:
                
                if len(page.select(q_sel)[0].select(sel[0])) > 0:
                    
                    a_struct = sel[-1]
                    a_tag = sel[0]

        # find answer structure in a text      
        elif q_struct == 'text' or q_struct == 'dialogue' or q_struct == 'special':

            # texts do not contain multipe choice answer structures
            if sel[-1] == 'multiple_c':
                continue
            
            # is the answer structure a gap_option or a gap_options 
            else:
                
                if len(page.select(q_sel)[0].select(sel[0])) == 0:
                    continue
                
                else:
                    a_struct = sel[-1]

                    if a_struct == 'gap_options':
                        a_tag = sel[0].strip('option').strip()
                    else:
                        a_tag = sel[0]
        
    if a_tag != None:
        return (a_struct, a_tag)
    
    else:
        return ('no struct tag', 'no answer tag')

def find_ca_struct(q_struct, page):
    '''
    Helper function for finding the structure of correct answers of the tests from test-english
    '''
       
    # varibles
    ca_struct = None
    ca_struct_tag = None

    # first find the correct answer type
    if q_struct == 'dialogue':
        
        ca_struct = 'ca_dialogue'
        ca_struct_tag = '.watupro-choices-columns'
    
    elif len(page.select('.watupro-choices-columns')) > 1:

        ca_struct = 'ca_multiple'
        ca_struct_tag = '.watupro-choices-columns'
    
    elif len(page.select('.watupro-choices-columns')) == 1:

        ca_struct = 'ca_single'
        ca_struct_tag = '.watupro-choices-columns'
    
    return (ca_struct, ca_struct_tag)

def find_ca_feedback_struct(ca_struct, page):
    '''
    helper function for finding the feedback structure of the answers for a test page
    '''
    
    ca_fb_sct = list()

    if ca_struct[0] == 'ca_single':
        
        # check for bullets
        if len(page.select(ca_struct[-1])[0].select('.show-question-choices')) > 0:
            
            ca_fb_sct.append(ca_struct[0] + '_bullets')
            ca_fb_sct.append(ca_struct[0] + ' ' + '.show-question-choices > .correct-answer')
        
        # if no bullets then assign tag
        else:
            
            ca_fb_sct.append(ca_struct[0])  
            ca_fb_sct.append('.watupro-main-feedback > p, h4') 
    
    # assign dialogue struct and tag 
    elif ca_struct[0] == 'ca_dialogue':

        ca_fb_sct.append(ca_struct[0])
        ca_fb_sct.append('.watupro-main-feedback > p, h4')
    
    # assign struct tag for feedback with multiple answers
    elif ca_struct[0] == 'ca_multiple':
        
        ca_fb_sct.append(ca_struct[0])

        # check if bullets
        if len(page.select(ca_struct[-1])[0].select('.show-question-choices')) > 0:

            ca_fb_sct[0] = ca_fb_sct[0] + '_bullets'
         
            # check for feedback
            if len(page.select(ca_struct[-1])[0].select('.watupro-main-feedback')) == 0:
                
                ca_fb_sct[0] += '_wof' 
                ca_fb_sct.append('.show-question-choices .correct-answer')
            
            # if feedback assign corresponding tag
            else:
                
                ca_fb_sct[0] += '_wf' 

                # see if feedback contains p or h4 tags
                if len(page.select(ca_struct[-1])[0].select('.watupro-main-feedback > p, h4')) == 0:
                    
                    ca_fb_sct.append(['.watupro-main-feedback', '.show-question-choices .correct-answer'])
                
                else: 
                    
                    ca_fb_sct.append(['.watupro-main-feedback > p, h4', '.show-question-choices .correct-answer'])

        # if no bullets assign tag for normal multiple
        else:
            
            ca_fb_sct[0] += '_normal'

            # see if feedback contains p or h4 tags
            if len(page.select(ca_struct[-1])[0].select('.watupro-main-feedback > p, h4')) == 0:
                
                ca_fb_sct.append('.watupro-main-feedback')
            
            else: 

                ca_fb_sct.append('.watupro-main-feedback > p, h4')
    
    return tuple(ca_fb_sct)
    
def retr_q_id(soup):
    
    # retrieve the form id
    pattern = re.compile(r'\d+')
    id_string = soup.parent.attrs['id']
    match = pattern.search(id_string)
    id = id_string[match.start():match.end()]
    
    return id

def parse_tests_questions(g_quest_sel, q_selectors, page):
    '''
    helper function for parsing questions of tests from test-english
    '''
    
    # necessary variables 
    questions = page.select(g_quest_sel)
    q_struct = find_q_struct(g_quest_sel, page)
    a_struct = find_a_struct(q_struct[0], q_selectors, g_quest_sel, page)
    
    # print(q_struct)
    # print(a_struct)

    # empty questions and answers strings and question number counter
    parsed_q = []
    parsed_a = []
    q_number = 0

    # parse all questions questions in the test form
    questions = page.select(g_quest_sel)
    
    for question in questions:

        if q_struct[0] == 'form':

            # count questions
            if len(question.select('.numbox ')) != 0:
                
                q_number += len(question.select('.numBox'))
            
            else:

                q_number += len(question.select('.watupro_num'))
            
            # remove number from questions
            question.select('.watupro_num')[0].clear()

            # ----------------- parse form  questions and answers -------------------
        
            # replace inputs and parse answers if gap_options or gap_option
            if a_struct[0] == 'gap_option' or a_struct[0] == 'gap_options':
                
                # replace inputs with literal gap string
                inputs = question.select(a_struct[-1])
                
                if a_struct == 'gap_option': 

                    new_soup = rem_soup_ins_re(inputs, question, '_'*5)

                else:
                    new_soup = rem_soup_ins_re(inputs, question, '_'*6)
                
                # parse questions with one gap or more gaps
                if new_soup.get_text().rfind('\xa0') != -1:

                    parsed_q.append(new_soup.get_text().encode('ascii', 'ignore').decode().strip())
                
                else:
                    
                    parsed_q.append(new_soup.get_text().strip())

            
                # parse answers unless gap_option
                if a_struct[0] == 'gap_options':

                    parsed_a.append([answer.get_text() for answer in question.select(a_struct[-1]) if answer.get_text() != ''])         
                    
            else:
                
                # parse questions 
                if question.select(q_struct[-1])[0].get_text().rfind('\xa0') != -1:
                
                    parsed_q.append(question.select(q_struct[-1])[0].get_text().encode('ascii', 'ignore').decode().strip())
                else:
                    parsed_q.append(question.select(q_struct[-1])[0].get_text().strip())

                # --------------- parse form answers -------------
            
                # remove bullets for answers with bullet points
                if a_struct[0] == 'multiple_c_bullets':
                    
                    for answer_n in question.select('i'):
                        
                        answer_n.clear()
                        
                parsed_a.append([answer.get_text().encode('ascii', 'ignore').decode().strip() for answer in question.select(a_struct[-1])])


        elif q_struct[0] == 'text' or q_struct[0] == 'dialogue' or q_struct[0] == 'special':       

            text = question
            new_soup = None 

            # number of possible answers
            answers = text.select(a_struct[-1])
            
            # parse answers only if options 
            if a_struct[0] == 'gap_options':
                
                parsed_a.append([[option.get_text() for option in answer if option.get_text() != ''] for answer in answers])
    
            # if there are Numboxes replace them with gaps, else replace inputs
            if len(text.select('.numBox')) > 0:
            
                for num_box in text.select('.numBox'):
                    
                    # count numbers
                    if num_box.get_text() == '0':
                        
                        num_box.string.replace_with("_"*1 + text.select('.textGap')[0].get_text() + "_"*1)

                        text.select('.textGap')[0].clear()

                        continue

                    else:

                        q_number += 1

                num_box.string.replace_with("_"*3 + num_box.get_text() + "_"*3)
           
            # replace inputs if special struct else clear the inputs
            elif q_struct[0] == 'special' and len(answers) > 0:

                new_soup = rem_soup_ins_re(answers, question, '_'*5)

            else:    

                # remove inputs or select
                for answer in answers:
                    answer.clear() 

            if q_struct[0] == 'text': 
                
                # parse questions
                for paragraph in text.select(q_struct[-1]):
                    
                    if paragraph.get_text() == '':

                        continue

                    if paragraph.get_text().rfind('\xa0') != -1 :
                    
                        parsed_q.append(paragraph.get_text().encode('ascii', 'ignore').decode().strip())

                    else:
                        parsed_q.append(paragraph.get_text().strip())
                    
            else:
                
                # change text to new soup
                if q_struct[0] == 'special' and a_struct[0] != 'no struct tag':

                    text = new_soup
                
                # parse questions
                for line in text.find_all(['h4', 'p']):
                    
                    if line.get_text().rfind('\xa0') != -1:
                    
                        parsed_q.append(line.get_text().encode('ascii', 'ignore').decode().strip())

                    else:
                        parsed_q.append(line.get_text().strip())

                # handle excercise 4 writing (special case)
                if a_struct[0] == 'no struct tag':

                    a_tag = '.watupro-question-choice label'

                    # parse answers
                    parsed_a.append([answer.get_text().encode('ascii', 'ignore').decode().strip() for answer in text.select(a_tag)])
    
    # return parsed content
    return (parsed_q, parsed_a, q_number)

def parse_tests_answers(q_struct, page):

    '''
    Function for parsing the correct answers of tests from the tests website
    '''
    
    # find struct for correct answers page and struct for retrieving the feedback data
    ca_sct = find_ca_struct(q_struct, page)
    ca_fb_sct =  find_ca_feedback_struct(ca_sct, page)

    print(ca_sct)
    print(ca_fb_sct)

    # get the main elements
    ca_answers = page.select(ca_sct[-1])

    # empty storage
    ca = list()
    ca_fb = list()

    # loop through columns
    for column in ca_answers:
        
        # print('-'*75)
        # print(column.select(ca_fb_sct[-1]))

        # check struct, store answers 
        if ca_fb_sct[0] == 'ca_multiple_normal':
            
            if ca_fb_sct[-1] == '.watupro-main-feedback > p, h4':
                
                if len(column.select(ca_fb_sct[-1])) > 1:

                    ca.append([line.get_text().encode('ascii', 'ignore').decode() for line in column.select(ca_fb_sct[-1])])
                
                else:

                    ca.append(column.select(ca_fb_sct[-1])[0].get_text().encode('ascii', 'ignore').decode())

            else:

                ca.append(column.select(ca_fb_sct[-1])[0].get_text().encode('ascii', 'ignore').decode())

        elif ca_fb_sct[0] == 'ca_multiple_bullets_wof':
            pass

        elif ca_fb_sct[0] == 'ca_multiple_bullets_wf':
            pass

    print(ca)

                    

            
    

    
     