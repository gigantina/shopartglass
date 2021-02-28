from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, SelectField, IntegerField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm
from models import *


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField()


class ItemForm(FlaskForm):
    name = StringField("Название")
    first_image = FileField('Первое фото', validators=[Optional()])

    second_image = FileField('Опционально: второе фото', validators=[Optional()])

    categories = [(i.id, i.name) for i in Category.query.all()]

    category = SelectField('Категория', choices=categories)
    price = IntegerField('Цена')
    is_active = BooleanField('В наличии')
    text = TextAreaField('Описание')
    value = IntegerField('Количество товара')

    submit = SubmitField('Сохранить')


class CategoryForm(FlaskForm):
    name = StringField("Название")
    submit = SubmitField('Сохранить')
