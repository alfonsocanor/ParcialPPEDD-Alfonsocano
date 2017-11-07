#!/usr/bin/env python3
from flask import Flask, render_template, request, session, abort, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_bootstrap import Bootstrap
import csv
import re
import os

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'ThisissecretIFTS18'

class Login(FlaskForm):
    username = StringField('Usuario')
    password = PasswordField('Contraseña')

class References(FlaskForm):
    clientName = StringField('Nombre del cliente:')
    productname = StringField('Nombre del producto:')
    K = StringField('Número de ranking:') #CHANGE FOR A REAL VARIABLE NAME

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
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            X = csv.reader(X)
            for row in X:
                if row[self.client] == self.clientName:
                    aux = 1 #Conditional build for deploying a list if the name is exactly as in the DB
        if aux == 1: #If the name is exactly as in the DB
            with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
                X = csv.reader(X)
                list_ProductsPerClients = []
                for row in X:
                    if row[self.client] == self.clientName:
                        list_ProductsPerClients.append(row[self.product])
                    else:
                        pass
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
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            X = csv.reader(X)
            for row in X:
                if self.productname == row[self.product]:
                    aux = 1
        if aux == 1:
            with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
                X = csv.reader(X)
                list_clientsPerProduct = []
                for row in X:
                    if row[self.product] == self.productname and row[self.client] not in list_clientsPerProduct:
                        list_clientsPerProduct.append([row[self.product_id], row[self.client], row[self.quantity], row[self.price]])
            return list_clientsPerProduct
        else: #If the name is not the same and more than 3 characters are entered
            with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
                list_ProductsPerClients = []
                X = csv.reader(X)
                if len(self.productname) >= 3:
                    list_aux = ['search']
                    for row in X:
                        if self.productname in row[self.product]:
                            list_aux.append(row[self.product])
                    for i in list_aux:
                        if i not in list_ProductsPerClients:
                            if i == 'PRODUCTO':
                                pass
                            else:
                                list_ProductsPerClients.append(i)
            return list_ProductsPerClients

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
                    print(row[0])
                    print(row[1])
                    if login.username.data == row[1] and login.password.data == row[0]:
                        session['logged_in'] = True
                        return redirect('/')
            if login.password.data == None and login.username.data == None:
                X = False
            elif login.password.data == '' and login.username.data == '':
                X = False
            else:
                X = True
        return render_template('login.html', login=login, X=X, Y=Y)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/login')

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
        return render_template('productsPerClient.html', name=name, Y=Y, X=X, Z=Z, W=W)
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
        return render_template('clientsPerProducts.html', product=product, Y=Y, X=X, Z=Z, W=W)
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
