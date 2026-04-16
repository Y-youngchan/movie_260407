from flask import Blueprint, render_template, request, abort
import requests

bp = Blueprint('film', __name__, url_prefix='/film')

@bp.route('/event', methods=['GET'])
def event():
    return render_template('event.html')

@bp.route('/store', methods=['GET'])
def store():
    return render_template('store.html')

@bp.route('/store/redticket', methods=['GET'])
def store_redticket():
    return render_template('store_redticket.html')

@bp.route('/store/vipticket', methods=['GET'])
def store_vipticket():
    return render_template('store_vipticket.html')

@bp.route('/store/bestcombo', methods=['GET'])
def store_bestcombo():
    return render_template('store_bestcombo.html')

@bp.route('/store/pay', methods=['GET'])
def store_pay():
    product_id = request.args.get('product_id', type=int)

    products = {
        1: {
            "name": "일반 관람권(2D)",
            "price": 18000,
            "image": "img/redticket.png",
            "detail": "일반 관람권(2D) 1매"
        },

        2: {
            "name": "VIP 관람권",
            "price": 25000,
            "image": "img/blackticket.png",
            "detail": "VIP 관람권 1매"
        },

        3: {
            "name": "BEST COMBO 교환권",
            "price": 25000,
            "image": "img/BEST COMBO 교환권.png",
            "detail": "반반콤보 or 싱글스낵콤보 중 택1"
        }
    }

    product = products.get(product_id)

    if not product:
        abort(404)

    return render_template('store_pay.html', product=product)

@bp.route('/confirm', methods=['POST'])
def confirm():
    data = request.json

    url = "https://api.tosspayments.com/v1/payments/confirm"

    headers = {
        "Authorization": "Basic YOUR_SECRET_KEY"
    }

    body = {
        "paymentKey": data['paymentKey'],
        "orderId": data['orderId'],
        "amount": data['amount']
    }

    res = requests.post(url, json=body, headers=headers)
    return res.json()

@bp.route('/store/pay/success')
def success():
    paymentKey = request.args.get('paymentKey')
    orderId = request.args.get('orderId')
    amount = request.args.get('amount')

    return f"결제 성공! {orderId}"

@bp.route('/store/pay/fail')
def fail():
    return "결제 실패"

@bp.route('/movie/list', methods=['GET'])
def movie_list():
    return render_template('movie_list.html')

@bp.route('/movie/list/info/<int:movie_id>', methods=['GET'])
def movie_info(movie_id):
    return render_template('movie_info/movie_info_1.html', movie_id=movie_id)

@bp.route('/booking', methods=['GET','POST'])
def booking():
    return render_template('booking.html')

