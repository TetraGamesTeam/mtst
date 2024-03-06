from pydub.utils import mediainfo
import librosa
import os

directory = os.getcwd()
extension = '.mp3'
logs = []
ord_id = int(input('\033[32m Введите начальную позицию id: \033[0m'))

def get_absolute_paths(directory, extension):
    absolute_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                absolute_paths.append(os.path.join(root, file))
    return absolute_paths

def get_length_and_beat(file_path):
    global add
    add = ''
    audio_info = mediainfo(file_path)
    try:
        length_in_deciseconds = int(float(audio_info['duration']) * 10)
        y, sr = librosa.load(file_path)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        beat_in_deciseconds = int(60 / tempo * 10) if tempo > 0 else 0
    except KeyError:
        length_in_deciseconds = int(float(audio_info['duration']) * 10)
        beat_in_deciseconds = 0
        add = 'Не удалось определить BPM.'
    return length_in_deciseconds, beat_in_deciseconds

def rename_file_with_info(file_path, length, beat, ord_id):
    file_name, file_ext = os.path.splitext(file_path)
    new_file_name = f"{file_name}_{length}_{beat}_{ord_id}{extension}"
    head, tail = os.path.split(new_file_name)
    logs.append(f'\033[32m [УСПЕХ] \033[0m {file_path} переименован в "{tail}". {add}')
    os.rename(file_path, new_file_name)

path_list = get_absolute_paths(directory, extension)

for path_str in path_list:  
    file_name, file_ext = os.path.splitext(path_str) 
    ogg_path = path_str.replace(".mp3", ".ogg") 
    os.system(f'ffmpeg -i "{path_str}" -ab 128k -vn -ac 2 "{ogg_path}"') 
    length, beat = get_length_and_beat(path_str) 
    extension = '.ogg' 
    rename_file_with_info(ogg_path, length, beat, ord_id) 
    ord_id += 1 

for each in logs:
    print(each)