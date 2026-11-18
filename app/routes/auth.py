from flask import Blueprint, request, redirect, url_for
from app.extensions import db
from app.models import User
from werkzeug.security import check_password_hash
from flask import flash
from flask_login import login_user


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.session.scalar(db.select(User).where(User.email == email))

        if not user:
            flash('Usuario não encontrado', 'danger')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password_hash, password):
            flash('Senha incorreta', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)

        return redirect(url_for('home.index'))