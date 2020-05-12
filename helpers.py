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


def find_page_struct(page, struct):
    '''
    helper function which finds the structure of the target given a list of structure names and their tags
    '''

    struct_type = None
    
    for structure in struct:

        # determine page struct
        if len(page.select(structure[0][0])) > 0:
            
            struct_type = structure[0][-1]

            return struct_type

def find_q_struct(selector, page):
    '''
    Helper function that finds the question structure of the test
    there are two structures:
        - forms -> these contain more then one watu-question
        - texts -> these contain just one watu-question 
    '''
    q_struct = None
    
    if len(page.select(selector)) > 1:
        
        q_struct = 'form'

    
    elif len(page.select(selector)) == 1:
        
        q_struct = 'text'

    return q_struct, selector

def find_a_struct(q_struct, sels, q_sel, page):
    '''
    Helper function that finds the answer structure of the test
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
                    
                    a_struct = sel[-1]
                    a_tag = sel[0]

                    # is the multiple choice as option 
                    if len(page.select(q_sel)[0].select(sel[0])[0].select('select')) != 0:
                        
                        a_struct = a_struct + '_options'        
                    
                    # is the multiple choice as bullets
                    elif len(page.select(q_sel)[0].select(sel[0])[0].select('label')) != 0:

                        a_struct = a_struct + '_bullets'
                    
                    # is the multiple choice as box
                    elif len(page.select(q_sel)[0].select(sel[0])[0].select('ul')) != 0:
                
                        a_struct = a_struct + '_boxes'

                else:
                    continue
        
            # is the a_struct a gap_option or a gap_options?             
            else:
                
                if len(page.select(q_sel)[0].select(sel[0])) > 0:
                    
                    a_struct = sel[-1]
                    a_tag = '.watu-question .question-content'


        # find answer structure in a text      
        elif q_struct == 'text':

            # texts do not contain multipe choice answer structures
            if sel[-1] == 'multiple_c':
                continue
            
            # is the answer structure a gap_option or a gap_options 
            else:
                
                if len(page.select(q_sel)[0].select(sel[0])) == 0:
                    continue
                
                else:
                    a_struct = sel[-1]

    if a_tag != None:
        return (a_struct, a_tag)
    
    else:
        return (a_struct, 'no a tag')
        
