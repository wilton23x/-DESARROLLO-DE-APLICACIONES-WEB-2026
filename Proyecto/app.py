from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/contactos")
def contactos():
    return render_template("contactos.html")

@app.route("/productos")
def lista_productos():
    return render_template("productos/listproducts.html")

@app.route("/productos/nuevo")
def nuevo_producto():
    return render_template("productos/form.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)