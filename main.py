#!/usr/bin/env python3
from flask import Flask, render_template, request, session, abort, flash, redirect, sessions, Session, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_bootstrap import Bootstrap
import csv
import re
import os
from time import strftime

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'ThisissecretIFTS18'

class Login(FlaskForm):
    username = StringField('Usuario')
    password = PasswordField('Contraseña')
    passwordConfirmation = PasswordField('Confirmar Contraseña')

class References(FlaskForm):
    clientName = StringField('Nombre del cliente:')
    productname = StringField('Nombre del producto:')
    K = StringField('Número de ranking:') #CHANGE FOR A REAL VARIABLE NAME
    exportFile = SubmitField('Exportar')

class FileCheck():
    def __init__(self, fileName):
        self.fileName = fileName
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            pass

    def lenthRecord(self):
        self.lenthRecord = 0
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            X = csv.reader(X)
            rowcount = 0
            for row in X:
                rowcount += 1
                try:
                    if len(row) != 5:
                        raise ValueError()
                except ValueError:
                    self.lenthRecord = 1
                    return self.lenthRecord

    def orderFields(self):
        self.orderFields = 0
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            X = X.readline()
            X = X.replace('\n', '')
            X = X.split(',')
        try:
            for field in X:
                if field == 'CLIENTE':
                    self.client = X.index(field)
                elif field == 'CODIGO':
                    self.product_id = X.index(field)
                elif field == 'PRODUCTO':
                    self.product = X.index(field)
                elif field == 'CANTIDAD':
                    self.quantity = X.index(field)
                elif field == 'PRECIO':
                    self.price = X.index(field)
            return self.product, self.client, self.product_id, self.price, self.quantity #It returns a tupla
        except AttributeError:
            self.orderFields = 1
            return self.orderFields

    def productIdValue(self):
        self.productIdValue = 0
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            X = csv.reader(X)
            rowcount = 0
            for row in X:
                rowcount += 1
                try:
                    if row[self.product_id] == 'CODIGO':
                        pass
                    elif row[self.product_id] is '':
                        raise ValueError()
                except ValueError:
                    self.productIdValue = 1
                    return self.productIdValue

    def quantityValue(self):
        self.quantityValue = 0
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            X = csv.reader(X)
            rowcount = 0
            for row in X:
                rowcount += 1
                if row[self.quantity] == 'CANTIDAD':
                    pass
                else:
                    try:
                        row[self.quantity] = float(row[self.quantity]) #Transform the str value into float 
                        row[self.quantity] = str(row[self.quantity]) #Python let the . after base 10
                        Y = row[self.quantity].split('.') #Split the string in 2 numbers into a list. The second must be compared
                        Y[1] = int(Y[1]) # Transform the 2nd number (An integer)
                        if Y[1] is not 0: # Evaluate if it's an integer value or not. Different to 0?
                            raise ValueError()
                    except ValueError:
                        self.quantityValue = 1
                        return self.quantityValue

    def priceValue(self):
        self.priceValue = 0
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            X = csv.reader(X)
            rowcount = 0
            for row in X:
                rowcount += 1
                if row[self.price] == 'PRECIO':
                    pass
                else:
                    try:
                        row[self.price] = float(row[self.price]) #Transform the str value into float 
                        row[self.price] = str(row[self.price]) #Python let the . after base 10
                        Y = row[self.price].split('.') #Split the string in 2 numbers into a list. The second must be compared
                        Y[1] = int(Y[1]) # Transform the 2nd number (An integer)
                        if Y[1] is '': # Evaluation if it's a float value or not. If the split put a '', it was a int
                            raise ValueError()
                    except ValueError:
                        self.priceValue = 1
                        return self.priceValue

