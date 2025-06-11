from colorama import Fore, Back, Style
import settings



class Karta:
    WARTOSCI_KART = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    KOLORY_KART = ('kier', 'karo', 'pik', 'trefl')
    

    def __init__(self, wartosc, kolor):
        assert wartosc in self.WARTOSCI_KART
        assert kolor in self.KOLORY_KART
        self.wartosc = wartosc
        self.kolor = kolor
        self.odkryta = False


    def __lt__(self, karta2):
        return self.WARTOSCI_KART.index(self.wartosc) < self.WARTOSCI_KART.index(karta2.wartosc)


    def __gt__(self, karta2):
        return self.WARTOSCI_KART.index(self.wartosc) > self.WARTOSCI_KART.index(karta2.wartosc)


    @property
    def czerwona(self):
        return self.kolor in ('kier', 'karo')


    @property
    def czarna(self):
        return self.kolor in ('pik', 'trefl')


    def rozny_kolor(self, karta):
        return (self.czerwona and karta.czarna) or (self.czarna and karta.czerwona)


    def rowny_kolor(self, karta):
        return (self.czerwona and karta.czerwona) or (self.czarna and karta.czarna)


    def mniejsza_o_1(self, karta):
        return self.WARTOSCI_KART.index(self.wartosc) == self.WARTOSCI_KART.index(karta.wartosc) + 1


    def wieksza_o_1(self, karta):
        return self.WARTOSCI_KART.index(self.wartosc) == self.WARTOSCI_KART.index(karta.wartosc) - 1


    @property
    def znak_koloru(self):
        if self.kolor == 'kier':
            return '♥'
        if self.kolor == 'karo':
            return '♦'
        if self.kolor == 'pik':
            return '♠'
        if self.kolor == 'trefl':
            return '♣'
       

    @property
    def symbol(self):
        if settings.KOLORY:
            return f'{Fore.RED if self.czerwona else Fore.LIGHTWHITE_EX}{self.wartosc}{self.znak_koloru}{Fore.WHITE}'
        else:
            return f'{self.wartosc}{self.znak_koloru}'


    @property
    def symbol_zakryta(self):
        if settings.KOLORY:
            return f'{Fore.LIGHTBLACK_EX}■■{Fore.WHITE}'
        else:
            return f'■■'
            


    def __repr__(self):
        return f'<Karta: {self.symbol} >'

