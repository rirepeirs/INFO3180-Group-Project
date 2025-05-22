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
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.models import User, Profile, Favourite
from app.forms import RegisterForm, LoginForm, ProfileForm 
from werkzeug.security import check_password_hash


###
# Routing for your application.
###

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/assets/<path:filename>')
def assets(filename):
    return app.send_static_file(os.path.join('assets', filename))

@app.route('/api/register', methods=['POST'])
def register():
    """Accepts user information and saves it to the database."""
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            return jsonify({'error': 'Email already in use'}), 400        
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
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({'token': access_token, 'user': user.to_dict()}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    return jsonify(form.errors), 400

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout a user."""
    if current_user.is_authenticated:
        logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/profiles', methods=['GET'])
@jwt_required()
def get_profiles():
    """Return all profiles."""
    profiles = db.session.execute(db.select(Profile)).scalars()
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
        return jsonify({'profiles':result}), 200
    else:
        return jsonify({'error': 'No existing profile'}), 404

@app.route('/api/profiles', methods=['POST'])
@jwt_required()
def add_profile():
    print("📥 Received POST /api/profiles")
    user_id = get_jwt_identity()
    print("🟢 JWT identity:", user_id)
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    print("🔵 Incoming JSON keys:", list(data.keys())) 
    print("🔵 Incoming JSON data:", data)
    form = ProfileForm(data=data, meta={'csrf': False})
    print("🔴 Form errors:", form.errors)

    if user.can_add_profile():
        if form.validate():
            new_profile = Profile(
                user_id_fk=user_id,
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
            return jsonify({'message': 'Profile created', 'profile_id': new_profile.id}), 201
        print("Form data:", form.data)
        print("Form errors:", form.errors)
        return jsonify({'message': 'Validation error', 'errors': form.errors}), 422  
    return jsonify({'error': 'Profile limit reached'}), 400


@app.route('/api/profile/<int:profile_id>', methods=['GET'])
@jwt_required()
def get_profile(profile_id):
    viewer_id = get_jwt_identity()

    profile = db.session.execute(
        db.select(Profile).filter_by(id=profile_id)
    ).scalar_one_or_none()

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
            'family_oriented': profile.family_oriented,
            'viewer_id': viewer_id 
        }), 200
    else:
        return jsonify({'error': 'Profile not found'}), 404

@app.route('/api/profiles/<int:user_id>/favourite', methods=['POST'])
@jwt_required()
def add_favourite(user_id):
    """Add user to Favourites for logged in user."""
    current_user_id = get_jwt_identity()
    # # You cannot view your own profile 
    if current_user_id == user_id:
         return jsonify({'error': 'Action not allowed'}), 400
    favourited = db.session.execute(
        db.select(Favourite).filter_by(user_id_fk=current_user_id, fav_user_id_fk=user_id)).scalars().first()
    if favourited:
        return jsonify({'message': 'Already favourited'}), 200
    new_favourite = Favourite(user_id_fk=current_user_id, fav_user_id_fk=user_id)
    db.session.add(new_favourite)
    db.session.commit()
    return jsonify({'message': 'Added to favourites'}), 201

@app.route('/api/profiles/<int:user_id>/favourite', methods=['DELETE'])
@jwt_required()
def remove_favourite(user_id):
    """Remove a user from favourites."""
    current_user_id = get_jwt_identity()

    favourite = db.session.execute(
        db.select(Favourite).filter_by(user_id_fk=current_user_id, fav_user_id_fk=user_id)
    ).scalars().first()

    if not favourite:
        return jsonify({'error': 'Not favourited'}), 404

    db.session.delete(favourite)
    db.session.commit()
    return jsonify({'message': 'Removed from favourites'}), 200


@app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
@jwt_required()
def get_matches(profile_id):
    try:
        # Step 1: Get the requesting profile
        profile = db.session.get(Profile, profile_id)
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404

        current_user_id = profile.user_id_fk

        # Step 2: Find matching profiles, excluding the same profile and same user
        matched_profiles = db.session.execute(
            db.select(Profile).filter(
                Profile.id != profile_id,
                Profile.user_id_fk != current_user_id,
                Profile.parish == profile.parish,
                Profile.fav_cuisine == profile.fav_cuisine,
                Profile.birth_year.between(profile.birth_year - 5, profile.birth_year + 5)
            )
        ).scalars().all()

        # Step 3: Build the result
        result = []
        for match in matched_profiles:
            user = db.session.get(User, match.user_id_fk)
            result.append({
                'id': match.id,
                'user_id_fk': match.user_id_fk,
                'description': match.description,
                'parish': match.parish,
                'biography': match.biography,
                'sex': match.sex,
                'race': match.race,
                'birth_year': match.birth_year,
                'height': match.height,
                'fav_cuisine': match.fav_cuisine,
                'fav_colour': match.fav_colour,
                'fav_school_subject': match.fav_school_subject,
                'political': match.political,
                'religious': match.religious,
                'family_oriented': match.family_oriented,
                'user': {
                    'name': user.name,
                    'username': user.username,
                    'email': user.email,
                    'photo': user.photo
                }
            })

        return jsonify(result), 200  # Even if it's empty, it's still 200 OK

    except Exception as e:
        # Catch unexpected issues and log for debugging
        import traceback
        traceback.print_exc()  # Optional: logs full stack trace in terminal
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500




@app.route('/api/search', methods=['GET'])
@jwt_required()
def search_profiles():
    """Search for profiles by name, birth year, sex, race, or any
     combination of these four (4) fields; and return JSON results."""
    name = request.args.get('name')
    birth_year = request.args.get('birth_year')
    sex = request.args.get('sex')
    race = request.args.get('race')
    # query = db.select(Profile)
    query = Profile.query
    if name:
        query = query.join(User).filter(User.name.ilike(f"%{name}%"))
    if birth_year:
        query = query.filter(Profile.birth_year == int(birth_year))
    if sex:
        query = query.filter(Profile.sex == sex)
    if race:
        query = query.filter(Profile.race.ilike(f"%{race}%"))
    results = query.all()
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



@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get Details of a user."""
    user = db.session.get(User, user_id)
    if user:
        profiles = user.profiles or []  
        data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'photo': user.photo,
            'date_joined': user.date_joined.isoformat(),
            'profiles': [{
                'profile_id': p.id,
                'description': p.description,
                'parish': p.parish,
                'biography': p.biography,
                'sex': p.sex,
                'race': p.race,
                'birth_year': p.birth_year,
                'height': p.height,
                'fav_cuisine': p.fav_cuisine,
                'fav_colour': p.fav_colour,                    
                'fav_school_subject': p.fav_school_subject,
                'political': p.political,
                'religious': p.religious,
                'family_oriented': p.family_oriented,
                'user': {  
                        'id': user.id,
                        'name': user.name,
                        'photo': user.photo
                        }
                }for p in profiles]
        }
        return jsonify({'user': data})
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_logged_in_user():
    """Return the currently logged-in user's basic info."""
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id,'username': user.username,'email': user.email}), 200


@app.route('/api/favourites', methods=['GET'])
@jwt_required()
def get_favourites():
    """Get profiles of users favourited by the current user."""
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    favourites = user.favourites
    result = []

    for fav in favourites:
        fav_user = fav.fav_user
        profile = Profile.query.filter_by(user_id_fk=fav_user.id).first()

        if profile:
            result.append({
                'profile_id': profile.id,
                'user_id_fk': fav_user.id,
                'birth_year': profile.birth_year,
                'sex': profile.sex,
                'race': profile.race,
                'description': profile.description,
                'biography': profile.biography,
                'height': profile.height,
                'fav_cuisine': profile.fav_cuisine,
                'fav_colour': profile.fav_colour,
                'fav_school_subject': profile.fav_school_subject,
                'political': profile.political,
                'religious': profile.religious,
                'family_oriented': profile.family_oriented,
                'user': {
                    'name': fav_user.name,
                    'username': fav_user.username,
                    'email': fav_user.email,
                    'photo': fav_user.photo
                }
            })

    return jsonify({'favourites': result}), 200


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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
    return jsonify({'error': 'Not found'}), 404
