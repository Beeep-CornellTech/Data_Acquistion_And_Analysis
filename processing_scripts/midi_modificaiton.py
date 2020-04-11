import pretty_midi
import json
import sys
import os
#import random

"""
https://www.noterepeat.com/articles/how-to/213-midi-basics-common-terms-explained#H
http://craffel.github.io/pretty-midi/
"""

"""GOOD_INSTRUMENTS = {
    'Distortion Guitar': 30,
    'Acoustic Grand Piano': 0, # AKA Drums...don't ask me why
    'Overdriven Guitar': 29,
    'Electric Bass (finger)': 33,
    'Electric Bass (pick)': 34,
    'Electric Guitar (clean)':  27,
    "Acoustic Guitar (steel)": 25,
    }"""

# maps instrument program to token representation in language, 
# Used to replace track names with more useful values
CHANNELS_TO_NEW_NAMES = {
    19: 'RO',
    4: 'EP',
    30: 'DG',
    0: 'AGP',
    29: 'OG',
    34: 'EB',
    27: 'EGC',
    25: 'AGS'
}

# Maps program numbers of instruments to use to instruments that can be replaced by it
GOOD_INSTRUMENT_TO_ACCEPTABLES = {
    19: set([50,42,41,109,20,53,9,80,85,81,87,31,120,35, 48, 49]),
    4: set([5]),
    30: set([]),
    0: set([117, 112, 93, 91,95, 94, 118]),
    29: set([]),
    34: set([33, 36, 32]),
    27: set([68, 45, 110, 69, 71, 86, 82, 26]),
    25: set([40, 41, 22, 24, 106])
}

NOT_CONVERTABLE = -1000 # program number used when instrument is not in GOOD_INSTRUMENT_TO_ACCEPTABLES as key or value


"""GOOD_INSTRUMENT_NUMBERS = GOOD_INSTRUMENTS.values()
BASSES = [GOOD_INSTRUMENTS['Electric Bass (pick)'], GOOD_INSTRUMENTS['Electric Bass (finger)']]
GUITARS = [GOOD_INSTRUMENTS['Distortion Guitar'], GOOD_INSTRUMENTS['Overdriven Guitar'], \
    GOOD_INSTRUMENTS["Acoustic Guitar (steel)"], GOOD_INSTRUMENTS['Electric Guitar (clean)']]"""

"""def remove_extra_instruments(instruments):
    hit_list = []
    for i in range(len(instruments)):
        instr = instruments[i]
        if instr.program not in GOOD_INSTRUMENT_NUMBERS:
            hit_list.append(i)
    
    counter = 0
    for index_to_remove in hit_list:
        del instruments[index_to_remove - counter]
        counter += 1"""


"""def get_valid_program_number(program_list):
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
            change_instrument_type(instr)"""



def get_shouvik_program_number(program_number):
    """
    Checks to see if program_number is equivilant to a key of GOOD_INSTRUMENT_TO_ACCEPTABLES or if
    it is in GOOD_INSTRUMENT_TO_ACCEPTABLES[k] for some key k. If this is true, k is returned. Else, 
    NOT_CONVERTABLE is returned
    """
    for k in GOOD_INSTRUMENT_TO_ACCEPTABLES:
        if program_number == k or program_number in GOOD_INSTRUMENT_TO_ACCEPTABLES[k]:
            return k

    return NOT_CONVERTABLE
        

def replace_shouvik(instruments):
    """
    Replaces insturment with "core instrument" using info from shouvik, deletes
    instrument if no valid matching is found for a given instrument

    :param instruments: list of instrument objects beloning to sepecific midi file
    :return: None, modifies instruments object as described above
    """
    hit_list = [] # For Removal
    for i in range(len(instruments)):
        instr = instruments[i]
        new_program_number = get_shouvik_program_number(instr.program)
        if new_program_number == NOT_CONVERTABLE:
            hit_list.append(i)
        else:
           instr.program = new_program_number
    
    # purge instrument of any element whose index is in hit_list
    counter = 0
    for index_to_remove in hit_list:
        del instruments[index_to_remove - counter]
        counter += 1
            

def change_instrument_names(instruments):
    """
    For each instrument object in instruments list, make name equal to
    the token representation of that instrument
    """
    for instr in instruments:
        instr.name = CHANNELS_TO_NEW_NAMES[instr.program]

TRANSFORMATIONS = [('REPLACE_SHOUVIK', replace_shouvik)] # transformation to perform on midi files

def transform_and_save(new_midi, transform, new_directory, f_name):
    """
    Applies transform function to new_midi, modifies track name of all instruments retained,
    and saves result in new_directory/f_name
    """
    transform(new_midi.instruments)
    change_instrument_names(new_midi.instruments)
    new_midi.write(f'{new_directory}/{f_name}')

def main(directory):
    """
    Performs all transformations in TRANSFORMATIONS on all files in directory, saving resulting midis in
    directory + transform_name

    Assumes all children of directory are midi files
    """
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
