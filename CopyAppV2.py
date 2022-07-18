# cel: zrobić aplikację która znajdzie podany rodzaj
# plików i przeniesie je do określonego folderu

import os
import shutil
from zipfile import *
import tkinter as tk

window = tk.Tk()
window.geometry("800x600")
window.resizable(False, False)
window.config(bg='dark grey')


class Program():
    def __init__(self):
        self.rozszerzenia = []
        self.vars = []  # zbiera wartosci checkboxow z rozszerzeniami plikow
        self.szerokosc_przyciskow = 20
        self.archiwa = ['rar', 'zip', 'gz', '7z', 'tar', 'cab', ]
        self.obrazy = ['jpg', 'jpeg', 'tiff', 'png', 'bmp', 'raw', 'psd', 'gif', 'dxf',
                       'dwf', 'dwg', 'ai', 'cdr', 'eps', 'svg', 'swf', 'wmf']
        self.wideo = ['gp', 'asf', 'avi', 'dv', 'dvd', 'flv', 'm2ts', 'mkv', 'mov', 'mp4', 'mpg', 'smv', 'svcd', 'ts',
                      'wmv', 'vcd',
                      'mov']
        self.muzyka = ['mp3', 'ogg', 'wav', 'flac', ]
        self.dokumenty = ['pdf', 'doc', 'xml', 'docx', 'txt']
        self.zabronione = ['bin', 'sys']
        self.aplikacje = ['exe', ]
        self.sciezka = os.path.abspath(os.path.curdir)

        self.ramka_glowna = tk.Frame(window, border=1,
                                     width=700, height=300,
                                     background='dark grey', )
        tk.Label(self.ramka_glowna, text='Wybierz opcję:',
                 width=20, borderwidth=2).grid(column=0, row=0, padx=10, sticky='W',)
        tk.Button(self.ramka_glowna, text='Sortuj Pliki',
                  width=self.szerokosc_przyciskow, command=self.sortujPliki).grid(column=1, row=0, sticky='W')
        tk.Button(self.ramka_glowna, text='Sortuj Foldery',
                  width=self.szerokosc_przyciskow, command=self.pokaz_foldery).grid(column=1, row=1, sticky='W')
        tk.Button(self.ramka_glowna, text='Sortuj automatycznie', command=self.rob_wszystko,
                  width=self.szerokosc_przyciskow).grid(column=1, row=2)
        tk.Button(self.ramka_glowna, text='Spakuj do ZIP', command=self.zip_it,
                  width=self.szerokosc_przyciskow).grid(column=1, row=3)
        self.ramka_glowna.pack(fill='both')
        self.ramka_dolna = tk.Frame(window, width=700, height=300, background='dark grey')
        self.ramka_dolna.pack(fill='both', pady=20)
        self.ramka_komunikatow = tk.Frame(window)
        self.aktualny_folder()
        self.ramka_komunikatow.pack(fill='x', pady=20)

        tk.Label(self.ramka_dolna, text='Program służy do sekgregacji plików. \n'
                                    'Upewnij się, że znajduje się w folderze, który chcesz uporządkować!\n'
                                    'Posegregowane pliki będą znajdować się w folderach o '
                                    'nazwie rozszerzenia pliku...\n'
                                    'Upewnij się, że znajdują się tu tylko pliki .exe tylko do instalacji.', justify='left', anchor='nw').pack(fill='both')

    def zip_it(self):
        foldery = os.listdir(self.sciezka)
        grupy = ['Archiwa', 'Dokumenty', 'Obrazy', 'Filmy', 'Instalki', 'Muzyka']
        komunikaty='Rozpoczynam pracę...\n'
        spakowanych=0
        for element in foldery:
            if os.path.isdir(element):
                if element in grupy:
                    komunikaty+=f'\t Znaleziono folder {element}\n\t Archiwizuję...\n'
                    spakowanych += 1
                    nazwa = element + '.zip'

                    with ZipFile(nazwa, 'w') as file:
                       subfoldery = os.listdir(element)
                       for subfolder in subfoldery:
                           pliki = os.listdir(f'{element}\{subfolder}')
                           for plik in pliki:

                                adres = f'{element}\{subfolder}\{plik}'
                                file.write(adres)


        komunikaty+=f'Kończę pracę. Spakowanych plików: {spakowanych}'
        tk.Label(self.ramka_komunikatow, text=komunikaty, justify='left', anchor='w').pack(fill='x')

    def rob_wszystko(self):
        self.rozszerzenia.clear() # czyści zmienna
        komunikaty='Szukam unikalnych rozszerzeń plików...\n'

        self.szukaj_rozszerzen() # szuka aktualnych rozszerzen
        lista = self.rozszerzenia # tworzy parametr dla funkcji przenoszenia plikow
        komunikaty+='Znaleziono rozszerzenia spełniające kryteria\n'
        self.przeniesPliki(lista) # segreguje pliki w folderach
        komunikaty+='\t- Zakończone\n'

        komunikaty+='Szukanie folderów spełniających kryteria\n'
        foldery = self.szukaj_folderow() # szuka foldery z plikami
        komunikaty+=f'\t- Znaleziono następujące foldery: {foldery}\n'
        self.segreguj_foldery(foldery) # segreguje foldery z plikami
        komunikaty+='\t- Zakończone.\n'

        tk.Label(self.ramka_komunikatow, text=komunikaty, justify='left', anchor='w').pack(fill='x')

    def segreguj_liste(self, lista, elementow_na_linie):
        elementow=elementow_na_linie
        tekst=''
        licznik=0
        for ele in lista:
            if licznik<=elementow:
                tekst+=f'.{ele}, '
                licznik+=1
            else:
                tekst+='\n'
                licznik=0
        return tekst

    def aktualizuj_folder(self):
        aktualny = self.adres.get()
        self.sciezka = aktualny
        self.informacje.destroy()
        self.czyscRamki()
        self.aktualny_folder()

    def aktualny_folder(self): # informacje o aktualnym folderze w ktorym znajduje sie program wykonujacy
        komunikaty='Dane o folderze:\n'
        komunikaty+=f'Aktualny folder: \n\t{self.sciezka} \n'
        self.adres = tk.Entry(self.ramka_glowna, width=90)
        self.adres.grid(column=0, row=5, columnspan=3, sticky='w')
        self.adres.insert(0, self.sciezka)
        zmien = tk.Button(self.ramka_glowna, text='Zmień', command=self.aktualizuj_folder)
        zmien.grid(row=5, column=2, sticky='e')

        self.szukaj_rozszerzen()
        if len(self.rozszerzenia)>0:
            komunikaty+=f'\t - Grupy plików do segregacji: {len(self.rozszerzenia)}\n \t {self.segreguj_liste(self.rozszerzenia, 10)}\n'
        else:
            komunikaty+='\t - Brak plików spełniających kryteria\n'
        foldery = self.szukaj_folderow()
        if len(foldery)>0:
            komunikaty+= f'\t - Foldery do segregacji: {len(foldery)} \n'
        else:
            komunikaty+='\t - Folderów : 0, musisz najpierw posegregować pliki\n'
        self.informacje=tk.Label(self.ramka_glowna, text=komunikaty, justify='left', anchor='nw', height=8, width=54)
        self.informacje.grid(column=2, row=0, rowspan=4)

    def segreguj_foldery(self, lista):
        if len(lista)>0:
            for element in lista:
                try:
                    os.mkdir(element)
                except:
                    pass
            for element in lista:
                if element.lower() in self.archiwa:
                    self.przeniesFolder('Archiwa', element)
                elif element.lower() in self.obrazy:
                    self.przeniesFolder('Obrazy', element)
                elif element.lower() in self.wideo:
                    self.przeniesFolder('Filmy', element)
                elif element.lower() in self.muzyka:
                    self.przeniesFolder('Muzyka', element)
                elif element.lower() in self.dokumenty:
                    self.przeniesFolder('Dokumenty', element)
                elif element.lower() in self.aplikacje:
                    self.przeniesFolder('Instalki', element)
                else:
                    pass

    def szukaj_rozszerzen(self):# tworzy liste rozszerzen
        # tworzy foldery glowne, z formetem plikow i porzadkuje zawartosc
        pliki = os.listdir(self.sciezka)
        self.rozszerzenia.clear()
        # zapisz wszystkie rozszerzenia ktore spelniaja kryteria
        for element in pliki:

            plik = element.split('.')
            if len(plik)>1:
                roz = plik[1]
                nazwa = plik[0]
            else:
                roz = ''
                nazwa=''

            if roz.lower() in self.archiwa \
                    or roz.lower() in self.muzyka \
                    or roz.lower() in self.dokumenty \
                    or roz.lower() in self.wideo \
                    or roz.lower() in self.obrazy \
                    or roz.lower() in self.aplikacje \
                    and nazwa != 'copyapp' and roz.lower():
                if roz.lower() not in self.rozszerzenia:
                    self.rozszerzenia.append(roz.lower())

    def szukaj_folderow(self):
        foldery = os.listdir(self.sciezka)
        lista_folderow = []
        for element in foldery:
            if element.lower() in self.archiwa or \
                    element.lower() in self.obrazy or \
                    element.lower() in self.wideo or \
                    element.lower() in self.muzyka or \
                    element.lower() in self.dokumenty or \
                    element.lower() in self.aplikacje:
                lista_folderow.append(element)
        return lista_folderow

    def pokaz_foldery(self):
        self.czyscRamki()
        lista_folderow= self.szukaj_folderow()
        if len(lista_folderow)>0:
            lista=''
            for element in lista_folderow:
                lista+=element + ', '
            tk.Label(self.ramka_komunikatow, text=f'Znaleziono foldery do sortowania: {lista[:-2]}. '
                                                  f'Czy mam je posegregować?').pack(fill='x')
            potwierdz=tk.Button(self.ramka_komunikatow, text='Tak', command=lambda: self.segreguj_foldery(lista_folderow))
            potwierdz.pack()
        else:
            tk.Label(self.ramka_komunikatow, text='Nie znaleziono folderów spełniających kryteria. Najpierw posortuj pliki.').pack(fill='x')

    def czyscRamki(self):
        for child in self.ramka_komunikatow.winfo_children():
            child.destroy()
        for child in self.ramka_dolna.winfo_children():
            child.destroy()
        self.aktualny_folder()

    def przeniesFolder(self, nazwa, element):
        self.czyscRamki()
        folder = nazwa

        try:
            os.mkdir(folder)
        except FileExistsError:
            pass

        try:
            shutil.move(os.path.abspath(element), os.path.dirname(os.path.abspath(element)) + "\\" + folder)

        except shutil.Error:
            pass

    def przeniesPliki(self, lista):
        pliki = os.listdir(self.sciezka)
        licznik = 0
        komunikaty=''
        for element in lista:
            try:
                os.mkdir(element)
            except:
                pass
        for x in pliki:
            if os.path.isfile(x):
                podziel = x.split('.')
                roz = podziel[-1]
                if roz.lower() in lista and podziel[0] != 'copyapp':
                    nowa_sciezka = os.path.dirname(os.path.abspath(x)) + "\\" + roz

                    if shutil.move(os.path.abspath(x), nowa_sciezka):
                        komunikaty+=f'- Pomyślnie przeniesiono plik {x} \n'
                        licznik += 1
                    else:
                        komunikaty+=f'- Nie udało się przenieść pliku {x}\n'
                else:
                    continue
        self.czyscRamki()
        self.rozszerzenia.clear()
        self.kom=tk.Label(self.ramka_komunikatow, text=komunikaty)
        self.kom.pack(side='left')

    def sprawdzZaznaczone(self):
        potwierdzone = []
        for index, check in enumerate(self.vars):
            if check.get() == 1:
                try:
                    potwierdzone.append(self.rozszerzenia[index])
                except:
                    pass
        if len(potwierdzone)>0:

            self.przeniesPliki(potwierdzone)

    def sortujPliki(self):
        self.czyscRamki()
        pliki = os.listdir(self.sciezka)

        for x in pliki:
            if os.path.isfile(x):
                podziel = x.split('.')
                roz = podziel[-1].upper()
                if roz.lower() in self.archiwa \
                        or roz.lower() in self.muzyka \
                        or roz.lower() in self.dokumenty \
                        or roz.lower() in self.wideo \
                        or roz.lower() in self.obrazy \
                        or roz.lower() in self.aplikacje \
                        and podziel[0] != 'copyapp':
                    if roz.lower() not in self.rozszerzenia:
                        self.rozszerzenia.append(roz.lower())
                else:
                    continue
        if len(self.rozszerzenia)>0:
            tk.Label(self.ramka_dolna, text='Znaleziono rozszerzenia:')

            for index, element in enumerate(self.rozszerzenia):
                var = tk.IntVar()
                self.vars.append(var)
                self.check = tk.Checkbutton(self.ramka_dolna, variable=var, text=element, name=str(index))
                self.check.pack(side='left')
                self.check.select()

            tk.Button(self.ramka_dolna, text='Dalej', command=self.sprawdzZaznaczone).pack()


Program()
window.mainloop()

# dodać funkcję pakowania folderów do zip
