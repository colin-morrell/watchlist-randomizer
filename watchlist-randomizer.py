import sys
import csv
import random
import requests

class Title:

    def __init__(self, row):
        self.title = row[5].decode('utf-8')
        self.rating = row[8]
        self.year = row[10]
        self.genres = [g.upper() for g in row[11].split(',')]
        self.director = row[14].decode('utf-8')


    def toString(self):
        print '[+] %s (%s) %s%s\tdir. %s' % (self.title, self.year, self.rating, u'\u2606',
                                        self.director)


def banner():

    print """
                   _ _ _ ____ ___ ____ _  _ _    _ ____ ___ 
                   | | | |__|  |  |    |__| |    | [__   |  
                   |_|_| |  |  |  |___ |  | |___ | ___]  |  
                                                            
                ____ ____ _  _ ___  ____ _  _ _ ___  ____ ____ 
                |__/ |__| |\ | |  \ |  | |\/| |   /  |___ |__/ 
                |  \ |  | | \| |__/ |__| |  | |  /__ |___ |  \  [ v1.0 ]\n"""


def getRandom(l):
    return random.choice(l)


def getGenre(genres_dict):

    genre = raw_input('[?] What genre are you in the mood for?\n\t-> ').upper()
    help_terms = ['?', 'IDK', 'HELP']

    if genre in help_terms:
        print '\n'
        print '[!] VIEW...........view available genres'
        print '[!] HELP...........see this help info'
        print '[!] RANDOM.........select from random genre'
        print '\n'
        getGenre(genres_dict)
    if 'VIEW' in genre:
        print '[!] Available genres:'
        for key in genres_dict:
            print key
        getGenre(genres_dict)
    elif 'RANDOM' in genre:
        getRandom(genres_dict[getRandom(genres_dict.keys())]).toString()
        sys.exit()
    else:
        if genre in genres_dict:
            getRandom(genres_dict[genre]).toString()
            sys.exit()
        else:
            print '[!] Genre not found. To view genres, type VIEW'
            getGenre(genres_dict)


def getWatchListFromURL(url, genres_dict):

    r = requests.get(url, stream=True)
    rtext = r.text.encode('utf-8').split('\n')
    mycsv = csv.reader(rtext, delimiter=',')

    for row in mycsv:
        if row and 'Position' not in row[0]:
            t = Title(row)
            for g in t.genres:
                g = g.strip()
                if g in genres_dict:
                    genres_dict[g].append(t)
                else:
                    genres_dict[g] = [t]


def main():

    if len(sys.argv) < 2:
        print '[!] Usage: python %s [imdb_watchlist_url]' % sys.argv[0]
        sys.exit()

    banner()
    
    genres_dict = {}
    watchlist_url = sys.argv[1]

    getWatchListFromURL(watchlist_url, genres_dict)

    getGenre(genres_dict)
  

if __name__ == '__main__':
    main()
