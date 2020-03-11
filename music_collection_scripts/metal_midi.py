import os
import os.path
import requests
from bs4 import BeautifulSoup

DOMAIN = 'https://metal-midi.grahamdowney.com/isanmusic.webs.com'
#DOMAIN = 'https://metal-midi.grahamdowney.com'
MID_DOM = '.mid'
MIDI_DOM = '.midi'
METAL_MIDI_DIRECTORY = 'metallica_midis'
#METAL_MIDI_DIRECTORY = 'metal_midi_music'

def lena_gana_nam_link_se(link):
    pre_start = link.rfind('/')
    return METAL_MIDI_DIRECTORY + '/' + link[pre_start+1:]

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

def page_request():
    status_code = 0
    try:
        result = requests.get('https://metal-midi.grahamdowney.com/isanmusic.webs.com/metallica.html')
        #result = requests.get('https://metal-midi.grahamdowney.com/midi.html')
        if result.status_code != 200:
            status_code = result.status_code
            raise Exception('Status Code Failed')
        return result.text
    except Exception as e:
        print('Failed to get page because status code %d:\n%s' % (status_code, str(e)))

def download_music():
    if os.path.isdir(METAL_MIDI_DIRECTORY):
        print('ERRROR, ALREADY EXECUTED')
        return
    
    os.mkdir(METAL_MIDI_DIRECTORY)
    web_page_txt = page_request()
    if web_page_txt is None:
        return
    soup = BeautifulSoup(web_page_txt, 'html.parser')
    download_tags = soup.find_all(href=True)
    potential_links_to_look_at = []
    counter = 0
    for tag in download_tags:
        network_request = tag['href']
        if network_request is not None and len(network_request) >= 4 and MID_DOM in network_request[-4:].lower():
            if 'http' not in network_request[0:4]:
                network_request = DOMAIN+'/'+ network_request
            counter += get_song_saved(network_request)
        else:
            potential_links_to_look_at.append(network_request)
    print('SONGS: DOWNLOADED: ', counter)
    print('Consider looking at these links')
    for n in potential_links_to_look_at:
        print(n)


download_music()
