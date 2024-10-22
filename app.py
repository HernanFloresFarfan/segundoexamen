from flask import Flask, session, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_la_sesion'

@app.route('/')
def index():
    if 'productos' not in session:
        session['productos'] = []
    return render_template('index.html', productos=session['productos'])

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    # Cuando el método es GET, mostrar el formulario para agregar productos
    if request.method == 'GET':
        return render_template('agregar_producto.html')  # Cargar tu página 'Agregar Producto'

    # Cuando el método es POST, procesar los datos del formulario
    if request.method == 'POST':
        productos = session['productos']
        
        try:
            # Crear un diccionario para el nuevo producto
            nuevo_producto = {
                'id': request.form['id'],
                'nombre': request.form['nombre'],
                'cantidad': int(request.form['cantidad']),  # Puede lanzar un ValueError
                'precio': float(request.form['precio']),    # Puede lanzar un ValueError
                'fecha_vencimiento': request.form['fecha_vencimiento'],
                'categoria': request.form['categoria']
            }
        except ValueError:
            return "Error: Cantidad o Precio no son válidos."

        # Asegurar que el ID sea único
        for producto in productos:
            if producto['id'] == nuevo_producto['id']:
                return "El ID ya existe, debe ser único."

        # Agregar el producto al array de productos
        productos.append(nuevo_producto)
        session['productos'] = productos
        return redirect(url_for('index'))

@app.route('/eliminar/<id>')
def eliminar_producto(id):
    productos = session['productos']
    session['productos'] = [producto for producto in productos if producto['id'] != id]
    return redirect(url_for('index'))

# Nueva ruta para editar producto
@app.route('/editar/<id>')
def editar_producto(id):
    productos = session['productos']
    producto = next((producto for producto in productos if producto['id'] == id), None)
    
    if producto:
        return render_template('editar.html', producto=producto)
    return "Producto no encontrado", 404

# Nueva ruta para actualizar el producto
@app.route('/actualizar/<id>', methods=['POST'])
def actualizar_producto(id):
    productos = session['productos']
    producto = next((producto for producto in productos if producto['id'] == id), None)

    if producto:
        try:
            # Actualizar los datos del producto
            producto['nombre'] = request.form['nombre']
            producto['cantidad'] = int(request.form['cantidad'])
            producto['precio'] = float(request.form['precio'])
            producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
            producto['categoria'] = request.form['categoria']
        except ValueError:
            return "Error: Cantidad o Precio no son válidos."
        
        session['productos'] = productos
        return redirect(url_for('index'))
    
    return "Producto no encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)
