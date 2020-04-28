# Скрипт получает на вход путь к папке с архивами (или работает в текущей папке), распаковывает все архивы,
# достаёт для каждого архива имя исполнителя/год выпуска альбома/название альбома и создаёт структуру каталогов
# следующего вида Название исполнителя/Год выпуска альбома - Название альбома/Файлы с композициями

# TODO Добавить другие форматы, кроме mp3 (?)
# TODO Протестировать скрипт
# TODO Добавить консольный интерфейс (?)
# TODO Если в извлекаемой папке несколько папок с мп3?
# TODO Рефакторинг
# TODO Перевести все комментарии на английский
# TODO Добавить файл ридми
# TODO Добавить вывод общего числа успешно распакованных архивов и числа архивов, которые не удалось распаковать

import taglib
import sys
import os
import patoolib
import shutil
import re
import unidecode

#----------------------------------------------------------------------------------------------------------------------------------

# Функция получает год из строки, если года нет - возвращается пустая строка
def getYearFromString(s):
    strList = re.findall('[1-2][0-9][0-9][0-9]',s)
    if strList != []:
        return strList[0]
    else:
        return ''

#----------------------------------------------------------------------------------------------------------------------------------

# Функция получает год выпуска альбома из тегов mp3 файла
def getYearFromMp3Tags(tags):
    if 'DATE' in tags and tags['DATE'] != [] and tags['DATE'][0] != '' :
        return tags['DATE'][0]
    if 'RELEASEDATE' in tags and tags['RELEASEDATE'] != []:
        year = getYearFromString(tags['RELEASEDATE'][0])
        if year != '':
            return year
    if 'COPYRIGHT' in tags and tags['COPYRIGHT'] != []:
        year = getYearFromString(tags['COPYRIGHT'][0])
        if year != '':
            return year
    return ''
#----------------------------------------------------------------------------------------------------------------------------------

# Функция получает название группы из тегов mp3 файла
def getBandFromMp3Tags(tags):
    if 'ARTIST' in tags and tags['ARTIST'] != [] and tags['ARTIST'][0] != '':
        return tags['ARTIST'][0].title().replace('/','-')
    else:
        return ''

# ----------------------------------------------------------------------------------------------------------------------------------

# Функция получает название альбома из тегов mp3 файла
def getAlbumFromMp3Tags(tags):
    if 'ALBUM' in tags and tags['ALBUM'] != [] and tags['ALBUM'][0] != '':
        return tags['ALBUM'][0].title().replace('/','-')
    else:
        return ''


#----------------------------------------------------------------------------------------------------------------------------------

# Функция получает нужные параметры альбома (Название альбома, Название группы, Год выпуска) из mp3-файла
def getAlbumParamsFromMp3(mp3Path):
    song = taglib.File(mp3Path)
    albumParams = {}
    albumParams['ALBUM'] = getAlbumFromMp3Tags(song.tags)
    albumParams['BAND'] = getBandFromMp3Tags(song.tags)
    albumParams['YEAR'] = getYearFromMp3Tags(song.tags)
    if albumParams['ALBUM'] == '' or albumParams['BAND'] == '' or albumParams['YEAR'] == '':
        albumParams = {}
    return albumParams

#----------------------------------------------------------------------------------------------------------------------------------		

# Функция ищет в заданной папке папку с mp3, если папки с mp3 нет - возвращается пустая строка
def findMp3Path(folderPath):
    for directory, dirs, files in os.walk(folderPath):
        for file in files:
            if file.endswith('.mp3'):
                return directory
    return ''

#----------------------------------------------------------------------------------------------------------------------------------		

# Функция получает параметры альбома из папки, где лежат mp3-файлы
def getAlbumParamsFromMp3FolderPath(mp3FolderPath):
    for file in os.listdir(mp3FolderPath):
        if file.endswith('.mp3'):
            albumParams = getAlbumParamsFromMp3(mp3FolderPath + '\\' + file)
            return albumParams
    return {}

#----------------------------------------------------------------------------------------------------------------------------------		

# Функция перемещает все файлы из одной папки в другую
def moveFiles(srcDir, dstDir):
    for file in os.listdir(srcDir):
        shutil.move(srcDir + '\\' + file, dstDir)

#----------------------------------------------------------------------------------------------------------------------------------

# Функция распаковывает архив, извлекает из распакованной папки данные вида Группа/Год/Альбом, создаёт структуру папок вида Группа/Год - Альбом и перемещает туда файлы, старая папка удаляется
def parseMusicalArchive(archivePath):
    folderPath = os.path.splitext(archivePath)[0]  # Папка для распаковки (удаляем расширение)
    os.mkdir(folderPath)
    try:
        patoolib.extract_archive(archivePath, outdir=folderPath)
    except Exception as e:
        print('Warning: ' + str(e))
    # os.remove(archivePath)
    mp3FolderPath = findMp3Path(folderPath)  # Находим папку с mp3 в извлеченной папке
    if mp3FolderPath != '':
        albumParams = getAlbumParamsFromMp3FolderPath(mp3FolderPath)  # Получаем параметры альбома
        if albumParams != {}:
            bandPath = workingDir + '\\' + albumParams['BAND']  # Создаём папку с группой, если её ещё нет
            if not os.path.exists(bandPath):
                os.mkdir(bandPath)
            albumPath = bandPath + '\\' + albumParams['YEAR'] + ' - ' + albumParams['ALBUM']  # Создаём папку с альбомом
            os.mkdir(albumPath)
            moveFiles(mp3FolderPath, albumPath)  # Перемещаем файлы в новую папку
            shutil.rmtree(folderPath)  # Удаляем старую папку
			
            return True
        else:
            print('Warning: Can not extract album params from ' + mp3FolderPath + '. This folder will not be parsed!')
    else:
        print('Warning: There is no folder with mp3 in ' + folderPath)
		
    return False

#----------------------------------------------------------------------------------------------------------------------------------
		
# Функция парсит все архивы в рабочем каталоге
def parseMusicalArchives(workingDir):
    
    extracted = 0
    failed = 0
    
    for file in os.listdir(workingDir):
        if file.endswith('.zip') or file.endswith('.rar') or file.endswith('.7z'):
            asciiFile = unidecode.unidecode(file)  # Преобразуем имя файла в ascii и переименовываем его
            os.rename(workingDir + '\\' + file, workingDir + '\\' + asciiFile)
            archivePath = workingDir + '\\' + asciiFile
            if parseMusicalArchive(archivePath):
                extracted += 1
            else:
                failed += 1
	
    print("--------------------------------------------------------------------------------------------------")
    print("Extracted: ", extracted)
    print("Failed: ", failed)

#----------------------------------------------------------------------------------------------------------------------------------			

if __name__ == "__main__":
    # Получение на вход пути к каталогу (или работа в каталоге, где запущен скрипт)
    workingDir = os.getcwd()

    if len(sys.argv) > 1:
        workingDir = sys.argv[1]

    parseMusicalArchives(workingDir)

    #print('Musical archives successfully parsed.')









