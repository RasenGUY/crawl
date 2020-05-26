import os

class Content:
    '''
    common base class for all content
    '''

    def __init__(self, url, title, content, folder):
        self.url = url #string 
        self.p_title = title # string 
        self.test_content = content # information from content where content is a dictionary


    def print(self):
        '''
        printing function for content
        '''
        print('URL: {}'.format(self.url)) 
        print('Page Title: {}'.format(self.p_title)) 
        print('Content: {}'.format(self.url)) 