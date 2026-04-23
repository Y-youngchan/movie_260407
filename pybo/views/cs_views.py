import os
from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash, g, abort

from werkzeug.utils import secure_filename

from pybo.models import Faq, Review, Notice, User
from pybo import db
from pybo.forms import NoticeForm, ReviewForm
from pybo.views.auth_views import login_required



bp = Blueprint('cs', __name__, url_prefix='/cs')


# ==================================================
# 공지사항 관리자 권한 체크 (추가)
# super / manager 만 허용
# ==================================================
def notice_admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if g.user is None:
            flash('로그인이 필요합니다.')
            return redirect(url_for('auth.login'))

        if g.user.admin_role not in ['super', 'manager']:
            flash('관리자 권한이 없습니다.')
            return redirect(url_for('main.index'))

        return view(*args, **kwargs)

    return wrapped_view


# notice_list
@bp.route("/notice/notice_list/")
def notice_list():
    page = request.args.get('page', type=int, default=1)

    notice_list=Notice.query.order_by(Notice.created_date.desc())


    notice_list = notice_list.paginate(page=page, per_page=15)  # 한페이지에 보여야할 게시물

    return render_template("cs/notice/notice_list.html", notice_list=notice_list)


# notice_detail
@bp.route("/notice/detail/<int:notice_id>")
def notice_detail(notice_id):
  
    notice = Notice.query.get_or_404(notice_id)

    # 이전 글 (현재 글보다 id 작은 것 중 가장 큰 값)
    prev_notice = Notice.query.filter(
        Notice.id < notice_id
    ).order_by(Notice.id.desc()).first()

    # 다음 글 (현재 글보다 id 큰 것 중 가장 작은 값)
    next_notice = Notice.query.filter(
        Notice.id > notice_id
    ).order_by(Notice.id.asc()).first()

    return render_template(
        "cs/notice/notice_detail.html",
        notice=notice,
        prev_notice=prev_notice,
        next_notice=next_notice
    )
# ===============================
# 공지사항 등록
# 관리자만 가능 (추가)
# ===============================
@bp.route('/notice/create/', methods=('GET', 'POST'))
@notice_admin_required
def notice_create():

    form = NoticeForm()

    if request.method == 'POST' and form.validate_on_submit():

        notice = Notice(
            theater=form.theater.data,
            title=form.title.data,
            content=form.content.data,
            create_date=datetime.now()
        )

        db.session.add(notice)
        db.session.commit()

        flash('공지사항이 등록되었습니다.')

        return redirect(url_for('cs.notice_list'))

    return render_template(
        'cs/notice/notice_form.html',
        form=form
    )


# ===============================
# 공지사항 수정
# ===============================
@bp.route('/notice/modify/<int:notice_id>/', methods=('GET', 'POST'))
@notice_admin_required
def notice_modify(notice_id):

    notice = Notice.query.get_or_404(notice_id)
    form = NoticeForm(obj=notice)

    if request.method == 'POST' and form.validate_on_submit():

        notice.theater = form.theater.data
        notice.title = form.title.data
        notice.content = form.content.data

        db.session.commit()

        flash('공지사항이 수정되었습니다.')

        return redirect(
            url_for(
                'cs.notice_detail',
                notice_id=notice.id
            )
        )

    return render_template(
        'cs/notice/notice_form.html',
        form=form
    )


# ===============================
# 공지사항 삭제
# ===============================
@bp.route('/notice/delete/<int:notice_id>/')
@notice_admin_required
def notice_delete(notice_id):

    notice = Notice.query.get_or_404(notice_id)

    db.session.delete(notice)
    db.session.commit()

    flash('공지사항이 삭제되었습니다.')

    return redirect(url_for('cs.notice_list'))


# FAQ
@bp.route("/faq/")
def faq_list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', default='', type=str)
    faq_list = Faq.query.order_by(Faq.create_date.desc())
    faq_list = faq_list.paginate(page=page, per_page=10)

    return render_template("cs/faq/faq.html", faq_list=faq_list)

