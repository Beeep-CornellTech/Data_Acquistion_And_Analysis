import pretty_midi
import json
import sys
import os
from collections import defaultdict

def get_instrument_info(directory, instrument_velocities):
    file_names = os.listdir(directory)
    for fname in file_names:
        try:
            with open(directory + '/' + fname, 'rb') as f:
                midi = pretty_midi.PrettyMIDI(f)
                for instr in midi.instruments:
                    for n in instr.notes:
                        instrument_velocities[instr.program].add(int(n.velocity))
        except Exception as err:
            print(f"Issue with {fname} :  {err}")
            continue

def main():
    instrument_velocities = defaultdict(set)
    for folder in sys.argv[1:]:
        print('Doing '+ folder)
        get_instrument_info(folder, instrument_velocities)

    json_data = {}
    for k in instrument_velocities:
        json_data[int(k)] = sorted(list(instrument_velocities[k]))

    with open('music_analysis_scripts/velocities.json', 'w') as f:
        f.write(json.dumps(json_data))

if __name__ == '__main__':
    main()



