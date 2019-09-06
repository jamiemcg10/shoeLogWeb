from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, LogRunForm, RegistrationForm, ShoeCalcForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Activity
from werkzeug.urls import url_parse
from sqlalchemy import func


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = LoginForm()
    
    if form.validate_on_submit():   
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Sign In', form=form)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
 

@app.route('/logrun', methods=['GET', 'POST'])
def logrun():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
        
    form = LogRunForm()
    
    if form.validate_on_submit():
        run = Activity(date = form.date.data, walk_miles = form.walk.data, 
            run_miles = form.run.data, total_miles = form.walk.data + form.run.data, 
            type = form.type.data, shoe=form.shoe.data, user_id = current_user.id)
        db.session.add(run)
        db.session.commit()
        
        return redirect(url_for('logrun'))
     
    return render_template('logrun.html', title='Log Run', form=form)
    
    
@login_required    
@app.route('/viewshoes', methods=['GET', 'POST'])
def viewshoes():
    
    form = ShoeCalcForm()
    
    #total_mi = form.total_mi
    #walk_mi = form.walk_mi
    #run_mi = form.run_mi   

   
    if form.validate_on_submit():
        print(form.shoe.data)
        #matching_activities = Activity.query(func.sum(Activity.total_miles)).filter(Activity.shoe == form.shoes[int(form.shoe.data)][1])
        matching_activities = db.session.query(db.func.sum(Activity.total_miles), db.func.sum(Activity.walk_miles), db.func.sum(Activity.run_miles)).filter(Activity.shoe == form.shoes[int(form.shoe.data)][1])
        print(matching_activities)
        for act in matching_activities:
            print(act[0])
        print("valid")
        form.total_mi = act[0]
        form.walk_mi = act[1]
        form.run_mi = act[2]

    return render_template('viewshoes.html', title='Shoes', form=form)
