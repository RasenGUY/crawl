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

   
    def create_folder_path(self, link_p, home):
        '''

        Utility function for creating a folder path which can be utilized to store data
        returns a directory path, the home variable is refers to the home directory used for storing the tests if no home directory is given, home variable will take on the home path of the users machine
        '''
        
        if home == None:
            home = os.environ['HOME']
        
        if link_p[-1].isdigit() == True:
        
            folder_path = home + link_p[:len(link_p)-1]
        
        else:
            
            if link_p[-1] != '/':
                folder_path = home + link_p + '/'
            else:
                folder_path = home + link_p
        
        return folder_path
        

    def write_parsed_content(self, folder_path, content):
        '''
        
        Utility function for storing data into text files
        '''
        

class Listening(Content):

    '''
    Subclass for content parsed from listening tests
    '''

    def ___init__(self, url, title, content, audio_response):
        
        # initialize subclass GT
        Content.__init__(self, url, title, content)

        self.audio_response = audio_response # req response -> to use for storing 
        