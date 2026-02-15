from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo Libro
class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)

# Crear base de datos
with app.app_context():
    db.create_all()

# Página principal
@app.route("/")
def index():
    libros = Libro.query.all()
    return render_template("index.html", libros=libros)

# Agregar libro
@app.route("/agregar", methods=["POST"])
def agregar():
    titulo = request.form["titulo"]
    autor = request.form["autor"]

    nuevo_libro = Libro(titulo=titulo, autor=autor)
    db.session.add(nuevo_libro)
    db.session.commit()

    return redirect("/")

# Eliminar libro
@app.route("/eliminar/<int:id>")
def eliminar(id):
    libro = Libro.query.get(id)
    db.session.delete(libro)
    db.session.commit()
    return redirect("/")

# Mostrar formulario editar
@app.route("/editar/<int:id>")
def editar(id):
    libro = Libro.query.get(id)
    return render_template("editar.html", libro=libro)

# Actualizar libro
@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    libro = Libro.query.get(id)
    libro.titulo = request.form["titulo"]
    libro.autor = request.form["autor"]

    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
