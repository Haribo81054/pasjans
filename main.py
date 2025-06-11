import argparse
import colorama
from rozgrywka import Rozgrywka
import settings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gra Pasjans')
    parser.add_argument('-bw', action='store_true', help='Tryb bez kolorów')

    args = parser.parse_args()
    if args.bw:
        settings.KOLORY = False

    if settings.KOLORY:
        colorama.init()
    rozgrywka = Rozgrywka()
    rozgrywka.start()