class GeneralConsults(FileCheck):
    def __init__(self, fileName):
        super().__init__(fileName)
    def productsPerClient(self, clientName):
        aux = 0
        self.clientName = clientName
        W = FileCheck(self.fileName) #Random variable name
        T = W.orderFields() #Random variable name
        self.product = T[0]
        self.client = T[1]
        self.product_id = T[2]
        self.price = T[3]
        self.quantity = T[4]
        totalPrice = 0
        totalQuantity = 0
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            X = csv.reader(X)
            for row in X:
                if row[self.client] == self.clientName:
                    aux = 1 #Conditional build for deploying a list if the name is exactly as in the DB
        if aux == 1: #If the name is exactly as in the DB
            list_ProductsPerClients = []
            list_ProductsPerClients_Aux = [] #Used as the first pivot to put the csv data into a list
            list_ProductsPerClients_Aux2 = [] #Used as the second pivot to return unique values
            with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
                X = csv.reader(X)
                for row in X:
                    if row[self.client] == self.clientName:
                        if row[self.product] not in list_ProductsPerClients_Aux:
                            list_ProductsPerClients_Aux.append([row[self.product_id], row[self.product]])
                i = 0
                L = len(list_ProductsPerClients_Aux)
                while i < L:
                    with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
                        X = csv.reader(X)
                        for row in X:
                            if row[self.client] == self.clientName and row[self.product] == list_ProductsPerClients_Aux[i][1]:
                                totalQuantity = totalQuantity + float(row[self.quantity])
                                totalPrice = totalPrice + float(row[self.price])
                    list_ProductsPerClients_Aux2.append([list_ProductsPerClients_Aux[i][0], list_ProductsPerClients_Aux[i][1], round(totalQuantity, 2), round(totalPrice, 2)])
                    i += 1
                    totalPrice = 0
                    totalQuantity = 0
                for j in list_ProductsPerClients_Aux2: #List Aux 2 used for let just 1 value per product per client
                    if j not in list_ProductsPerClients:
                        list_ProductsPerClients.append(j)
            return list_ProductsPerClients
        else: #If the name is not the same and more than 3 characters are entered
            with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
                list_ProductsPerClients = []
                X = csv.reader(X)
                if len(self.clientName) >= 3:
                    list_aux = ['search']
                    for row in X:
                        if self.clientName in row[self.client]:
                            list_aux.append(row[self.client])
                    for i in list_aux:
                        if i not in list_ProductsPerClients:
                            if i == 'CLIENTE':
                                pass
                            else:
                                list_ProductsPerClients.append(i)
            return list_ProductsPerClients

    def clientsPerProduct(self, productname):
        aux = 0
        self.productname = productname
        H = FileCheck(self.fileName) #Random variable name
        T = H.orderFields() #Random variable name
        self.product = T[0] #value return from a tupla / method orderFields
        self.client = T[1] #value return from a tupla / method orderFields
        self.product_id = T[2] #value return from a tupla / method orderFields
        self.price = T[3]
        self.quantity = T[4]
        totalPrice = 0
        totalQuantity = 0
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            X = csv.reader(X)
            for row in X:
                if self.productname == row[self.product]:
                    aux = 1
        if aux == 1: #If the name is exactly as in the DB
            list_clientsPerProduct = []
            list_clientsPerProduct_Aux = []
            list_clientsPerProduct_Aux2 = []
            with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
                X = csv.reader(X)
                for row in X:
                    if row[self.product] == self.productname and row[self.client] not in list_clientsPerProduct_Aux:
                        list_clientsPerProduct_Aux.append([row[self.product_id], row[self.client], row[self.quantity], row[self.price]])
            L = len(list_clientsPerProduct_Aux)
            i = 0
            while i < L:
                for j in list_clientsPerProduct_Aux:
                    if list_clientsPerProduct_Aux[i][1] == j[1]:
                        totalQuantity = totalQuantity + float(j[2])
                        totalPrice = totalPrice + float(j[3])
                list_clientsPerProduct_Aux2.append([list_clientsPerProduct_Aux[i][0], list_clientsPerProduct_Aux[i][1], round(totalQuantity, 2), round(totalPrice, 2)])
                i += 1
                totalPrice = 0
                totalQuantity = 0
            for j in list_clientsPerProduct_Aux2: #List Aux 2 used for let just 1 value per product per client
                if j not in list_clientsPerProduct:
                    list_clientsPerProduct.append(j)
            return list_clientsPerProduct
        else: #If the name is not the same and more than 3 characters are entered
            with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
                list_clientsPerProduct = []
                X = csv.reader(X)
                if len(self.productname) >= 3:
                    list_aux = ['search']
                    for row in X:
                        if self.productname in row[self.product]:
                            list_aux.append(row[self.product])
                    for i in list_aux:
                        if i not in list_clientsPerProduct:
                            if i == 'PRODUCTO':
                                pass
                            else:
                                list_clientsPerProduct.append(i)
            list_clientsPerProduct_Aux = list_clientsPerProduct
            list_clientsPerProduct = []
            for j in list_clientsPerProduct_Aux: #List Aux 2 used for let just 1 value per product per client
                    if j not in list_clientsPerProduct:
                        list_clientsPerProduct.append(j)
            return list_clientsPerProduct

    def n_MostSelledProducts(self, K):
        self.K = K
        try:
            K = int(K)
        except TypeError:
            K = 0
        except ValueError:
            K = 0
        H = FileCheck(self.fileName) #Random variable name just used in this method
        T = H.orderFields() #Random variable name just used in this method
        self.product = T[0] #value returned from a tupla / method orderFields from class FileCheck
        self.client = T[1] #value returned from a tupla / method orderFields from class FileCheck
        self.product_id = T[2] #value returned from a tupla / method orderFields from class FileCheck
        self.quantity = T[4]
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            X = csv.reader(X)
            list_RackingMostSelledProducts = []
            list_aux = []
            for row in X:
                list_aux.append(row[self.product_id])
            for i in list_aux:
                if i not in list_RackingMostSelledProducts:
                    if i == 'CODIGO':
                        pass
                    else:
                        list_RackingMostSelledProducts.append(i)
        u = len(list_RackingMostSelledProducts)
        dictMax = {}
        auxList = []
        c = 0
        while c < u: #The auxList is built for creating lists into it and used them to save the quantities selled per products
            auxList.append([])
            c += 1
        c = 0
        while c < u:
            with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
                X = csv.reader(X)
                for row in X:
                    if row[self.product_id] == list_RackingMostSelledProducts[c]:
                        quantityInt = row[self.quantity].split('.') #slipt quantity value and use the index 0 as an int
                        auxList[c].append(int(quantityInt[0]))
                    else:
                        pass
            Key = list_RackingMostSelledProducts[c]
            dictMax[Key] = auxList[c]
            c += 1
        max = 0
        n = 1
        maxList = []
        if int(self.K) >= u: #It limits the racking to the lenth of the csv products single value
            self.K = u
        while n <= int(self.K):
            for i in dictMax:
                X = sum(dictMax[i])
                if X > max:
                    max = X
                    maxKey = i
                else:
                    max = max
            del dictMax[maxKey]
            with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
                X = csv.reader(X)
                for row in X:
                    if row[self.product_id] == maxKey:
                        P = row[self.product] #Product description is P
            maxList.append([n, maxKey, P, max])
            max = 0
            n += 1
        return maxList

    def n_ClientsExpendedMoreMoney(self, K):
        self.K = K
        try:
            K = int(K)
        except TypeError:
            K = 0
        except ValueError:
            K = 0
        H = FileCheck(self.fileName) #Random variable name just used in this method
        T = H.orderFields() #Random variable name just used in this method
        self.product = T[0] #value returned from a tupla / method orderFields from class FileCheck
        self.client = T[1] #value returned from a tupla / method orderFields from class FileCheck
        self.product_id = T[2] #value returned from a tupla / method orderFields from class FileCheck
        self.price = T[3]
        with open(os.path.join(os.path.dirname(__file__), self.fileName )) as X:
            X = csv.reader(X)
            list_ClientsExpendedMoreMoney = []
            list_aux = []
            for row in X:
                list_aux.append(row[self.client])
            for i in list_aux:
                if i not in list_ClientsExpendedMoreMoney:
                    if i == 'CLIENTE':
                        pass
                    else:
                        list_ClientsExpendedMoreMoney.append(i)
        u = len(list_ClientsExpendedMoreMoney)
        dictMax = {}
        auxList = []
        c = 0
        while c < u: #The auxList is built for creating lists into it and used them to save the clients whom expended more money
            auxList.append([])
            c += 1
        c = 0
        while c < u:
            with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
                X = csv.reader(X)
                for row in X:
                    if row[self.client] == list_ClientsExpendedMoreMoney[c]:
                        auxList[c].append(float(row[self.price]))
                    else:
                        pass
            Key = list_ClientsExpendedMoreMoney[c]
            dictMax[Key] = auxList[c]
            c += 1
        max = 0
        n = 1
        maxList = []
        maxKey = 'First'
        if int(self.K) >= u:
            self.K = u
        while n <= int(self.K):
            for i in dictMax:
                X = sum(dictMax[i])
                if X > max:
                    max = X
                    maxKey = i
                else:
                    max = max
            maxList.append([n, maxKey, round(max, 2)])
            del dictMax[maxKey]
            max = 0
            n += 1
        return maxList
        

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('/home.html')
    else:
        return render_template('/home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    Y = False
    X = False
    if session.get('logged_in'):
        return redirect('/')
    else:
        try:
            filecheck = FileCheck('db.csv')
            filecheck.orderFields()
            filecheck.productIdValue()
            filecheck.quantityValue()
            filecheck.priceValue()
        except:
            Y = True
        login = Login()
        if login.validate_on_submit():
            X = False
            with open(os.path.join(os.path.dirname(__file__), 'users.csv')) as X:
                X = csv.reader(X)
                for row in X:
                    if login.username.data == row[0] and login.password.data == row[1]:
                        session['username'] = login.username.data
                        session['password'] = login.password.data
                        session['logged_in'] = True
                        return redirect('/')
            if login.password.data == None and login.username.data == None:
                X = False
            elif login.password.data == '' and login.username.data == '':
                X = False
            else:
                X = True
        return render_template('login.html', login=login, X=X, Y=Y)

@app.route("/createaccount", methods=['GET', 'POST'])
def createAccount():
    account = Login()
    W = False #Variable used for activate some validators html from render_template has
    Y = False #Variable used for activate some validators html from render_template has
    Z = False #Variable used for activate some validators html from render_template has
    if session.get('logged_in'):
        return redirect('/')
    else:
        if account.validate_on_submit():
            with open(os.path.join(os.path.dirname(__file__), 'users.csv')) as X:
                X = csv.reader(X)
                for row in X:
                    if row[0] == account.username.data and (account.password.data == '' or account.passwordConfirmation.data == ''):
                        W = True
                        return render_template('createaccounts.html', account=account, W=W)
                    if (row[0] != account.username.data and account.username.data != '') and (account.password.data == '' or account.passwordConfirmation.data == ''):
                        Y = True
                        return render_template('createaccounts.html', account=account, Y=Y)
                    if (row[0] != account.username.data and account.username.data != '') and (account.password.data != account.passwordConfirmation.data):
                        Z = True
                        return render_template('createaccounts.html', account=account, Z=Z)
                    if (account.username.data != '' and account.password.data == '' and account.passwordConfirmation.data == '') or (X == False or Y == False or Z == False):
                        with open(os.path.join(os.path.dirname(__file__), 'users.csv'), 'a',newline='') as X:
                            X = csv.writer(X, delimiter=',')
                            X.writerow([account.username.data, account.password.data])
                        return redirect ('/login')
        return render_template('createaccounts.html', account=account, W=W, Y=Y, Z=Z)

@app.route("/passwordchange", methods=['GET', 'POST'])
def passwordChange():
    passwordChange = Login()
    W = False #Variable used for activate some validators html from render_template has
    Y = False #Variable used for activate some validators html from render_template has
    Z = False #Variable used for activate some validators html from render_template has
    if passwordChange.validate_on_submit():
        if passwordChange.password.data == '' or passwordChange.passwordConfirmation.data == '':
            Y = True
            return render_template('passwordchange.html', passwordChange=passwordChange, Y=Y)
        if passwordChange.password.data != passwordChange.passwordConfirmation.data:
            W = True
            return render_template('passwordchange.html', passwordChange=passwordChange, W=W)
        if passwordChange.password.data == session['password']:
            Z = True
            return render_template('passwordchange.html', passwordChange=passwordChange, Z=Z) 
        with open(os.path.join(os.path.dirname(__file__), 'users.csv'), 'r') as X, open(os.path.join(os.path.dirname(__file__), 'users_backup.csv'), 'w') as Y:
            X = csv.reader(X)
            Y = csv.writer(Y)
            for row in X:
                print(row)
                print(session['username'])
                if row[0] == session['username']:
                    Y.writerow([row[0], passwordChange.password.data])
                else:
                    Y.writerow([row[0], row[1]])
                print(row)
        os.rename((os.path.join(os.path.dirname(__file__), 'users_backup.csv')), (os.path.join(os.path.dirname(__file__), 'users.csv')))
        return redirect('/')
        
    return render_template('/passwordchange.html', passwordChange=passwordChange)

@app.route("/profile")
def profile():
    if session['logged_in'] == False:
        return redirect('/')
    else:
        return render_template('profile.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/')

@app.route('/productsperclient', methods=['GET', 'POST'])
def productsPerClient():
    if session.get('logged_in'):
        name = References()
        X = False
        Y = []
        Z = True
        W = False
        if name.clientName.data == '':
            Z = False
        if name.validate_on_submit():
            W = False
            Z = True
            X = True
            gc = GeneralConsults('db.csv')
            Y = gc.productsPerClient(name.clientName.data)
            if Y == [] or (len(Y) == 1 and Y[0] == 'search'):
                Z = False
                name.clientName.data = ''
            elif Y[0] == 'search':
                W = True
                Y.remove('search')
            if name.exportFile.data:
                T = strftime("%Y%m%d_%H%M%S")
                print(T)
                with open(os.path.join(os.path.dirname(__file__), 'resultados_'+T+'.csv'), 'a') as X:
                    X = csv.writer(X, delimiter=',')
                    for i in Y:
                        X.writerow([name.clientName.data, i[0], i[1], i[2], i[3]])
                return send_file(os.path.join(os.path.dirname(__file__), 'resultados_'+T+'.csv'), attachment_filename='resultados_'+T+'.csv', as_attachment=True)
        return render_template('productsperclient.html', name=name, Y=Y, X=X, Z=Z, W=W)
    else:
        return redirect ('/login')

@app.route('/clientsperproduct', methods=['GET', 'POST'])
def clientsPerProduct():
    if session.get('logged_in'):
        product = References()
        X = False
        Y = []
        Z = True
        W = False
        if product.productname.data == '':
            Z = False
        if product.validate_on_submit():
            W = False
            Z = True
            X = True
            gc = GeneralConsults('db.csv')
            Y = gc.clientsPerProduct(product.productname.data)
            if Y == [] or (len(Y) == 1 and Y[0] == 'search'):
                Z = False
                product.productname.data = ''
            elif Y[0] == 'search':
                W = True
                Y.remove('search')
        print(Y)
        return render_template('clientsperproducts.html', product=product, Y=Y, X=X, Z=Z, W=W)
    else:
        return redirect('/login')

@app.route('/clientsexpendedmoremoney', methods=['GET', 'POST'])
def clientsExpendedMoreMoney():
    if session.get('logged_in'):
        ranking = References()
        X = False
        Y = []
        Z = True #varible used to hide table if the value is not correct or empty
        try:
            aux = ranking.K.data
            aux = int(aux)
        except TypeError:
            ranking.K.data = ''
            Z = False
        except ValueError:
            ranking.K.data = ''
            Z = False
        if ranking.validate_on_submit():
            if ranking.K.data == '':
                ranking.K.data = 0
            X = True
            gc = GeneralConsults('db.csv')
            Y = gc.n_ClientsExpendedMoreMoney(ranking.K.data)
            if ranking.K.data == 0:
                ranking.K.data = ''
        return render_template('clientsexpendedmoremoney.html', ranking=ranking, Y=Y, X=X, Z=Z)
    else:
        return redirect('/login')

@app.route('/mostselledproducts', methods=['GET', 'POST'])
def mostSelledProducts():
    if session.get('logged_in'):
        ranking = References()
        X = False
        Y = []
        Z = True #varible used to hide table if the value enter is not correct or empty
        try:
            aux = ranking.K.data
            aux = int(aux)
        except TypeError:
            ranking.K.data = ''
            Z = False
        except ValueError:
            ranking.K.data = ''
            Z = False
        if ranking.validate_on_submit():
            if ranking.K.data == '':
                ranking.K.data = 0
            X = True
            gc = GeneralConsults('db.csv')
            Y = gc.n_MostSelledProducts(ranking.K.data)
            if ranking.K.data == 0:
                ranking.K.data = ''
        return render_template('mostselledproducts.html', ranking=ranking, Y=Y, X=X, Z=Z)
    else:
        return redirect('/login')

@app.errorhandler(404)
def not_found_error(error):
    X = True
    return render_template('/error.html', X=X)

@app.errorhandler(500)
def not_found_error(error):
    Y = True
    return render_template('/error.html', Y=Y)

if __name__ == '__main__':
    app.run(debug=True)
