from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import *

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка"
    else:
        return render_template('create.html')


@app.route('/admin/', methods=['POST', 'GET'])
@login_required
def admin():
    return render_template('admin.html')


if __name__ == "__main__":
    app.run(debug=True)

if __name__ == '__main__':
    app.run()

