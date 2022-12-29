# from flask import Flask, render_template, redirect, url_for, request, flash, abort
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, FieldList, DateTimeField, SelectField, HiddenField
# from wtforms.validators import DataRequired, URL, EqualTo
# from flask_bootstrap import Bootstrap
#
# # Initializing app using Flask Class
# app = Flask(__name__)
# # SECRET_KEY needed to secure forms
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# # Using Bootstrap library from flask_bootstrap
# Bootstrap(app)
#
#
# class RegForm(FlaskForm):
#     email = StringField(label='Enter your Email', validators=[DataRequired()])
#     password = StringField(label='Enter your Password', validators=[DataRequired()])
#     # You can get the value of a hidden field by using form.role.render_kw['value']
#     # role = HiddenField(id='user_role', name='role',
#     #                    render_kw={'value': 'owner'}, validators=[DataRequired(), EqualTo('role')])
#     role = HiddenField(name='role',
#                        default='OWNER', validators=[DataRequired()])
#     submit = SubmitField(label='Register')
#
#
# @app.route('/', methods=['POST', 'GET'])
# def test_hidden():
#     form = RegForm()
#     if form.validate_on_submit():
#         print(form.email.data)
#         print(form.password.data)
#         # You can get the value of a hidden field by using form.role.render_kw['value']
#         # print(form.role.render_kw['value'])
#         print(form.role.data)
#
#     return render_template('testfield.html', form=form)
#
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True, use_reloader=False)
#
#
#
#
#
#
#
#
#
#
#
# @app.route('/register/<role>', methods=['POST', 'GET'])
# def customer_register():
#         form = OwnerRegisterForm()
#         if form.validate_on_submit():
#             print(form.role.data)
#             print(form.role.default)
#             if User.query.filter_by(email=form.email.data).first():
#                 # User already exists
#                 flash("You've already signed up with that email, log in instead!")
#                 return redirect(url_for('home'))
#
#             hash_and_salted_password = generate_password_hash(
#                 form.password.data,
#                 method='pbkdf2:sha256',
#                 salt_length=8
#             )
#             new_user = User(
#                 username=form.username.data,
#                 email=form.email.data,
#                 password=hash_and_salted_password,
#                 role=form.role.data
#             )
#             if Store.query.filter_by(store_name=form.store_name.data).first():
#                 flash("You've already signed up with that email, log in instead!")
#                 return redirect(url_for('home'))
#             else:
#                 new_store = Store(owner=new_user, store_name=form.store_name.data)
#                 db.session.add(new_store)
#                 db.session.add(new_user)
#                 db.session.commit()
#                 login_user(new_user)
#         return 'Successfully registered'
# return render_template('customer-register.html', form=form)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
