class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    #добавление блока меню
    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("ошибка чтения бд")
        return []

    #добавление новости
    def createpost(self, title, full_text):
        try:
            #для округления из милисекунд используем math.floor
           
            self.__cur.execute("INSERT INTO news VALUES(NULL, ?, ?)", (title, full_text))
            #commit() сохраняет новые данные в базе данных
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД"+str(e))
            return False

        return True

    #отображение новости
    def getNew(self, newId):
        try:
            self.__cur.execute(f"SELECT title, full_text FROM news WHERE id = {newId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("ошибка получения статьи из БД"+str(e))

        return (False, False)

    def getContact(self, contact_text):
        try:
            self.__cur.execute("INSERT INTO contact VALUES(NULL, ?)", (contact_text))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД"+str(e))
            return False
        return True 

    #отображение всех новостей
    def getNewsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, full_text FROM news")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("ошибка получения статьи из БД"+str(e))

        return[]
