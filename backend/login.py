import re

from flask import Flask, render_template, request, session, redirect, url_for
import pymysql, pymysql.cursors
import mysql.connector
import os
import datetime
from flask import request


app = Flask(__name__)

app.secret_key = 'my_secret_key'
ProfileUtilisateur = {}
msg = ""
url = "main"
connectionAction = "Se connecter"
dbConnection = None

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
    url="main"
    connectionAction="Se connecter"


    return render_template('login.html',url=url,connection = connectionAction)
 

msg = ""
url = "main"
connectionAction = "Se connecter"
def setConnectedPage():
    msg = 'Vous etes connectés '
    url = "logout"
    connectionAction = "Se deconnecter"

def getConn():
    conn = None


    if not conn:
        if (os.getenv('APP_ENV') == 'PROD'):
            conn = DBManager(password_file='/run/secrets/db-password')
        else:
            conn = DBManagerDev()
    return conn


@app.route("/login", methods=['POST'])
def login():
    global dbConnection
    dbConnection = getConn()
    msg = ''

    if request.method == 'POST' and 'courriel' in request.form and 'motpasse' in request.form:
        getConn().populate_db()
        userEmail = '"'+request.form.get('courriel')+'"'
        password = request.form.get('motpasse')
        userNamne=""
        cmd = 'SELECT password FROM users WHERE email=' + userEmail + ';'
        dbConnection.cursor.execute(cmd)
        userPasswordsRecords = []
        for record in dbConnection.cursor:
            userPasswordsRecords.append(record[0])


        if (userPasswordsRecords != None) and (password == userPasswordsRecords[0]):
            cmd = 'SELECT * FROM users WHERE email=' + userEmail + ';'
            dbConnection.cursor.execute(cmd)
            userRecords = []
            for record in dbConnection.cursor:
                userRecords.append(record)

        if userRecords:
            session['loggedin'] = True
            session['email'] = userEmail
            #session['username'] = account['username']
            username = userRecords[0][3]
            msg = 'Vous etes connectés '
            url = "logout"
            connectionAction = "Se deconnecter"
            return render_template('bienvenu.html', loginMsg=msg,user=username,url = url,connection=connectionAction)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', loginMsg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)


    return redirect(url_for('main'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    roleRecords=[]
    cmd = 'SELECT id_role FROM Roles;'
    dbConnection.cursor.execute(cmd)
    for record in dbConnection.cursor:
        roleRecords.append(record[0])

    if request.method == 'POST'and 'firstname' in request.form and 'username' in request.form and \
             'password' in request.form and 'email' in request.form and \
             'city' in request.form and 'country' in request.form:
        firstname = request.form['firstname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        noCivique = request.form['noCivique']
        city = request.form['city']
        phone = request.form['phone']
        rue = request.form['rue']
        userRole = request.form['userRole']

        country = request.form['country']
        #dbConnection.cursor.execute('INSERT INTO Utilisateurs VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)', (username, firstname, email, phone, role, password, noCivique,rue,city,country ))

        dbConnection.cursor.execute('SELECT courriel_utilisateur FROM Utilisateurs WHERE courriel_utilisateur = %s',(email,))
        emailRecords = []
        for record in dbConnection.cursor:
             emailRecords.append(record[0])

        if emailRecords:
             msg = "L'utilsateur existe déjà"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "l'adresse est invalide !"
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'le nom ne doit contenir que des lettres et des chiffres'
        else:
            dbConnection.cursor.execute('INSERT INTO Utilisateurs(nom_utilisateur,prenom_utilisateur,'
                                        'courriel_utilisateur,telephone_utilisateur,role_utilisateur,'
                                        'mot_de_passe,no_civique,rue,ville,pays)VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)',
                                        (username, firstname, email, phone, userRole,
                                         password, noCivique,rue,city,country ))
            dbConnection.connection.commit()
            msg = 'Vous etes bien enregistés'

    elif request.method == 'POST':
        msg = 'Remplir le formulaire'
    return render_template('register.html', msg = msg,url=url,connection = connectionAction,roles=roleRecords)





@app.route("/utilisateurs")
def ajouter_utilisateur():
    return render_template('utilisateurs.html')
@app.route("/roles/ajouter",methods=['POST','GET'])
def role():
    if request.method == 'POST':


        getConn().cursor.execute('INSERT INTO Roles(id_role,nom_role,desc_role) VALUES(%s,%s,%s);',(request.form['userRoleId'], request.form['userRoleName'],
                                                              request.form['userRoleDesc']))
        getConn().connection.commit()
        return render_template('add_role.html',msg = msg,url=url,connection = connectionAction)
    if request.method == 'GET':

        return render_template('add_role.html',msg = msg,url=url,connection = connectionAction)


@app.route("/roles")
def listRole():
    return render_template("roles.html",msg = msg,url=url,connection = connectionAction)
@app.route("/accueil")
def home():

    return render_template('about.html',msg = msg,url=url,connection = connectionAction)


if __name__ == "__main__":
    app.run()


