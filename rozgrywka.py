import random, copy
from itertools import product
from colorama import Fore, Back, Style, Cursor
from karta import Karta
from stos_kart import StosKart, Kolumna, StosRezerwowy, StosKoncowy
from ekran import Ekran
from konsola import Konsola
from exceptions import PasjansException
import settings

# https://www.geeksforgeeks.org/how-to-detect-if-a-specific-key-pressed-using-python/


class Rozgrywka:
    def __init__(self):
        self.poziom_trudnosci = 1 #1 - łatwy, 3 - trudny
        self.ekran = Ekran(self)
        self.konsola = Konsola(self)
        self.rozdaj()


    def rozdaj(self):
        self.wygrana = False
        self.koniec_gry = False
        self.wyjsc = False
        self.stan = ['P', 0, 0, 0, 0, 0]
        self.wyborgracza1 = 0
        self.wyborgracza2 = 0
        self.ilosckart = 0
        self.idxrezerwowy = -1
        self.iloscruchow = 0
        self.stan_kart = []

        talia = StosKart([Karta(w, k) for w, k in product(Karta.WARTOSCI_KART, Karta.KOLORY_KART)])
        assert len(talia) == 52
        talia.potasuj()

        self.kolumny = [Kolumna(talia.usun(i+1), numer_stosu=i+1) for i in range(7)]
        self.stos_rezerwowy = StosRezerwowy(talia.stos, numer_stosu='R')
        self.stosy_koncowe = [StosKoncowy(numer_stosu=l) for i, l in enumerate(['A', 'B', 'C', 'D'])]
        self.stos_rezerwowy.potasuj()


    def start(self):
        self.konsola.start()


    def zachowaj_stan_kart(self):
        self.stan_kart.append([
            copy.deepcopy(self.kolumny),
            copy.deepcopy(self.stos_rezerwowy),
            copy.deepcopy(self.stosy_koncowe),
            copy.deepcopy(self.ilosckart),
            copy.deepcopy(self.idxrezerwowy),
            copy.deepcopy(self.iloscruchow),
        ])
        if len(self.stan_kart) > 3:
            self.stan_kart = self.stan_kart[-3:]


    def cofnij_ruch(self):
        if len(self.stan_kart) > 0:
            self.kolumny, self.stos_rezerwowy, self.stosy_koncowe, self.ilosckart, self.idxrezerwowy, self.iloscruchow = self.stan_kart.pop()
        for stos in self.kolumny:
            stos.wybrany = False
        for stos in self.stosy_koncowe:
            stos.wybrany = False
        self.stos_rezerwowy.wybrany = False



    def sprawdz_wygrana(self):
        if all([len(k) == 0 for k in self.kolumny]) and len(self.stos_rezerwowy) == 0:
            self.wygrana = True


    def przesun_miedzy_kolumnami(self, kolumna1, kolumna2, num):
        '''Przesuwa num kart z kolumny1 do kolumny2'''
        if kolumna1.mozna_usunac(num) and kolumna2.mozna_dodac(kolumna1.stos[-num:]):
            self.zachowaj_stan_kart()
            kolumna2.dodaj(kolumna1.usun(num))
        else:
            raise PasjansException(f'Nie można przesunac {num} kart z {kolumna1.stos_nr_str} do {kolumna2.stos_nr_str}')
        self.sprawdz_wygrana()


    def przesun_na_stos_koncowy(self, kolumna, stos_koncowy, num):
        '''Przesuwa num kart z kolumny lub stosu_rezerwowego do stosu_koncowego'''
        num = 1
        if kolumna.mozna_usunac(num) and stos_koncowy.mozna_dodac(kolumna.stos[-num:]):
            self.zachowaj_stan_kart()
            stos_koncowy.dodaj(kolumna.usun(num))
        else:
            raise PasjansException(f'Nie można przesunac karty z {kolumna.stos_nr_str} do {stos_koncowy.stos_nr_str}')
        self.sprawdz_wygrana()


    def przesun_ze_stosu_rezerwowego_do_kolumny(self, kolumna, idx):
        '''Przesuwa num z stosu rezerwowego do kolumny'''
        if self.stos_rezerwowy.mozna_usunac_dowolna_karte(idx) and kolumna.mozna_dodac([self.stos_rezerwowy.stos[idx]]):
            self.zachowaj_stan_kart()            
            kolumna.dodaj([self.stos_rezerwowy.usun_dowolna_karte(idx)])
        else:
            raise PasjansException(f'Nie można przesunac kartę {abs(idx)} ze stosu rezerwowego do {kolumna.stos_nr_str}')
        self.sprawdz_wygrana()
        

    def przesun_ze_stosu_rezerwowego_na_koncowy(self, stos_koncowy, idx):
        if self.poziom_trudnosci == 1: #poziom łatwy
            if self.stos_rezerwowy.mozna_usunac_dowolna_karte(idx) and stos_koncowy.mozna_dodac([self.stos_rezerwowy.stos[idx]]):
                self.zachowaj_stan_kart()            
                stos_koncowy.dodaj([self.stos_rezerwowy.usun_dowolna_karte(idx)])
            else:            
                raise PasjansException(f'Nie można przesunac karty z Stosu Rezerwowego do Stosu Koncowego')
        elif self.poziom_trudnosci == 3: #poziom trudny
            if self.stos_rezerwowy.mozna_usunac_dowolna_karte(idx) and stos_koncowy.mozna_dodac([self.stos_rezerwowy.stos[idx]]):
                self.zachowaj_stan_kart()            
                stos_koncowy.dodaj([self.stos_rezerwowy.usun_dowolna_karte(idx)])
            else:            
                raise PasjansException(f'Nie można przesunac karty z Stosu Rezerwowego do Stosu Koncowego')
        self.sprawdz_wygrana()


    def dobierz_ze_stosu_rezerwowego(self, poziom_trudnosci):
        self.zachowaj_stan_kart()
        if poziom_trudnosci == 1: #poziom łatwy
            if abs(self.idxrezerwowy) < len(self.stos_rezerwowy):
                self.idxrezerwowy -= 1
            else:
                self.idxrezerwowy = -1
                self.stos_rezerwowy.potasuj()
        elif poziom_trudnosci == 3: #poziom trudny
            if abs(self.idxrezerwowy-3) < len(self.stos_rezerwowy):
                self.idxrezerwowy -= 3
            else:
                self.stos_rezerwowy.potasuj()
                self.idxrezerwowy = -1 
    

    def zapisz_w_tabeli_wynikow(self, imie):
        '''Zapisuje wynik w tabeli wyników, jeśli kwalifikuje się on jako jeden z najlepszych'''
        with open(settings.PLIK_WYNIKI) as f:
            wyniki = [w.split(',') for w in f.readlines() if w.strip()]
        wyniki = [(int(p), n.strip()) for p, n in wyniki]
        wyniki.sort()
        max_wynik = max(wyniki)[0]
        if self.iloscruchow <= max_wynik or len(wyniki) < settings.MAX_WYNIKI:
            if len(wyniki) >= settings.MAX_WYNIKI:
                wyniki = wyniki[:settings.MAX_WYNIKI-1]
            wyniki.append((self.iloscruchow, imie))
            wyniki.sort(reverse=True)
            with open(settings.PLIK_WYNIKI, 'w') as f:
                for p,n in wyniki:
                    f.write(','.join([str(p), n]))
                    f.write('\n')


    def wyswietl_stan(self):
        # rysuj stosy
        if self.stan[0] == 'P':
            if self.stan[1] == 0:
                self.ekran.wypisz(' ' * 40 + 'Pasjans' + ' ' * 40, 1, 3, color=f'{Fore.BLACK}{Back.GREEN}')
                self.ekran.wypisz(' ' * 40 + 'Witamy!' + ' ' * 40, 3, 3)
                self.ekran.wypisz('Co chcesz teraz zrobić?', 4, 3)
                self.ekran.wypisz('1. Zagrać', 5, 3)
                self.ekran.wypisz('2. Zmienić poziom trudności', 6, 3)
                self.ekran.wypisz('3. Zobaczyć tabelę najlepszych wyników', 7, 3)
                self.ekran.wypisz('4. Wyjść', 8, 3)

            elif self.stan[1] == 'ZPT':
                self.ekran.wypisz('Jaki poziom trudności chcesz ustawić?', 4, 3)
                self.ekran.wypisz('1. Łatwy', 5, 3)
                self.ekran.wypisz('2. Trudny', 6, 3)
                self.czyzrobione = False

            elif self.stan[1] == 'ZTNW':
                pass
        elif self.stan[0] == 'Wygrana': #WIP
            self.ekran.wypisz(' ' * 40 + 'Wygrana!' + ' ' * 40, 1, 3, color=f'{Fore.BLACK}{Back.GREEN}')
            self.ekran.wypisz('Liczba ruchów: ' + str(self.iloscruchow), 3, 3)
            self.ekran.wypisz('Liczba ruchów: ' + str(self.iloscruchow), 3, 3)
            self.ekran.wypisz('Wciśnij enter a następnie wpisz swoje imię: ' + str(self.iloscruchow), 5, 0)
            self.ekran.rysuj()
            print(Cursor.POS(0, 7))
            input()
            print('Wpisz teraz swoje imię:')
            imie = input()
            self.zapisz_w_tabeli_wynikow(imie)
            self.rozdaj()
            self.stan[0] = 'P'
        elif self.stan[0] == 'Wyniki':
            self.ekran.wypisz(' ' * 30 + 'Tabela najlepszych wyników' + ' ' * 30, 1, 3, color=f'{Fore.BLACK}{Back.GREEN}')
            with open(settings.PLIK_WYNIKI) as f:
                wyniki = [w.split(',') for w in f.readlines() if w.strip()]
            wyniki = [(int(p), n.strip()) for p, n in wyniki]
            wyniki.sort()
            for i, (p, n) in enumerate(wyniki):
                self.ekran.wypisz(f'{" " if i<9 else ""}{i+1}. {p:>4} ruchów   {n}', 3+i, 6)
            self.stan[0] = 'P'
        else:
            self.ekran.wypisz(' ' * 20 + 'Kolumny' + ' ' * 20, 1, 3, color=f'{Fore.BLACK}{Back.YELLOW}')
            for i, kolumna in enumerate(self.kolumny):
                self.ekran.wypisz(kolumna.reprezentacja(), 3, 3+7*i)
            self.ekran.wypisz(' ' * 6 + 'Stosy Koncowe' + ' ' * 7, 1, 55, color=f'{Fore.BLACK}{Back.YELLOW}')
            for i, stos_koncowy in enumerate(self.stosy_koncowe):
                self.ekran.wypisz(stos_koncowy.reprezentacja(tylko_karta_nr=-1), 3, 55+7*i)
            
            if self.poziom_trudnosci == 1: #poziom łatwy
                self.ekran.wypisz(' Stos Rezerwowy ', 1, 85, color=f'{Fore.BLACK}{Back.YELLOW}')
                if abs(self.idxrezerwowy) <= len(self.stos_rezerwowy):
                    self.ekran.wypisz(self.stos_rezerwowy.reprezentacja(tylko_karta_nr=self.idxrezerwowy), 3, 90)
            elif self.poziom_trudnosci == 3: #poziom trudny
                self.ekran.wypisz('   Stos Rezerwowy  ', 1, 85, color=f'{Fore.BLACK}{Back.YELLOW}')
                if abs(self.idxrezerwowy) <= len(self.stos_rezerwowy):
                    self.ekran.wypisz(self.stos_rezerwowy.reprezentacja(tylko_karta_nr=self.idxrezerwowy), 3, 85)
                if abs(self.idxrezerwowy-1) <= len(self.stos_rezerwowy):
                    self.ekran.wypisz(self.stos_rezerwowy.reprezentacja(tylko_karta_nr=self.idxrezerwowy-1), 3, 92)
                if abs(self.idxrezerwowy-2) <= len(self.stos_rezerwowy):
                    self.ekran.wypisz(self.stos_rezerwowy.reprezentacja(tylko_karta_nr=self.idxrezerwowy-2), 3, 99)
            
            if self.stan[0] == 0:
                self.ekran.wypisz('Co chcesz zrobic?', 22, 3)
                self.ekran.wypisz('Q. Przeniesc karte miedzy kolumnami', 23, 3)
                self.ekran.wypisz('W. Przeniesc karte do stosu koncowego', 24, 3)
                self.ekran.wypisz('E. Dobrac karty ze stosu rezerwowego', 25, 3)
                self.ekran.wypisz('R. Przeniesc karty ze stosu rezerwowego do kolumny/stosu koncowego', 26, 3)
                self.ekran.wypisz('K. Zakończ grę', 27, 3)
                if len(self.stan_kart) > 0:
                    self.ekran.wypisz('C. Cofnij ruch', 28, 3)
            
            elif self.stan[0] == 1:
                self.ekran.wypisz('Z ktorej kolumny chcesz przeniesc karte?', 22, 3)
                if self.stan[1] == 1:
                    self.ekran.wypisz('Do ktorej kolumny chcesz przeniesc karte', 24, 3)
                elif self.stan[1] == 2:
                    self.ekran.wypisz('Ile kart chcesz przesunąć?', 26, 3)
            
            elif self.stan[0] == 2:
                self.ekran.wypisz('Z ktorej kolumny chcesz przeniesc karte?', 22, 3)
                if self.stan[1] == 1:
                    self.ekran.wypisz('Na ktory stos chcesz przeniesc karte?', 24, 3)
            
            elif self.stan[0] == 4:
                self.ekran.wypisz('A. Przeniesc karte do kolumny', 22, 3)
                self.ekran.wypisz('B. Przeniesc karte do stosu koncowego', 23, 3)
                if self.stan[1] == 'A':
                    self.ekran.wypisz('Do której kolumny chcesz przenieść karte?', 22, 3)
                    self.ekran.wypisz('                                          ', 23, 3)
                    self.stan[1] = 'A1'
                if self.stan[1] == 'B':
                    self.ekran.wypisz('Do którego stosu końcowego chcesz przenieść karte?', 22, 3)
                    self.ekran.wypisz('                                          ', 23, 3)
                    self.stan[1] = 'B1'


