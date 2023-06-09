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
    usage = '''
    usage: ./spider [-r -l -p -v] URL
    URL: indicates the intital url for scraping.
    -r: Indicates that any link found in URL should be checked recursively.
        By default it will finish when it gets all the webpage links.
    -l: Sets a maximum depth to the -r flag.
    -p: Indicates the path to save the images.
    -v: Prints more information when scraping.
    '''
    if (len(args) < 2):
        print(usage)

    flags={'url': None ,'recurse': False ,'depth': 0 ,'path': './data', 'verbose': False}
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
            flags['depth'] = -1  
            i += 1
        elif (flag == 'p'):
            flags['path'] = args[i + 1]
            path = flags['path']
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
    if (not os.path.exists(flags['path'])):
        os.mkdir(flags['path'])
        print("made dir {flags['path']}")
    else:
        print("didnt make dir", os.path.exists(flags['path']), flags['path'])
    return (flags)

log_file = 'log_file.txt'

def hard_domain_check(url, check_domain=True):
    return 
    if (get_domain(url) != "https:42barcelona.com"):
        raise BaseException(f"Getting out of 42Barcelona", url)

def clean_link(link, check_domain=True):
    if (not link):
        return ""
    if (link.startswith('www.')):
        link = link.replace('www.', 'https:')
    link = link.replace('https://', 'https:', 1)
    link = link.replace('https:www.', 'https:', 1)
    link = link.replace('http://', 'http:', 1)
    link = link.replace('http:www.', 'http:', 1)
    link = link.replace('file://', 'file:', 1)
    while (link.endswith(('/', '#'))):
        link = link[:-1]
    return link

def get_domain(link):
    #print(f'Getting domain from: {link}')
    link = clean_link(link, check_domain=False)
    if (link.startswith('file:')):
        return ('filetype')
    # cut subdirectory
    if link.startswith('https:'):
        scheme_end = len('https:') + 1
    else:
        scheme_end = len('http:') + 1
    if ('/' in link):
        link = link[0:link.find('/')]
    # cut port
    if (':' in link[scheme_end:]):
        link=link[:link.find(':', scheme_end)]
    return link

def valid_link(link):
    if (not link):
        return (False)
    clean_link(link)
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
    if (get_domain(url) == 'filetype'):
        res_dct['status_code'] = 200
        path = clean_link(url)[len('file:'):]
        print(f"opening local file {path}")
        try:
            with open(path, "br") as f:
                res_dct['content'] = f.read()
            with open(path, "r") as f:
                res_dct['text'] = f.read()
            res_dct['url'] = url
        except Exception as e :
            if (type(e) == UnicodeDecodeError):
                res_dct['text'] = None
            else:
                print(f"unable to open {path}")
                res_dct['status_code'] = '404' if os.path.exists(url) else '403'
        res_dct['encoding'] = None
    else:
        hard_domain_check(url)
        # Asser url is valid for get_url
        #url = clean_link(url)[len('https:'):]
        #url = 'https://' + url 
        url = url.replace('https:', 'https://')
        url = url.replace('http:', 'http://')
        print(f'Getting: {url}')
        try: 
            resp = requests.get(url)
        except Exception as e:
            res_dct['status_code'] = 42 #something whent wrong
        else:
            res_dct['content'] = resp.content 
            res_dct['url'] = url
            res_dct['text'] = resp.text
            res_dct['encoding'] = resp.encoding
            res_dct['status_code'] = resp.status_code
    return res_dct
    
