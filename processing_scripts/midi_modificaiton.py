import pretty_midi
import json
import sys
import os
import random

"""
https://www.noterepeat.com/articles/how-to/213-midi-basics-common-terms-explained#H
http://craffel.github.io/pretty-midi/
"""

GOOD_INSTRUMENTS = {
    'Distortion Guitar': 30,
    'Acoustic Grand Piano': 0, # AKA Drums...don't ask me why
    'Overdriven Guitar': 29,
    'Electric Bass (finger)': 33,
    'Electric Bass (pick)': 34,
    'Electric Guitar (clean)':  27,
    "Acoustic Guitar (steel)": 25,
    }

CHANNELS_TO_NEW_NAMES = {
    30: 'DG',
    0: 'AGP',
    29: 'OG',
    33: 'EBF',
    34: 'EBP',
    27: 'EGC',
    25: 'AGS'
}


GOOD_INSTRUMENT_NUMBERS = GOOD_INSTRUMENTS.values()
BASSES = [GOOD_INSTRUMENTS['Electric Bass (pick)'], GOOD_INSTRUMENTS['Electric Bass (finger)']]
GUITARS = [GOOD_INSTRUMENTS['Distortion Guitar'], GOOD_INSTRUMENTS['Overdriven Guitar'], \
    GOOD_INSTRUMENTS["Acoustic Guitar (steel)"], GOOD_INSTRUMENTS['Electric Guitar (clean)']]

def remove_extra_instruments(instruments):
    hit_list = []
    for i in range(len(instruments)):
        instr = instruments[i]
        if instr.program not in GOOD_INSTRUMENT_NUMBERS:
            hit_list.append(i)
    
    counter = 0
    for index_to_remove in hit_list:
        del instruments[index_to_remove - counter]
        counter += 1


def get_valid_program_number(program_list):
    i = len(program_list)
    while i >= len(program_list):
        i = int(random.uniform(0, len(program_list)))
    return program_list[i]

def change_instrument_type(instrument):
    if instrument.is_drum:
        instrument.program = GOOD_INSTRUMENTS['Acoustic Grand Piano'] # Accoustic Grand Piano is essentially drums
        return
    if 'bass' in pretty_midi.program_to_instrument_name(instrument.program).lower():
        instrument.program = get_valid_program_number(BASSES)
    else:
        instrument.program = get_valid_program_number(GUITARS)

def replace_random(instruments):
    for instr in instruments:
        if instr.program not in GOOD_INSTRUMENT_NUMBERS:
            change_instrument_type(instr)



def change_instrument_names(instruments):
    for instr in instruments:
        instr.name = CHANNELS_TO_NEW_NAMES[instr.program]


TRANSFORMATIONS = [('REMOVE', remove_extra_instruments), ('REPLACE_RANDOM', replace_random)]

def transform_and_save(new_midi, transform, new_directory, f_name):
    transform(new_midi.instruments)
    change_instrument_names(new_midi.instruments)
    new_midi.write(f'{new_directory}/{f_name}')

def main(directory):
    file_names = os.listdir(directory)
    for (transform_name, transform) in TRANSFORMATIONS:
        new_directory = directory + transform_name.upper()
        if os.path.isdir(new_directory):
            print(f'ALREADY EXISTS: {new_directory}')
            continue 
        os.mkdir(new_directory)
        for fname in file_names:
            try:
                with open(directory + '/' + fname, 'rb') as f:
                    new_midi = pretty_midi.PrettyMIDI(f)
                    transform_and_save(new_midi, transform, new_directory, fname)     
            except Exception as err:
                print(f"Issue with {fname} :  {err}")
                continue
        print(f'FINISHED {transform_name} on {directory}')

if __name__ == '__main__':
    for directory in sys.argv[1:]:
        main(directory)
