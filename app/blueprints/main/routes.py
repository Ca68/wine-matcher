from werkzeug.utils import redirect
from .import bp as app
from flask import render_template, request, url_for, flash
from flask_login import current_user, login_required
from app import db, mail
from flask_mail import Message
from app.blueprints.authentication.models import User
import boto3
from flask import current_app
import time, smtplib
from werkzeug.utils import secure_filename
import requests
import json
import os


"""
CREATE - POST
READ - GET
UPDATE - PUT
DELETE - DELETE
"""

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    s3 = boto3.client('s3', aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'))


    if request.method == 'POST':
        u = User.query.get(current_user.id)
        u.first_name = request.form.get('first_name')
        u.last_name = request.form.get('last_name')
        u.email = request.form.get('email')
        u.bio = request.form.get('bio')
    
        if len(request.files)>0:
            s3.upload_fileobj(
                request.files.get('profile-image'),
                'final-project-cg',
                request.files.get('profile-image').filename,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': request.files.get('profile-image').content_type
                }
            )
            u.image = f"{current_app.config.get('AWS_BUCKET_LOCATION')}{request.files.get('profile-image').filename}"


        
        
        db.session.commit()
        flash('Profile updated successfully', 'info')
        return redirect(url_for('main.profile'))

    return render_template('profile.html')


@app.route('/contact', methods= ['GET', 'POST'])
def contact():
    if request.method == 'POST':
        form_data = {
            'email' : request.form.get('email'),
            'message' : request.form.get('message'),
            'subject' : request.form.get('subject')
        }
        
        
        
        server = smtplib.SMTP(current_app.config.get('MAIL_SERVER'), current_app.config.get('MAIL_PORT'))
        server.ehlo()
        server.starttls()
        server.login(current_app.config.get('MAIL_USERNAME'), current_app.config.get('MAIL_PASSWORD'))
        server.sendmail(current_app.config.get('MAIL_USERNAME'),current_app.config.get('MAIL_USERNAME'), 
                f'\nFROM: {form_data["email"]}\nSUBJECT: {form_data["subject"]}\n\n MESSAGE: {form_data["message"]}')
        server.quit()
        flash('Thank you for your message. We will get back to you as soon as possible.', 'success')
        return redirect(url_for('main.contact'))
    return render_template("contact.html")



@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method=='POST':
        request_ingredients = requests.get('https://api.spoonacular.com/recipes/findByIngredients?ingredients='+ request.form['q'] + "&apiKey=" + current_app.config.get('API_KEY'))
        data = json.loads(request_ingredients.text)
        
        
        request_wine = requests.get('https://api.spoonacular.com/food/wine/pairing?food=' + request.form['q'] + "&apiKey=" + current_app.config.get('API_KEY'))
        wine_data = json.loads(request_wine.text)
        
        return render_template('search.html', data=data, wine_data=wine_data, API_KEY=current_app.config.get('API_KEY')) if data != [] else render_template('search.html', data="", wine_data="")
    else:
        return render_template('search.html', wine_data="")
    


    
@app.route('/recipe/<recipe_id>', methods=['GET'])
def recipe(recipe_id):
    response = requests.get("https://api.spoonacular.com/recipes/informationBulk?ids="+recipe_id+"&includeNutrition=true&apiKey="+ 'cbd78de638ac4506b83523211062b587')
    return render_template("recipe.html", recipe_id=json.loads(response.text)), 200