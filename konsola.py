from pynput.keyboard import Key, KeyCode, Listener
from colorama import Fore, Back, Style
from exceptions import PasjansException
from stos_kart import StosKart
import settings


class Konsola:
    def __init__(self, rozgrywka):
        self.rozgrywka = rozgrywka


    def start(self):
        self.rozgrywka.ekran.wyczysc()
        self.rozgrywka.wyswietl_stan()
        self.rozgrywka.ekran.rysuj()
        with Listener(on_press = self.on_press) as listener:   
            listener.join()


    def on_press(self, key):
        self.rozgrywka.ekran.wyczysc()
        test_alert = False
        alert_str = None

        if self.rozgrywka.stan[0] == 'P':
            if key == KeyCode.from_char('1') and self.rozgrywka.stan[1] != 'ZPT': #zagrać
                self.rozgrywka.rozdaj()
                self.rozgrywka.stan[0] = 0
                self.rozgrywka.stan[1] = 0

            elif self.rozgrywka.stan[1] == 'ZPT':
                if key == KeyCode.from_char('1'):
                    self.rozgrywka.poziom_trudnosci = 1
                    self.rozgrywka.stan[1] = 0
                elif key == KeyCode.from_char('2'):
                    self.rozgrywka.poziom_trudnosci = 3
                    self.rozgrywka.stan[1] = 0             
            elif key == KeyCode.from_char('2') or self.rozgrywka.stan[1] == 'ZPT': #zmienić poz. trudności
                self.rozgrywka.stan[1] = 'ZPT'

            elif key == KeyCode.from_char('3') and self.rozgrywka.stan[1] != 'ZPT': #zobaczyć tab. naj. wyników
                self.rozgrywka.stan[0] = 'Wyniki'
                    
            elif key == KeyCode.from_char('4') and self.rozgrywka.stan[1] != 'ZPT': #wyjść
                self.rozgrywka.wyjsc = True
        else:

            if self.rozgrywka.stan[0] == 1:
                if self.rozgrywka.stan[1] == 0:
                    if key in [KeyCode.from_char(str(i+1)) for i in range(7)]:
                        self.rozgrywka.wyborgracza1 = key.char
                        self.rozgrywka.kolumny[int(self.rozgrywka.wyborgracza1)-1].wybrany = True
                        self.rozgrywka.stan[1] = 1
                elif self.rozgrywka.stan[1] == 1:
                    if key in [KeyCode.from_char(str(i+1)) for i in range(7)]:
                        self.rozgrywka.wyborgracza2 = key.char
                        self.rozgrywka.kolumny[int(self.rozgrywka.wyborgracza2)-1].wybrany = True
                        self.rozgrywka.stan[1] = 2
                elif self.rozgrywka.stan[1] == 2:
                    self.rozgrywka.ilosckart = key.char
                    try:
                        self.rozgrywka.przesun_miedzy_kolumnami(self.rozgrywka.kolumny[int(self.rozgrywka.wyborgracza1)-1], 
                                                            self.rozgrywka.kolumny[int(self.rozgrywka.wyborgracza2)-1], 
                                                            int(self.rozgrywka.ilosckart))
                        self.rozgrywka.iloscruchow += 1
                    except PasjansException as exc:
                        alert_str = str(exc)                    
                        
                    finally:
                        self.rozgrywka.stan[0] = 0
                        self.rozgrywka.stan[1] = 0
                        for kolumna in self.rozgrywka.kolumny:
                            kolumna.wybrany = False

            elif self.rozgrywka.stan[0] == 2:
                if self.rozgrywka.stan[1] == 0:
                    if key in [KeyCode.from_char(str(i+1)) for i in range(7)]:
                        self.rozgrywka.wyborgracza1 = key.char
                        self.rozgrywka.kolumny[int(self.rozgrywka.wyborgracza1)-1].wybrany = True
                        self.rozgrywka.stan[1] = 1
                elif self.rozgrywka.stan[1] == 1:
                    if key in [KeyCode.from_char(c) for c in 'AaBbCcDd']: 
                        self.rozgrywka.wyborgracza2 = ord(key.char.lower())-ord('a')
                        self.rozgrywka.stosy_koncowe[int(self.rozgrywka.wyborgracza2)].wybrany = True
                        self.rozgrywka.stan[1] = 2
                        try:
                            self.rozgrywka.przesun_na_stos_koncowy(
                                self.rozgrywka.kolumny[int(self.rozgrywka.wyborgracza1)-1],
                                self.rozgrywka.stosy_koncowe[int(self.rozgrywka.wyborgracza2)],
                                1)
                            self.rozgrywka.iloscruchow += 1
                        except PasjansException as exc:
                            alert_str = str(exc)                                        
                        finally:
                            self.rozgrywka.stan[0] = 0
                            self.rozgrywka.stan[1] = 0
                            for kolumna in self.rozgrywka.kolumny:
                                kolumna.wybrany = False
                            for sk in self.rozgrywka.stosy_koncowe:
                                sk.wybrany = False
                            self.rozgrywka.stos_rezerwowy.wybrany = False

            elif self.rozgrywka.stan[0] == 3:
                self.rozgrywka.stan[0] = 0

            elif self.rozgrywka.stan[0] == 4:
                self.rozgrywka.stos_rezerwowy.wybrany = True
                if key == (KeyCode.from_char('a') or KeyCode.from_char('A')) and self.rozgrywka.stan[0] == 4 and self.rozgrywka.stan[2] != 2:
                    self.rozgrywka.stan[1] = 'A'
                    self.rozgrywka.stan[2] = 1
                elif self.rozgrywka.stan[1] == 'A1' and self.rozgrywka.stan[2] == 1:
                    if key in [KeyCode.from_char(str(i+1)) for i in range(7)]:
                        self.rozgrywka.wyborgracza1 = key.char
                        self.rozgrywka.kolumny[int(self.rozgrywka.wyborgracza1)-1].wybrany = True
                        self.rozgrywka.stan[1] = 'A1'
                    
                    try:
                        self.rozgrywka.przesun_ze_stosu_rezerwowego_do_kolumny(
                            self.rozgrywka.kolumny[int(self.rozgrywka.wyborgracza1)-1],
                            self.rozgrywka.idxrezerwowy)  
                        self.rozgrywka.iloscruchow += 1
                    except PasjansException as exc:
                        alert_str = str(exc)
                    finally:
                        self.rozgrywka.stan[0] = 0
                        self.rozgrywka.stan[1] = 0
                        self.rozgrywka.stos_rezerwowy.wybrany = False
                        for kolumna in self.rozgrywka.kolumny:
                            kolumna.wybrany = False

                elif key == (KeyCode.from_char('b') or KeyCode.from_char('B')) and self.rozgrywka.stan[0] == 4 and self.rozgrywka.stan[2] != (1 and 2):
                    self.rozgrywka.stan[1] = 'B'
                    self.rozgrywka.stan[2] = 2
                elif self.rozgrywka.stan[1] == 'B1' and self.rozgrywka.stan[2] == 2:
                    if key in [KeyCode.from_char(c) for c in 'AaBbCcDd']: 
                        self.rozgrywka.wyborgracza2 = ord((key.char).lower()) - ord('a')
                        self.rozgrywka.stan[1] = 'B2'
                        try:
                            self.rozgrywka.przesun_ze_stosu_rezerwowego_na_koncowy( 
                                self.rozgrywka.stosy_koncowe[int(self.rozgrywka.wyborgracza2)], 
                                self.rozgrywka.idxrezerwowy)
                            self.rozgrywka.iloscruchow += 1
                        except PasjansException as exc:
                            alert_str = str(exc)                    
                    
                        finally:
                            self.rozgrywka.stan[0] = 0
                            self.rozgrywka.stan[1] = 0
                            self.rozgrywka.stan[2] = 0
                            self.rozgrywka.stos_rezerwowy.wybrany = False
                            for kolumna in self.rozgrywka.kolumny:
                                kolumna.wybrany = False

        if key == Key.esc:
            pass
        elif key == Key.end:
            self.rozgrywka.wyjsc = True
        #elif key == KeyCode.from_char('t'):
        #    test_alert = True
        elif (key == KeyCode.from_char('q') or key == KeyCode.from_char('Q')) and self.rozgrywka.stan[0] == 0:
            self.rozgrywka.stan[0] = 1
        elif (key == KeyCode.from_char('w') or key == KeyCode.from_char('W')) and self.rozgrywka.stan[0] == 0:
            self.rozgrywka.stan[0] = 2
        elif (key == KeyCode.from_char('e') or key == KeyCode.from_char('E')) and self.rozgrywka.stan[0] == 0:
            self.rozgrywka.dobierz_ze_stosu_rezerwowego(self.rozgrywka.poziom_trudnosci)
            self.rozgrywka.iloscruchow += 1
        elif (key == KeyCode.from_char('r') or key == KeyCode.from_char('R')) and self.rozgrywka.stan[0] == 0:
            self.rozgrywka.stan[0] = 4
            self.rozgrywka.stos_rezerwowy.wybrany = True
        elif (key == KeyCode.from_char('k') or key == KeyCode.from_char('K')) and self.rozgrywka.stan[0] == 0:
            self.rozgrywka.koniec_gry = True
        elif (key == KeyCode.from_char('c') or key == KeyCode.from_char('C')) and self.rozgrywka.stan[0] == 0:
            self.rozgrywka.cofnij_ruch()
        #elif (key == KeyCode.from_char('l') or key == KeyCode.from_char('L')) and self.rozgrywka.stan[0] == 0:
        #    self.rozgrywka.wygrana = True

        if self.rozgrywka.koniec_gry:
            self.rozgrywka.ekran.wyczysc()
            self.rozgrywka.stan[0] = 'P'
            self.rozgrywka.stan[1] = 0
            self.rozgrywka.stan[2] = 0
            self.rozgrywka.koniec_gry = False

        if self.rozgrywka.wygrana:
            self.rozgrywka.stan[0] = 'Wygrana'
            
            
        self.rozgrywka.wyswietl_stan()
        if alert_str is not None:
            self.rozgrywka.ekran.alert(alert_str)

        #if test_alert:
        #    self.rozgrywka.ekran.alert('alert testowy')

        self.rozgrywka.ekran.rysuj()
        
        if self.rozgrywka.wyjsc:
            self.rozgrywka.ekran.wyczysc()
            return False



