# python libraries
from urllib import parse
import requests
from bs4 import BeautifulSoup
import os
import re
import sys

# app libraries
from helpers import *
from schemes import *
from tests_parser import *
from view import *

sys.setrecursionlimit(10000)

class Webpage:
    
    """
    common base information structure of the target website
    """

    # intialize basic information of website
    def __init__(self, url, headers, title, ils_if, target_params):
        """
        initialize common base information
        """
        self.abs_url = parse.urlparse(url).scheme + "://" + parse.urlparse(url).netloc
        self.rel_url = parse.urlparse(url).path
        self.headers = headers
        self.title = title
        self.ils_if = ils_if
        self.target_params = target_params

class Tests(Webpage):

    """
    Information structure for reading tests
    instance receives a postlink and a test object and an answers object that contain the tags required for' getting the data

    --------------------------------------------------------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, url, headers, title, ils_if, target_params, post):

        # initialize base class WebPage
        Webpage.__init__(self, url, headers, title, ils_if, target_params)

        self.post_link = post # link for making post_requests, this is unique for tests websites
        self.tag_scheme = dict() # tag scheme for retrieving content from a page 



class Crawler:
    """

    Utility for cralwling and extracting information from target websites 
    """
    def __init__(self, site, ils=False, folder_name=None):
        self.site = site
        self.surfed_ils = set()
        
        if ils == False:
            self.ils = set()
        else: 
            self.ils = feed_crawler_links(folder_name)


    def get_page(self, url, method, headers, return_req_object=False, parser='html.parser', payload={}):
        """
        utility function that sends a request to a target website
        method can be get or post and return a soup object 
        """
        soup = None
        req = None
        timeout = (None, None)

        while soup == None:
            
            # get request
            if method == "GET":
                    
                try:
                    req = requests.get(url, headers=headers, timeout=timeout)
                    req.raise_for_status()

                except requests.exceptions.HTTPError as errh:

                    print('HTTP Error:', errh)
                
                except requests.exceptions.ConnectionError as errc:
                
                    print('Connection Error:', errc)
                    timeout = (15, 15) 
                    continue
                
                except requests.exceptions.Timeout as errt:
                    
                    print('Timeout Error:', errt)
                    timeout = (15, 15)
                    continue  

                except requests.exceptions.RequestException as err:
                    
                    print('Oops Something went wrong', err)

                soup = BeautifulSoup(req.text, parser)

            # post request
            else:

                try:
                    req = requests.post(url, headers=headers, data=payload, timeout=timeout)
                    req.raise_for_status()

                
                except requests.exceptions.HTTPError as errh:

                    print('HTTP Error:', errh)
                
                except requests.exceptions.ConnectionError as errc:
                
                    print('Connection Error:', errc)
                    timeout = (15, 15)  
                    continue

                except requests.exceptions.Timeout as errt:
                    
                    print('Timeout Error:', errt)
                    timeout = (15, 15)
                    continue  

                except requests.exceptions.RequestException as err:
                    
                    print('Oops Something went wrong', err)

                soup = BeautifulSoup(req.text, parser)
                
        if return_req_object == False:
            return soup
        if return_req_object == True:
            return soup, req

    def get_links(self, url):
        """
        utility function for getting all of internal links of a website based on a chosen selector with g_links being the tags for the search
        """
        # get all the internal links of webpage
        try:

            for link in self.get_page(url, 'GET', self.site.headers[0]).find_all(self.site.ils_if[0], attrs=self.site.ils_if[-1]):
                print("-"*20)
            
                if re.compile(r'\?p=[0-9]*').match(link.attrs['href']) != None:
                    link.attrs['href'] = self.site.abs_url + link.attrs['href']

                if link.attrs['href'] not in self.ils:
                    self.ils.add(link.attrs['href'])
                    print('Stored: {}'.format(link.attrs['href']))
                    print('Surfing --> {}'.format(link.attrs['href']))
                    
                    self.get_links(link.attrs['href'])
            
                else:
                    print(link.attrs['href'], end=' ')
                    print("already exists surfing to new link")
                    continue

        except AttributeError as e:
            print(e)
            print("Continuing")


    def check_if_target(self, url, pattern=None, look_for_inst=False):
        
        '''
        class utility to for determining whether a page url contains target information defined by the page_target parameters 
        if look_for_inst is set to true, then the function will also return the instances of a target url from a list of internal links which can either be found with the get_links class function or loaded from a file and then assigned to the ils (internal links) variable of the crawler
        '''

        # check if the page is a target page 
        target_exists = self.get_page(url, 'GET', self.site.headers[0]).find(self.site.target_params[0], attrs= self.site.target_params[-1])
        
        # find and return target page link with number of instances in ils
        if target_exists != None:
            
            # functionality for retrieving instances of the link
            if look_for_inst == True: 

                inst = find_pattern_inst(pattern, self.ils)

                return (url, inst)

            else:
                return url
        else:
            return None
       
               
    def parse_tests_site(self):
        # some variables for keeping track of links
        target_nums = 0
        link_nums = 0
        home = '/home/raguy92/downloads/' 

        # loop through links in this case
        for link in self.ils:

            # determine target_page type
            target = self.check_if_target(link, pattern=re.compile(rf'{link}.*'), look_for_inst=True)
            print("-"*100)

            if target != None:

                # target url and num of instances
                p_url = target[0]
                p_nums = target[-1]

                target_nums += 1
                print("Found target {}".format(p_url))
                print("Number of Instances {}".format(p_nums))
                print("Number of Targets found {}".format(target_nums))

                # retrieve questions page
                q_page, req = self.get_page(p_url, 'GET', self.site.headers[0], parser='html.parser', return_req_object=True)

                # retrieve answers page
                self.site.headers[-1][-1]['quiz_id'] = retr_q_id(q_page.select('.quiz-form')[0])
                
                ca_page = self.get_page(self.site.post_link, 'POST', self.site.headers[-1][0], parser='lxml', payload=self.site.headers[-1][-1])
    
                # get test type 
                link_p = parse.urlparse(req.url).path.strip('/')
                test_type = link_p.split('/')[0] 

                # if test_type == 'level-test':
                #     link_p = 'level-test/'

                # if test-category is level-test 
                if test_type == 'listening':
                    
                    # assign scheme appropriate to test type
                    self.site.tag_scheme = listening_scheme

                    try:
                        # parse content
                        content = parse_tests_content(q_page, ca_page, self.site.tag_scheme)
                    
                        # retrieve audio
                        audio_link = get_audio_link(q_page, self.site.tag_scheme)
                        payload = {'search_txt': audio_link}
                        post_link = 'https://www.easymp3converter.com/models/convertProcess.php'

                        ad_page = self.get_page(post_link, 'POST', self.site.headers[0], payload=payload, parser='lxml')

                        d_links = ad_page.find_all('option')
                        d_link = None

                        for link in d_links:

                            if link.get_text() == 'mp3\xa0128kbps':
                                d_link = 'https:' + link.attrs['data-link']

                        content['audio'] = d_link
                    
                    except Exception as e:

                        with open('logs.txt', 'a+') as logs:
                            
                            logs.write(p_url + '\n')
                            logs.write('\n')
                            logs.write('\t\t' + str(e) + '\n')
                            logs.write('\n')

                        print('Found Error Here')
                        print("Continuing")
                    
                    # initialize an instant and store parsed info in this instance
                    p_test = Listening(p_url, content['test_title'], content)
                    p_test.show_parsed_items()
                    
                    # create folder path 
                    f_path = p_test.create_folder_path(link_p, home)
                    print(f_path)

                else: 

                    # assign scheme
                    self.site.tag_scheme = general_scheme
 
                    try:
                        # parse content
                        content = parse_tests_content(q_page, ca_page, self.site.tag_scheme)
                    
                    except Exception as e:

                        with open('logs.txt', 'a+') as logs:
                            
                            logs.write(p_url + '\n')
                            logs.write('\n')
                            logs.write('\t\t' + str(e) + '\n')
                            logs.write('\n')

                        print('Found Error Here')
                        print("Continuing")

                    # initialize content instance
                    p_test = Content(p_url, content['test_title'], content)
                    p_test.show_parsed_items()

                    # create folder path 
                    f_path = p_test.create_folder_path(link_p, home)
                    print(f_path)
                
            else:

                link_nums += 1
                print("Target not found")
                print("Continuing.........")
                print("Number of links surfed {}".format(link_nums))
        
        
        # write total links surfed and numbers surfed in logs
        with open('logs.txt', 'a+') as logs:
            
            logs.write('Total num of links surfed {}, Total num of targets found {}'.format(link_nums, target_nums))

                



if __name__ == "__main__":

    # website schemes and information
    websites = [
        [
            "https://test-english.com/",
            [
                {"User-Agent": "Mozilla/75.0"}, 
                [
                {"User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0 Chrome/73.0.3683.103", "X-Requested-With": "XMLHttpRequest"}, {"action": "watupro_submit", "quiz_id": ''}
                ]
            ],
            '.header h1',
            ["a", {"href" : re.compile(r'(\?p=[0-9]*)|((https://)|(https://www\.))test-english\.com')}],
            ["form", {"class" : "quiz-form"}],
            "https://test-english.com/staging01/wp-admin/admin-ajax.php"
        ],
        ["http://www.englishprofile.org/wordlists/evp"],
    ]

    # create website and crawler instance
    test = Tests(websites[0][0], websites[0][1], websites[0][2], websites[0][3], websites[0][4], websites[0][5])
    test_crawler = Crawler(test, ils=True, folder_name='eng_test_links.txt')
    
    test_crawler.parse_tests_site()