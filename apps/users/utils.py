#Funciones extras de la aplicacion user
#funciones de python
import random
import string

#funcion generado de codigo de activacion de usuario

def code_generator(size=9, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size)) 
