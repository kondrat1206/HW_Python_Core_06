import sys
import os
import shutil
import re

def check_args(arg):

    if len(arg) < 2:
        print("Отсутствует аргумент командной строки. Пожалуйста, укажите путь к вашей папке.")
        print("Например: main.py c:/Users/Name/Desktop/Мотлох")
        exit()
    else:
        path_dir = arg[1]
        

    if os.path.exists(path_dir) and os.path.isdir(path_dir):
        real_path = re.sub(r'[\\]', '/', os.path.normpath(os.path.realpath(path_dir)))
        print("Папка существует.")
        print(f"Приступаю к разбору папки {real_path}")
    else:
        print(f"Папка '{path_dir}' не существует. попробуйте ввести путь еще раз")
        exit()

    return real_path


def list_files_recursive(real_path):

    list_files = []
    for root, dirs, files in os.walk(real_path):
        for file in files:
            file_path = os.path.join(root, file)
            #print(file_path)
            list_files.append(file_path)

    return list_files


def normalize(dir):
    list_files = list_files_recursive(dir)
    for file in list_files:
        file = re.sub(r'[\\]', '/', file) # Полный путь к файлу
        filename_ext = file.split("/")[-1]  # Получаем имя файла с расширением
        #print(filename_ext)
        if "." in filename_ext:
            name_parts = filename_ext.split('.')
            ext = name_parts[-1]                   # Получаем расширение
            filename = '.'.join(name_parts[:-1])   # получаем имя без расширения
            path = file.split(filename)[0]  # Получаем путь к файлу
            #print(f"Нормализуем файл, расположенный по пути {path}")
            sort_dir = path.split(new_dir + '/')[-1].split('/')[0]
            #print(sort_dir)
            if sort_dir != 'archives' and sort_dir != 'unknown':
                trans_filename = translate(filename)
                new_filename = re.sub(r'[^a-zA-Z0-9]', '_', trans_filename.strip())
                new_file = path + new_filename + '.' + ext
                if file != new_file:
                    if not os.path.exists(new_file):
                        os.rename(file, new_file)
                    else:
                        os.remove(new_file)
                        os.rename(file, new_file)


def remove_empty_directories(new_dir):
    for root, dirs, files in os.walk(new_dir, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Check if directory is empty
                os.rmdir(dir_path)


def sort(library, extension, file, new_dir):

    excluded_dirs = []

    for key, ext_group in library.items():
        excluded_dirs.append(key)

    file = re.sub(r'[\\]', '/', file)
    print(file)
    print(new_dir)
    filedir_src = file.split(new_dir)[1].split('/')[1]
    #print(filedir_src)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    is_recorded = False
    if filedir_src in excluded_dirs:
        is_recorded = True
    for key, ext_group in library.items():
        for ext_example in ext_group:
            if extension.strip().lower() == ext_example.strip().lower():
                new_group_dir = f'{new_dir}/{key}'
                if not os.path.exists(new_group_dir):
                    os.makedirs(new_group_dir)
                try: 
                    shutil.copy(file, new_group_dir)
                except shutil.SameFileError:
                    continue
                else:
                    os.remove(file)
                    is_recorded = True
                    print("---------------------------------------------------------------------------------------------------------------------------------")
                    print(f'Найден известный файл {file}  {excluded_dirs}')
                    print(f'Размещаем в директории {key} c известными типами файлов {ext_group}')
                    print("---------------------------------------------------------------------------------------------------------------------------------")
                    break
                
    if is_recorded == False:
        new_group_dir = f'{new_dir}/unknown'
        if not os.path.exists(new_group_dir):
            os.makedirs(new_group_dir)
        try: 
            shutil.copy(file, new_group_dir)
        except shutil.SameFileError:
            pass
        else:
            os.remove(file)
            print("---------------------------------------------------------------------------------------------------------------------------------")
            print(f'Найден неизвестный файл {file}')
            print(f'Размещаем в директории unknown c неизвестными типами файлов')
            print("---------------------------------------------------------------------------------------------------------------------------------")
        
                
def translate(name):

    symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    trans = {}

    for ind, i in enumerate(symbols):
        trans[ord(i.lower())] = translation[ind].lower()
        trans[ord(i.upper())] = translation[ind].upper()

    name = name.translate(trans)

    return name


def unpack_archives(library, archive_dir):

    arc_files = list_files_recursive(archive_dir)
    for file in arc_files:
        file = re.sub(r'[\\]', '/', file) # Полный путь к файлу
        filename_ext = file.split("/")[-1]  # Получаем имя файла с расширением
        name_parts = filename_ext.split('.')
        ext = name_parts[-1]                   # Получаем расширение
        for key, ext_group in library.items():
            if key == 'archives':
                for ext_example in ext_group:
                    if ext == ext_example.lower():
                        filename = '.'.join(name_parts[:-1])   # получаем имя без расширения
                        unpacked_dir = archive_dir + "/" + filename
                        if not os.path.exists(unpacked_dir):
                            os.makedirs(unpacked_dir)
                        shutil.unpack_archive(file, unpacked_dir)
            

if __name__ == '__main__':


    library = {'images':('JPEG', 'PNG', 'JPG', 'SVG'),
               'video':('AVI', 'MP4', 'MOV', 'MKV'),
               'documents':('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
               'audio':('MP3', 'OGG', 'WAV', 'AMR'),
               'archives':('ZIP', 'GZ', 'TAR'),
               'scripts':('JS', 'CSS')
              }

    real_path = check_args(sys.argv)
    
    new_dir = real_path
    
    list_files = list_files_recursive(real_path)
    for file in list_files:
        filename = file.split("/")[-1]  # Получаем имя файла с расширением
        extension = file.split(".")[-1]  # Получаем расширение файла
        sort(library, extension, file, new_dir)
    print('Файлы отсортированы')

    archive_dir = f'{real_path}/archives'
    if os.path.exists(archive_dir):
        print('Обнаружены архивы, приступаем к распаковке')

        unpack_archives(library, archive_dir)
        print("Архивы распакованы, их содержимое отсортировано")
    else:
        print('Архивы не обнаружены')

    normalize(new_dir)
    print('Имена файлов, за исключением неизвестных типов и распакованных архивов - нормализованы. Завершение работы')

    remove_empty_directories(new_dir)
    print(f'Ваши файлы отсортированы в директории {new_dir}, пустые папки удалены')