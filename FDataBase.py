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

    def getContact(self):
        get_contact = '''SELECT * FROM contact'''
        try:
            self.__cur.execute(get_contact)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка добавления статьи в БД")
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

    #отображение продукта
    def getProduct(self, alias):
        try:
            self.__cur.execute(f"SELECT title_product, body_product FROM product WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("ошибка получения продукта из БД"+str(e))

        return (False, False)

    #отображение всех новостей
    def getNewsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, full_text FROM news")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("ошибка получения статьи из БД"+str(e))

        return[]

#добавление блока администрирование
    def getAdminPanel(self):
        admin_panel = '''SELECT * FROM adminpanel'''
        try:
            self.__cur.execute(admin_panel)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("ошибка чтения бд")
        return []

#добавление продукта
    def addproduct(self, title_product, body_product, url):
        try:
            #проверка на уникальность URL продукта
            self.__cur.execute(f"SELECT COUNT() as `count` FROM product WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] >0:
                print("продукт с таким url уже есть")
                return False


            self.__cur.execute("INSERT INTO product VALUES(NULL, ?, ?, ?)", (title_product, url, body_product))
            #commit() сохраняет новые данные в базе данных
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления продукта в БД"+str(e))
            return False

        return True

#отображение всех продуктов
    def getProductsAll(self):
        try:
            self.__cur.execute(f"SELECT id, title_product, url, body_product FROM product")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("ошибка получения продуктов из БД"+str(e))

        return[]

### ДОБАВЛЕНИЕ НОВОГО ЮЗЕРА
    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (name, email, hpsw))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД"+str(e))
            return False

        return True

    
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из ДБ"+str(e))
        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("ошибка получения данных из БД"+str(e))

        return False
