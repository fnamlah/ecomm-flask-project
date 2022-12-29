# Testing what can be imported into other modules:
# class StoreManager:
#
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email


# Access the database in other modules
# with app.app_context():
    # all_products_owned_by_a_user = db.session.query(User).filter_by(username='fnamlah').first().store_owned_by_user[0].product_in_store
    # for store in all_products_owned_by_a_user:
    #     print(store.product_in_store)
    # order = Order.query.filter_by(buyer=buyer, product_name='Lavender').first()
    # random_user = random.choice(all_users)
    # new_user = CurrentUser(username=random_user.username, email=random_user.email)

# print(new_user.username)
# print(current_user)

# print(all_products_owned_by_a_user)
# print(current_user)
# with app.app_context():
#     targeted_order = db.session.query(Order).filter_by(id=7).first()
    # targeted_order = Order.query.filter_by(id=7).first()

    # targeted_order.product_description = 'hello world'
    # db.session.commit()
    # print(targeted_order.product_description)
