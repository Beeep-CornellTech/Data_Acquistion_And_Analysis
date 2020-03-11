from music21.midi import MidiFile
import os
import sys


def process_von_dir(path):
    midi_type_to_count = [0,0,0]
    number_of_tracks_to_count = dict()
    metric_v_time = [0,0]

    midi_files = os.listdir(path)
    for i in range(len(midi_files)):
        file_name = midi_files[i]
        try:
            midi = MidiFile()
            midi.open(filename=path + '/' + file_name)
            midi.read()
            midi_type_to_count[midi.format] += 1
        except Exception as e:
            print('Failiure at song %d, %s: %s' %(i, file_name, str(e)))
            continue 
        trk_count = len(midi.tracks)
        if trk_count not in number_of_tracks_to_count:
            number_of_tracks_to_count[trk_count] = 0
        number_of_tracks_to_count[trk_count] += 1

        is_metric = midi.ticksPerSecond is None and midi.ticksPerQuarterNote is not None
        assert(is_metric or midi.ticksPerSecond is not None and midi.ticksPerQuarterNote is None)
        metric_v_time[is_metric] += 1
        midi.close()

    print('*********\nData For %s:' % path)
    print('Type Counts:\t', midi_type_to_count)
    print('timDev metric versus time based:\t', metric_v_time)
    print('Number of tracks with corresponding counts:')
    for track_counts in number_of_tracks_to_count:
        print('%d\t%d' %(track_counts, number_of_tracks_to_count[track_counts]))
    print('**************\n')


for directory in sys.argv[1:]:
    process_von_dir(directory)

