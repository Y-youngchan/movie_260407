from flask import Blueprint, render_template, request

from pybo import db
from pybo.models import Notice


bp = Blueprint('cs',__name__, url_prefix='/cs')

@bp.route("/notice/list", methods=['GET'])
def notice_list():
    # page = request.args.get('page', type=int, default=1)

    notice_list = Notice.query\
        .order_by(Notice.create_date.desc())
        # .paginate(page=page, per_page=10)

    return render_template("cs/notice_list.html", notice_list=notice_list)