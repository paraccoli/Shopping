from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, abort, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .forms import ProductForm, LoginForm, RegistrationForm, UpdateUserForm
import os
from werkzeug.utils import secure_filename
from flask import current_app
from . import db
from .models import Product, User, CartItem, Order, OrderItem, Notification, Inquiry, Favorite, Review, ReviewComment, ReviewLike
from PIL import Image

main = Blueprint('main', __name__)

@main.route('/')
def index():
    products = Product.query.all()

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('index.html', products=products, cart_count=cart_count, notification_count=notification_count)

@main.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        admin_user = User(username=username, email=email, is_admin=True)
        admin_user.set_password(password)
        db.session.add(admin_user)
        db.session.commit()
        flash('管理者アカウントが作成されました。')
        return redirect(url_for('main.index'))
    return render_template('create_admin.html')


@main.route('/search')
def search():
    query = request.args.get('query')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    products = Product.query
    if query:
        products = products.filter(Product.name.like(f'%{query}%'))
    if min_price:
        products = products.filter(Product.price >= min_price)
    if max_price:
        products = products.filter(Product.price <= max_price)
    products = products.all()
    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('search_results.html', products=products, query=query, cart_count=cart_count, notification_count=notification_count)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('登録が完了しました。')
        return redirect(url_for('main.login'))

    cart_count = 0
    notification_count = 0
    return render_template('register.html', form=form, cart_count=cart_count,notification_count=notification_count)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('ユーザー名またはパスワードが無効です。')
            return redirect(url_for('main.login'))
        if user.is_banned:
            flash('あなたはBANされています。管理者にお問い合わせください。')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.index'))
    cart_count = 0
    notification_count = 0
    return render_template('login.html', form=form, cart_count=cart_count,notification_count=notification_count)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/user_info')
@login_required
def user_info():
    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('user_info.html', cart_count=cart_count, notification_count=notification_count)

@main.route('/update_user', methods=['GET', 'POST'])
@login_required
def update_user():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar = form.avatar.data
            avatar_filename = secure_filename(avatar.filename)
            avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], avatar_filename)
            img = Image.open(avatar)
            img = img.resize((50, 50))
            img.save(avatar_path)
            current_user.avatar_filename = avatar_filename
        current_user.username = form.username.data
        current_user.nickname = form.nickname.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('ユーザー情報が更新されました。')
        return redirect(url_for('main.user_info'))
    form.username.data = current_user.username
    form.nickname.data = current_user.nickname

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('update_user.html', form=form, cart_count=cart_count, notification_count=notification_count)

@main.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = current_user
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/user_list')
@login_required
def user_list():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('user_list.html', users=users, cart_count=cart_count, notification_count=notification_count)

@main.route('/user_management')
@login_required
def user_management():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('user_management.html', users=users, cart_count=cart_count, notification_count=notification_count)

@main.route('/ban_user/<int:user_id>', methods=['POST'])
@login_required
def ban_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    user.is_banned = True
    db.session.commit()
    flash(f'{user.username}をBANしました。')

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return redirect(url_for('main.user_management', cart_count=cart_count, notification_count=notification_count))


@main.route('/unban_user/<int:user_id>', methods=['POST'])
@login_required
def unban_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    user.is_banned = False
    db.session.commit()
    flash(f'{user.username}のBANを解除しました。')

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return redirect(url_for('main.user_management', cart_count=cart_count, notification_count=notification_count))

@main.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        abort(403)
    form = ProductForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = secure_filename(image.filename)
        image_path = os.path.join(current_app.root_path, 'static/images', filename)
        image.save(image_path)
        new_product = Product(name=form.name.data, price=form.price.data, description=form.description.data, image_filename=filename)
        db.session.add(new_product)
        db.session.commit()
        flash('商品が追加されました。')
        return redirect(url_for('main.index'))

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('add_product.html', form=form, cart_count=cart_count, notification_count=notification_count)

