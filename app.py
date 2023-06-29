from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from forms import RegistrationForm, LoginForm, ReservationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lavieestainsi'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UNA_COCHE.db'

db = SQLAlchemy(app)
admin = Admin(app, name='josias_dmin', template_mode='bootstrap3')


# pour la session#

# Modèle Utilisateur
@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('inscription'))


# Modèle Utilisateur
class Utilisateur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(40), nullable=False)
    prenom = db.Column(db.String(60), nullable=False)
    Nom_utilisateur = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Utilisateur:{self.Nom} : {self.prenom} : {self.Nom_utilisateur} Email: {self.email} : {self.mot_de_passe} : {self.date_creation.strftime("%d/%m/%Y,%H:%M:%S")}'
    
class Vehicule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marque = db.Column(db.String(100), nullable=False)
    modele = db.Column(db.String(100), nullable=False)
    annee = db.Column(db.String(4), nullable=True)
    description = db.Column(db.Text, nullable=False)
    # image = db.Column(db.ImageField, nullable=False)

    def __repr__(self):
        return f'Vehicule(id={self.id}, marque={self.marque}, modele={self.modele}'
class ProfileChauffeur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    numero_telephone = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'ProfileChauffeur(id={self.id}, nom={self.nom}, prenom={self.prenom})'



admin.add_view(ModelView(Utilisateur, db.session))
admin.add_view(ModelView(Vehicule, db.session)) 
# admin.add_view(ModelView(Reservation, db.session))
admin.add_view(ModelView(ProfileChauffeur, db.session))
# admin.add_view(ModelView(Facture, db.session))


# Modèle Réservation
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=False)
    num_guests = db.Column(db.Integer, nullable=False)
    vehicle_choice = db.Column(db.String(100), nullable=False)
    driver_choice = db.Column(db.Boolean, nullable=False)


# -------------------------- les routes---------------------------#

# Route Accueil
@app.route('/')
@app.route('/accueil')
def accueil():
    return render_template('Accueil.html', title='Accueil')


# Route À propos
@app.route('/apropos')
def apropos():
    return render_template('Apropos.html', title='À propos')


# Route Services
@app.route('/services')
def services():
    return render_template('Services.html', title='Services')


# Route Véhicule
# Route Véhicule
# Route Véhicule
@app.route('/vehicule', methods=['GET', 'POST'])
def vehicule():
    if request.method == 'POST' and 'image' in request.files:
        image = request.files['image']
        filename = images.save(image)
        marque = request.form['marque']
        modele = request.form['modele']
        
        vehicule = Vehicule(marque=marque, modele=modele, image=filename)
        db.session.add(vehicule)
        db.session.commit()

    vehicules = Vehicule.query.all()
    return render_template('vehicule.html', vehicules=vehicules)






# Route Inscription
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('services'))
    form = RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.mot_de_passe.data).decode('utf-8')
        utilisateur = Utilisateur(Nom=form.Nom.data,
                                  prenom=form.prenom.data,
                                  Nom_utilisateur=form.Nom_utilisateur.data,
                                  email=form.email.data,
                                  mot_de_passe=encrypted_password)
        db.session.add(utilisateur)
        db.session.commit()
        flash(f'Votre compte a été créé avec succès pour {form.Nom_utilisateur.data}', category='success')
        return redirect(url_for('connexion'))
    return render_template('Inscription.html', title='Inscription', form=form)


# Route Connexion
# Route Connexion
@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('accueil'))
    form = LoginForm()
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(email=form.email.data).first()
        if utilisateur and bcrypt.check_password_hash(utilisateur.mot_de_passe,form.mot_de_passe.data):
            login_user(utilisateur)
            flash(f'Connexion réussie avec succès pour {form.email.data}', category='success')
            return redirect(url_for('accueil'))
        else:
            flash(f'Échec de la connexion. Veuillez entrer les bonnes informations pour {form.email.data}', category='danger')
    return render_template('Connexion.html', title='Connexion', form=form)

# Route deconnexion


# Route Déconnexion
@app.route('/deconnexion')
def deconnexion():
    logout_user()
    return redirect(url_for('connexion'))


# Route Réservation de véhicule
@app.route('/reservation', methods=['GET', 'POST'])
@login_required
def reservation():
    form = ReservationForm()
    if form.validate_on_submit():
        reservation = Reservation(
            full_name=form.full_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            check_in=form.check_in.data,
            check_out=form.check_out.data,
            num_guests=form.num_guests.data,
            vehicle_choice=form.vehicle_choice.data,
            driver_choice=form.driver_choice.data
        )
        db.session.add(reservation)
        db.session.commit()
        flash('Réservation effectuée avec succès', category='success')
        return redirect(url_for('accueil'))
    return render_template('reservation.html', title='Réservation', form=form)


# Instanciation de la base de données
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
