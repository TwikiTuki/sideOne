#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import sys
import os
import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
class colors:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'
    ENDC = '\033[0m'

def get_flags(args):
    usage = 'usage: ./spider [-r -l -p -S] URL'
    if (len(args) < 2):
        print(usage)

    flags={'url': None ,'recurse': False ,'depth': -1 ,'path': './images', 'verbose': False}
    flags['url'] = args[-1]
    i = 1
    max_i = len(args) - 1
    # Get the flags
    while i < max_i:
        flag = args[i][1:]
        # Assert the last flags arguments does not require an aditional argument
        if (i == max_i - 1 and flag in ['p', 'l']):
            print(usage)
            raise ValueError(f'Expected argument for -{flag}')
        # Now get the flags
        if (flag == 'r'):
            flags['recurse'] = True  
            i += 1
        elif (flag == 'p'):
            flags['path'] = args[i + 1]
            path = flags['path']
            if (not os.path.isdir(flags['path'])):
                raise FileNotFoundError(f'Spider: No such file or direcotry: {path}')
            i += 2
        elif (flag == 'l' ):
            flags['depth'] = args[i + 1]
            if (not flags['depth'].isdigit()):
                raise TypeError("depth (-l) must be a non negative integer")
            flags['depth'] = int(flags['depth'])
            i += 2
        elif (flag == 'v'):
            flags['verbose'] = True
            i += 1
        else:
            print(usage)
            raise ValueError(f'flag "{flag}" at index {i} is not allowed \n {usage}')
        if (not flags['recurse']):
            flags['depth'] = 0
    return (flags)

log_file = 'log_file.txt'

def hard_domain_check(url, check_domain=True):
    return 
    if (get_domain(url) != "https:42barcelona.com"):
        raise BaseException(f"Getting out of 42Barcelona", url)

def clean_link(link, check_domain=True):

    if (not link):
        return ""
    link = link.replace('https://', 'https:', 1)
    link = link.replace('https:www.', 'https:', 1)
    link = link.replace('http://', 'http:', 1)
    link = link.replace('http:www.', 'http:', 1)
    link = link.replace('file://', 'file:', 1)
    if (link[-1] == '/'):
        link = link[:-1]
#   if (check_domain):
#        print("checking domain in clean_link (shouldnt if comming from get_domain)")
#    hard_domain_check(link, check_domain=check_domain)
    return link

def get_domain(link):
    #print(f'Getting domain from: {link}')
    link = clean_link(link, check_domain=False)
    if (link.startswith('file:')):
        return ('localhost')
    # cut subdirectory
    scheme_end = len('https:') + 1
    if ('/' in link):
        link = link[0:link.find('/')]
    # cut port
    if (':' in link[scheme_end:]):
        link=link[:link.find(':', scheme_end)]
    return link

def valid_link(link):
    if (not link):
        return (False)
    link = clean_link(link)
    if (link.startswith('https:')):
        domain_start = len('https:')
    elif (link.startswith('http:')):
        domain_start = len('http:')
    elif (link.startswith('file:')):
        domain_start = len('file:')
    else:
        return (False)
    return len(link) - domain_start > 0

def get_url(url):
    res_dct = {}
    if (get_domain(url) == 'localhost'):
        res_dct['status_code'] = 200
        path = clean_link(url)[len('file:'):]
        print(f"opening local file {path}")
        try:
            with open(path, "r") as f:
                res_dct['text'] = f.read()
            res_dct['url'] = url
        except Exception as e :
            print(f"unable to open {path}")
            res_dct['status_code'] = '404' if os.path.exists(url) else '403'
        res_dct['content'] = None
        res_dct['encoding'] = None
    else:
        print(url, get_domain(url))
        hard_domain_check(url)
        # Asser url is valid for get_url
        url = clean_link(url)[len('https:'):]
        url = 'https://' + url 
        print(f'Getting: {url}')
        try: 
            resp = requests.get(url)
        except Exception:
            res_dct['status_code'] = 42 #something whent wrong
        else:
            res_dct['content'] = resp.content 
            res_dct['url'] = url
            res_dct['text'] = resp.text
            res_dct['encoding'] = resp.encoding
            res_dct['status_code'] = resp.status_code
    return res_dct
    
def scrap_url(url, visited):
    raise "Shouldnt be here"
    resp = get_url("https://www.42barcelona.com/")
    parser = Parser()
    parser.feed(resp['text'])

def generate_interesting_list(new_list, old_list, domain, verbose = True):
    print("FINDING NEW LINKS")
    result = []
    for link in new_list:
        link = clean_link(link)
        if (domain == 'localhost' and not link.startswith('file:')):
            link = '/' + link if link[0] != '/' else link 
            link = 'file:' + link
        if (verbose): print("New possible: ", end="")
        if (not valid_link(link)):
            if (verbose): print(f'\t{"ommited because the link is not valid":45}', colors.red, link, colors.ENDC)
            continue
        elif (get_domain(link) != domain):
            if (verbose): print(f'\t{"ommited because the domain is not valid":45}', colors.red, link, colors.ENDC)
            continue
        elif (link in old_list or link in result):
            if (verbose): print(f'\t{"ommited because already found":45}', colors.orange, link, colors.ENDC)
            continue
        else:
            if (verbose): print(f'\t{"adding":45}', colors.green, link, colors.ENDC)
            assert get_domain(link) == domain, 'The domain is not valid!!!!'
            result.append(link)
    result = set(result)
    
    return (result)
if (__name__ == '__main__'):
    urls = {}
    flags = get_flags(sys.argv)
    domain = get_domain(flags['url'])
    if (not valid_link(flags['url'])):
            print(f"No valid link: '{flags['url']}'")
            exit()
    pending_links = [(flags['url'], flags['depth'])]
    found_links = []
    found_links = [link[0] for link in pending_links]
    found_images = []
    while (pending_links):
        link, depth = pending_links.pop()
        print(f"PARSING ANOTHER LINK (dep: {depth}, {link})")
        hard_domain_check(link)
        resp = get_url(link)
        if (resp['status_code'] != 200):
            status_code = resp['status_code']
            print(colors.red, f'ERROR: status_code = {status_code} {link}', colors.ENDC)
            continue
        soup = BeautifulSoup(resp['text'])
        # Add the links from the page to the list of pending links
        if (depth):
            links = soup.find_all("a")
            links = [link.attrs['href'] for link in links if link.has_attr('href')]
            links = generate_interesting_list(links, found_links, domain, verbose = flags['verbose'])
            found_links += links
            pending_links += [(l, depth - 1) for l in links]
        # Add images from the page to the list of images to get

        imgs = soup.find_all("img")
        #print('!!!!!images: ', imgs)
        imgs  = [img.attrs['src'] for img in imgs if img.has_attr('src')]
        imgs = generate_interesting_list(imgs, found_images, domain, verbose = flags['verbose'])
        found_images += imgs

    print("CHECKED ALL THE WEBPAGE")
    for i, img in enumerate(found_images):
        resp = get_url(img)
        if (resp['status_code'] != 200):
            continue;
        #TO DO get shur we have an image
        name = img.split('?')[0]
        name = img.split('/')[-1]
        name = f'image_{i}__{name}'
        path = flags['path']
        path = f'./{path}/'
        path = path + name
        print(f'{path}: {img}')
        image_file = open(path, 'wb') 
        image_file.write(resp['content'])
        image_file.close()








#TODO
#Falta gestionar una flag
#Falta comprobar el tipus dels links i si son imarges afegirlos
#Falta gestionar fitxers locals
#Falta probar amb recursivitat

