from flask import Blueprint, render_template, request, abort
import requests, base64

bp = Blueprint('film', __name__, url_prefix='/film')

@bp.route('/event', methods=['GET'])
def event():
    return render_template('event.html')

# 스토어

@bp.route('/store', methods=['GET'])
def store():
    return render_template('store.html')

# 상품페이지
# 관람권

@bp.route('/store/redticket', methods=['GET'])
def store_redticket():
    return render_template('store_redticket.html')

@bp.route('/store/vipticket', methods=['GET'])
def store_vipticket():
    return render_template('store_vipticket.html')

# 스낵음료

@bp.route('/store/bestcombo', methods=['GET'])
def store_bestcombo():
    return render_template('store_bestcombo.html')

@bp.route('/store/singlecombo', methods=['GET'])
def store_singlecombo():
    return render_template('store_singlecombo.html')

@bp.route('/store/snacksvoucher', methods=['GET'])
def store_snacksvoucher():
    return render_template('store_snacksvoucher.html')

@bp.route('/store/popcorn_large', methods=['GET'])
def store_popcorn_large():
    return render_template('store_popcorn_large.html')

@bp.route('/store/popcorn_medium', methods=['GET'])
def store_popcorn_medium():
    return render_template('store_popcorn_medium.html')

@bp.route('/store/selfdrink', methods=['GET'])
def store_selfdrink():
    return render_template('store_selfdrink.html')

# 굿즈
# 진격의거인

@bp.route('/store/jin_eren', methods=['GET'])
def store_jin_eren():
    return render_template('store_jin_eren.html')

@bp.route('/store/jin_mikasa', methods=['GET'])
def store_jin_mikasa():
    return render_template('store_jin_mikasa.html')

@bp.route('/store/jin_levi', methods=['GET'])
def store_jin_levi():
    return render_template('store_jin_levi.html')

# 체인소 맨

@bp.route('/store/chain_denji', methods=['GET'])
def store_chain_denji():
    return render_template('store_chain_denji.html')

@bp.route('/store/chain_makima', methods=['GET'])
def store_chain_makima():
    return render_template('store_chain_makima.html')


@bp.route('/store/chain_reje', methods=['GET'])
def store_chain_reje():
    return render_template('store_chain_reje.html')

# 귀멸의 칼날

@bp.route('/store/ds_holo_buttonbadge', methods=['GET'])
def store_ds_holo_buttonbadge():
    return render_template('store_ds_holo_buttonbadge.html')

@bp.route('/store/ds_char_buttonbadge', methods=['GET'])
def store_ds_char_buttonbadge():
    return render_template('store_ds_char_buttonbadge.html')

@bp.route('/store/ds_grap_buttonbadge', methods=['GET'])
def store_ds_grap_buttonbadge():
    return render_template('store_ds_grap_buttonbadge.html')

# 스토어 결제
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

@bp.route('/movie/list', methods=['GET'])
def movie_list():
    return render_template('movie_list.html')

@bp.route('/movie/list/info/<int:movie_id>', methods=['GET'])
def movie_info(movie_id):
    return render_template('movie_info/movie_info_1.html', movie_id=movie_id)

@bp.route('/booking', methods=['GET','POST'])
def booking():
    return render_template('booking.html')

@bp.route('/person/seat', methods=['GET','POST'])
def person_seat():
    return render_template('person_seat.html')