def solve_host(model, incomplete):
    '''
        !!!! it expects a cleaned url returned by the function clean_link()
        It tries to figure out whteer the incomplete url has a host or not. If it doesnt it  tries to use the model's host
    '''
    #print(f"\nsovling_host: model = {model}, incomplete = {incomplete}")
    if (not model or not incomplete):
        return (incomplete)
    model = clean_link(model)
    if ('/' in model and get_domain(model) == 'filetype'):
        model = '/'.join(model.split('/')[:-1])
    #print(f"after clean: model = {model}, incomplete = {incomplete}")
    # Check wheter it should have domain, if it should return the original
    if (incomplete.startswith(('http', 'https'))):
        return (incomplete)
    incomplete = incomplete.replace("file:", "")
    if (incomplete[0] == '/' and get_domain(model) == 'filetype'):
        result = 'file:' + incomplete
    elif (incomplete[0] == '/'):
        result = model.split('?')[0]
        if (result[-1] == '/'):
            result = result[:-1]
        result = result.split('/')[0]
        result += incomplete
    elif (incomplete[0:2] == './'):
        result = model.split('?')[0]
        if (result[-1] == '/'):
            result = result[:-1]
        result += incomplete[1:]
    else: 
        result = model.split('?')[0]
        if (result[-1] == '/'):
            result = result[:-1]
        result += '/' + incomplete
    return (result)

def generate_interesting_list(new_list, old_list, old_link, domain, verbose = True):
    print("FINDING NEW LINKS/IMAGES")
    result = []
    for link in new_list:
        print(f"NEW LINK TO TEST {link}")
        link = clean_link(link)
        link = solve_host(old_link, link)
        if (verbose): print("  New possible: ", end="")
        if (not valid_link(link)):
            if (verbose): print(f' {"ommited the link is not valid":38}', colors.red, link, colors.ENDC)
            continue
        elif (domain and get_domain(link) != domain):
            if (verbose): print(f' {"ommited the domain is not valid":38}', colors.red, link, colors.ENDC)
            continue
        elif (link in old_list or link in result):
            if (verbose): print(f' {"ommited already found":38}', colors.orange, link, colors.ENDC)
            continue
        else:
            if (verbose): print(f' {"adding":38}', colors.green, link, colors.ENDC)
            assert not domain or get_domain(link) == domain, 'The domain is not valid!!!!'
            result.append(link)
    result = set(result)
    return (result)

def initial_local_url_check(url):
    url = clean_link(url)
    if (not url or url.startswith(('http', 'https'))):
        return (url)
    if (url.startswith('file:')):
        url = url[len('file:'):]
    if (url[0] != '/' and url[0:2] != './'):
        url = './' + url
    url = 'file:' + url
    return (url)
    
if (__name__ == '__main__'):
    print("HELLOOW SPIDY") 
    urls = {}
    flags = get_flags(sys.argv)
    flags['url'] = initial_local_url_check(flags['url'])
    print(f"flags: {flags}")
    domain = get_domain(flags['url'])
    #print("The starting link will be:", flags['url'])
    if (not valid_link(flags['url'])):
        print(f"Not valid link: '{flags['url']}'")
        exit()
    pending_links = [(flags['url'], flags['depth'])]
    found_links = []
    found_links = [link[0] for link in pending_links]
    found_images = []
    while (pending_links):
        link, depth = pending_links.pop()
        print(f"\nPARSING ANOTHER LINK (dep: {depth}, {link})")
        resp = get_url(link)
        if (resp['status_code'] != 200):
            status_code = resp['status_code']
            print(colors.red, f'ERROR: status_code = {status_code} {link}', colors.ENDC)
            continue
        soup = BeautifulSoup(resp['text'], features="html.parser")
        # Add the links from the page to the list of pending links
        if (depth):
            links = soup.find_all("a")
            links = [link.attrs['href'] for link in links if link.has_attr('href')]
            links = generate_interesting_list(links, found_links, link, domain, verbose = flags['verbose'])
            found_links += links
            pending_links += [(l, depth - 1) for l in links]
        # Add images from the page to the list of images to get
        imgs = soup.find_all("img")
        imgs  = [img.attrs['src'] for img in imgs if img.has_attr('src')]
        imgs = generate_interesting_list(imgs, found_images, link, None, verbose = flags['verbose'])
        found_images += imgs

    print("\nCHECKED ALL THE WEBPAGE")
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
        print(f'  image {img}\n  saved on {path}')
        image_file = open(path, 'wb') 
        image_file.write(resp['content'])
        image_file.close()

#TODO
#Falta gestionar una flag
#Falta gestinoar urls relatives
#Falta gestionar fitxers locals
#No se si crea l'arixu on ficar les imatgeo

#Testejar amb altres webs
