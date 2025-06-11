import random
from colorama import Fore, Back, Style
from exceptions import PasjansException
import settings



class StosKart:
    def __init__(self, karty=[], numer_stosu=None):
        self.stos = []
        self.stos.extend(karty)
        self.numer_stosu = numer_stosu
        self.wybrany = False


    def potasuj(self):
        random.shuffle(self.stos)


    def mozna_dodac(self, karty):
        return True


    def mozna_usunac(self, num):
        if len(self.stos) > 0:
            return True
        else:
            return False


    def dodaj(self, karty):
        if self.mozna_dodac(karty):
            self.stos.extend(karty)
        else:
            raise PasjansException(f'Nie można dodać kart do {self.stos_nr_str}')
        

    def usun(self, num):
        if self.mozna_usunac(num):
            return list(reversed([self.stos.pop() for i in range(num)]))
        else:
            raise PasjansException(f'Nie można usunąć kart z {self.stos_nr_str}')

                                
    @ property
    def stos_nr_str(self):
        if self.numer_stosu is not None:
            return f'{self.__class__.__name__} nr {self.numer_stosu}'
        else:
            return self.__class__.__name__
   

    def reprezentacja(self, tylko_karta_nr=None, numer_stosu=True):
        if settings.KOLORY:
            BG = Back.BLUE
            BGH = Back.GREEN if self.wybrany else BG
            RST = Back.BLACK
        else:
            BG = BGH = RST = ''
        lista_repr = []
        lista_repr.append(f'{BGH}  {self.numer_stosu}  {RST}' if numer_stosu else '     ')
        lista_repr.append('     ')
        lista_repr.append(f'{BG}     {RST}')
        if len(self.stos) == 0:
            #lista_repr.append(f'{BG}  □□ {RST}')
            lista_repr.append(f'{BG}     {RST}')
            stos = []
        elif tylko_karta_nr is not None:            
            stos = [self.stos[tylko_karta_nr]]
        else:
            stos = self.stos

        for karta in stos:
            if karta.odkryta:
                sym = karta.symbol if karta.wartosc == '10' else f' {karta.symbol}'
                lista_repr.append(f'{BG} {sym} {RST}')
            else:
                lista_repr.append(f'{BG}  {karta.symbol_zakryta} {RST}')
        lista_repr.append(f'{BG}     {RST}')
        return lista_repr

 
    def __len__(self):
        return len(self.stos)


    def __repr__(self):
        return f'<{self.__class__.__name__}: {" ".join([k.symbol for k in self.stos])} >'



class Kolumna(StosKart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i, karta in enumerate(self.stos):
            karta.odkryta = True if i == len(self.stos) - 1 else False


    def mozna_usunac(self, num):
        return super().mozna_usunac(num) and all([k.odkryta for k in self.stos[-num:]])
        

    def mozna_dodac(self, karty):
        return len(karty) > 0 and \
               super().mozna_dodac(karty) and \
               all([k.odkryta for k in karty]) and \
               (self.stos[-1].rozny_kolor(karty[0]) and self.stos[-1].mniejsza_o_1(karty[0]) if len(self.stos) > 0 else True) and \
               all([karty[i].rozny_kolor(karty[i+1]) and karty[i].mniejsza_o_1(karty[i+1]) for i in range(len(karty)-1)]) and \
               (karty[0].wartosc == 'K' if len(self.stos) == 0 else True)


    def usun(self, num):
        karty = super().usun(num)
        if len(self.stos) > 0:
            self.stos[-1].odkryta = True
        return karty
    



class StosKoncowy(StosKart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def potasuj(self):
        raise PasjansException(f'Nie można tasować stosu końcowego')

    
    def mozna_usunac(self):
        raise PasjansException(f'Nie można usuwać kart ze stosu końcowego')
    

    def mozna_dodac(self, karty):
        return super().mozna_dodac(karty) and \
               all([k.odkryta for k in karty]) and \
               (self.stos[-1].kolor == karty[0].kolor and self.stos[-1].wieksza_o_1(karty[0]) if len(self.stos) > 0 else True) and \
               all([karty[i].kolor == karty[i+1].kolor and karty[i].wieksza_o_1(karty[i+1]) for i in range(len(karty)-1)]) and \
               (karty[0].wartosc == 'A' if len(self.stos) == 0 else True)



class StosRezerwowy(StosKart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i, karta in enumerate(self.stos):
            #karta.odkryta = False
            karta.odkryta = True

    
    def mozna_usunac_dowolna_karte(self, idx):
        if idx < 0:
            return bool(-len(self.stos) <= idx <= -1)
        else:
            return bool(0 <= idx < len(self.stos))
        


    def usun_dowolna_karte(self, idx):
            if self.mozna_usunac_dowolna_karte(idx):
                return self.stos.pop(idx)
            else:
                raise PasjansException(f'Nie można usunąć karty nr {idx} ze Stosu Rezerwowego.')

