import sys, os, shutil, re
from collections import namedtuple
from colorama import Fore, Back, Style
import settings

RE_KOLORY = re.compile('\x1b[^m]+?m')


# https://stackoverflow.com/questions/5161552/python-curses-handling-window-terminal-resize
# https://docs.python.org/3/library/curses.html


RozmiarEkranu = namedtuple('RozmiarEkranu', ['w', 'h'])

class Ekran:
    def __init__(self, rozgrywka):
        self.rozgrywka = rozgrywka
        self.wyczysc()
    

    def wyczysc(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        terminal_size = shutil.get_terminal_size()
        self.rozmiar = RozmiarEkranu(terminal_size.columns - 1, terminal_size.lines - 1)
        self.znaki = [[' '] * self.rozmiar.w for i in range(self.rozmiar.h)]
        self.kolory = [[''] * self.rozmiar.w for i in range(self.rozmiar.h)]


    def rysuj(self):
        if settings.KOLORY:
            for i in range(len(self.znaki)):
                for j in range(len(self.znaki[i])):
                    if self.kolory[i][j]:
                        self.znaki[i][j] = self.kolory[i][j] + self.znaki[i][j]
#        print([''.join(self.znaki[i]) for i in range(len(self.znaki))])
        print('\n'.join([''.join(self.znaki[i]) for i in range(len(self.znaki))]), end='')
    

    def wypisz(self, strs, wiersz, kolumna, color=None):
        assert isinstance(strs, (list, tuple, str))
        if isinstance(strs, str):
            strs = [strs]
        assert len(strs) <= self.rozmiar.h
        for k, s in enumerate(strs):
            znaki_wiersza = []
            i = 0
            j = 0
            if settings.KOLORY:
                self.kolory[wiersz+k][kolumna+j:kolumna+j+len(s)] = [''] * len(s)
                prev_m = None
                for m in RE_KOLORY.finditer(s):
                    znaki = list(s[i:m.start()])
                    j += len(znaki)
                    znaki_wiersza.extend(znaki)
                    if prev_m is not None and prev_m.end() == m.start():
                        self.kolory[wiersz+k][kolumna+j] += m.group(0)
                    else:
                        self.kolory[wiersz+k][kolumna+j] = m.group(0)
                    prev_m = m
                    i = m.end()
            znaki_wiersza.extend(list(s[i:]))

            if not kolumna + len(znaki_wiersza) <= self.rozmiar.w:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(Fore.RED + Back.WHITE + '\nKonsola jest za mała do uruchomnienia gry.')
                print('Prosze powiększyć konsolę.\n' + Style.RESET_ALL)
                sys.exit(1)

            self.znaki[wiersz+k][kolumna:kolumna+len(znaki_wiersza)] = znaki_wiersza
            if settings.KOLORY and color is not None:
                self.kolory[wiersz+k][kolumna] = color
                self.kolory[wiersz+k][kolumna+len(znaki_wiersza)] = Style.RESET_ALL



    def alert(self, s, color=None):
        assert len(s) + 7 <= self.rozmiar.w
        self.wypisz([
            f'╔{"═".join([""] * (len(s)))} Esc ╗',
            f'║{" ".join([""] * (len(s)+5))}║',
            f'║  {s}  ║',
            f'║{" ".join([""] * (len(s)+5))}║',
            f'╚{"═".join([""] * (len(s)+5))}╝',
        ], 
        int((self.rozmiar.h - 5) / 2), 
        int((self.rozmiar.w - len(s) - 7) / 2),
        color=Back.RED if color is None else color)
        


