# cel: zrobić aplikację która znajdzie podany rodzaj
# plików i przeniesie je do określonego folderu

import os
import shutil
import sys

archiwa = ['rar', 'zip', 'gz', '7z', 'tar', 'cab', ]
obrazy = ['jpg', 'jpeg', 'tiff', 'png', 'bmp', 'raw', 'psd', 'gif', 'dxf',
          'dwf', 'dwg', 'ai', 'cdr', 'eps', 'svg', 'swf', 'wmf']
wideo = ['gp', 'asf', 'avi', 'dv', 'dvd', 'flv', 'm2ts', 'mkv', 'mov', 'mp4', 'mpg', 'smv', 'svcd', 'ts', 'wmv', 'vcd',
         'mov']
muzyka = ['mp3', 'ogg', 'wav', 'flac', ]
dokumenty = ['pdf', 'doc', 'xml', 'docx', 'txt']
zabronione = ['bin', 'sys']
ostrzezenie = ['exe']


def tworzFoldery(lista):
    for x in lista:
        try:
            os.mkdir(x)
            print(f'Stworzono folder: {x}')
        except FileExistsError:
            print(f'- Folder {x} już istnieje.')

def przeniesPliki(lista):
    pliki = os.listdir(os.path.curdir)
    licznik = 0
    for x in pliki:
        if os.path.isfile(x):
            podziel = x.split('.')
            roz = podziel[-1]
            if roz.upper() in lista and podziel[0]!='copyapp':
                nowa_sciezka = os.path.dirname(os.path.abspath(x)) + "\\" + roz

                if shutil.move(os.path.abspath(x), nowa_sciezka):
                    print(f'- Pomyślnie przeniesiono plik {x}')
                    licznik+=1
                else:
                    print(f'- Nie udało się przenieść pliku {x}')

            else:
                continue
    print(f'Przeniesionych plików: {licznik}')


def sprawdz_rozszerzenia():
    global archiwa, muzyka, wideo, dokumenty, obrazy, zabronione, ostrzezenie


    print('Witaj w programie do sekgregacji plików. \nUpewnij się, że program znajduje się w folderze, który chcesz uporządkować!\n'
          'Posegregowane pliki będą znajdować się w folderach o nazwie rozszerzenia pliku...')
    rozszerzenia = []
    pliki = os.listdir(os.path.curdir)
    pomijaj = None
    print('-'*50)
    print('Przed przeniesieniem plików .exe upewnij się, że znajdują się tu tylko pliki instalacyjne !')
    pytanie = input('Czy dodać pliki .exe do sortowania? [T/N]')
    if pytanie.upper() == 'T':
        pomijaj = False
    else:
        pomijaj = True

    for x in pliki:
        if os.path.isfile(x):
            podziel = x.split('.')
            roz = podziel[-1].upper()
            if roz.lower() in archiwa or roz.lower() in muzyka or roz.lower() in dokumenty \
                    or roz.lower() in wideo or roz.lower() in obrazy or roz.lower() in ostrzezenie and podziel[0]!='copyapp':
                if roz not in rozszerzenia and roz.lower() not in zabronione and len(roz)<=4:
                    if roz.lower()=='exe' and pomijaj==False:
                        rozszerzenia.append(roz.upper())
                    elif roz.lower()!='exe':
                        rozszerzenia.append(roz.upper())
                else:
                    continue
            else:
                continue
    if len(rozszerzenia) > 0:
        print('Znaleziono poniższe rozszerzenia plików:')
        for x in rozszerzenia:
            print(f'- .{x}')
        if len(rozszerzenia)>1:
            pytanie1 = input('Czy chcesz posegregować wszystkie [T] czy tylko wybrane pliki [N]?')
        else:
            pytanie1 = input('Posegregować ten typ plików? [T/N] ')
        if pytanie1.upper()=='T':
            print('- Tworzenie folderów...')
            tworzFoldery(rozszerzenia)
            print('- Zakończono tworzenie folderów.')
            print('- Przenoszenie plików')
            przeniesPliki(rozszerzenia)

        elif pytanie1.upper() == 'N' and len(rozszerzenia)>1:
            pytanie = input('Czy chcesz posegregować tylko wybrane pliki? [T/N]')
            if pytanie.upper() == 'T':
                wybrane = input('Podaj po przecinku wybrane rozszerzenia( bez kropek ): ')
                if len(wybrane) > 0:
                    wybrane = wybrane.rstrip().split(',')
                    kopia = rozszerzenia[:]
                    rozszerzenia.clear()
                    for x in wybrane:
                        if x.upper() in kopia:
                            rozszerzenia.append(x.upper())
                        else:
                            print(f'Rozszerzenie: .{x} jest niepoprawne.')
                print('Rozszerzenia które wybrałeś to: ')
                for x in rozszerzenia:
                    print(f"- {x}")
                pytanie = input('Czy chcesz posegregować te pliki ?[T/N]')
                if pytanie.upper()=='T':
                    print('- Tworzenie folderów...')
                    tworzFoldery(rozszerzenia)
                    print('- Zakończono tworzyć foldery.')
                    print('- Przenoszenie plików')
                    przeniesPliki(rozszerzenia)
                else:
                    print('Kończę pracę! Do zobaczenia!')
        elif len(rozszerzenia)<=1 and pytanie1.upper()=='N':
            print('-'*50)
            print('Nie wybrano żadnej opcji')
            print('-' * 50)
        else:

            print('Nie rozpoznałem polecenia. Kończę pracę...')
            sys.exit()
    else:
        print('-'*100)
        print('Nie znaleziono plików spełniających kryteria...')
        print('-' * 100)


def przeniesFolder(nazwa, element):
    folder = nazwa
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass
    print(f'- Przenoszę {element} do {folder}')
    try:
        shutil.move(os.path.abspath(element), os.path.dirname(os.path.abspath(element)) + "\\" + folder)
        print(f'- Pomyślnie przeniesiono {element}')
    except shutil.Error:
        print(f'- Nie udało się przenieść folderu {element}')


def sortowanieFolderow():
    global archiwa, obrazy, wideo, muzyka, dokumenty
    pliki = os.listdir(os.path.curdir)
    pomijaj = ['Archiwa', 'Obrazy', 'Filmy', 'Muzyka', 'Inne', 'Instalki', 'Dokumenty']
    for element in pliki:
        if os.path.isdir(element):
            if element not in pomijaj:
                print(f'Znalazłem folder: {element}')
            else:
                continue
            if element.lower() in archiwa:
                przeniesFolder('Archiwa', element)
            elif element.lower() in obrazy:
                przeniesFolder('Obrazy', element)
            elif element.lower() in wideo:
                przeniesFolder('Filmy', element)
            elif element.lower() in muzyka:
                przeniesFolder('Muzyka', element)
            elif element.lower() in dokumenty:
                przeniesFolder('Dokumenty', element)
            elif element.lower() == 'exe':
                przeniesFolder('Instalki', element)
            else:
                pass


while True:
    print('Wybierz czynność:')
    print('[1] - sortowanie plików wg rozszerzeń')
    print('[2] - sortowanie folderów wg typów')
    print('[3] - zakończ pracę')
    odpowiedz = input('Wybieram: ')
    print('='*100)
    if odpowiedz == '1':
        sprawdz_rozszerzenia()
    elif odpowiedz == '2':
        sortowanieFolderow()
    elif odpowiedz == '3':
        break
    else:
        print('Niepoprawny numer. Spróbuj ponownie...')

