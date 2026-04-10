from flask import Blueprint, url_for, redirect, render_template

from pybo.forms import UserCreateForm

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('customerservice/question_list.html')

