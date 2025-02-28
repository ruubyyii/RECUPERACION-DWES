from flask import Flask, url_for, render_template, redirect, request
from flask_mysqldb import MySQL
from config import config
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models.entities.User import User
from models.ModelUser import ModelUser
from flask_wtf import CSRFProtect
# generar token para realizar el pedido con 5 mins de validez
from flask_jwt_extended import create_access_token
# mandar correos
import smtplib


# INICIALIZACIONES DE LIBRERIAS
app = Flask(__name__)
db = MySQL(app)
login_manager = LoginManager(app)

# FLASK_LOGIN
@login_manager.user_loader
def get_by_id(id):
    return ModelUser.get_by_id(db,id)

# WELCOME
@app.route('/')
def welcome():
    return render_template('welcome.html')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
    
        username = request.form.get('username')
        password = request.form.get('password')
        fullname = request.form.get('fullname')

        user = User(0, username, password, fullname)
        ModelUser.register(db, user)
        logged_user = ModelUser.login(db, user)
        login_user(logged_user)

        return redirect(url_for('tienda'))

    else:
        if current_user.is_authenticated:
            return redirect(url_for('tienda'))
        return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user = User(0, username, password, '')
        logged_user = ModelUser.login(db, user)

        if logged_user:
            login_user(logged_user)
            if logged_user.password:
                print('Sesion iniciada correctamente!')
                return redirect(url_for('tienda'))
            else:
                print('Error al introducir la contraseña!!')
                return redirect(url_for('login'))
        else:
            print('Error al introducir usuario!!')
            return redirect(url_for('login'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('tienda'))
        return render_template('login.html')

# WELCOME TIENDA
@app.route('/tienda')
@login_required
def tienda():
    return render_template('tienda.html', logged_user=current_user)

# TIENDA PRODUCTOS
@app.route('/produtos')
@login_required
def productos():

    productos = ModelUser.getProductos(db)

    return render_template('productos.html', logged_user=current_user, productos=productos)

# CARRITO
@app.route('/carrito')
@login_required
def carrito():

    carrito = ModelUser.getCarrito(db, current_user.id)

    render_template('carrito.html', logged_user=current_user, carrito=carrito)

# AÑADIR AL CARRITO
@app.route('/addCarrito/<string:id>')
@login_required
def addCarrito(id):
    
    ModelUser.addCarrito(db, current_user.id)
    return redirect(url_for('carrito'))

# REALIZAR PEDIDO (JWT)
@app.route('/realizarPedido')
@login_required
def realizarPedidio():
    return render_template('realizarPedido.html')

# PEDIDO EXITOSO
@app.route('/pedidoExitoso')
def pedidoExitoso():
    pass

# ERROR EN EL PEDIDO
@app.route('/pedidoExitoso')
def pedidoExitoso():
    pass

#### ADMIN MENU ####
@app.route('/admin')
def admin():

    return render_template('admin.html')

# MENU USUARIOS
@app.route('/adminUsers')
def adminUsers():
    
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    return render_template('adminUsers.html', users=users)

@app.route('/deleteUser/<string:id>')
def deleteUser(id):
    
    cur = db.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = %s', (id,))
    db.connection.commit()

    return redirect(url_for('adminUsers'))

@app.route('/editUser/<string:id>')
def editUser():
    pass

# MENU PRODUCTOS
@app.route('/adminProductos')
def adminProductos():
    
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM productos')
    productos = cur.fetchall()

    return render_template('adminProductos.html', productos=productos)

@app.route('/deleteProducto/<id>')
def deleteProducto(id):
    
    cur = db.connection.cursor()
    cur.execute('DELETE FROM productos WHERE id = %s', (id,))
    db.connection.commit()

    return redirect(url_for('adminProductos'))

@app.route('/editUser/<string:id>', methods=['POST'])
def editProduct(id):
    pass

# CERRAR SESION
@app.route('/logout')
def logout():
    logout_user()
    print('Sesion cerrada con exito!')
    return redirect(url_for('login'))

# ERROR 404
@app.errorhandler(404)
def error_404(error):
    return '<h1>ERROR 404 no se pudo cargar la pagina :(</h1>'

# ERROR 401
@app.errorhandler(401)
def error_401(error):
    print('ERROR 401 NO TIENES PERMISO !!')
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()