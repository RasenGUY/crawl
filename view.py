import os

class Content:
    '''
    common base class for all content
    '''

    def __init__(self, url, title, content):
        self.url = url #string 
        self.title = title # string
        self.body = content


    def show_parsed_items(self):
        '''

        Class utility for printing parsed content
        '''
        
        print('URL: {}'.format(self.url)) 
        print('Page Title: {}'.format(self.title)) 
        print('Content: {}'.format(self.body))

   
    def create_folder_path(self, link, dest):
        '''

        Utility function for creating a folder path which can be utilized to store data 
        '''
        pass

    def write_parsed_content(self, folder_name, content):
        '''
        
        Utility function for storing data into text files
        '''
        pass




class GT(Content): # general test
    '''
    Subclass for content parsed from tests -> level-tests, grammer-points, use-of-english, writing
    '''

    def __init__(self, url, title, content, folder, p_nums):

        Content.__init__(self, url, title, content)

        self.folder = folder   # parsed folder path for downloading test content
        self.p_nums = p_nums # instances of target link     

class Listening(GT):

    '''
    Subclass for content parsed from listening tests
    '''

    def ___init__(self, url, title, content, folder, p_nums, audio_response):
        
        # initialize subclass GT
        GT.__init__(self, url, title, content, folder, p_nums)

        self.audio_response = audio_response # req response -> to use for storing 
        