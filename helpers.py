import re
from bs4 import BeautifulSoup, Tag, NavigableString

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
        
        
        # check if special
        if len(page.select('.question-content h4')) > 0:
            
            q_struct = 'special'
            q_tag = '.question-content'
        
        else:
            
            q_struct = 'text'
            # tag to retreive questins or questions
            q_tag = '.question-content p'

    
    if len(page.find_all(string=re.compile(r'Dialogue \d+'))) > 0:

        q_struct = 'dialogue'
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
            ca_fb_sct.append('.show-question-choices .correct-answer')
        
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
    id_string = soup.attrs['id']
    
    match = pattern.search(id_string)
    id = id_string[match.start():match.end()]
   
    return id

def parse_tests_questions(g_quest_sel, page, q_struct, a_struct):
    '''
    helper function for parsing questions of tests from test-english
    '''
    
    # necessary variables 
    questions = page.select(g_quest_sel)

    # empty questions and answers strings and question number counter
    parsed_q = []
    parsed_a = []
    q_number = 0

    # parse all questions questions in the test form
    questions = page.select(g_quest_sel)

    # remove all breadcrumbs
    bread_crumbs = page.select('.watupro-qnum-info')
    for crumb in bread_crumbs:
        crumb.clear()
    
    for question in questions:

        if q_struct[0] == 'form':

            # count questions
            if len(question.select('.numbox ')) != 0:
                
                q_number += len(question.select('.numBox'))
            
            else:

                q_number += len(question.select('.watupro_num'))
            
            # remove number from questions
            if len(question.select('.watupro_num')) > 0:  
                question.select('.watupro_num')[0].clear()

            # ----------------- parse form  questions and answers -------------------
        
            # replace inputs and parse answers if gap_options or gap_option
            if a_struct[0] == 'gap_option' or a_struct[0] == 'gap_options':
                
                if a_struct[0] == 'gap_option': 
                    # replace inputs with literal gap string
                    inputs = question.select(a_struct[-1])
                    new_soup = rem_soup_ins_re(inputs, question, '_'*5)

                else:

                    # replace inputs with literal gap string
                    inputs = question.select(a_struct[-1].strip('option'))
                    new_soup = rem_soup_ins_re(inputs, question, '_'*6)
                
                # parse questions with one gap or more gaps
                if new_soup.get_text().rfind('\xa0') != -1:

                    parsed_q.append(new_soup.get_text().replace('\xa0', ' ').strip())
                
                else:
                    
                    parsed_q.append(new_soup.get_text().strip())

            
                # parse answers unless gap_option
                if a_struct[0] == 'gap_options':

                    parsed_a.append([answer.get_text() for answer in question.select(a_struct[-1]) if answer.get_text() != ''])         
                    
            else:
                
                # parse questions 
                if question.select(q_struct[-1])[0].get_text().rfind('\xa0') != -1:
                
                    parsed_q.append(question.select(q_struct[-1])[0].get_text().replace('\xa0', ' ').strip())
                else:
                    parsed_q.append(question.select(q_struct[-1])[0].get_text().strip())

                # --------------- parse form answers -------------
            
                # remove bullets for answers with bullet points
                if a_struct[0] == 'multiple_c_bullets':
                    
                    for answer_n in question.select('i'):
                        
                        answer_n.clear()
                        
                parsed_a.append([answer.get_text().replace('\xa0', ' ').strip() for answer in question.select(a_struct[-1])])


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
                
                numbers = text.select('.numBox')
                
                # count numbers replace numbox with gaps
                for num_box in numbers:
                    
                    # remove example text if there is any
                    if num_box.get_text() == '0':
                        
                        num_box.insert(1, ' ' + '_'*2 + text.select('.textGap')[0].get_text() + '_'*2)

                        text.select('.textGap')[0].clear()

                        continue

                    else:

                        q_number += 1

                    if q_struct[0] == 'text':
                        
                        num_box.string.replace_with(num_box.get_text() +' ' + '__'*4 + ' ')
                    
                    elif q_struct[0] == 'dialogue': 

                        num_box.string.replace_with(' '+ num_box.get_text() +' ' + '__'*4 )

            # replace inputs if special struct else clear the inputs
            if q_struct[0] == 'special' and len(answers) > 0:

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
                    
                        parsed_q.append(paragraph.get_text().replace('\xa0', ' ').strip())

                    else:
                        parsed_q.append(paragraph.get_text().strip())
                    
            else:
                
                # change text to new soup
                if q_struct[0] == 'special' and a_struct[0] != 'no struct tag':

                    text = new_soup
                
                # parse questions
                for line in text.find_all(['h4', 'p']):
                    
                    if line.get_text().rfind('\xa0') != -1:
                    
                        parsed_q.append(line.get_text().replace('\xa0', ' ').strip())

                    else:
                        
                        if line.get_text() != '':

                            parsed_q.append(line.get_text().strip())

                # handle excercise 4 writing (special case)
                if a_struct[0] == 'no struct tag':

                    a_tag = '.watupro-question-choice label'

                    # parse answers
                    parsed_a.append([answer.get_text().replace('\xa0', ' ').strip() for answer in text.select(a_tag)])
    
    # return parsed content
    return (parsed_q, parsed_a, q_number)

