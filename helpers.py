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
        
        struct_type = None
        # determine page struct
        if len(page.select(structure[0][0])) > 0:
            
            struct = structure[0][-1]

            return struct_type
    