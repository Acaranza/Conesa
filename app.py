#!/usr/bin/env python
import csv
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap

from forms import LoginForm, SaludarForm, RegistrarForm, NuevoClienteForm

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'

@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())

@app.route('/clientes', methods=['GET', 'POST'])
def generar_tabla_clientes():
    csv     = open("./DB/clientes.csv",  "r", encoding="utf-8") #Abrir archivo csv 
    doc     = csv.read()  # Devuelve un string que es el contenido del archivo
    csv.close() #Libera el rchivo para lectura y escritura
    lines   = doc.split("\n")  #Divide el string segun el separador (barra n es salto de linea)
	# Llenar variables para enviar al html
    fields  = lines[0].split(",") #Divde la primer linea del string con comas. Es para extreaer  el encabezado de los campos
    clients = lines[1:]  # Lista- Trae los registros a partir de la segunda linea
    for idx, client in enumerate(clients): # itera por cada registro asignando el indice del registro en idx y el contenido del registro en client
        clients[idx] = clients[idx].split(',') #Devuelve una lista/ agarra un string y lo divide en varios strings utilizando la coma.
    return render_template('clientes.html', fields=fields, clients=clients, client_count=len(clients)) #Llama al html con los parametros  fields y clients .

@app.route('/sobre', methods=['GET', 'POST'])
def sobre():
    return render_template('sobre.html')

@app.route('/saludar/<usuario>')
def saludar_persona(usuario):
    return render_template('usuarios.html', nombre=usuario)

@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)


@app.route('/nuevo_cliente', methods=['GET', 'POST'])
def NuevoCliente():
	formulario = NuevoClienteForm()
	if formulario.validate_on_submit():
		#if formulario.password.data == formulario.password_check.data:
		with open('./DB/clientes.csv', 'a+') as archivo:
			archivo_csv = csv.writer(archivo)
			registro = [ 
			formulario.nombre				.data
			, formulario.edad				.data
			, formulario.direccion			.data
			, formulario.pais				.data
			, formulario.documento			.data
			, formulario.fecha_alta			.data
			, formulario.correo_electronico	.data
			, formulario.trabajo			.data
			]
			archivo_csv.writerow(registro)
		flash('Cliente creado correctamente')
		return redirect(url_for('generar_tabla_clientes'))
	#else:
	#    flash('Las passwords no matchean')
	return render_template('nuevo_cliente.html', form=formulario)

@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
