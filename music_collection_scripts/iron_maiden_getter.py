import os
import os.path
import requests
from bs4 import BeautifulSoup

DOMAIN = 'http://www.maidenmidi.com/'
MID_DOM = '.mid'
DIRECTORY = 'iron_maiden_midis'

def lena_gana_nam_link_se(link):
    pre_start = link.rfind('/')
    return DIRECTORY + '/' + link[pre_start+1:]

def get_song_saved(link):
    file_name = lena_gana_nam_link_se(link)
    try:
        result = requests.get(link)
        if result.status_code != 200:
            raise Exception('Status Code ' + str(result.status_code))
        with open(file_name, 'wb') as f:
            f.write(result.content)
            print('Got song ' + file_name)
            return True
    except Exception as e:
        print('Failed to get %s becase %s' % (file_name, e))
        return False

def page_request(url=DOMAIN):
    status_code = 0
    try:
        result = requests.get(url)
        if result.status_code != 200:
            status_code = result.status_code
            raise Exception('Status Code Failed')
        return result.text
    except Exception as e:
        print('Failed to get page because status code %d:\n%s' % (status_code, str(e)))


def get_songs_saved(url):
    if 'http' not in url:
        url = DOMAIN + '/' + url
    web_page_txt = page_request(url)
    if web_page_txt is None:
        return 
    soup = BeautifulSoup(web_page_txt, 'html.parser')
    potential_songs = soup.find_all(href=True)
    counter = 0
    for tag in potential_songs:
        ref = tag['href']
        if ref is not None and len(ref) >= 4 and MID_DOM in ref[-4:].lower():
            counter += get_song_saved(DOMAIN + '/' + ref)
    print(f'GOT {counter} songs from {url}\n')
    return counter



def download_music():
    if os.path.isdir(DIRECTORY):
        print('ERRROR, ALREADY EXECUTED')
        return
    
    os.mkdir(DIRECTORY)
    main_web_page_txt = page_request()
    if main_web_page_txt is None:
        return
    soup = BeautifulSoup(main_web_page_txt, 'html.parser')
    potential_music_pages = soup.find_all(href=True)
    potential_links_to_look_at = []
    counter = 0
    for page in potential_music_pages:
        network_request = page['href']
        if network_request is not None:
            counter += get_songs_saved(network_request)
        else:
            potential_links_to_look_at.append(network_request)
    
    print('SONGS: DOWNLOADED: ', counter)
    print('Consider looking at these links')
    for n in potential_links_to_look_at:
        print(n)


download_music()
