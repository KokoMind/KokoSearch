import colorama
from colorama import Fore, Back, Style
import os


class Dashboard:
    """This class will be my dashboard of my crawler to track every action happen in my Crawler"""

    def __init__(self, num_threads):
        self.num_threads = num_threads

        # Colorama settings
        colorama.init(autoreset=True)
        self.pos = lambda y, x: '\x1b[%d;%dH' % (y, x)
        rows, columns = os.popen('stty size', 'r').read().split()
        self.MINY, self.MAXY = 1, int(rows) - 2
        self.MINX, self.MAXX = 1, int(columns) - 2

        # initial Prints
        print('%s%s%s%s%s' % (self.pos(self.MAXY / 10, self.MAXX / 2.5), Fore.WHITE, Back.BLACK, Style.NORMAL, "THE BEST CRAWLER IN THE WORLD THE KOKO CRAWLER"), end='')
        print('%s%s%s%s%s' % (self.pos(self.MAXY / 6, 130), Fore.WHITE, Back.BLACK, Style.NORMAL, "Frontier"), end='')
        print('%s%s%s%s%s' % (self.pos(self.MAXY / 6, 50), Fore.WHITE, Back.BLACK, Style.NORMAL, "Controller"), end='')
        print('%s%s%s%s%s' % (self.pos(self.MAXY / 3, self.MAXX / 2), Fore.WHITE, Back.BLACK, Style.NORMAL, "Crawlers"), end='')

        # initial Prints For threads with it's settings
        self.thread_settings = []
        every = (self.MAXX / 4) + 5
        X = - (every / 1.5)
        X_init = X
        Y = 18
        for i in range(self.num_threads):
            self.thread_settings.append({})
            if not (i % 4) and i:
                Y += 6
                X = X_init
            X += every
            print('%s%s%s%s%s' % (self.pos(Y, X), Fore.WHITE, Back.BLACK, Style.NORMAL, "Thread-" + str(i)), end='')
            self.thread_settings[i]['stat_pos'] = self.pos(Y + 2, X + 2)
            self.thread_settings[i]['crawled_pos'] = self.pos(Y + 3, X + 2)
            self.thread_settings[i]['tocrawl_pos'] = self.pos(Y + 4, X + 2)
            self.thread_settings[i]['dns'] = self.pos(Y + 5, X + 2)
            print('%s%s%s%s%s' % (self.pos(Y + 2, X - 15), Fore.WHITE, Back.BLACK, Style.NORMAL, "Current Status:"), end='')
            print('%s%s%s%s%s' % (self.pos(Y + 3, X - 15), Fore.WHITE, Back.BLACK, Style.NORMAL, "CRAWLED:"), end='')
            print('%s%s%s%s%s' % (self.pos(Y + 4, X - 15), Fore.WHITE, Back.BLACK, Style.NORMAL, "TOCRAWL:"), end='')
            print('%s%s%s%s%s' % (self.pos(Y + 5, X - 15), Fore.WHITE, Back.BLACK, Style.NORMAL, "DNS:"), end='')
            print('%s%s%s%s%s' % (self.thread_settings[i]['stat_pos'], Fore.WHITE, Back.BLACK, Style.DIM, "URL fetched"), end='')

    def __del__(self):
        print('%s%s%s%s%s' % (self.pos(self.MAXY, self.MAXX / 2), Fore.RED, Back.WHITE, Style.NORMAL, "BYE BYE"), end='\n')
        print(Style.RESET_ALL)

    def print_cur_status(self, str, thread_id):
        pass
