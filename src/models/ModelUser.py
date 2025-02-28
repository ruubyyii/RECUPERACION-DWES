from .entities.User import User
from werkzeug.security import generate_password_hash

class ModelUser():

    @classmethod
    def login(cls, db, user):

        try:
            cursor = db.connection.cursor()
            sql = 'SELECT * FROM users WHERE username = %s'

            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()

            if row:
                id = row[0]
                username = row[1]
                password = User.check_password(row[2], user.password)
                fullname = row[3]

                user = User(id, username, password, fullname)

                return user
            else:
                return None

        except Exception as e:

            raise Exception(e)

    @classmethod
    def register(cls, db, user):
        try:
            hashed_password = generate_password_hash(user.password)

            cur = db.connection.cursor()
            cur.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (user.username, hashed_password, user.fullname))
            db.connection.commit()
        except Exception as e:
            print('Error al registrar usuario!!')
            raise Exception(e)

    @classmethod
    def get_by_id(cls, db, id):

        try:
            cursor = db.connection.cursor()
            sql = 'SELECT id, username, fullname FROM users WHERE id = %s'

            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row:
                id = row[0]
                username = row[1]
                fullname = row[2]

                logged_user = User(id, username, None, fullname)

                return logged_user
            else:
                return None

        except Exception as e:

            raise Exception(e)
        
    @classmethod
    def getProductos(cls, db):

        cur = db.connection.cursor()
        cur.execute('SELECT * FROM productos')
        data = cur.fetchall()

        if data: 
            print('Prodcutos cargados con exito!')
            return data
        else:
            print('Error al recoger productos!!')
            return None
    
    @classmethod
    def getCarrito(cls, db, user_id):

        cur = db.connection.cursor()
        cur.execute('SELECT * FROM productos WHERE id = %s', (user_id))
        data = cur.fetchall()

        if data: 
            print('Prodcutos cargados con exito!')
            return data
        else:
            print('Error al recoger productos!!')
            return None

    @classmethod
    def addCarrito(cls, db, user_id):

        cur = db.connection.db()
        cur.execute('INSERT INTO VALUES (NULL, NULL, NULL, NULL, NULL, %s) productos WHERE id = %s', (user_id))
        db.connection.commit()
