from flask import (
    Flask, request, render_template, redirect,
    url_for, flash, get_flashed_messages, session
)
import flask_example.db as db
from flask_example.validator import validate
from json import loads, dumps


app = Flask(__name__)
app.secret_key = "secret_key"


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    current_user = session.get('user')
    return render_template(
        'index.html',
        messages=messages,
        current_user=current_user,
        )


@app.post('/login')
def login():
    users = loads(request.cookies.get('users', dumps([])))
    form_data = request.form.to_dict()
    name, email = form_data['name'], form_data['email']
    for user in users:
        if user['name'] == name and user['email'] == email:
            session['user'] = user
            break
    else:
        flash('Wrong password or name', 'Error')
    return redirect(url_for('index'))


@app.route('/logout', methods=['POST', 'DELETE'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/users/', methods=['GET', 'POST'])
def users():
    users = loads(request.cookies.get('users', dumps([])))
    if request.method == 'GET':
        messages = get_flashed_messages(with_categories=True)
        term = request.args.get('term', '')
        filtered_users = list(filter(lambda x: term in x['name'], users))
        return render_template(
            'users/index.html',
            users=filtered_users,
            search=term,
            messages=messages
        )
    if request.method == 'POST':
        new_user = request.form.to_dict()
        errors = validate(new_user)
        if errors:
            return render_template(
                'users/new.html',
                user=new_user,
                errors=errors
            ), 422
        db.create(users, new_user)
        flash(f'New user {new_user["name"]} was created!', 'success')
        response = redirect(url_for('users'))
        response.set_cookie('users', dumps(users))
        return response


@app.get('/users/<id>')
def get_user(id):
    users = loads(request.cookies.get('users', dumps([])))
    user = db.get_user(users, int(id))
    if user is None:
        return "User not found", 404
    return render_template(
        'users/show.html',
        user=user
    )


@app.get('/users/new')
def new_user():
    return render_template(
        'users/new.html',
        user={'name': '', 'email': ''},
        errors={}
    )


@app.route('/users/<id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    users = loads(request.cookies.get('users', dumps([])))

    if request.method == 'GET':
        user = db.get_user(users, int(id))
        if user is None:
            return "User not found", 404
        return render_template(
            'users/edit.html',
            user=user,
            errors={},
        )

    if request.method == 'POST':
        user = request.form.to_dict()
        errors = validate(user)
        if errors:
            return render_template(
                'users/edit.html',
                user=user,
                errors=errors,
            ), 422
        db.patch(users, user, int(id))
        flash('User has been updated', 'success')
        response = redirect(url_for('users'))
        response.set_cookie('users', dumps(users))
        return response


@app.route('/users/<id>/delete', methods=['GET', 'POST'])
def delete_user(id):
    users = loads(request.cookies.get('users', dumps([])))

    if request.method == 'GET':
        return render_template(
            'users/delete.html',
            id=id,
            current_user=session.get('user')
        )
    if request.method == 'POST':
        db.delete(users, int(id))
        flash('User has been deleted', 'success')
        response = redirect(url_for('users'))
        response.set_cookie('users', dumps(users))
        return response
