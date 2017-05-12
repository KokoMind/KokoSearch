import colorama
from colorama import Fore, Back, Style
import os
from datetime import datetime


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
        print('%s%s%s%s%s' % (self.pos(2, self.MAXX / 2.5), Fore.WHITE, Back.BLACK, Style.NORMAL, "THE BEST CRAWLER IN THE WORLD THE KOKO CRAWLER"), end='')
        print('%s%s%s%s%s' % (self.pos(self.MAXY / 12, 100), Fore.WHITE, Back.BLACK, Style.NORMAL, "Frontier:"), end='')
        print('%s%s%s%s%s' % (self.pos(self.MAXY / 12, 30), Fore.WHITE, Back.BLACK, Style.NORMAL, "Controller:"), end='')

        # initial Prints For Controller with it's settings
        # TODO

        # initial Prints For Frontier with it's settings
        # TODO

        # initial Prints For threads with it's settings
        self.thread_settings = []
        every = (self.MAXX / 9)
        X = -11
        X_init = X
        Y = 6
        for i in range(self.num_threads):
            self.thread_settings.append({})
            if not (i % 9) and i:
                Y += 6
                X = X_init
            X += every
            print('%s%s%s%s%s' % (self.pos(Y, X), Fore.WHITE, Back.BLACK, Style.NORMAL, "Thread-" + str(i)), end='')
            self.thread_settings[i]['stat_pos'] = self.pos(Y + 1, X + 2)
            self.thread_settings[i]['crawled_pos'] = self.pos(Y + 2, X + 2)
            self.thread_settings[i]['refused_pos'] = self.pos(Y + 3, X + 2)
            self.thread_settings[i]['tocrawl_pos'] = self.pos(Y + 4, X + 2)
            self.thread_settings[i]['dns_pos'] = self.pos(Y + 5, X + 2)
            print('%s%s%s%s%s' % (self.pos(Y + 1, X - 7), Fore.WHITE, Back.BLACK, Style.NORMAL, "Status:"), end='')
            print('%s%s%s%s%s' % (self.pos(Y + 2, X - 7), Fore.WHITE, Back.BLACK, Style.NORMAL, "CRAWLED:"), end='')
            print('%s%s%s%s%s' % (self.pos(Y + 3, X - 7), Fore.WHITE, Back.BLACK, Style.NORMAL, "REFUSED:"), end='')
            print('%s%s%s%s%s' % (self.pos(Y + 4, X - 7), Fore.WHITE, Back.BLACK, Style.NORMAL, "TOCRAWL:"), end='')
            print('%s%s%s%s%s' % (self.pos(Y + 5, X - 7), Fore.WHITE, Back.BLACK, Style.NORMAL, "DNS:"), end='')

    def __del__(self):
        print('%s%s%s%s%s' % (self.pos(self.MAXY, self.MAXX / 2), Fore.RED, Back.WHITE, Style.NORMAL, "BYE BYE"), end='\n')
        print(Style.RESET_ALL)

    def print_cur_stat(self, str, thread_id):
        print('%s%s%s%s%s' % (self.thread_settings[thread_id]['stat_pos'], Fore.WHITE, Back.BLACK, Style.DIM, str), end='')

    def print_crawled(self, str, thread_id):
        print('%s%s%s%s%s' % (self.thread_settings[thread_id]['crawled_pos'], Fore.WHITE, Back.BLACK, Style.DIM, str), end='')

    def print_refused(self, str, thread_id):
        print('%s%s%s%s%s' % (self.thread_settings[thread_id]['refused_pos'], Fore.WHITE, Back.BLACK, Style.DIM, str), end='')

    def print_tocrawl(self, str, thread_id):
        print('%s%s%s%s%s' % (self.thread_settings[thread_id]['tocrawl_pos'], Fore.WHITE, Back.BLACK, Style.DIM, str), end='')

    def print_dns(self, str, thread_id):
        print('%s%s%s%s%s' % (self.thread_settings[thread_id]['dns_pos'], Fore.WHITE, Back.BLACK, Style.DIM, str), end='')

    def print_conn_lost(self, str):
        print('%s%s%s%s%s' % (self.pos(self.MAXY / 12, 36), Fore.RED, Back.BLACK, Style.NORMAL, str), end='')

    def print_frontier_stat(self, stre):
        print('%s%s%s%s%s' % (self.pos(self.MAXY / 12, 115), Fore.GREEN, Back.BLACK, Style.NORMAL, stre + "  " + str(datetime.now().isoformat())), end='')
