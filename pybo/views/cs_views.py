import os
from datetime import datetime
from idlelib import query

from flask import Blueprint, render_template, request, redirect, url_for

from pybo import db
from pybo.forms import NoticeForm, AnswerForm
from pybo.models import Notice, Answer


bp = Blueprint('cs',__name__, url_prefix='/cs')

# notice_list
@bp.route("/notice/list")
def notice_list():
    page = request.args.get('page', type=int, default=1)


    notice_list = Notice.query.paginate(page=page, per_page=10)  # 한페이지에 보여야할 게시물

    return render_template("cs/notice/notice_list.html", notice_list=notice_list)

# notice_detail
@bp.route("/notice/detail/<int:notice_id>")
def notice_detail(notice_id):
    notice_detail = Notice.query.get(notice_id)
    return render_template("cs/notice/notice_detail.html", notice=notice_detail, notice_detail=notice_detail)