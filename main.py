import sys
import os
import shutil
import re

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
            if sort_dir != 'archives' or sort_dir != 'unknown':
                trans_filename = translate(filename)
                new_filename = re.sub(r'[^a-zA-Z0-9]', '_', trans_filename.strip())
                new_file = path + new_filename + '.' + ext
                os.rename(file, new_file)


def sort(library, extension, file):

    file = re.sub(r'[\\]', '/', file)
    new_dir = f'{os.path.dirname(real_path)}/{os.path.basename(real_path)}_sorted'
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    is_recorded = False
    for key, ext_group in library.items():
        #print(key, ext_group)
        for ext_example in ext_group:
            if extension.strip().lower() == ext_example.strip().lower():
                new_group_dir = f'{new_dir}/{key}'
                if not os.path.exists(new_group_dir):
                    os.makedirs(new_group_dir)
                shutil.copy(file, new_group_dir)
                is_recorded = True
                print("---------------------------------------------------------------------------------------------------------------------------------")
                print(f'Найден известный файл {file}')
                print(f'Размещаем в директории {key} c известными типами файлов {ext_group}')
                print("---------------------------------------------------------------------------------------------------------------------------------")
                break
                
    if is_recorded == False:
        new_group_dir = f'{new_dir}/unknown'
        if not os.path.exists(new_group_dir):
            os.makedirs(new_group_dir)
        shutil.copy(file, new_group_dir)
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
            


library = {'images':('JPEG', 'PNG', 'JPG', 'SVG'),
           'video':('AVI', 'MP4', 'MOV', 'MKV'),
           'documents':('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
           'audio':('MP3', 'OGG', 'WAV', 'AMR'),
           'archives':('ZIP', 'GZ', 'TAR'),
           'scripts':('JS', 'CSS')
           }



if len(sys.argv) < 2:
    print("Отсутствует аргумент командной строки. Пожалуйста, укажите путь к вашей папке.")
    print("Например: main.py c:/Users/Name/Desktop/Мотлох")
    exit()
else:
    path_dir = sys.argv[1]

if os.path.exists(path_dir) and os.path.isdir(path_dir):
    real_path = re.sub(r'[\\]', '/', os.path.normpath(os.path.realpath(path_dir)))
    print("Папка существует.")
    print(f"Приступаю к разбору папки {real_path}")
else:
    print(f"Папка '{path_dir}' не существует. попробуйте ввести путь еще раз")
    exit()

new_dir = re.sub(r'[\\]', '/', f'{os.path.dirname(real_path)}/{os.path.basename(real_path)}_sorted')
if os.path.exists(new_dir):
    shutil.rmtree(new_dir)
list_files = list_files_recursive(real_path)
for file in list_files:
    filename = file.split("/")[-1]  # Получаем имя файла с расширением
    extension = file.split(".")[-1]  # Получаем расширение файла
    #print(extension)
    sort(library, extension, file)

print('Файлы отсортированы')

archive_dir = f'{os.path.dirname(real_path)}/{os.path.basename(real_path)}_sorted/archives'
if os.path.exists(archive_dir):
    print('Обнаружены архивы, приступаем к распаковке')
    #unpacked_dir = archive_dir + '/unpacked'
    #if not os.path.exists(unpacked_dir):
        #os.makedirs(unpacked_dir)
    arc_files = list_files_recursive(archive_dir)
    for file in arc_files:
        file = re.sub(r'[\\]', '/', file) # Полный путь к файлу
        filename_ext = file.split("/")[-1]  # Получаем имя файла с расширением
        name_parts = filename_ext.split('.')
        ext = name_parts[-1]                   # Получаем расширение
        filename = '.'.join(name_parts[:-1])   # получаем имя без расширения
        unpacked_dir = archive_dir + "/" + filename
        if not os.path.exists(unpacked_dir):
            os.makedirs(unpacked_dir)
        shutil.unpack_archive(file, unpacked_dir)


    print("Архивы распакованы, их содержимое отсортировано")

else:
    print('Архивы не обнаружены')

normalize(new_dir)

print('Имена файлов, за исключением неизвестных типов и распакованных архивов - нормализованы. Завершение работы')
print(f'Ваши файлы отсортированы в директории {new_dir}')