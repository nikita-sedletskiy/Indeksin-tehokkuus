
import sqlite3
from random import randint
from random import choices
from string import ascii_uppercase
from string import digits
from time import perf_counter 
import os

class Main:
    """
    Main class, uses as arguments (filename:str, tablename:str).
    """
    def __init__(self, filename:str, tablename:str):
        self.__filename = filename
        self.__tablename = tablename
        self.__Main()

    def __Main(self):
         while True:
            if os.path.isfile(self.__filename):
                os.remove(self.__filename)
            self.__db = DB(self.__filename,self.__tablename)
            command = int(input('Choose test (1,2,3) or exit 4: '))
            if command == 1:
                self.__db._test(command)
            if command == 2:
                self.__db._test(command)
            if command == 3:
                self.__db._test(command)
            if command == 4:
                q = input('Save last DB? Y/n ')
                if q == 'n' or q == 'N':
                    os.remove(self.__filename)
                break

class DB:
    """
    DB class, use as args (filename:str, tablename:str), have some functions to play with.
    """

    def __init__(self,filename:str,tablename:str):
        self._x = 1000000 # how many rows to create
        self._y = 1000 # how many requests to make
        self._filename = filename
        self.__tablename = tablename
        self.__db = sqlite3.connect(self._filename)
        self.__db.isolation_level = None

    def _test(self,t):
        #¤ Available functions to test ¤
        #self.__create_table()
        #self._insert_tables()
        #self._insert_tables_py()
        #self._insert_tables_slow()
        #self._create_index('idx_elokuvat','vuosi')
        #self._request_film_count()
        #self._request_film_count_py()

        self.__create_table()
        if t == 2:
            self._create_index('idx_elokuvat','vuosi')
        insert_start = perf_counter()
        self._insert_tables()
        insert_stop = perf_counter()
        if t == 3:
            self._create_index('idx_elokuvat','vuosi')
        filmcounter_start = perf_counter()
        self._request_film_count_py()
        filmcounter_stop = perf_counter()
        print("Elapsed time during INSERT TABLE:", insert_stop-insert_start)  
        print("Elapsed time during counter request:", filmcounter_stop-filmcounter_start)
        print ("File size: "+'{:,.0f}'.format(os.path.getsize(self._filename)/float(1<<20))+" MB")

    def _request_film_count(self): #290 sec
        self.__db.execute("BEGIN")
        cmd = "SELECT COUNT(*) FROM Elokuvat GROUP BY vuosi = (ABS(RANDOM()) % (2000 - 1900) + 1900) LIMIT 1 OFFSET 1"
        for i in range(1,self._y+1):
            self.__db.execute(cmd)
        self.__db.execute("COMMIT")


    def _request_film_count_py(self): #37.62 sec, much better performance with pythons random fuction than sqls
        self.__db.execute("BEGIN")
        for i in range(1,self._y+1):
            self.__db.execute('SELECT COUNT(*) FROM Elokuvat WHERE vuosi = ?',[randint(1900,2000)])
        self.__db.execute("COMMIT")

    def _insert_tables_py(self): #4.26 sec , slower than sql req
        self.__db.execute("BEGIN")
        cmd = 'INSERT INTO '+self.__tablename
        for i in range(1,self._x+1):
            self.__db.execute(cmd + '(nimi, vuosi) VALUES (?,?)',[''.join(choices(ascii_uppercase + digits, k=6)),randint(1900,2000)])
        self.__db.execute("COMMIT")

    def _insert_tables(self): #2.87 sec
        self.__db.execute("BEGIN")
        cmd = "INSERT INTO "+self.__tablename+" (nimi, vuosi) VALUES ( CHAR((ABS(RANDOM()) % (65 - 90) + 65)) || CHAR((ABS(RANDOM()) % (65 - 90) + 65)) || CHAR((ABS(RANDOM()) % (65 - 90) + 65)) || CHAR((ABS(RANDOM()) % (65 - 90) + 65)) || CHAR((ABS(RANDOM()) % (65 - 90) + 65)), (ABS(RANDOM()) % (2000 - 1900) + 1900))"
        for i in range(1,self._x+1):
            self.__db.execute(cmd)
        self.__db.execute("COMMIT")

    def _insert_tables_slow(self): #17.04 sec
        cmdstr = 'INSERT INTO '+self.__tablename+' (nimi, vuosi) VALUES ( CHAR((ABS(RANDOM()) % (65 - 90) + 65)) || CHAR((ABS(RANDOM()) % (65 - 90) + 65)) || CHAR((ABS(RANDOM()) % (65 - 90) + 65)) || CHAR((ABS(RANDOM()) % (65 - 90) + 65)) || CHAR((ABS(RANDOM()) % (65 - 90) + 65)), (ABS(RANDOM()) % (2000 - 1900) + 1900) );'
        cmd = 'BEGIN;'
        cmd += cmdstr * self._x
        cmd += 'COMMIT;'
        self.__db.executescript(cmd).fetchall()    
    


    def _create_index(self, index:str, props:str):
        try:
            cmd = 'CREATE INDEX '+index+' ON '+self.__tablename+' ('+props+');'
            self.__db.execute(cmd).fetchall()
            return True
        except Exception as e:
            return False

    def _drop_index(self, index:str):
        try:
            cmd = 'DROP INDEX [IF EXISTS] '+index+';'
            self.__db.execute(cmd).fetchall()
            return True
        except Exception as e:
            return False

    def __create_table(self):
        try:
            cmd = 'CREATE TABLE '+self.__tablename+' (id INTEGER PRIMARY KEY, nimi TEXT, vuosi INTEGNER)'
            self.__db.execute(cmd).fetchall()
            return True
        except Exception as e:
            return False

    def __remove_table(self):
        try:
            cmd = 'DROP TABLE IF EXISTS ' + self.__tablename
            self.__db.execute(cmd).fetchall()
            return True
        except Exception as e:
            print(e)
            return False



db = Main('elokuvat.db','Elokuvat')