def parse_tests_answers(q_struct, page, ca_sct, ca_fb_sct):

    '''
    Function for parsing the correct answers of tests from the tests website
    '''

    # get the main elements
    ca_answers = page.select(ca_sct[-1])

    # empty storage
    ca = list()
    ca_fb = list()

    # remove 'correct' text 
    cor_syms = page.select('.watupro-screen-reader')
    for symbol in cor_syms:
        symbol.clear()
    
    # unwrap u tags
    u_tags = page.select('u')
    for tag in u_tags:
        tag.unwrap()

    # insert space before and after content in <strong> tags
    strong_tags = page.select('strong')
    
    if len(strong_tags) != 0:
        
        for tag in strong_tags:

            if isinstance(tag, NavigableString):

                tag.insert(0, ' ') 
                tag.insert(len(''.join(tag.contents)), ' ')
            
            elif isinstance(tag, Tag):

                tag.unwrap()
                tag.insert(0, ' ') 
                tag.insert(len(''.join(tag.contents)), ' ')
            
            else:
                continue
                

    # loop through columns
    for column in ca_answers:
        
        # print('-'*75)
        # print(column.select(ca_fb_sct[-1]))

        # check struct, store answers 
        if ca_fb_sct[0] == 'ca_multiple_normal':
            
            if ca_fb_sct[-1] == '.watupro-main-feedback > p, h4':
                
                if len(column.select(ca_fb_sct[-1])) > 1:

                    ca.append([line.get_text().replace('\xa0', ' ') for line in column.select(ca_fb_sct[-1])])
                
                else:

                    ca.append(column.select(ca_fb_sct[-1])[0].get_text().replace('\xa0', ' '))

            else:

                ca.append(column.select(ca_fb_sct[-1])[0].get_text().replace('\xa0', ' '))
        
        # store answers with multiple columns bullets and w/wo feedback
        elif ca_fb_sct[0] == 'ca_multiple_bullets_wf' or ca_fb_sct[0] == 'ca_multiple_bullets_wof' or ca_fb_sct[0] == 'ca_single_bullets':
            
            if ca_fb_sct[0] == 'ca_multiple_bullets_wf':
                
                ca_fb_sel = ca_fb_sct[-1][-1]
            
            else: 
                
                ca_fb_sel = ca_fb_sct[-1]

            # store correct answers check if column contains multiple correct answers first
            if len(column.select(ca_fb_sel)) > 1:

                ca.append([line.get_text().replace('\xa0', ' ') for line in column.select(ca_fb_sel)])
            
            else:
                
                ca.append(column.select(ca_fb_sel)[0].get_text().replace('\xa0', ' '))
            
            
            # store with feedback only for ca_multiple_bullets_wf 
            if ca_fb_sct[0] == 'ca_multiple_bullets_wf':

                # store feedback  
                if ca_fb_sct[-1][0] == '.watupro-main-feedback > p, h4':
                    
                    # store elements in list aof list if feedback contains more then one p or h
                    if len(column.select(ca_fb_sct[-1][0])) > 1:

                        ca_fb.append([line.get_text().replace('\xa0', ' ') for line in column.select(ca_fb_sct[-1][0])])
                    
                    # store in list of strings if feedback contains only one p element 
                    else:

                        ca_fb.append(column.select(ca_fb_sct[-1][0])[0].get_text().replace('\xa0', ' ').strip(' '))
                
                # store feedback as is if tag is just .watupro-main-feedback  
                else:

                    ca_fb.append(column.select(ca_fb_sct[-1][0])[0].get_text().replace('\xa0', ' ').strip(' '))

        # store correct answers with dialogue struct
        elif ca_fb_sct[0] == 'ca_dialogue' or ca_fb_sct[0] == 'ca_single':
            
            # add '.' after number in numbox
            numbers = column.select('.numBox')
            for num in numbers:
                num.insert(1, '.')

            # store all of the p, and h4 elements in column in list of lists
            ca.append([line.get_text().replace('\xa0', ' ').strip() for line in column.select(ca_fb_sct[-1])])

    return (ca, ca_fb)

def parse_tests_expls(page, selector):
    
    '''
    Helper function for retrieving explanation data from tests just provide the page, and approriate selector
    '''

    elements = page.select(selector)
    parsed_expls = []
    
    # unwrap all unnecessary markup
    for markup in page.select('#explanation em, #explanation u, #explanation i, #explanation span'):
        markup.unwrap()

    # handle all the elements on explanation page
    for element in elements:

        # handle images
        if element.name == 'img':
            parsed_expls.append([element.attrs['data-wpfc-original-src'].replace('website18/', ''), element.attrs['alt']])
            continue

        # handle lists 
        if element.name == 'ul':
            item = element.get_text().replace('\xa0', ' ').replace('\n', '\n\t')
            parsed_expls.append(item[:len(item)-2])
            continue 

        if element.get_text() == '' or element.get_text() == '\xa0':
            pass
        
        else:
            parsed_expls.append(element.get_text().replace('\xa0', ' '))

           
    return parsed_expls

        
        



    
     