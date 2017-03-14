"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager
from app.models import UserProfile 

from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from forms import *
from time import gmtime, strftime

from werkzeug.utils import secure_filename

ID = 62007000




###
# Excercise 2 File listing Method
###
def fileList():
    
    uploadedFiles = []
    filenames = []
    rootdir = os.getcwd() 

    print "log: " + rootdir
    
    for subdir, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
        for file in files:
            print os.path.join(subdir, file) 
            filepath = os.path.join(subdir, file);
            filename = os.path.basename(filepath)
            uploadedFiles.append(filepath)
            filenames.append(filename)
            
    return filenames
    
    
    
def isJpeg(file):

    return "jpg"== os.path.splitext(file)            
         
         
            
@app.route('/filelisting')
def files():
    
    uploads = fileList()
    
    return render_template('files.html', files=uploads )
 


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")
    
    
def timeinfo():
    return strftime("%d ,%m %Y %H:%M:%S", gmtime())
    
    
@app.route("/profile/<userid> ", methods=['GET'])
def user(userid):
    
    user = UserProfile.query.filter_by(id = userid ).first()
    if request.method=='GET':
        return render_template('userprofile.html', user =user )
    
    elif request.method == "POST" and request.headers['Content-Type'] == "application/json":
        user_json = {}
        user_json["userid"] = user.userid
        user_json["username"] = user.first-name + user.last_name
        user_json["image"] = user.userid + '.jpg'
        user_json["gender"] = user.gender
        user_json["age"] = user.age
        user_json["profile_created_on"] = user.get_date()
        return jsonify(user_json)
 
    
    
@app.route('/profiles', methods=['GET','POST'])   
def profiles():
    
    
    users = db.session.query(UserProfile).all()
    
    if request.method == 'GET':
        return  render_template('profiles.html', users = users)
        
       
    elif request.method == "POST" and request.headers['Content-Type'] == "application/json":
        users_list = []
        for user in users:
            users_list += [{"username": user.first_name+user.get_id, "userid":user.get_id}]
        user_json = {"users":users_list}
        return jsonify(user_json)
       
    else:
        flash("Unable to get request")
        return redirect(url_for('home'))
    
    
    # return render_template('profiles.html', users = users)


@app.route('/profile', methods=['GET', 'POST']) 
def profile(): 
    
    
    file_folder = app.config['UPLOAD_FOLDER']
    
    form = uploadForm();
    
    if request.method == "GET":
        return render_template('profile.html', form=form)


    elif request.method == 'POST' and form.validate_on_submit():
        
        fname = form.firstname.data
        lname = form.lastname.data
        age = form.age.data
        bio = form.bio.data
        gender = form.gender.data
        
        
        date = timeinfo()
        
        userID = ID + int(user.get_id())
        
        username = fname + userID
        
        
        user = UserProfile(first_name=fname, last_name = lname, age = age, bio= bio, gender=gender, date=date, userid = userID , username = username )
        db.session.add(user)
        db.session.commit()
        
        image = form.upload.data
        image.save(os.path.join(file_folder, str(userID)+".jpg"))
        


        flash('User: '+str(userID) +' created')
        return redirect(url_for('home'))
        
    elif request.method == 'GET':
        
        fname = request.args.get('firstname')
        lname = request.args.get('lastname')
        age = request.args.get('age')
        bio = request.args.get('bio')
        gender = request.args.get('gender')
        
        
        date = timeinfo()
        
        userID = ID + int(user.get_id())
        
        username = fname + userID
        
        user = UserProfile(first_name=fname, last_name = lname, age = age, bio= bio, gender=gender, date=date, userid = userID , username = username )
        db.session.add(user)
        db.session.commit()
        
        
        image = form.upload.data
        image.save(os.path.join(file_folder, userID+".jpg"))
        
 
        flash('Uploaded with [GET] User: '+ str(userID) +' created ')
        return redirect(url_for('home'))
        
    flash('ERROR IN SUBMISSION')
    

    return render_template('profile.html', form=form)
    
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in')
            return redirect(url_for('add_file'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
