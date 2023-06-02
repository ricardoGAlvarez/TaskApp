from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import date
from flask import flash
from tkinter import messagebox 
app=Flask (__name__)
mysql=MySQL()

#ENTORNO DE PRODUCCION
# app.config['MYSQL_DATABASE_HOST']='b2budm4wynsuvdqurcml-mysql.services.clever-cloud.com'
# app.config['MYSQL_DATABASE_USER']='uq5uxklfvlrowiyf'
# app.config['MYSQL_DATABASE_PASSWORD']='MP7stpSXOHAonQ8uoybm'
# app.config['MYSQL_DATABASE_DB']='b2budm4wynsuvdqurcml'

#ENTORNO DE DESARROLLO
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='bdejemplopy'
mysql.init_app(app)

usuario="pepe"
password="1234"
@app.route('/')
def inicio():
    return render_template('pages/index.html')


@app.route('/login', methods=['POST'])
def login():
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']
    if _usuario != usuario or _password != password:
        return redirect('/')
    else:
        conexion=mysql.connect()
        cursor= conexion.cursor()
        cursor.execute("SELECT * FROM `reclamos` WHERE `estado` = 0")
        reclamo=cursor.fetchall()
        conexion.commit()
        return render_template('pages/pendientes.html', reclamo=reclamo)

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
    fecha_actual = date.today()
    _nombre=request.form['txtNyA']
    _calle=request.form['txtCalle']
    _barrio=request.form['txtBarrio']
    _problema=request.form['txtProblema']
    _estado=0
    _historial=_problema
    _fecha= fecha_actual
    sql_filter="SELECT calle FROM `reclamos` WHERE calle=%s"
    conexion= mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql_filter, (_calle,))
    result=cursor.fetchone()
    if result:
       messagebox.showerror("Error", "La direccion ya posee un reclamo")
       return redirect('/nuevo')
    else:
        sql= "INSERT INTO   `reclamos` ( `id`, `nombre`, `barrio`,  `calle`,  `problema`,`estado`,`historial`,`fecha`) VALUE(NULL,%s,%s,%s,%s,%s,%s,%s);"
        datos=(_nombre,_barrio,_calle,_problema,_estado,_historial,_fecha )
        conexion= mysql.connect()
        cursor=conexion.cursor()
        cursor.execute(sql,datos)
        conexion.commit()
        reclamo_id = cursor.lastrowid

        sql_historial="INSERT INTO `historial` (`id`, `detalles`, `fecha`, `reclamo_id`) VALUE(NULL, %s, %s, %s);"
        datos_historial=(_historial, _fecha, reclamo_id)
        cursor.execute(sql_historial, datos_historial)
        conexion.commit()
        messagebox.showinfo("Exito", "Reclamo agregado correctamente")

    
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
    historial= elemento[6]
    fecha= elemento[7]


    return render_template('pages/edit.html', id=id, nombre=nombre, calle=calle, barrio=barrio, problema=problema, estado=estado, historial=historial, fecha=fecha)

@app.route('/edit/guardar/<int:id>', methods=['POST'])
def actualizar(id):
    fecha_actual = date.today()

    _nombre = request.form['txtNyA']
    _calle = request.form['txtCalle']
    _barrio = request.form['txtBarrio']
    _problema = request.form['txtProblema']
    _estado=0
    _fecha=fecha_actual
    _reclamo_id=id
    _historial=request.form['txtHistorial']
    sql = "UPDATE `reclamos` SET `nombre` = %s, `barrio` = %s, `calle` = %s, `problema` = %s, `estado` = %s,`historial` = %s  WHERE `reclamos`.`id` = %s"
    datos = (_nombre, _barrio, _calle, _problema,_estado,_historial, id)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    sql_historial="INSERT INTO `historial` (`id`, `detalles`, `fecha`, `reclamo_id`) VALUE(NULL, %s, %s, %s);"
    datos_historial=(_historial, _fecha, _reclamo_id)
    cursor.execute(sql_historial, datos_historial)
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


@app.route('/historial/<int:id>', methods=['GET'])
def ver_reclamo(id):
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
    fecha= elemento[7]

    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM historial WHERE reclamo_id = %s",(id,))
    historial_lista=cursor.fetchall()
    conexion.commit()

    return render_template('pages/historial.html', id=id, nombre=nombre, calle=calle, barrio=barrio, problema=problema, estado=estado, fecha=fecha, historial_lista=historial_lista)



if __name__=='__main__':
    app.run(debug=True)