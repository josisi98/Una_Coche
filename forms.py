from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    Nom=StringField(label='Nom',validators=[DataRequired(),Length(min=4,max=30)])
    prenom=StringField(label='prenom',validators=[DataRequired(),Length(min=4,max=30)])
    Nom_utilisateur=StringField(label='Nom_utilisateur', validators=[DataRequired(),Length(min=4,max=30)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField(label='mot de passe', validators=[DataRequired(), Length(min=8,max=20)])
    confir_motdepasse = PasswordField(label='confirm mot de passe', validators=[DataRequired(),EqualTo('mot_de_passe')])
    submit = SubmitField(label='Inscription')
    
class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField(label='mot de passe', validators=[DataRequired(), Length(min=8,max=20)])
    submit = SubmitField(label='Connexion')
    
class ReservationForm(FlaskForm):
    full_name = StringField('Nom complet', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone_number = StringField('Numéro de téléphone', validators=[DataRequired()])
    check_in = StringField('Date d\'arrivée', validators=[DataRequired()])
    check_out = StringField('Date de départ', validators=[DataRequired()])
    num_guests = IntegerField('Nombre de clients', validators=[DataRequired()])
    vehicle_choice = SelectField('Véhicule', choices=[('car', 'Voiture'), ('suv', 'SUV'), ('van', 'Fourgonnette')])
    driver_choice = SelectField('Chauffeur', choices=[('yes', 'Oui'), ('no', 'Non')])


