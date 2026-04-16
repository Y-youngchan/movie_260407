from flask import Blueprint, render_template

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

@bp.route('/store/pay', methods=['GET'])
def store_pay():
    return render_template('store_pay.html')

@bp.route('/movie/list', methods=['GET'])
def movie_list():
    return render_template('movie_list.html')

@bp.route('/movie/list/info/<int:movie_id>', methods=['GET'])
def movie_info(movie_id):
    return render_template('movie_info/movie_info_1.html', movie_id=movie_id)

@bp.route('/booking', methods=['GET','POST'])
def booking():
    return render_template('booking.html')

