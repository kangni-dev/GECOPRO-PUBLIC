from flask import Flask, render_template, request
import pymysql, pymysql.cursors
import mysql.connector
import os


app = Flask(__name__)
ProfileUtilisateur = {}
class DBManagerDev:
    def __init__(self, database='gecodb', host="localhost", user="root"):

        self.connection = mysql.connector.connect(
            user=user,
            password = 'toula666',
            host=host,  # name of the mysql service as set in the docker compose file
            database=database,
            auth_plugin='mysql_native_password'
        )

        self.cursor = self.connection.cursor()

    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS users')
        self.cursor.execute('CREATE TABLE users (email varchar(50), password varchar(12), name varchar(20), avatar varchar(40))')
        self.cursor.executemany('INSERT INTO users (email, password,name,avatar) VALUES (%s, %s,%s,%s);',
                                [('kafog@ulaval.ca','12345','kangni', 'MonChat.jpg')])
        self.connection.commit()

    def query_users(self):
        self.cursor.execute('SELECT name FROM users')
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec


class DBManager:
    def __init__(self, database='gecodb', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user,
            password=pf.read(),
            host=host,  # name of the mysql service as set in the docker compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()

    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS users')
        self.cursor.execute('CREATE TABLE users (email varchar(50), password varchar(12), name varchar(20), avatar varchar(40))')
        self.cursor.executemany('INSERT INTO users (email, password,name,avatar) VALUES (%s, %s,%s,%s);',
                                [('kafog@ulaval.ca','12345','kangni', 'MonChat.jpg')])
        self.connection.commit()

    def query_users(self):
        self.cursor.execute('SELECT name FROM users')
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec

@app.route("/")
def main():
    return render_template('login.html')
 


conn = None


@app.route("/login", methods=['POST'])
def login():
    global conn
    if not conn:
        if(os.getenv('APP_ENV')=='PROD'):
            conn = DBManager(password_file='/run/secrets/db-password')
        else:
            conn =DBManagerDev()

        conn.populate_db()
    courriel = '"' + request.form.get('courriel') + '"'
    passe = request.form.get('motpasse')


    cmd = 'SELECT password FROM users WHERE email=' + courriel + ';'

    conn.cursor.execute(cmd)
    rec = []
    for c in conn.cursor:
        rec.append(c[0])
    newPass =rec[0]

    if (rec != None) and (passe == newPass):
        cmd = 'SELECT * FROM users WHERE email=' + courriel + ';'
        info = conn.cursor.execute(cmd)
        userInfo=[]
        for c in conn.cursor:
            userInfo.append(c)

        global ProfileUtilisateur
        ProfileUtilisateur["courriel"] = courriel
        ProfileUtilisateur["nom"] = userInfo[0][2]
        ProfileUtilisateur["avatar"] = userInfo[0][3]
        return render_template('bienvenu.html', profile=ProfileUtilisateur)

    return render_template('login.html', message=newPass)





if __name__ == "__main__":
    app.run()


