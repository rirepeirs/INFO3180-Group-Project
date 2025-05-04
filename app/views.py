"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash, session, abort, send_from_directory
import os, uuid
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func
from werkzeug.utils import secure_filename
from app.models import User, Profile, Favourite
# from app.forms import RegisterForm, LoginForm, ProfileForm #Uncomment when forms are created
from werkzeug.security import check_password_hash


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/register', methods=['POST'])
def register():
    """Accepts user information and saves it to the database."""
    form = RegisterForm()
    if form.validate_on_submit():
        dp = form.photo.data
        filename = secure_filename(dp.filename)
        filename = f"{uuid.uuid4()}_{secure_filename(dp.filename)}"
        new_user = User(
            username=form.username.data,
            password=form.password.data,
            name=form.name.data,
            email=form.email.data,
            photo=filename
        )
        db.session.add(new_user)
        db.session.commit()
        dp.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'Account created'}), 201
    return jsonify(form.errors), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Accepts login credentials as username and password."""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = db.session.execute(db.select(User).filter_by(username=username)).scalars().first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'photo': user.photo,
                'date_joined': user.date_joined.isoformat()
            }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify(form.errors), 400

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout a user."""
    if current_user.is_authenticated:
        logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/profiles', methods=['GET'])
@login_required
def get_profiles():
    """Return all profiles."""
    profiles = db.session.execute(db.select(Profile)).scalars()
    # profiles = current_user.profiles
    # profiles = db.session.execute(db.select(Profile).
    # filter_by(user_id_fk=current_user.id)).scalars().all()
    if profiles:
        result = [{
            'id': profile.id,
            'user_id_fk': profile.user_id_fk,
            'description': profile.description,
            'parish': profile.parish,
            'biography': profile.biography,
            'sex': profile.sex,
            'race': profile.race,
            'birth_year': profile.birth_year,
            'height': profile.height,
            'fav_cuisine': profile.fav_cuisine,
            'fav_colour': profile.fav_colour,
            'fav_school_subject': profile.fav_school_subject,
            'political': profile.political,
            'religious': profile.religious,
            'family_oriented': profile.family_oriented
        } 
        for profile in profiles]
        return jsonify(result), 200
    else:
        return jsonify({'error': 'No existing profile'}), 404

@app.route('/api/profiles', methods=['POST'])
@login_required
def add_profile():
    """Used for adding new profiles."""
    if current_user.can_add_profile():
        form = ProfileForm()
        if form.validate_on_submit():
            new_profile = Profile(
                user_id_fk=current_user.id,
                description=form.description.data,
                parish=form.parish.data,
                biography=form.biography.data,
                sex=form.sex.data,
                race=form.race.data,
                birth_year=form.birth_year.data,
                height=form.height.data,
                fav_cuisine=form.fav_cuisine.data,
                fav_colour=form.fav_colour.data,
                fav_school_subject=form.fav_school_subject.data,
                political=form.political.data,
                religious=form.religious.data,
                family_oriented=form.family_oriented.data
            )
            db.session.add(new_profile)
            db.session.commit()
            return jsonify({'message': 'Profile created successfully'}), 201
        return jsonify(form.errors), 400
    return jsonify({'error': 'Profile limit reached'}), 400

@app.route('/api/profile/<int:profile_id>', methods=['GET'])
@login_required
def get_profile(profile_id):
    """Get Details of a specific profile."""
    profile = db.session.get(Profile, profile_id)
    if profile:
        return jsonify({
            'id': profile.id,
            'user_id_fk': profile.user_id_fk,
            'description': profile.description,
            'parish': profile.parish,
            'biography': profile.biography,
            'sex': profile.sex,
            'race': profile.race,
            'birth_year': profile.birth_year,
            'height': profile.height,
            'fav_cuisine': profile.fav_cuisine,
            'fav_colour': profile.fav_colour,
            'fav_school_subject': profile.fav_school_subject,
            'political': profile.political,
            'religious': profile.religious,
            'family_oriented': profile.family_oriented
        }), 200
    else:
        return jsonify({'error': 'No existing profile'}), 404

@app.route('/api/profiles/<int:user_id>/favourite', methods=['POST'])
@login_required
def add_favourite(user_id):
    """Add user to Favourites for logged in user."""
    # # You cannot view your own profile 
    # if current_user.user_id == user_id:
    #     return jsonify({'error': 'Action not allowed'}), 400
    favourited = db.session.execute(db.select(Favourite).filter_by(user_id_fk=current_user.id, fav_user_id_fk=user_id)).scalars().first()
    if favourited:
        return jsonify({'message': 'Already favourited'}), 200
    new_favourite = Favourite(user_id_fk=current_user.id, fav_user_id_fk=user_id)
    db.session.add(new_favourite)
    db.session.commit()
    return jsonify({'message': 'Added to favourites'}), 201

