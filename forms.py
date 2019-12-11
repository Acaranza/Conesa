from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, IntegerField
from wtforms.validators import Required
import csv


class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')

class SaludarForm(FlaskForm):
    usuario = StringField('Nombre: ', validators=[Required()])
    enviar = SubmitField('Saludar')

class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Registrarse')

class NuevoClienteForm(FlaskForm):
	nombre				= StringField('Nombre'				, validators=[Required()])
	edad				= IntegerField('Edad'				, validators=[Required()])
	direccion			= StringField('Dirección'			, validators=[Required()])
	pais				= StringField('País'				, validators=[Required()])
	documento			= StringField('Documento'			, validators=[Required()])
	fecha_alta			= DateField('Fecha Alta'			, validators=[Required()])
	correo_electronico	= StringField('Correo Electrónico'	, validators=[Required()])
	trabajo				= StringField('Trabajo'				, validators=[Required()])
	
	agregar				= SubmitField('Agregar')
