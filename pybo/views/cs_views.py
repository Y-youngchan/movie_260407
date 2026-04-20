import os
from datetime import datetime
from idlelib import query

from flask import Blueprint, render_template, request, redirect, url_for


from pybo.models import Faq
from pybo import db
from pybo.forms import NoticeForm, AnswerForm, ReviewForm
from pybo.models import Notice
from pybo.models import Review


bp = Blueprint('cs',__name__, url_prefix='/cs')

# notice_list
@bp.route("/notice/notice_list/")
def notice_list():
    page = request.args.get('page', type=int, default=1)

    notice_list = Notice.query.order_by(Notice.create_date.desc())

    notice_list = notice_list.paginate(page=page, per_page=15)  # 한페이지에 보여야할 게시물

    return render_template("cs/notice/notice_list.html",notice_list=notice_list)

# notice_detail
@bp.route("/notice/detail/<int:notice_id>")
def notice_detail(notice_id):
    notice_detail = Notice.query.get(notice_id)
    prev_notice = Notice.query.get(notice_id - 1)
    next_notice = Notice.query.get(notice_id + 1)
    return render_template("cs/notice/notice_detail.html", notice=notice_detail, prev_notice=prev_notice, next_notice=next_notice)

@bp.route("/faq/")
def faq_list():
    page = request.args.get('page', type=int, default=1)
    faq_list = Faq.query.order_by(Faq.create_date.desc())
    faq_list = faq_list.paginate(page=page, per_page=10)
    print(faq_list)
    return render_template("cs/faq/faq.html", faq_list=faq_list)

@bp.route("/review/")
def review_list():
    page = request.args.get('page', type=int, default=1)
    review_list = Review.query.all()
    return render_template("cs/review/review.html", review_list=review_list)

@bp.route('/review/create/')
def review_create():
    form = ReviewForm()
    return render_template('cs/review/review_form.html', review_create=review_create,form=form)



