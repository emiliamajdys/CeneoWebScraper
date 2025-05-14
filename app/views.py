from app import app

from flask import render_template

@app.route('/')
@app.route('/<name>')
def index(name="world"):
    return render_template("index.html")


@app.route("/extract")
def extract():
    return render_template("extract.thml")

@app.route("/products")
def extract():
    return render_template("products.thml")

@app.route("/author")
def extract():
    return render_template("author.thml")

@app.route("/product/<product_id>")
def extract(product_id):
    return render_template("product.thml", product_id==product_id)