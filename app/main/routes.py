from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, DirCreationForm, PreviewForm, \
MakeProjectForm
from app.main.make_directories import makeDirectories, makeRootProjectPath
from app.models import User
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = DirCreationForm()    
    if form.validate_on_submit():
        preview = PreviewForm()
        projectType = request.form.get('project_type')     
        client = request.form.get('client').replace(" ", "_")
        brand = request.form.get('brand').replace(" ", "_")
        solution = request.form.get('solution').replace(" ", "_")
        clientCode = request.form.get('client_code')
        projectCode = (client[0:3] + brand[0:2]).upper()
        fullSolution = projectCode + "_" + solution + "_" + clientCode
        user_agent = request.user_agent
        platform = user_agent.platform
        path = makeRootProjectPath(projectType, client, brand, fullSolution, form)
        if platform == 'windows':
            previewpath = path.replace("/mnt/optimus", "O:")
        else:
            previewpath = path
        if path is not None:        
            return render_template('preview.html', title=('Preview'), path=path, previewpath=previewpath, projectCode=projectCode, preview=preview)
        else:
            flash('You cannot use Animation as a directory name.')
            return redirect(url_for('main.index'))  
    return render_template('index.html', title=('Home'), form=form)

@bp.route('/preview', methods=['GET', 'POST'])
def preview():
    form = PreviewForm()
    if form.validate_on_submit():        
        mkproj = MakeProjectForm()
        path = request.form.get('hiddenFilePath')        
        code = request.form.get('hiddenProjectCode')
        user = User.query.filter_by(username=current_user.username).first_or_404()
        log = makeDirectories(user, path.lstrip().rstrip(), code.lstrip().rstrip())
        return render_template('mkproj.html', title=('Make Project'), mkproj=mkproj, log=log) 
    return render_template('preview.html', title='Preview', form=form)

@bp.route('/mkproj', methods=['GET', 'POST'])
def mkproj():
    form = MakeProjectForm() 
    return render_template('mkproj.html', title='Make Project', form=form)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

