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

    flags={'url': None ,'recurse': False ,'depth': -1 ,'path': None}
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
                raise FileNotFoundError(f'No such file or direcotry: {path}')
            i += 2
        elif (flag == 'l' ):
            flags['depth'] = args[i + 1]
            if (not flags['depth'].isdigit()):
                raise TypeError("depth (-l) must be a non negative integer")
            flags['depth'] = int(flags['depth'])
            i += 2
        else:
            print(usage)
            raise ValueError(f'flag "{flag}" at index {i} is not allowed \n {usage}')
        if (not flags['recurse']):
            flags['depth'] = 0
    return (flags)

log_file = 'log_file.txt'

def hard_domain_check(url, check_domain=True):
    print(f'Hard checking {url}')
    if (get_domain(url) != "https:42barcelona.com"):
        raise BaseException("Getting out of 42Barcelona", url)

def clean_link(link, check_domain=True):

    if link == None:
        raise Exception("the link you are trying to celan is None")
    link = link.replace('https://', 'https:', 1)
    link = link.replace('https:www.', 'https:', 1)
    if (link[-1] == '/'):
        link = link[:-1]
#   if (check_domain):
#        print("checking domain in clean_link (shouldnt if comming from get_domain)")
#    hard_domain_check(link, check_domain=check_domain)
    return link

def get_domain(link):
    #print(f'Getting domain from: {link}')
    link = clean_link(link, check_domain=False)
    # cut subdirectory
    scheme_end = len('https:') + 1
    if ('/' in link):
        link = link[0:link.find('/')]
    # cut port
    if (':' in link[scheme_end:]):
        link=link[:link.find(':', scheme_end)]
    return link

def get_url(url):
    print(url, get_domain(url))
    hard_domain_check(url)
    # Asser url is valid for get_url
    url = clean_link(url)[len('https:'):]
    url = 'https://' + url
    res_dct = {}
    resp = requests.get(url)
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

if (__name__ == '__main__'):
    urls = {}
    flags = get_flags(sys.argv)
    domain = get_domain(flags['url'])
    resp = get_url("https://www.42barcelona.com/")
    resp = get_url("https://www.42barcelona.com/es/actualidad/actitud-42-dani-lopez/")
    resp = get_url(flags['url'])
    soup = BeautifulSoup(resp['text'])
    links = soup.find_all("a")
    links = [link.attrs['href'] for link in links if link.has_attr('href')]
    links_aux = []
    '''
    for link in links:
        if (get_domain(link) != domain):
            continue
        link = clean_link(link)
        else:
            links_aux.append(link)
    links = links_aux
    '''

    pending_links = []
    found_links = []
    for link in links:
        print("\ttesting: ", link, end='')
        if (get_domain(link) != domain):
            print('\tinvalid domain')
            continue
        link = clean_link(link)
        if (link in found_links):
            print('\talready added')
            continue
        else:
            print('\tadded')
            pending_links.append(link)
            found_links.append(link)
    #        hard_domain_check(link)
    with open('__log_file__.txt', 'w') as f:
        for link in found_links:
            f.write(link)
            f.write('\n')

        '''
        if (get_domain(link) == domain and link not in found_links):
            pending_links.append(link)
            found_links.append(link)
            print('added', link)
            hard_domain_check(link)
        '''
    print("MADE FIRST LOAD\n")
    while (pending_links):
        print("PARSING ANOTHER LINK")
        link = pending_links.pop()
        hard_domain_check(link)
        resp = get_url(link)
        if (resp['status_code'] != 200):
            continue
        soup = BeautifulSoup(resp['text'])
        links = soup.find_all("a")
        links = [link.attrs['href'] for link in links if link.has_attr('href')]
        print("FINDING NEW LINKS")
        for link in links:
            print("New possible link:", end="")
            if (get_domain(link) != domain):
                print(f'\t{"ommited because the domain is not valid":45}', colors.red, link, colors.ENDC)
                continue
            elif (link in found_links):
                print(f'\t{"ommited because already found":45}', colors.orange, link, colors.ENDC)
                continue
            else:
                print(f'\t{"addin":45}', colors.green, link, colors.ENDC)
                print('Domains: ', get_domain(link), domain)
                print("willl surviveeeeee")
                assert get_domain(link) == domain, 'The domain is not valid!!!!'
                print("stiiiillll aliveeeee")
                pending_links.append(link) 
                found_links.append(link)
                last_added = found_links[-1]
                print(f'\tlast found: {last_added}, added: {link}')

