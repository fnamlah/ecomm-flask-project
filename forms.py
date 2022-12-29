from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, DateTimeField, SelectField, HiddenField, IntegerField
from wtforms.validators import DataRequired, URL


class OwnerRegisterForm(FlaskForm):
    store_name = StringField(label='Enter your Store Name', validators=[DataRequired()])
    username = StringField(label='Enter your Username', validators=[DataRequired()])
    email = StringField(label='Enter your Email', validators=[DataRequired()])
    password = StringField(label='Enter your Password', validators=[DataRequired()])
    role = HiddenField(name='role', default='owner', validators=[DataRequired()])
    submit = SubmitField(label='Register')


class CustomerForm(FlaskForm):
    username = StringField(label='Enter your Username', validators=[DataRequired()])
    email = StringField(label='Enter your Email', validators=[DataRequired()])
    password = StringField(label='Enter your Password', validators=[DataRequired()])
    role = HiddenField(name='role', default='customer', validators=[DataRequired()])
    submit = SubmitField(label='Register')


class CustomerLoginForm(FlaskForm):
    username = StringField(label='Enter your Username', validators=[DataRequired()])
    email = StringField(label='Enter your Email', validators=[DataRequired()])
    password = StringField(label='Enter your Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class OwnerLoginForm(FlaskForm):
    username = StringField(label='Enter your Username', validators=[DataRequired()])
    email = StringField(label='Enter your Email', validators=[DataRequired()])
    password = StringField(label='Enter your Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class ProductForm(FlaskForm):
    # it should take the user_id AKA owner_id & store_id
    # stores = Store.query.filter_by(owner_id=current_user.id).all()
    # # db.session.query()
    # # User.query.filter_by()
    # for stores in current_user.store:
    #     list_of_stores = stores
    #     store_name = SelectField('Your Stores', choices=str, validators=[DataRequired()])
    store_name = StringField(label='Enter a Your Store name', validators=[DataRequired()])
    product_name = StringField(label='Enter a Product name', validators=[DataRequired()])
    product_description = StringField(label='Enter a Product name', validators=[DataRequired()])
    quantity = IntegerField(label='How many pieces you would like to list', validators=[DataRequired()])
    submit = SubmitField(label='Submit Product')


class OrderForm(FlaskForm):
    quantity = IntegerField(label='How many pieces', validators=[DataRequired()])
    submit = SubmitField(label='Buy')