@app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
@login_required
def get_matches(profile_id):
    """Get a list of all profiles that match a specific criteria stated below."""
    profile = db.session.get(Profile, profile_id)
    matched_profiles = db.session.execute(
        db.select(Profile).filter(
            Profile.id != profile_id,
            Profile.parish == profile.parish,
            Profile.fav_cuisine == profile.fav_cuisine,
            Profile.birth_year.between(profile.birth_year - 5, profile.birth_year + 5)
        )
    ).scalars().all()
    if matched_profiles:
        result = [{
            'id': profile.id,
            'user_id_fk': profile.user_id_fk,
            'description': profile.description,
            'parish': profile.parish,
            'biography': profile.biography,
            'sex': profile.sex,
            'race': profile.race,
            'birth_year': profile.birth_year,
            'height': profile.height,
            'fav_cuisine': profile.fav_cuisine,
            'fav_colour': profile.fav_colour,
            'fav_school_subject': profile.fav_school_subject,
            'political': profile.political,
            'religious': profile.religious,
            'family_oriented': profile.family_oriented
        } 
        for profile in matched_profiles]
        return jsonify(result), 200
    return jsonify({'message': 'No matches'}), 404

@app.route('/api/search', methods=['GET'])
@login_required
def search_profiles():
    """Search for profiles by name, birth year, sex, race, or any
     combination of these four (4) fields; and return JSON results."""
    name = request.args.get('name')
    birth_year = request.args.get('birth_year')
    sex = request.args.get('sex')
    race = request.args.get('race')
    query = db.select(Profile)
    if name:
        query = query.filter(Profile.description.ilike(f"%{name}%"))
    if birth_year:
        query = query.filter(Profile.birth_year == int(birth_year))
    if sex:
        query = query.filter(Profile.sex.ilike(f"%{sex}%"))
    if race:
        query = query.filter(Profile.race.ilike(f"%{race}%"))
    results = db.session.execute(query).scalars().all()
    if results:
        profiles_list = [{
            'id': profile.id,
            'user_id_fk': profile.user_id_fk,
            'description': profile.description,
            'parish': profile.parish,
            'biography': profile.biography,
            'sex': profile.sex,
            'race': profile.race,
            'birth_year': profile.birth_year,
            'height': profile.height,
            'fav_cuisine': profile.fav_cuisine,
            'fav_colour': profile.fav_colour,
            'fav_school_subject': profile.fav_school_subject,
            'political': profile.political,
            'religious': profile.religious,
            'family_oriented': profile.family_oriented
        } for profile in results]
        return jsonify(profiles_list), 200
    return jsonify({'message': 'No profiles found'}), 404

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get Details of a user."""
    user = db.session.get(User, user_id)
    if user:
        data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'photo': user.photo,
            'date_joined': user.date_joined.isoformat()  
        }
        return jsonify({'user': data})
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/users/<int:user_id>/favourites', methods=['GET'])
@login_required
def get_favourites(user_id):
    """Get users that a user has favoured."""
    user = db.session.get(User, user_id)
    favourites = user.favourites
    # favourited = db.session.execute(db.select(Favourite).filter_by(user_id_fk=user_id)).scalars().first()
    if favourites:
        result = [{
                'id': profile.user.id,
                'username': profile.user.username,
                'name': profile.user.name,
                'email': profile.user.email,
                'photo': profile.user.photo
            }
            for profile in favourites]
        return jsonify({'favourites': result}), 200
    return jsonify({'message': 'No favourites added'}), 404

@app.route('/api/users/favourites/<int:N>', methods=['GET'])
def get_top_favourites(N):
    """Get the top N favoured users based on the number of times they were favoured."""
    top_users = db.session.query(
        Favourite.fav_user_id_fk,
        func.count(Favourite.fav_user_id_fk).label('favourite_count')
    ).group_by(Favourite.fav_user_id_fk
    ).order_by(func.count(Favourite.fav_user_id_fk).desc()
    ).limit(N).all()
    if top_users:
        result = []
        for user_id, count in top_users:
            user = db.session.get(User, user_id)
            if user:
                result.append({
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'email': user.email,
                    'photo': user.photo,
                    'favourite_count': count
                })
        return jsonify(result), 200
    return jsonify({'message': 'No favourites found'}), 404

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404