import pretty_midi
import json
import sys
import os


"""
https://www.noterepeat.com/articles/how-to/213-midi-basics-common-terms-explained#H
http://craffel.github.io/pretty-midi/
"""

def main(directory):
    file_names = os.listdir(directory)
    songs = {}
    unique_instruments = set()
    for fname in file_names:
        try:
            with open(directory + '/' + fname, 'rb') as f:
                midi = pretty_midi.PrettyMIDI(f)
                instruments = midi.instruments
                songs[fname] = {'instruments': []}
                for instr in instruments:
                    instr_name = pretty_midi.program_to_instrument_name(instr.program) # Program number says what instrument, see doc above
                    songs[fname]['instruments'].append(instr_name)
                    unique_instruments.add(instr_name)
        except Exception as err:
            print(f"Issue with {fname} :  {err}")
            continue
            
    print(f'***UNIQUE INSTRUMENTS***\n{directory}')
    print(unique_instruments)
    print(len(unique_instruments))
    with open(f'music_analysis_scripts/{directory}DATA.json', 'w') as f:
        f.write(json.dumps(songs))


GUITAR = 'guitar'
BASS = 'bass'
VOCALS = 'vocals'
DRUMS = 'drums'

def get_new_instrument(instrument):
    instrument = instrument.lower()
    if 'bass' in instrument:
        return BASS
    if 'guitar' in instrument or 'gtr' in instrument or 'distort' in instrument:
        return GUITAR
    if 'drum' in instrument:
        return DRUMS
    if 'chorus' in instrument or 'vocal' in instrument:
        return VOCALS
    return try_by_member(instrument)

def fix_instruments(directory):
    unknowns = set()
    with open(f'{directory}DATA.json', 'r') as f:
        data = json.loads(f.read())
    bad_songs = 0
    for song in data:
        is_instrument_unknown = False
        instruments = data[song]['instruments']
        for i in range(len(instruments)):
            inst = instruments[i]
            new_inst = get_new_instrument(inst)
            if new_inst is None:
                is_instrument_unkown = True
                unknowns.add(inst)
            else:
                instruments[i] = new_inst
        bad_songs += is_instrument_unkown
    print(f"bad songs: {bad_songs}")
    for i in unknowns:
        print(i)
    with open(f'{directory}DATA.json', 'w') as f:
        f.write(json.dumps(f.read()))
    return None

MODES = {'-e': main, '-i': fix_instruments}
if __name__ == '__main__':
    if sys.argv[1] not in MODES:
        print('NEED ONE OF THE FOLLOWING MODES: {MODES.keys()}')
        exit()
    func = MODES[sys.argv[1]]
    for directory in sys.argv[2:]:
        func(directory)
        print()

