from bs4 import BeautifulSoup
import re 
import urllib
import time
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

#url of directory listings of packages
#create a webdriver object and set options for headless browsing
options = webdriver.ChromeOptions()
options.add_argument('--headless')
service = Service(executable_path=r'./chromedriver')
driver = webdriver.Chrome(service=service,options=options)


#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,driver):
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup

#tidies extracted text 
def process_control_file(control):
	# removes non-ascii characters
    control = control.encode('ascii',errors='ignore').decode('utf-8')  
     #repalces repeated whitespace characters with single space   
    control = re.sub('\s+',' ',control)      
    return control

''' More tidying
Sometimes the text extracted HTML webpage may contain javascript code and some style elements. 
This function removes script and style tags from HTML so that extracted text does not contain them.
'''
def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup


# Get url of control file
def is_valid_control_file(control_url,dir_url):
    try:
        ret_url = urllib.request.urlopen(control_url).geturl() 
    except:
    	# unable to access control_url
        return False       
    # removes url scheme (https,http or www) 
    urls = [re.sub('((https?://)|(www.))','',url) for url in [ret_url,dir_url]] 
    return not(urls[0]== urls[1])


#extracts all packages url 
def scrape_dir_page(dir_url,driver):
    print ('-'*20,'Scraping directory page','-'*20)
    control_links = []
    package_base_url = 'https://salsa.debian.org'
    #execute js on webpage to load package listings on webpage and get ready to parse the loaded HTML 
    soup = get_js_soup(dir_url,driver)     
    # get list of all <div> of the specified class
    for link_holder in soup.find_all('div',class_='gl-display-flex gl-align-items-center gl-flex-wrap title namespace-title gl-font-weight-bold gl-mr-3'): 
        rel_link = link_holder.find('a')['href'] #get url
        #url returned is relative, so we need to add base url
        control_links.append(package_base_url+rel_link) 
    print ('-'*20,'Found {} package listing urls'.format(len(control_links)),'-'*20)
    return control_links

