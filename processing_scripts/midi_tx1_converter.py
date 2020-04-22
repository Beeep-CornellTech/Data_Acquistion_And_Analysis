import pretty_midi
import sys
import os
import LakhNES.data.tx1_midi as txt_midi # MAKE SURE TO USE VERSION IN GROUP

def convert_dir_to_trans(directory, transform, trans_name):
    directory_name = directory[directory.rfind('/')+1:]
    out_dir = f'{trans_name}/{directory_name}_{trans_name}'
    if os.path.isdir(out_dir):
        print(f'Already exists: {directory_name}')
        return
    os.mkdir(out_dir)

    file_names = os.listdir(directory)
    read_mode = 'r' if transform == txt_midi.tx1_to_midi else 'rb'
    write_mode = 'wb' if transform == txt_midi.tx1_to_midi else 'w'
    for name in file_names:
        fp = f'{directory}/{name}'
        with open(fp, read_mode) as f:
            data = f.read()
        translation = transform(data)
        if trans_name == 'tx1' and len(translation.split('\n')) <= 1:
            continue
        with open(f"{out_dir}/{name[0:name.rfind('.')]}.{trans_name}", write_mode) as f:
            f.write(translation)

if __name__ == '__main__':
    trans_name = sys.argv[1].lower()
    if  trans_name == 'tx1':
        transform = txt_midi.midi_to_tx1
    elif trans_name == 'midi':
        transform = txt_midi.tx1_to_midi
    else:
        print(f'ERROR, First arg must be either midi or tx1, not {trans_name}')
        exit(1)

    if not os.path.isdir(trans_name):
        os.mkdir(trans_name)

    for directory in sys.argv[2:]:
        print(f'Working on {directory}')
        convert_dir_to_trans(directory, transform, trans_name)