@main.route('/delete_product', methods=['GET', 'POST'])
@login_required
def delete_product():
    if not current_user.is_admin:
        abort(403)
    if request.method == 'POST':
        admin_password = request.form.get('admin_password')
        if current_user.check_password(admin_password):
            product_ids = request.form.getlist('product_ids')
            for product_id in product_ids:
                product = Product.query.get(product_id)
                if product:
                    # 関連する Favorite レコードを削除
                    Favorite.query.filter_by(product_id=product_id).delete()
                    # 関連する OrderItem レコードを削除
                    OrderItem.query.filter_by(product_id=product_id).delete()
                    # 関連する CartItem レコードを削除
                    CartItem.query.filter_by(product_id=product_id).delete()
                    # 関連する Review レコードを削除
                    Review.query.filter_by(product_id=product_id).delete()
                    db.session.delete(product)
            db.session.commit()
            flash('選択された商品が削除されました。')
        else:
            flash('アドミンパスワードが正しくありません。')
        return redirect(url_for('main.delete_product'))

    products = Product.query.all()

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('delete_product.html', products=products, cart_count=cart_count, notification_count=notification_count)


@main.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id)
        db.session.add(cart_item)
    db.session.commit()
    flash('商品がカートに追加されました。')
    return redirect(url_for('main.index'))

@main.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    cart_count = sum(item.quantity for item in cart_items)
    notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, orders=orders, cart_count=cart_count, notification_count=notification_count)

@main.route('/place_order', methods=['POST'])
@login_required
def place_order():
    order = Order(user_id=current_user.id)
    db.session.add(order)
    db.session.commit()

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    for item in cart_items:
        order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
        db.session.add(order_item)
        db.session.delete(item)
    db.session.commit()

    flash('注文が完了しました。')
    return redirect(url_for('main.cart'))

