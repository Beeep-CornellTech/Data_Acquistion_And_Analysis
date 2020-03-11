import os
import os.path
import requests
from bs4 import BeautifulSoup

TOTAL_METAL_SONGS = 1753
SONGS_PER_PAGE = 20
MP3_TYPE = '.mp3'
FMA_DIRECTORY = 'fma_music'

def lena_gana_nam_link_se(link):
    pre_start = link.rfind('/')
    return FMA_DIRECTORY + '/' + link[pre_start+1:]

def get_song_saved(link):
    file_name = lena_gana_nam_link_se(link)
    try:
        result = requests.get(link)
        if result.status_code != 200:
            raise Exception('Status Code ' + str(result.status_code))
        with open(file_name, 'wb') as f:
            f.write(result.content)
            print('Got song ' + file_name)
    except Exception as e:
        print('Failed to get %s becase %s' % (file_name, e))

def page_request(genre, page_number):
    status_code = 0
    try:
        params = {'sort':'track_date_published','d':'1','page':str(page_number) }
        result = requests.get('https://freemusicarchive.org/genre/'+genre, params=params)
        if result.status_code != 200:
            status_code = result.status_code
            raise Exception('Status Code Failed')
        return result.text
    except:
        print('Failed to get page %d because status code %d' % (page_number, status_code))
        return None


def tets_get_music():
    get_music('https://files.freemusicarchive.org/storage-freemusicarchive-org/music/Ziklibrenbib/Peculate/st/Peculate_-_09_-_The_Immediate_Task.mp3')

def test_get_page():
    print(page_request('Metal',1))

def get_music_page_se(genre, page_number):
    if not os.path.isdir(FMA_DIRECTORY):
        os.mkdir(FMA_DIRECTORY)

    web_page_txt = page_request(genre, page_number)
    if web_page_txt is None:
        return
    soup = BeautifulSoup(web_page_txt, 'html.parser')
    download_tags = soup.find_all(title="Download")
    for tag in download_tags:
        network_request = tag['href']
        if network_request is not None and len(network_request) >= 4 and network_request[-4:] == MP3_TYPE:
            get_song_saved(network_request)


get_music_page_se('Metal', 1)
