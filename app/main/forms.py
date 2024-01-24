from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, FieldList, FormField, HiddenField
from app.main.wtforms_custom import ButtonField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, NoneOf
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class DirCreationForm(FlaskForm):
    project_type = SelectField(choices=[('client_REPLACE','Client'),
                            ('Pitch_work','Pitch'),
                            ('Viscira_Internal', 'Internal')],
                         default='client_REPLACE')
    client = StringField('Client',
                         validators=[DataRequired(),
                                               NoneOf('Animation', message='Animation is an Invalid Name!'),
                                               Length(min=0, max=25)])
    brand = StringField('Brand',
                        validators=[DataRequired(),
                                    NoneOf('Animation', message='Animation is an Invalid Name!'),
                                    Length(min=0, max=25)])
    solution = StringField('Solution',
                           validators=[DataRequired(),
                                       NoneOf('Animation', message='Animation is an Invalid Name!'),
                                       Length(min=0, max=25)])
    client_code = StringField('Client_Code',
                           validators=[DataRequired()])
    subDirList = FieldList(FormField())
    addField = ButtonField(label='Add Directory', id='addNewField')
    submit = SubmitField(label='Preview')
    hiddenNum = HiddenField()
    
    
class PreviewForm(FlaskForm):
    filePath = HiddenField()
    hiddenFilePath = HiddenField()
    hiddenProjectCode = HiddenField()
    makeProject = SubmitField(label='Make Project')
    
class MakeProjectForm(FlaskForm):
    hiddenFilePath = HiddenField()
    
