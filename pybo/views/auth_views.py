from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, Flask
from werkzeug.security import generate_password_hash, check_password_hash

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User, Product
import functools

bp=Blueprint('auth',__name__, url_prefix='/auth')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserCreateForm()

    if request.method == 'POST' and form.validate_on_submit():
        existing_user = User.query.filter_by(userid=form.userid.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash('이미 존재하는 아이디입니다.')
        elif existing_email:
            flash('이미 존재하는 이메일입니다.')
        else:
            user = User(
                userid=form.userid.data,
                username=form.username.data,
                password=generate_password_hash(form.password1.data),
                email=form.email.data,
                phone=form.phone.data.replace('-', ''),
                birth=datetime.strptime(form.birth.data, "%Y-%m-%d").date(),
                Terms_of_Service=form.Terms_of_Service.data,
                Privacy_Policy=form.Privacy_Policy.data,
                receive_emails=form.receive_emails.data
            )
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(userid=form.userid.data).first()

        if not user:
            error = '존재하지 않는 아이디입니다.'

        elif not check_password_hash(user.password, form.password.data):
            error = '비밀번호가 올바르지 않습니다.'

        if error is None:
            session.clear()
            session['user_id'] = user.id

            # 휴면회원 체크
            if user.status == 'sleep':
                return redirect(url_for('auth.sleep_member'))

            # 관리자
            if user.is_admin:
                return redirect(url_for('auth.admin'))

            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

#라우팅 함수보다 먼저 실행
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.get(User, user_id)

# 데코레이션 함수
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):

        # 로그인 안 된 경우
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))

        # 휴면회원 강제 이동
        if g.user.status == 'sleep':
            allow_pages = [
                'auth.sleep_member',
                'auth.wake_member',
                'auth.logout'
            ]

            if request.endpoint not in allow_pages:
                return redirect(url_for('auth.sleep_member'))

        return view(*args, **kwargs)

    return wrapped_view

# =====================
# 휴면회원 안내 페이지
# =====================
@bp.route('/sleep-member')
@login_required
def sleep_member():

    if g.user.status != 'sleep':
        return redirect(url_for('main.index'))

    return render_template('auth/sleep_member.html')

# =====================
# 휴면회원 해제
# =====================
@bp.route('/wake-member')
@login_required
def wake_member():

    if g.user.status == 'sleep':
        g.user.status = 'normal'
        db.session.commit()

    flash('휴면회원이 해제되었습니다.')
    return redirect(url_for('main.index'))


# ===========================
# 관리자 페이지
# ===========================

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):

        # 로그인 안 된 경우 로그인 페이지 이동
        if g.user is None:
            return redirect(url_for('auth.login'))

        # 관리자 계정이 아닌 경우 메인페이지 이동
        if not g.user.is_admin:
            flash('관리자만 접근 가능합니다.')
            return redirect(url_for('main.index'))

        return view(*args, **kwargs)

    return wrapped_view


# ===========================
# 슈퍼 관리자 전용 데코레이터
# admin_role = super 만 허용
# ===========================

def super_admin_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):

        # 로그인 안 했으면 로그인 페이지 이동
        if g.user is None:
            return redirect(url_for('auth.login'))

        # 관리자 계정이 아닌 경우
        if not g.user.is_admin:
            flash('권한이 없습니다.')
            return redirect(url_for('main.index'))

        # 관리자지만 슈퍼 관리자가 아닐 경우
        if g.user.admin_role != 'super':
            flash('권한이 없습니다.')
            return redirect(url_for('auth.admin'))

        return view(*args, **kwargs)

    return wrapped_view


# ==================================================
# 관리자 페이지
# 모든 관리자 접근 가능
# super / manager 둘 다 가능
# ==================================================

@bp.route('/admin')
@login_required
@admin_required
def admin():

    keyword = request.args.get('keyword', '')

    users = User.query.filter(
        User.username.contains(keyword) |
        User.email.contains(keyword)
    ).all()

    admins = User.query.filter_by(is_admin=True).all()

    products = Product.query.filter(
        Product.Productname.contains(keyword)
    ).all()

    total_users = User.query.count()
    normal_users = User.query.filter_by(status='normal').count()
    sleep_users = User.query.filter_by(status='sleep').count()

    soldout_products = Product.query.filter_by(status='soldout').count()
    normal_products = Product.query.filter_by(status='normal').count()

    return render_template(
        'admin.html',
        users=users,
        admins=admins,
        products=products,

        total_users=total_users,
        normal_users=normal_users,
        sleep_users=sleep_users,

        soldout_products=soldout_products,
        normal_products=normal_products
    )

# ==================================================
# 회원 상태 변경
# super / manager 둘 다 가능
# ==================================================

@bp.route('/admin/user/<int:user_id>/status')
@login_required
@admin_required
def change_user_status(user_id):

    user = User.query.get_or_404(user_id)

    if user.status == 'normal':
        user.status = 'sleep'
    else:
        user.status = 'normal'

    db.session.commit()

    flash('회원 상태가 변경되었습니다.')
    return redirect(url_for('auth.admin'))


# ==================================================
# 관리자 권한 부여
# 슈퍼 관리자만 가능
# ==================================================

@bp.route('/admin/user/<int:user_id>/grant-admin')
@login_required
@super_admin_required
def grant_admin(user_id):

    user = User.query.get_or_404(user_id)

    user.is_admin = True
    user.admin_role = 'manager'

    db.session.commit()

    flash('관리자 권한이 부여되었습니다.')
    return redirect(url_for('auth.admin'))


# ==================================================
# 관리자 권한 해제
# 슈퍼 관리자만 가능
# ==================================================

@bp.route('/admin/user/<int:user_id>/remove-admin')
@login_required
@super_admin_required
def remove_admin(user_id):

    user = User.query.get_or_404(user_id)

    if user.id == g.user.id:
        flash('본인 계정은 권한 해제할 수 없습니다.')
        return redirect(url_for('auth.admin'))

    if user.admin_role == 'super':
        flash('슈퍼관리자는 해제할 수 없습니다.')
        return redirect(url_for('auth.admin'))

    user.is_admin = False
    user.admin_role = None

    db.session.commit()

    flash('관리자 권한이 해제되었습니다.')
    return redirect(url_for('auth.admin'))

# ==========================
# 공지사항 관리자 권한
# super / manager 허용
# ==========================
def notice_admin_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):

        if g.user is None:
            return redirect(url_for('auth.login'))

        if not g.user.is_admin:
            flash('권한이 없습니다.')
            return redirect(url_for('main.index'))

        if g.user.admin_role not in ['super', 'manager']:
            flash('권한이 없습니다.')
            return redirect(url_for('main.index'))

        return view(*args, **kwargs)

    return wrapped_view

# 상품 관리 함수
@bp.route('/admin/product/<int:product_id>/status')
@login_required
@admin_required
def change_product_status(product_id):

    product = Product.query.get_or_404(product_id)

    if product.status == 'normal':
        product.status = 'soldout'
    else:
        product.status = 'normal'

    db.session.commit()

    flash('상품 상태가 변경되었습니다.')
    return redirect(url_for('auth.admin'))