import argparse
from jazz import bushgraft_midi_downloader as bmd

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("output", help="folder to store downloaded songs")
	parser.add_argument("num_songs", help="number of songs to download", type=int)
	args = parser.parse_args()

	bg_downloader = bmd.BushGraftMidiDownloader(num_songs=int(args.num_songs), download_folder=args.output)
	bg_downloader.get_song_links()
	bg_downloader.download_songs()
