from flask import session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, SelectField, IntegerField, \
    RadioField
from wtforms.validators import DataRequired, Optional
from wtforms_components import EmailField

from models import Category, Item
import phonenumbers


def cost2cart(cost):
    if cost != 0:
        return f'  {cost}₽'
    else:
        return ''


def cart2cost(cart):
    return int(cart[:-1].lstrip())


def additemtocart(id, amount):
    print(session['cart'])
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append([id, amount])
    session.modified = True
    print(session['cart'])
    return session

def deletefromcart(id):
    if 'cart' not in session:
        session['cart'] = []
    for i in range(len(session['cart'])):
        if session['cart'][i][0] == id:
            session['cart'].pop(i)
            break
    session.modified = True
    print(session['cart'])
    return session


def deletecart():
    session['cart'] = []


def get_cart():
    cart = {}
    for id, amount in session['cart']:
        if id not in cart:
            cart[id] = 0
        cart[id] += amount
    return cart


def checkcart():
    cart = get_cart()
    for id in cart:
        amount = int(Item.query.get(id).value)
        if cart[id] > amount:
            session['cart'] = [[id_, amount] for id_, amount in session['cart'] if id != id_]


def from_cart_to_list():
    res = []
    cart = get_cart()
    for id in cart:
        res.append([Item.query.get(id), cart[id]])
    return res


def sum_cart():
    if 'cart' not in session:
        session['cart'] = []
    price = 0
    for id, amount in session['cart']:
        price += int(Item.query.get(id).price) * int(amount)
    return price


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField()


class ItemForm(FlaskForm):
    name = StringField("Название")
    first_image = FileField('Первое фото', validators=[Optional()])

    second_image = FileField('Опционально: дополнительное фото', validators=[Optional()])

    categories = [(i.id, i.name) for i in Category.query.all()]

    category = SelectField('Категория', choices=categories)
    price = IntegerField('Цена')
    is_active = BooleanField('В наличии')
    text = TextAreaField('Описание')
    value = IntegerField('Количество товара')

    submit = SubmitField('Сохранить')



class CheckoutForm(FlaskForm):
    name = StringField("Имя")
    email = EmailField("E-mail")
    phone = StringField('Телефон', validators=[DataRequired()])

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValueError('Invalid phone number')

    submit = SubmitField('Отправить')


class CategoryForm(FlaskForm):
    name = StringField("Название")
    submit = SubmitField('Сохранить')
