import pretty_midi
import json
import sys
import os


"""
https://www.noterepeat.com/articles/how-to/213-midi-basics-common-terms-explained#H
http://craffel.github.io/pretty-midi/
"""

def main(directory, cumulative_instrument_counts):
    file_names = os.listdir(directory)
    songs = {}
    unique_instruments = set()
    instr_presences = {}
    total_song_durations = 0
    for fname in file_names:
        try:
            with open(directory + '/' + fname, 'rb') as f:
                midi = pretty_midi.PrettyMIDI(f)
                total_song_durations += midi.get_end_time()
                instruments = midi.instruments
                songs[fname] = {'instruments': []}
                for instr in instruments:
                    instr_type = pretty_midi.program_to_instrument_name(instr.program) # Program number says what instrument, see doc above
                    if instr_type not in instr_presences:
                        instr_presences[instr_type] = set()
                    if instr_type not in cumulative_instrument_counts:
                        cumulative_instrument_counts[instr_type] = set()
                    instr_presences[instr_type].add(fname)
                    cumulative_instrument_counts[instr_type].add(fname)
                    
                    songs[fname]['instruments'].append([instr_type, int(instr.program), instr.name]) # type and program store == info, name is used to map instruments in garadge band
                    unique_instruments.add(instr_type)
        except Exception as err:
            print(f"Issue with {fname} :  {err}")
            continue

    print(f'***UNIQUE INSTRUMENTS***\n{directory}')
    print(f'Not Bad Songs: {len(songs)}')
    print(unique_instruments)
    print(len(unique_instruments))
    with open(f'music_analysis_scripts/{directory}DATA.json', 'w') as f:
        f.write(json.dumps(songs))

    data = sorted(list(map(lambda x: (x[0], len(x[1])), instr_presences.items())), key=lambda x: x[1])
    for instr, presence in data:
        print(instr, presence / len(songs))
    print()
    return total_song_durations, len(songs)


if __name__ == '__main__':
    cumulative_instrument_counts = {}
    total_durrations = 0 # in seconds
    total_songs = 0
    for directory in sys.argv[1:]:
        duration, songs = main(directory, cumulative_instrument_counts)
        total_durrations += duration
        total_songs += songs
    
    print('CUMULATIVE RESULTS')
    print(f'Total Durration in seconds: {total_durrations}')
    instrument_data = sorted(list(map(lambda x: (x[0], len(x[1])), cumulative_instrument_counts.items())), key=lambda x: x[1])
    for (i, j) in instrument_data:
        print(i, j/total_songs)

