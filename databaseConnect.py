import sqlite3

def connectDB():
    con = sqlite3.connect('users.sqlite')
    cur = con.cursor()
    request = "SELECT * FROM sqlite_master where type='table';"
    tables = cur.execute(request).fetchall()
    # создание таблицы в базе данных если не была создана
    if not tables:
        requests = []
        requests.append("""CREATE TABLE users (
                            id           INTEGER UNIQUE
                                                 NOT NULL
                                                 PRIMARY KEY,
                            user_id      INTEGER NOT NULL,
                            nameV        STRING  NOT NULL,
                            discriptionV TEXT    NOT NULL,
                            linkV        STRING,
                            platno       INTEGER,
                            besplatno    INT,
                            cost         INTEGER,
                            otsrochka    BOOLEAN,
                            balls_user   INTEGER NOT NULL,
                            subjects     STRING  NOT NULL,
                            speciality   STRING
                        );""")
        cur.execute(requests[0])
        con.commit()

def writeDB(sqlRequest):
    con = sqlite3.connect('users.sqlite')
    cur = con.cursor()
    cur.execute(sqlRequest)
    con.commit()
def requestDB(id):
    con = sqlite3.connect('users.sqlite')
    cur = con.cursor()
    cur.execute(f"""SELECT * FROM users WHERE id = {id}""")
    return cur.fetchall()

connectDB()