# FAQ 등록하기
@bp.route('/faq/create/', methods=('GET', 'POST'))
@notice_admin_required
def faq_create():

    if request.method == 'POST':
        faq = Faq(
            kind=request.form['kind'],
            question=request.form['question'],
            answer=request.form['answer'],
            create_date=datetime.now()
        )

        db.session.add(faq)
        db.session.commit()

        flash('FAQ가 등록되었습니다.')
        return redirect(url_for('cs.faq_list'))

    return render_template('cs/faq/faq_form.html', faq=None)

# FAQ 수정하기
@bp.route('/faq/edit/<int:faq_id>/', methods=('GET', 'POST'))
@notice_admin_required
def faq_edit(faq_id):

    faq = Faq.query.get_or_404(faq_id)

    if request.method == 'POST':
        faq.kind = request.form['kind']
        faq.question = request.form['question']
        faq.answer = request.form['answer']

        db.session.commit()

        flash('FAQ가 수정되었습니다.')
        return redirect(url_for('cs.faq_list'))

    return render_template('cs/faq/faq_form.html', faq=faq)

# FAQ 삭제하기
@bp.route('/faq/delete/<int:faq_id>/')
@notice_admin_required
def faq_delete(faq_id):

    faq = Faq.query.get_or_404(faq_id)

    db.session.delete(faq)
    db.session.commit()

    flash('FAQ가 삭제되었습니다.')

    return redirect(url_for('cs.faq_list'))


# 1:1 문의 목록
@bp.route("/review/")
@login_required
def review_list():
    page = request.args.get('page', type=int, default=1)
    review_list=Review.query.order_by(Review.created_date.desc())

    review_list = review_list.paginate(page=page, per_page=10)


    return render_template("cs/review/review.html", review_list=review_list)


# 리뷰 폼 view함수
@bp.route('/review/create/', methods=('GET', 'POST'))
@login_required
def review_create():
    form = ReviewForm()
    if request.method == 'POST' and form.validate_on_submit():
        image_files = form.image.data
        image_paths = []

        # 저장 경로 : 오늘 날짜로 폴더 설정
        today = datetime.now().strftime('%Y%m%d')
        upload_folder = os.path.join(current_app.root_path, 'static/photo', today)
        os.makedirs(upload_folder, exist_ok=True)

        if image_files:
            for image_file in image_files:
                # 파일이 실제로 비어있지 않은지 확인
                if image_file and image_file.filename != '':
                    filename = secure_filename(image_file.filename)
                    file_path = os.path.join(upload_folder, filename)
                    image_file.save(file_path)

                    # DB용 상대 경로 리스트에 추가
                    image_paths.append(f'photo/{today}/{filename}')
        joined_image_paths = ",".join(image_paths) if image_paths else None

        review = Review(
            cs_ask=form.cs_ask.data,
            cs_place=form.cs_place.data,
            subject=form.subject.data,
            content=form.content.data,
            created_date=datetime.now(),
            image_path=joined_image_paths,
            user=g.user
        )

        db.session.add(review)
        db.session.commit()

        return redirect(url_for('cs.review_list'))
    return render_template('cs/review/review_form.html', form=form)

# =====================
#   리뷰 답변
# =====================
@bp.route('/review/answer/<int:review_id>/', methods=('GET', 'POST'))
@notice_admin_required
def review_answer(review_id):

    review = Review.query.get_or_404(review_id)

    if request.method == 'POST':

        review.answer_review = request.form['answer_review']
        review.answer_create_date = datetime.now()
        review.answer_status = 'done'
        review.answer_admin_id = g.user.id

        db.session.commit()

        flash('답변이 등록되었습니다.')

        return redirect(url_for('cs.review_detail', review_id=review.id))

    return render_template('cs/review/review_answer.html', review=review)




# 리뷰 상세
@bp.route('/review/detail/<int:review_id>', methods=['GET'])
@login_required

def review_detail(review_id):
    review = Review.query.get_or_404(review_id)

    # 로그인 안 했으면 차단
    if g.user is None:
        flash('로그인이 필요합니다.')
        return redirect(url_for('auth.login'))

    # 관리자면 통과
    if g.user.admin_role in ['super', 'manager']:
        return render_template(
            'cs/review/review_detail.html',
            review=review
        )


    # 본인 글만 허용
    if review.user != g.user:
        flash('본인이 작성한 문의만 확인 가능합니다.')
        return redirect(url_for('cs.review_list'))

    return render_template(
        'cs/review/review_detail.html',
        review=review
    )