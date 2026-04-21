import os
from datetime import datetime


from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename



from pybo.models import Faq
from pybo import db
from pybo.forms import NoticeForm, AnswerForm, ReviewForm
from pybo.models import Notice
from pybo.models import Review

bp = Blueprint('cs', __name__, url_prefix='/cs')


# notice_list
@bp.route("/notice/notice_list/")
def notice_list():
    page = request.args.get('page', type=int, default=1)

    notice_list = Notice.query.order_by(Notice.create_date.desc())

    notice_list = notice_list.paginate(page=page, per_page=15)  # 한페이지에 보여야할 게시물

    return render_template("cs/notice/notice_list.html", notice_list=notice_list)


# notice_detail
@bp.route("/notice/detail/<int:notice_id>")
def notice_detail(notice_id):
    notice_detail = Notice.query.get(notice_id)
    prev_notice = Notice.query.get(notice_id - 1)
    next_notice = Notice.query.get(notice_id + 1)
    return render_template("cs/notice/notice_detail.html", notice=notice_detail, prev_notice=prev_notice,
                           next_notice=next_notice)

# ===============================
# 공지사항 등록 (여기에 추가)
# ===============================
@bp.route('/notice/create/', methods=('GET', 'POST'))
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

        return redirect(url_for('cs.notice_list'))

    return render_template(
        'cs/notice/notice_form.html',
        form=form
    )


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
    review_list=Review.query.order_by(Review.created_date.desc())

    return render_template("cs/review/review.html", review_list=review_list)


# 리뷰 폼 view함수
@bp.route('/review/create/', methods=('GET', 'POST'))
def review_create():

    form = ReviewForm()
    if request.method == 'POST' and form.validate_on_submit():
        image_files = form.image.data,
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
            image_path=joined_image_paths
        )


        db.session.add(review)
        db.session.commit()

        return redirect(url_for('cs.review_list', review_id=review.id))
    return render_template('cs/review/review_form.html', form=form)

@bp.route('/review/detail/<int:review_id>', methods=['GET'])
def review_detail(review_id):
    # form = AnswerForm()
    review = Review.query.get(review_id)
    return render_template("cs/review/review_detail.html", review=review)





