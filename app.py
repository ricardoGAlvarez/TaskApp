from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app=Flask (__name__)
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='bdejemplopy'
mysql.init_app(app)


@app.route('/')
def inicio():
    return render_template('pages/index.html')

@app.route('/realizados')
def realizados():
    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM `reclamos` WHERE `estado` = 1")
    reclamo=cursor.fetchall()
    conexion.commit()
    return render_template('pages/realizados.html', reclamo=reclamo)

@app.route('/pendientes')
def pendientes():
    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM `reclamos` WHERE `estado` = 0")
    reclamo=cursor.fetchall()
    conexion.commit()
    return render_template('pages/pendientes.html', reclamo=reclamo)

@app.route('/nuevo')
def nuevo():
    return render_template('pages/nuevo.html')


@app.route('/nuevo/guardar', methods=['POST'])
def guardar():
    _nombre=request.form['txtNyA']
    _calle=request.form['txtCalle']
    _barrio=request.form['txtBarrio']
    _problema=request.form['txtProblema']
    _estado=0
    
    sql= "INSERT INTO   `reclamos` ( `id`, `nombre`, `barrio`,  `calle`,  `problema`,`estado`) VALUE(NULL,%s,%s,%s,%s,%s);"
    datos=(_nombre,_calle,_barrio,_problema,_estado )
    conexion= mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    return redirect('/pendientes')

@app.route('/edit/<int:id>', methods=['GET'])
def editar(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()

    sql = "SELECT * FROM reclamos WHERE id = %s"
    cursor.execute(sql, (id,))
    elemento = cursor.fetchone()

    nombre = elemento[1]
    calle = elemento[2]
    barrio = elemento[3]
    problema = elemento[4]
    estado= elemento[5]

    return render_template('pages/edit.html', id=id, nombre=nombre, calle=calle, barrio=barrio, problema=problema, estado=estado)

@app.route('/edit/guardar/<int:id>', methods=['POST'])
def actualizar(id):
    _nombre = request.form['txtNyA']
    _calle = request.form['txtCalle']
    _barrio = request.form['txtBarrio']
    _problema = request.form['txtProblema']
    _estado= request.form['txtEstado']
    sql = "UPDATE `reclamos` SET `nombre` = %s, `barrio` = %s, `calle` = %s, `problema` = %s, `estado` = %s WHERE `reclamos`.`id` = %s"
    datos = (_nombre, _barrio, _calle, _problema,_estado, id)
    print(dir(datos))
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/pendientes')

@app.route('/realizados/guardar/<int:id>', methods=['POST'])
def realizado(id):
    _estado= 1
    sql = "UPDATE `reclamos` SET `estado` = %s WHERE `reclamos`.`id` = %s"
    datos = (_estado, id)
    print(dir(datos))
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/pendientes')

@app.route('/realizados/pendientes/<int:id>', methods=['POST'])
def ponerpendiente(id):
    _estado= 0
    sql = "UPDATE `reclamos` SET `estado` = %s WHERE `reclamos`.`id` = %s"
    datos = (_estado, id)
    print(dir(datos))
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/realizados')

@app.route('/buscar/realizados')
def buscarrealizados():
    barrio = request.args.get('barrio')
    conexion = mysql.connect()
    cursor = conexion.cursor()
    if barrio:
        cursor.execute("SELECT * FROM `reclamos` WHERE `estado` = 1 AND `barrio` = %s", (barrio,))
    else:
        cursor.execute("SELECT * FROM `reclamos` WHERE `estado` = 1")
    reclamo = cursor.fetchall()
    conexion.commit()
    return render_template('pages/realizados.html', reclamo=reclamo)

@app.route('/buscar/pendientes')
def buscarpendientes():
    barrio = request.args.get('barrio')
    conexion = mysql.connect()
    cursor = conexion.cursor()
    if barrio:
        cursor.execute("SELECT * FROM `reclamos` WHERE `estado` = 0 AND `barrio` = %s", (barrio,))
    else:
        cursor.execute("SELECT * FROM `reclamos` WHERE `estado` = 0")
    reclamo = cursor.fetchall()
    conexion.commit()
    return render_template('pages/pendientes.html', reclamo=reclamo)

if __name__=='__main__':
    app.run(debug=True)