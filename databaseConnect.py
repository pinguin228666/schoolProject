import sqlite3


def connectDB():
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    request = "SELECT * FROM sqlite_master where type='table';"
    tables = cur.execute(request).fetchall()
    #linkV, vbesplatno, platno, cost, otsrochka, balls_user, subjects
    if not tables:
        requests = []
        requests.append("""CREATE TABLE users (
                            user_id      INTEGER PRIMARY KEY
                                                 UNIQUE
                                                 NOT NULL,
                            nameV        STRING  NOT NULL
                                                 UNIQUE,
                            discriptionV TEXT    NOT NULL,
                            linkV        STRING,
                            besplatno    INT,
                            platno       INTEGER,
                            cost         INTEGER,
                            otsrochka    BOOLEAN,
                            balls_user   INTEGER NOT NULL,
                            subjects     STRING  NOT NULL
                    );""")
        cur.execute(requests[0])
        con.commit()


def writeDB(sqlRequest):
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    cur.execute(sqlRequest)
    con.commit()

connectDB()