# 注文のキャンセル
@main.route('/cancel_order/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)
    if order.status != 'pending':
        flash('注文がすでに確定または発送されているため、取り消しできません。')
    else:
        order.status = 'cancelled'
        db.session.commit()
        flash('注文が取り消されました。')
    return redirect(url_for('main.cart'))

@main.route('/confirm_order/<int:order_id>', methods=['POST'])
@login_required
def confirm_order(order_id):
    if not current_user.is_admin:
        abort(403)
    order = Order.query.get_or_404(order_id)
    order.status = 'confirmed'
    db.session.commit()

    notification = Notification(user_id=order.user_id, subject='注文確定のお知らせ', message=f'注文 #{order.id} が確定されました。')
    db.session.add(notification)
    db.session.commit()

    flash('注文が確定されました。')
    return redirect(url_for('main.order_list'))

@main.route('/ship_order/<int:order_id>', methods=['POST'])
@login_required
def ship_order(order_id):
    if not current_user.is_admin:
        abort(403)
    order = Order.query.get_or_404(order_id)
    order.status = 'shipped'
    db.session.commit()

    notification = Notification(user_id=order.user_id, subject='注文発送のお知らせ', message=f'注文 #{order.id} が発送されました。')
    db.session.add(notification)
    db.session.commit()

    flash('注文が発送されました。')
    return redirect(url_for('main.order_list'))

@main.route('/order_list')
@login_required
def order_list():
    if not current_user.is_admin:
        abort(403)
    orders = Order.query.all()

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('order_list.html', orders=orders, cart_count=cart_count, notification_count=notification_count)

@main.route('/order_detail/<int:order_id>')
@login_required
def order_detail(order_id):
    if not current_user.is_admin:
        abort(403)
    order = Order.query.get_or_404(order_id)

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('order_detail.html', order=order, cart_count=cart_count, notification_count=notification_count)

@main.route('/notifications')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('notifications.html', notifications=notifications, cart_count=cart_count, notification_count=notification_count)

@main.route('/mark_as_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_as_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        abort(403)
    notification.is_read = True
    db.session.commit()
    return redirect(url_for('main.notifications'))

@main.route('/submit_inquiry', methods=['GET', 'POST'])
@login_required
def submit_inquiry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        inquiry = Inquiry(user_id=current_user.id, title=title, content=content)
        db.session.add(inquiry)
        db.session.commit()
        flash('お問い合わせが送信されました。')
        return redirect(url_for('main.index'))

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('submit_inquiry.html', cart_count=cart_count, notification_count=notification_count)

@main.route('/inquiry_list')
@login_required
def inquiry_list():
    if not current_user.is_admin:
        abort(403)
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('inquiry_list.html', inquiries=inquiries, cart_count=cart_count, notification_count=notification_count)

@main.route('/inquiry_detail/<int:inquiry_id>')
@login_required
def inquiry_detail(inquiry_id):
    if not current_user.is_admin:
        abort(403)
    inquiry = Inquiry.query.get_or_404(inquiry_id)

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('inquiry_detail.html', inquiry=inquiry, cart_count=cart_count, notification_count=notification_count)

@main.route('/update_inquiry_status/<int:inquiry_id>', methods=['POST'])
@login_required
def update_inquiry_status(inquiry_id):
    if not current_user.is_admin:
        abort(403)
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    inquiry.status = request.form['status']
    db.session.commit()
    return redirect(url_for('main.inquiry_list'))

@main.route('/send_notification', methods=['GET', 'POST'])
@login_required
def send_notification():
    if not current_user.is_admin:
        abort(403)

    if request.method == 'POST':
        user_id = request.form['user_id']
        subject = request.form['subject']
        message = request.form['message']

        if user_id == 'all':
            users = User.query.all()
        else:
            users = [User.query.get(user_id)]

        for user in users:
            notification = Notification(user_id=user.id, subject=subject, message=message)
            db.session.add(notification)
        db.session.commit()

        flash('通知が送信されました。')
        return redirect(url_for('main.send_notification'))

    users = User.query.all()

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('send_notification.html', users=users, cart_count=cart_count, notification_count=notification_count)

@main.route('/add_to_favorites/<int:product_id>', methods=['POST'])
@login_required
def add_to_favorites(product_id):
    product = Product.query.get_or_404(product_id)
    favorite = Favorite.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not favorite:
        favorite = Favorite(user_id=current_user.id, product_id=product_id)
        db.session.add(favorite)
        db.session.commit()
        flash('商品がお気に入りに追加されました。')
    else:
        flash('この商品は既にお気に入りに追加されています。')
    return redirect(url_for('main.index'))

@main.route('/favorites')
@login_required
def favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('favorites.html', favorites=favorites, cart_count=cart_count, notification_count=notification_count)

@main.route('/submit_review/<int:product_id>', methods=['GET', 'POST'])
@login_required
def submit_review(product_id):
    product = Product.query.get_or_404(product_id)
    ordered_products = [item.product for order in current_user.orders for item in order.items]
    if product not in ordered_products:
        flash('注文済みの商品のみレビューを投稿できます。')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        content = request.form['content']
        rating = int(request.form['rating'])
        review = Review(user_id=current_user.id, product_id=product_id, content=content, rating=rating)
        db.session.add(review)
        db.session.commit()
        flash('レビューが投稿されました。')
        return redirect(url_for('main.product_detail', product_id=product_id))

    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('submit_review.html', product=product, cart_count=cart_count, notification_count=notification_count)


@main.route('/product_reviews/<int:product_id>')
def product_reviews(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).all()

    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('product_reviews.html', product=product, reviews=reviews, cart_count=cart_count, notification_count=notification_count)

@main.route('/product_detail/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()

    cart_count = 0
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    notification_count = 0
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('product_detail.html', product=product, reviews=reviews, cart_count=cart_count, notification_count=notification_count)

@main.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    if request.method == 'POST':
        review.content = request.form['content']
        review.rating = int(request.form['rating'])
        db.session.commit()
        flash('レビューが更新されました。')
        return redirect(url_for('main.product_detail', product_id=review.product_id))

    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('edit_review.html', review=review, cart_count=cart_count, notification_count=notification_count)

@main.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    # 関連する ReviewLike レコードを削除
    ReviewLike.query.filter_by(review_id=review_id).delete()
    # 関連する ReviewComment レコードを削除
    ReviewComment.query.filter_by(review_id=review_id).delete()

    db.session.delete(review)
    db.session.commit()
    flash('レビューが削除されました。')
    return redirect(url_for('main.product_detail', product_id=review.product_id))

@main.route('/submit_review_comment/<int:review_id>', methods=['POST'])
@login_required
def submit_review_comment(review_id):
    review = Review.query.get_or_404(review_id)
    content = request.form['content']
    comment = ReviewComment(review_id=review_id, user_id=current_user.id, content=content)
    db.session.add(comment)
    db.session.commit()
    flash('コメントが投稿されました。')
    return redirect(url_for('main.product_detail', product_id=review.product_id))

@main.route('/like_review/<int:review_id>', methods=['POST'])
@login_required
def like_review(review_id):
    review = Review.query.get_or_404(review_id)
    like = ReviewLike.query.filter_by(review_id=review_id, user_id=current_user.id).first()
    if not like:
        like = ReviewLike(review_id=review_id, user_id=current_user.id)
        db.session.add(like)
        db.session.commit()
    return redirect(url_for('main.product_detail', product_id=review.product_id))

@main.route('/admin/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_review(review_id):
    if not current_user.is_admin:
        abort(403)

    review = Review.query.get_or_404(review_id)
    if request.method == 'POST':
        review.content = request.form['content']
        review.rating = int(request.form['rating'])
        db.session.commit()
        flash('レビューが更新されました。')
        return redirect(url_for('main.product_detail', product_id=review.product_id))

    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return render_template('admin_edit_review.html', review=review, cart_count=cart_count, notification_count=notification_count)

@main.route('/admin/delete_review/<int:review_id>', methods=['POST'])
@login_required
def admin_delete_review(review_id):
    if not current_user.is_admin:
        abort(403)

    review = Review.query.get_or_404(review_id)

    # 関連する ReviewLike レコードを削除
    ReviewLike.query.filter_by(review_id=review_id).delete()
    # 関連する ReviewComment レコードを削除
    ReviewComment.query.filter_by(review_id=review_id).delete()

    db.session.delete(review)
    db.session.commit()
    flash('レビューが削除されました。')
    return redirect(url_for('main.product_detail', product_id=review.product_id))

@main.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    if cart_item.user_id != current_user.id:
        abort(403)
    db.session.delete(cart_item)
    db.session.commit()
    flash('商品がカートから削除されました。')
    return redirect(url_for('main.cart'))

@main.route('/cancel_order_item/<int:order_item_id>', methods=['POST'])
@login_required
def cancel_order_item(order_item_id):
    order_item = OrderItem.query.get_or_404(order_item_id)
    if order_item.order.user_id != current_user.id:
        abort(403)
    if order_item.order.status != 'pending':
        flash('注文がすでに確定または発送されているため、取り消しできません。')
        return redirect(url_for('main.cart'))
    db.session.delete(order_item)
    db.session.commit()
    flash('注文アイテムが取り消されました。')
    return redirect(url_for('main.cart'))

@main.route('/update_quantity/<int:cart_item_id>', methods=['POST'])
@login_required
def update_quantity(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    if cart_item.user_id != current_user.id:
        abort(403)
    new_quantity = int(request.form['quantity'])
    if new_quantity > 0:
        cart_item.quantity = new_quantity
        db.session.commit()
        flash('数量が更新されました。')
    else:
        db.session.delete(cart_item)
        db.session.commit()
        flash('商品がカートから削除されました。')
    return redirect(url_for('main.cart'))