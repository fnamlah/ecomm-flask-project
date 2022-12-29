from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import OwnerRegisterForm, CustomerForm, ProductForm, CustomerLoginForm, OwnerLoginForm, OrderForm

# Initializing app using Flask Class
app = Flask(__name__)
# SECRET_KEY needed to secure forms
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# Using Bootstrap library from flask_bootstrap
Bootstrap(app)
# Configuring SQL DB:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e-comm-store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Setup login
login_manager = LoginManager()
login_manager.init_app(app)


# User-loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# store_manager = StoreManager(current_user)
# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    # This will act like a store objects attached to each user.
    # The "owner" refers to the owner property in the Store class.
    store_owned_by_user = db.relationship('Store', back_populates='owner')
    product_owned_by_user = db.relationship('Product', back_populates='product_owner')

    item_bought_by_user = db.relationship('Order', back_populates='buyer')


class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Create reference to the Store object, the "products" refers to the products properties in the User class
    owner = db.relationship('User', back_populates='store_owned_by_user')
    product_in_store = db.relationship('Product', back_populates='store_owner')
    buyer_from_store = db.relationship('Order', back_populates='store_bought_from')

    store_name = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.store_name}"


# Line below only required once, when creating DB.


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # This will act like a store objects attached to each user.
    # The "owner" refers to the owner property in the Store class.
    product_owner = db.relationship('User', back_populates='product_owned_by_user')
    store_owner = db.relationship('Store', back_populates='product_in_store')

    product_sold = db.relationship('Order', back_populates='product_bought')

    product_name = db.Column(db.String(250), unique=True, nullable=False)
    product_description = db.Column(db.String(500), nullable=False)


    def __repr__(self):
        return f"{self.product_name}"


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    buyer = db.relationship('User', back_populates='item_bought_by_user')
    product_bought = db.relationship('Product', back_populates='product_sold')
    store_bought_from = db.relationship('Store', back_populates='buyer_from_store')

    product_name = db.Column(db.String(250), nullable=False)
    product_description = db.Column(db.String(500), nullable=False)
    quantity_bought = db.Column(db.String(500), nullable=False)



# with app.app_context():
#     Order.alter(unique=False, column_name='product_name')
    # Order.alter(unique=False, column_name='product_name')


# with app.app_context():
#     db.session.execute(Order.alter(unique=False, column_name='product_name'))
#
#     db.session.commit()
    # db.drop_constraint('orders', column_name='product_name')
    # Order.drop_constraint(unique=False, column_name='product_name')
#     db.create_all()
# # Add a new column
# def alter_column():
#     db.session.execute('ALTER TABLE products ADD COLUMN quantity_available varchar(50)')
#     db.session.commit()
#
# # Call the function
# with app.app_context():
#     alter_column()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/registeration-page')
def registration():
    return render_template('registeration-page.html')


@app.route('/register/store', methods=['POST', 'GET'])
def owner_register():
    form = OwnerRegisterForm()
    if form.validate_on_submit():
        print(form.role.data)
        print(form.role.default)
        if User.query.filter_by(email=form.email.data).first() or User.query.filter_by(username=form.username.data).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('home'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hash_and_salted_password,
            role=form.role.data
        )
        if Store.query.filter_by(store_name=form.store_name.data).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('home'))
        else:
            new_store = Store(owner=new_user, store_name=form.store_name.data)
            db.session.add(new_store)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            # store welcome page including add product button
            return render_template('owner_main_page.html', user=current_user.username, store=new_store.store_name)
    return render_template('owner-register.html', form=form)


@app.route('/register/customer', methods=['POST', 'GET'])
def customer_register():
    form = CustomerForm()
    if form.validate_on_submit():
        print(form.role.data)
        print(form.role.default)
        if User.query.filter_by(email=form.email.data).first() or User.query.filter_by(username=form.username.data).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('home'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hash_and_salted_password,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('list_of_stores'))
    return render_template('owner-register.html', form=form)


def owner_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'owner':
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login')
def login():
    return render_template('login/login-page.html')


@app.route('/stores')
def list_of_stores():
    stores = db.session.query(Store).all()
    return render_template('list_stores.html', stores=stores)


@app.route('/stores/products/<store_targeted>')
def list_of_products(store_targeted):
    # stores = db.session.query(Store).all()
    store = Store.query.filter_by(store_name=store_targeted).first()
    return render_template('list_products.html', products=store.product_in_store, store=store)


@app.route('/login/customer', methods=['GET', 'POST'])
def customer_login():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Find user by email entered.
        user = User.query.filter_by(email=email).first()
        print(user)

        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        # Email exists and password correct
        else:
            login_user(user)
            return redirect(url_for('list_of_stores'))
    return render_template("login.html", logged_in=current_user.is_authenticated, form=form)


@app.route('/login/owner', methods=['GET', 'POST'])
def owner_login():
    form = OwnerLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Find user by email entered.
        user = User.query.filter_by(email=email).first()
        print(user)

        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        # Email exists and password correct
        else:
            login_user(user)
            return render_template('owner_main_page.html', user=current_user.username, store=current_user.store_owned_by_user[0])
    return render_template("login.html", logged_in=current_user.is_authenticated, form=form)


@app.route('/<current_store>/add_product', methods=['POST', 'GET'])
@owner_only
def add_product(current_store):
    form = ProductForm()
    if form.validate_on_submit():
        stores = Store.query.filter_by(owner_id=current_user.id).all()
        print(stores)
        store = Store.query.filter_by(store_name=current_store).first()
        new_product = Product(product_owner=current_user, store_owner=store,
                              product_name=form.product_name.data, product_description=form.product_description.data)
        db.session.add(new_product)
        db.session.commit()
        return 'product registered successfully'
    return render_template("add_product.html", logged_in=current_user.is_authenticated, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.username)
    return render_template("secrets.html", email=current_user.username, logged_in=True)


@app.route('/manage')
@owner_only
@login_required
def manage_store():
    return 'yes you are a MANAGER'


@app.route('/stores/products//<store_targeted>/<targeted_product>/order', methods=['POST', 'GET'])
@login_required
def order(store_targeted, targeted_product):
    form = OrderForm()
    if form.validate_on_submit():
        store = Store.query.filter_by(store_name=store_targeted).first()
        product = Product.query.filter_by(product_name=targeted_product).first()
        new_order = Order(buyer=current_user, product_bought=product,
                          store_bought_from=store, product_name=product.product_name,
                          product_description=product.product_description, quantity_bought=form.quantity.data)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('successful_order', store_targeted=store_targeted, targeted_product=targeted_product))
    return render_template('new_order.html', form=form, store=store_targeted, product=targeted_product)


@app.route('/stores/products/<store_targeted>/<targeted_product>/order/success', methods=['POST', 'GET'])
@login_required
def successful_order(store_targeted, targeted_product):
    store = Store.query.filter_by(store_name=store_targeted).first()
    success_order = Order.query.filter_by(buyer=current_user, product_name=targeted_product).first()
    return render_template('successful_order.html', user=current_user, store=store, order=success_order)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
















