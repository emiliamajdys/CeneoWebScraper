from app import app
import os
import json
import requests
from bs4 import BeautifulSoup
from flask import render_template, request, redirect, url_for
from config import headers
from app import utils

@app.route('/')
@app.route('/<name>')
def index(name="world"):
    return render_template("index.html")


@app.route("/extract")
def display_form():
    return render_template("extract.html")


@app.route("/extract", methods=["POST"])
def extract():
    product_id = request.form.get('product_id')
    next_page = (f"https://www.ceneo.pl/{product_id}#tab=reviews")
    all_opinions=[]
    while next_page:
        print(next_page)
        response = requests.get(next_page,headers=headers)
        if response.status_code ==200:
        
            page_dom = BeautifulSoup(response.text, "html.parser")
            opinions= page_dom.select("div.js_product-review:not(.user-post--highlight)")
            for opinion in opinions:
             
                single_opinion = {
                    key:utils.extract_feautre(opinion, *value)
                    for key, value in utils.selectors.items()
                  

                    }
                
                all_opinions.append(single_opinion)
           

            try:
                next_page="https://www.ceneo.pl"+ extract(page_dom, "a.pagination__next", "href")
            except TypeError:
                next_page= None
                print("Brak kolejnej strony")
        else: print(response.status_code)
    
    if not os.path.exists("./app/data/opinions"):
        os.mkdir("./app/data")
    if not os.path.exists("./app/data/opinions"):
        os.mkdir("./app/data")
    with open(f"./app/data/opinions{product_id}.json", "w", encoding="UTF-8") as jf:
        json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
    
    return redirect(url_for('product', product_id=product_id))


@app.route("/products")
def products():
    return render_template("products.thml")

@app.route("/author")
def author():
    return render_template("author.thml")

@app.route("/product/<product_id>")
def product(product_id):
    return render_template("product.thml", product_id==product_id)