from flask import Flask, render_template, request, redirect, url_for, flash, session

from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
import os

from config import config
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

app = Flask(__name__)

config_dict = config()
for key in config_dict:
    app.config[key] = config_dict[key]

app.config['STATIC_DIR'] = os.path.join(app.config['APP_DIR'], 'static')
app.config['UPLOAD_DIR'] = os.path.join(app.config['STATIC_DIR'], 'img')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
cost = 0


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


from forms import *
from models import *

@app.route('/', methods=['GET'])
def index():
    categories = Category.query.all()
    if request.method == 'GET':
        category = request.values.get('category')
        if category:
            category = int(category)
            items = Item.query.filter_by(category_id=category).all()
        else:
            items = Item.query.all()
    return render_template('index.html', cost=cost2cart(sum_cart()), categories=categories, items=items)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    cart_ = from_cart_to_list()
    sum_ = sum([item.price * amount for item, amount in cart_])
    return render_template('cart.html', items=cart_, sum_=sum_, cost=cost2cart(sum_cart()))


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def product(id):
    if request.method == 'POST':
        amount = request.form.get('amount')
        if amount:
            additemtocart(id, int(amount))
            checkcart()
    item = Item.query.get(id)
    return render_template('product.html', item=item, cost=cost2cart(sum_cart()))


@app.route('/admin/', methods=['POST', 'GET'])
@login_required
def admin():
    return render_template('admin.html')


@app.route('/admin/items/', methods=['POST', 'GET'])
def listitems():
    all_items = Item.query.all()
    all_items_table = [i.all() for i in all_items]
    for i in range(len(all_items_table)):
        for j in range(len(all_items_table[i])):
            if j == 1:
                all_items_table[i][j] = Category.query.get(all_items_table[i][j])
    all_items_table.insert(0, ['id', 'Категория', 'Название', 'Цена', 'В наличии', 'Количество', 'Описание', '',
                               ''])

    return render_template('table.html', data=all_items_table, last_id=all_items[-1].id + 1, mode=0)


@app.route('/admin/item/delete', methods=['POST', 'GET'])
def deleteitem():
    if request.method == 'GET':
        id = int(request.values.get('id'))
    item = Item.query.get(id)
    try:
        db.session.delete(item)
        db.session.commit()
    except:
        pass
    return redirect(url_for('listitems'))


@app.route('/admin/item/<string:id>', methods=['POST', 'GET'])
def edititem(id):
    id = int(id)
    obj = [i.id for i in Item.query.all()]
    new = False
    if id not in obj:
        new = True

    if new:
        form = ItemForm()
    else:
        item = Item.query.get(id)
        form = ItemForm(category_id=item.category_id, name=item.title, price=item.price, is_active=item.isActive,
                        text=item.text, first_image=item.first_image, second_image=item.second_image, value=item.value)

    message = ''
    if form.validate_on_submit():
        fi = ''
        si = ''
        if form.first_image.data:
            file = request.files.get('first_image', None)
            if file:
                file.save(os.path.join(app.config['UPLOAD_DIR'], file.filename))
                fi = file.filename

        if form.second_image.data:
            file = request.files.get('second_image', None)
            if file:
                file.save(os.path.join(app.config['UPLOAD_DIR'], file.filename))
                si = file.filename
        if new:
            item = Item(id=id, category_id=form.category.data, title=form.name.data, price=form.price.data,
                        isActive=form.is_active.data,
                        first_image=fi, second_image=si, text=form.text.data, value=form.value.data)
            try:
                db.session.add(item)
                db.session.commit()
                message = 'Изменения успешно сохранены!'
            except:
                pass

        else:
            item = Item.query.get(id)
            item.category_id, item.price, item.title, item.isActive = form.category.data, form.price.data, form.name.data, form.is_active.data
            item.value = form.value.data
            if type(form.first_image.data) != type('string') and form.first_image.data:
                item.first_image = form.first_image.data.filename
            if type(form.second_image.data) != type('string') and form.second_image.data:
                item.second_image = form.second_image.data.filename
            try:
                db.session.commit()
                message = 'Изменения успешно сохранены!'
            except:
                pass
    return render_template('create.html', form=form, message=message, mode=0)


@app.route('/admin/categories/', methods=['POST', 'GET'])
def listcategories():
    all_cat = Category.query.all()
    all_cat_table = [i.all() for i in all_cat]

    all_cat_table.insert(0, ['id', 'Категория'])
    return render_template('table.html', data=all_cat_table, last_id=all_cat[-1].id + 1)


@app.route('/admin/category/delete', methods=['POST', 'GET'])
def deletecategory():
    if request.method == 'GET':
        id = int(request.values.get('id'))
    category = Category.query.get(id)
    try:
        db.session.delete(category)
        db.session.commit()
    except:
        pass
    return redirect(url_for('listcategories'))


@app.route('/admin/category/<string:id>', methods=['POST', 'GET'])
def editcategory(id):
    id = int(id)
    obj = [i.id for i in Category.query.all()]
    new = False
    if id not in obj:
        new = True

    if new:
        form = CategoryForm()
    else:
        form = CategoryForm(name=Category.query.get(id).name)

    message = ''
    if form.validate_on_submit():
        if new:
            category = Category(id=id, name=form.name.data)
            try:
                db.session.add(category)
                db.session.commit()
                message = 'Изменения успешно сохранены!'
            except:
                pass

        else:
            category = Category.query.get(id)  # or whatever
            category.name = form.name.data
            try:
                db.session.commit()
                message = 'Изменения успешно сохранены!'
            except:
                pass
    return render_template('create.html', form=form, message=message, mode=1)


@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and form.password.data == user.password:
            login_user(user)
            return redirect(url_for('admin'))

        flash("Invalid username/password", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))


if __name__ == '__main__':
    host = '192.168.0.60'
    app.run(host=host, port=8000, debug=True)
