from flask import Blueprint, render_template, request, redirect, abort, url_for, session, jsonify

from pybo import db
from pybo.models import Product, Order, User, Payment
from pybo.views.auth_views import login_required
from datetime import datetime, timezone, timedelta

import uuid, requests, base64

bp = Blueprint('store', __name__, url_prefix='/store')

@bp.route("/main")
def store_main():
    products = Product.query.all()
    return render_template("store.html", products=products)

@bp.route("/product/<int:id>")
def product(id):
    product = Product.query.get_or_404(id)
    return render_template("product.html", product=product)

# 주문 생성
@bp.route('/order/create/<int:product_id>')
@login_required
def create_order(product_id):

    user = User.query.get(session.get("user_id"))
    product = Product.query.get_or_404(product_id)

    # 품절 상품 구매 차단
    if product.status == 'soldout':
        return "<script>alert('품절된 상품은 구매할 수 없습니다.'); location.href='/store/main';</script>"

    quantity = int(request.args.get('quantity', 1))

    total_price = product.Productprice * quantity

    order = Order(
        user_id=user.id,
        user_name=user.username,
        user_userid=user.userid,
        product_id=product.id,
        product_name=product.Productname,
        quantity=quantity,
        total_price=total_price,
        order_code=f"order_{product_id}_{user.id}_{uuid.uuid4().hex[:8]}"
    )

    db.session.add(order)
    db.session.commit()

    return redirect(url_for('store.store_pay', order_id=order.order_code))

@bp.route('/pay')
def store_pay():
    order_id = request.args.get('order_id')

    order = Order.query.filter_by(order_code=order_id).first_or_404()
    payment = Payment.query.filter_by(order_id=order.id).first()

    if not payment:
        payment = Payment(
            order_id=order.id,
            order_code=order.order_code,
            amount=order.total_price,
            status="READY"
        )
        db.session.add(payment)
        db.session.commit()

    return render_template('store_pay.html', order=order)

@bp.route('/pay/success')
def pay_success():
    order_code = request.args.get("order_id")

    # 토스에서 오는 값
    payment_key = request.args.get("paymentKey")
    method = request.args.get("method")

    order = Order.query.filter_by(order_code=order_code).first_or_404()
    payment = Payment.query.filter_by(order_id=order.id).first()

    # Payment 업데이트
    payment.payment_key = payment_key
    payment.method = method
    payment.status = "SUCCESS"
    payment.approved_at = datetime.now(timezone.utc)

    # Order도 성공 처리
    order.status = "SUCCESS"

    db.session.commit()

    return render_template('storepay_success.html', order=order)

@bp.route('/pay/fail')
def pay_fail():
    order_code = request.args.get("order_id")

    order = Order.query.filter_by(order_code=order_code).first()

    if order:
        payment = Payment.query.filter_by(order_id=order.id).first()

        if payment:
            payment.status = "FAIL"

        order.status = "FAIL"
        db.session.commit()

    return f"결제 실패 (order_id={order_code})"


@bp.route('/pay/cancel/<int:order_id>', methods=['POST'])
@login_required
def cancel_payment(order_id):

    order = Order.query.get_or_404(order_id)
    payment = Payment.query.filter_by(order_id=order.id).first()

    if not payment:
        return jsonify({"message": "결제 정보 없음"}), 400

    if payment.status != "SUCCESS":
        return jsonify({"message": "취소 불가 상태"}), 400

    # 70일 제한 (선택)
    if payment.approved_at:
        now = datetime.now(timezone.utc)
        approved_at = payment.approved_at.replace(tzinfo=timezone.utc) \
            if payment.approved_at.tzinfo is None else payment.approved_at

        if now > approved_at + timedelta(days=70):
            return jsonify({"message": "취소 기간 초과"}), 400

    # 🔥 토스 없이 DB만 처리
    payment.status = "CANCELLED"
    order.status = "CANCELLED"

    db.session.commit()

    return jsonify({"message": "취소 완료"})