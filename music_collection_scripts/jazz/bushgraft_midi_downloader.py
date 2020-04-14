import os
import os.path
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class BushGraftMidiDownloader():
	def __init__(self, num_songs, download_folder):
		self.num_songs = num_songs
		self.url = "https://bushgrafts.com/midi/"
		self.download_folder = download_folder

	def is_midi_link(self, link):
		return link != None and '.mid' in link.lower()

	def get_song_links(self):
		#get page
		try:
			page_response = requests.get(self.url)
			if page_response.status_code == 200:
				page_html = page_response.content
			else:
				print("Error in getting song page! {}".format(e))
				return	
		except Exception as e:
			print("Error in getting song page! {}".format(e))
			return

		page_soup = BeautifulSoup(page_html, 'html.parser')
		self.song_links = []
		for link in page_soup.find_all('a'):
			href = link.get('href')
			if self.is_midi_link(href):
				self.song_links.append(href)

		#print stats
		print("Number of links found: ", len(self.song_links))
		if self.song_links != -1:
			print("Number of songs required: ", self.num_songs)
			if len(self.song_links) > self.num_songs:
				self.song_links = self.song_links[:self.num_songs]

			print(self.song_links)

	def extract_song_name(self, link):
		tokens = link.split("/")
		return tokens[-1:][0].lower()

	def download_song(self, link, output_fname):
		try:
			result = requests.get(link)
			if result.status_code == 200:
				path = os.path.join(self.download_folder, output_fname)
				with open(path, 'wb') as f:
					f.write(result.content)
			else:
				print("Link: {}, error code: {}".format(link, result.status_code))
		except Exception as e:
			print('Failed to get %s becase %s' % (output_fname, e))
			return False

	def download_songs(self):
		for i in tqdm(range(len(self.song_links))):
			l = self.song_links[i]
			fname = self.extract_song_name(l)
			self.download_song(l, fname)
