from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.recaptcha import RecaptchaField

app = Flask(__name__)
app.secret_key = "6LfP8_EpAAAAAEnJ10d9q34jk8Ys0rvxsurTrTPc"
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfP8_EpAAAAABCFL1ra8cxW9xqQyhLb5zYI8rUc'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfP8_EpAAAAABCFL1ra8cxW9xqQyhLb5zYI8rUc'

# Formulário com CAPTCHA
class CaptchaForm(FlaskForm):
    recaptcha = RecaptchaField()
    submit = SubmitField('Verificar CAPTCHA')

# Formulário de senha
class PasswordForm(FlaskForm):
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Acessar')

@app.route('/', methods=['GET', 'POST'])
def index():
    captcha_form = CaptchaForm()
    if captcha_form.validate_on_submit():
        session['captcha_verified'] = True
        return redirect(url_for('password'))
    return render_template('index.html', form=captcha_form)

@app.route('/password', methods=['GET', 'POST'])
def password():
    if not session.get('captcha_verified'):
        return redirect(url_for('index'))
    
    password_form = PasswordForm()
    if password_form.validate_on_submit():
        if password_form.password.data == 'pixelpulse123':
            return redirect(url_for('content'))
        else:
            flash('Senha incorreta. Tente novamente.')
    return render_template('password.html', form=password_form)

@app.route('/content')
def content():
    if not session.get('captcha_verified'):
        return redirect(url_for('index'))
    return "Bem-vindo ao conteúdo do site!"

if __name__ == '__main__':
    app.run(debug=True)
