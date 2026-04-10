from flask import Blueprint, url_for, redirect, render_template

from pybo.forms import UserCreateForm

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    form = UserCreateForm()
    return render_template('signup.html', form=form)