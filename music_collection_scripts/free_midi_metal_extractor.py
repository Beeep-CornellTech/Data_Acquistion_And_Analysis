import os
import os.path
import requests
from bs4 import BeautifulSoup

DOMAIN = 'https://freemidi.org/'
STARTING_PAGE = 'genre-metal'
PAGEINATION = 'pagination'

ARTIST_LINK_CSS_CLASS = 'genre-link-text'

MID_DOM = '.mid'
DIRECTORY = 'free_midi'


s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0'})

def page_request(url=DOMAIN+STARTING_PAGE):
    status_code = 0
    try:
        result = s.get(url)
        if result.status_code != 200:
            status_code = result.status_code
            raise Exception('Status Code Failed')
        return result.text
    except Exception as e:
        print('Failed to get page because status code %d:\n%s' % (status_code, str(e)))

def lena_gana_nam_link_se(link):
    pre_start = link.rfind('/')
    return DIRECTORY + '/' + link[pre_start+1:]

def get_song_saved(link):
    file_name = lena_gana_nam_link_se(link) + MID_DOM
    try:
        s.get(link) # To get right cooky
        result = s.get(link)
        if result.status_code != 200:
            raise Exception('Status Code ' + str(result.status_code))
        
        if len(result.content) < 4 or result.content[0:4] != b'MThd':
            raise Exception('Bad result  ' +  result.content)

        with open(file_name, 'wb') as f:
            f.write(result.content)
            return True
    except Exception as e:
        print('Failed to get %s becase %s' % (file_name, e))
        return False

def get_song_form_download_ref(ref):
    # Convert downlaod href to url to actually download song
    ref_parts = ref.split('-')
    assert len(ref_parts) > 2 and ref_parts[0] == 'download3'
    song_id = ref_parts[1]
    url =  DOMAIN + 'getter-'+ song_id

    # Download song
    return get_song_saved(url)

def get_songs_from_page(url):
    web_page_txt = page_request(url)
    if web_page_txt is None:
        print('FAILLUIRE_2: ' + url)
        return 
    
    soup = BeautifulSoup(web_page_txt, 'html.parser')
    songs_elements = soup.find_all('div', class_='artist-song-cell')
    counter = 0
    for elem in songs_elements:
        ref = elem.find_all('a', href=True)
        assert(len(ref) == 1)
        ref = ref[0]['href']

        got_song = get_song_form_download_ref(ref)
        counter += got_song
        if not got_song:
            print('FAILED: ' + ref)
    
    if counter == 0:
        print('FAILLUIRE_1: ' + url)
    return counter

def get_songs_from_artist_pagination(url):
    web_page_txt = page_request(url)
    if web_page_txt is None:
        print('FAILLUIRE_3: ' + url)
        return 
    
    soup = BeautifulSoup(web_page_txt, 'html.parser')
    pagination = soup.find_all(class_=PAGEINATION)
    
    hit_self = False
    if len(pagination) >= 1:
        page_links = pagination[0].find_all('a', href=True)
        counter = 0
        for anchor_element in page_links:
            ref = anchor_element['href']
            if ref == '#': # needed since self link always appears twice
                if not hit_self:
                    counter += get_songs_from_page(url)
                    hit_self = True
            
            else:
                new_url = DOMAIN + ref
                counter += get_songs_from_page(new_url)
    else:
        counter += get_songs_from_page(url)

    return counter



def download_music():
    if os.path.isdir(DIRECTORY):
        print('ERRROR, ALREADY EXECUTED')
        return
    
    os.mkdir(DIRECTORY)
    main_web_page_txt = page_request()
    if main_web_page_txt is None:
        print('Crap')
        return
    soup = BeautifulSoup(main_web_page_txt, 'html.parser')
    artist_links = soup.find_all(class_=ARTIST_LINK_CSS_CLASS)
    counter = 0
    
    total_artists = len(artist_links)
    artists_done = 0
    print(total_artists)
    for element in artist_links:
        network_requests = element.find_all('a', href=True)
        assert len(network_requests) == 1
        network_request = network_requests[0]['href']
        counter += get_songs_from_artist_pagination(DOMAIN + network_request)

        artists_done += 1
        print('FINISHED ' + str(artists_done) + ' / ' + str(total_artists) )
    
    print('SONGS: DOWNLOADED: ', counter)
    

if __name__ == '__main__':
    download_music()
