# python libraries
from urllib import parse
import requests
from bs4 import BeautifulSoup
import os
import re
import sys

# app libraries
from helpers import *
from schemes import grammer_scheme
from tests_parser import *

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

    -------------------------------------------------------------------------------------------------------
    """

    def __init__(self, url, headers, title, ils_if, target_params, post, tag_scheme):

        # initialize base class WebPage
        Webpage.__init__(self, url, headers, title, ils_if, target_params)

        self.post_link = post # link for making post_requests, this is unique for tests websites
        self.tag_scheme = tag_scheme # tag scheme for retrieving content from a page 



class Crawler:
    """

    Utility for cralwling and extracting information from target websites 
    """
    def __init__(self, site):
        self.site = site
        self.ils = set()

    def get_page(self, url, method, headers, return_req_object=False, parser='html.parser', payload={}):
        """
        utility function that sends a request to a target website
        method can be get or post and return a soup object 
        """

        if method.lower() == "GET":
            try:
                req = requests.get(url, headers=headers)
            except requests.exceptions.RequestException:
                return None
            
            return BeautifulSoup(req.text, parser)

        else:
            try:
                req = requests.get(url, headers=headers, data=payload)
            except requests.exceptions.RequestException:
                return None
            
            if return_req_object == False:
                return BeautifulSoup(req.text, parser)
            if return_req_object == True:
                return BeautifulSoup(req.text, parser), req

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
            print("continuing")


    def check_if_target(self, url, pattern=None, list=None, look_for_inst=False):
        
        '''
        class utility to for determining whether a page url contains target information defined by the page_target parameters 
        if look_for_inst is set to true, then the function will also require a list and pattern by default those are set to None
        '''
        # see if the page has a form all test_pages on this site have one
        target_exists = self.get_page(url, 'GET', self.site.headers[0]).find(self.site.target_params[0], attrs= self.site.target_params[-1])
        
        # find and return test page with instance  
        if target_exists != None:
            
            # only if all of the internal links have already been extracted from the website
            if look_for_inst == True: 
                inst = find_pattern_inst(pattern, list)

                return url, inst

            else:
                return url
        else:
            return None
            
       
    def parse_tests_page(self):

        # loop through links
        for link in self.ils:

            # determine target_page type
            target = self.check_if_target(link, pattern=re.compile(rf'{link}.*'), list=test_crawler.ils, look_for_inst=True)

            print("-"*100)
            if target != None:
                print("Found target {}".format(target[0]))

                # retrieve questions page
                q_page, req = self.get_page(target[0], 'GET', self.site.headers[0], return_req_object=True, parser='lxml')

                # retrieve answers page
                payload = self.site.headers[-1][-1]
                self.site.headers[-1][-1]['quiz_id'] = retr_q_id(q_page.select('.quiz-form')[0])
                ca_page = self.get_page(target, 'POST', self.site.headers[-1][0], parser='lxml', payload=payload)

                # get test type 
                test_type = parse.urlparse(req.url).path.strip('/').split('/')[0]

                
                # if test-category is level-test 
                if test_type == 'level-test':
                    pass 

                    # create content instance for level-test
                    # create site instance for level-test
                        # parse page
                    # store information from level-test content instance
                    # create document out of content instance 
                    
                
                # if page is title is grammer-points do something
                # elif page_type == 'grammar-points':
                #     print('Page Type {}'.format(page_type))
                
                # if page is title is listening do something
                # elif page_type == 'listening':
                #     print('Page Type {}'.format(page_type))
                
                # if page is title is reading do something
                # elif page_type == 'reading':
                #     print('Page Type {}'.format(page_type))
                
                # if page is title is writing do something
                # elif page_type == 'writing':
                #     print('Page Type {}'.format(page_type))

                
            else:
                print("Target not found")
                print("Continuing.........")
                



if __name__ == "__main__":

    # website schemes and information
    websites = [
        [
            "https://test-english.com/",
            [{"User-Agent": "Mozilla/75.0"}, [{"User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0 Chrome/73.0.3683.103", "X-Requested-With": "XMLHttpRequest"}, {"action": "watupro_submit", "quiz_id": ''}]] ,
            'h1',
            ["a", {"href" : re.compile(r'(\?p=[0-9]*)|((https://)|(https://www\.))test-english\.com')}],
            ["form", {"class" : "quiz-form"}],
            "https://test-english.com/staging01/wp-admin/admin-ajax.php",
            grammer_scheme
        ],
        ["http://www.englishprofile.org/wordlists/evp"],
    ]

    # create website and crawler instance
    test = Tests(websites[0][0], websites[0][1], websites[0][2],websites[0][3], websites[0][4], websites[0][5], websites[0][6])
    test_crawler = Crawler(test)
    
    # feed links to crawler  
    test_crawler.ils = feed_crawler_links('eng_test_links.txt')
    #

    # test_crawler.parse_tests_page()


    # # find target links in list
    

    #     print('-'*50)
    #     if result != None:
    #         print('Found test at --> {}'.format(result[0]))
    #         if result[-1] > 1:
    #             print('test concists of {} pages'.format(result[-1]))
    #         else:
    #             print('test concists of {} page'.format(result[-1]))
    #     else:
    #         print("Didn't find target at --> {}".format(link))
    
# when target found
    # check test type (how do i find out test type, link title)
        # run parse function  


