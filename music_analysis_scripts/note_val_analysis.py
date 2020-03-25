import json
import sys
import os
from processing_scripts.midi_modificaiton import CHANNELS_TO_NEW_NAMES

INSTRUMENTS = CHANNELS_TO_NEW_NAMES.values()
MAX = 'max_pitch'
MIN = 'min_pitch'

def process_sentence(sentence, tags_to_min_max_pitches):
    if len(sentence) == 3 and sentence[1] == 'NOTEON':
        instr = sentence[0]
        assert sentence[0] in INSTRUMENTS
        pitch = int(sentence[-1])
        if instr not in tags_to_min_max_pitches:
            tags_to_min_max_pitches[instr] = {MIN: pitch, MAX: pitch}
        else:
            if tags_to_min_max_pitches[instr][MAX] < pitch:
                tags_to_min_max_pitches[instr][MAX] = pitch
            elif tags_to_min_max_pitches[instr][MIN] > pitch:
                tags_to_min_max_pitches[instr][MIN] = pitch

def process_song(fpath, tags_to_min_max_pitches):
    try:
        with open(fpath, 'r') as f:
            for line in f:
                line = line.strip()
                sentence = line.split('_')
                assert len(sentence) in (2,3)
                process_sentence(sentence, tags_to_min_max_pitches)

    except Exception as err:
        print(f"Issue with {fpath} :  {err}")
        
def update_instrument_mins_and_max_pitches(directory, tags_to_min_max_pitches):
    folder_names = os.listdir(directory)
    for f in folder_names:
        f = directory + '/'+ f
        if os.path.isdir(f):
            update_instrument_mins_and_max_pitches(f, tags_to_min_max_pitches)
        else:
            assert len(f) > 4 and '.tx1' == f[-4:]
            process_song(f, tags_to_min_max_pitches)
    print(f'DONE {directory}')

def main():
    tags_to_min_max_pitches = {}
    for folder in sys.argv[1:]:
        update_instrument_mins_and_max_pitches(folder, tags_to_min_max_pitches)

    with open('music_analysis_scripts/min_max_pitches.json', 'w') as f:
        f.write(json.dumps(tags_to_min_max_pitches))

if __name__ == '__main__':
    main()
    