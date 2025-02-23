from flask import Flask, render_template, request, make_response, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from database import login_pacient, login_administrator
from database import lista_pacienti, get_pacient_by_id, adaugare_pacient, editare_pacient, delete_pacient_by_id
from database import lista_medici, get_medic_by_id, editare_medic, delete_medic_by_id, adaugare_medic, get_medic_by_lab
from database import lista_dropdown_laboratoare, get_analize_by_medic, get_analize_by_month, get_analize_by_id, get_cost_total
from database import lista_analize, lista_categorii, lista_buletine, lista_laboratoare, get_analiza_by_categorie, get_pacient_by_year, lista_analize_by_id
from database import get_categorie_by_id, adaugare_categorie, delete_categorie_by_id, editare_categorie
from database import get_laborator_by_id, adaugare_laborator, delete_laborator_by_id, editare_laborator
from database import get_analiza_by_id1, lista_dropdown_categorii, adaugare_analiza, editare_analiza, delete_analiza_by_id
from database import adaugare_programare, get_programari_by_pacient

import random
import string
import secrets

def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

app = Flask(__name__)   # Flask constructor 
app.secret_key = generate_random_string(20)
login_manager = LoginManager(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


LOGINS = {}


@app.route('/')
def home():
    return render_template("login_final.html")


@app.route('/clinic-background.jpg')
def serve_image():
    return app.send_static_file('clinic-background.jpg')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    
    cookie = request.cookies.get("LOGIN_COOKIE")
    if cookie in LOGINS:
        del LOGINS[cookie]

    response = make_response(redirect("/", code=302))
    response.set_cookie('LOGIN_COOKIE', '', expires=0)
    return response


@app.route('/login_pacient_form', methods=['POST'])   
def login_pacient_form():
    # Access form data using request.form
    cnp = request.form.get('cnp')
    password = request.form.get('password')

    id = login_pacient(cnp, password)
    if id is None:
        return render_template("eroare_login.html")
    else:
        user = User(id)  # Creating a user object
        login_user(user)  # Logging in the user
        pacient = get_pacient_by_id(id)
        resp = make_response(render_template("dashboard_pacient.html", cnp=cnp, id=id, pacient=pacient))

        cookie = "".join(random.choices(string.ascii_lowercase, k=20))
        LOGINS[cookie] = (id, cnp)
        resp.set_cookie('LOGIN_COOKIE', cookie)
        return resp


@app.route('/login_administrator_form', methods=['POST'])   
def login_administrator_form():
    # Access form data using request.form
    nume = request.form.get('nume')
    password = request.form.get('password')

    id = login_administrator(nume, password)
    if id is None:
        return render_template("eroare_login.html")
    else:
        user = User(id)  # Creating a user object
        login_user(user)  # Logging in the user

        pacienti = lista_pacienti()
        resp = make_response(render_template("dashboard_administrator.html", name=nume, id=id, pacienti=pacienti))

        cookie = "".join(random.choices(string.ascii_lowercase, k=20))
        LOGINS[cookie] = (id, nume)
        resp.set_cookie('LOGIN_COOKIE', cookie)
        return resp
    

@app.route('/dashboard_pacient' , methods=['GET'])
def dashboard_pacient():
    cookie = request.cookies.get("LOGIN_COOKIE")
    id, cnp = LOGINS.get(cookie, (None, None))

    pacient = get_pacient_by_id(id)
    return render_template("dashboard_pacient.html", cnp=cnp, id=id, pacient=pacient)


@app.route('/dashboard_administrator' , methods=['GET'])
def dashboard_administrator():
    cookie = request.cookies.get("LOGIN_COOKIE")
    id, nume = LOGINS.get(cookie, (None, None))

    pacienti = lista_pacienti()
    return render_template("dashboard_administrator.html", name=nume, id=id, pacienti=pacienti)


@app.route('/lista_pacienti' , methods=['GET'])
@login_required
def dashboard():
    pacienti = lista_pacienti()
    return render_template("pacienti/lista_pacienti.html", pacienti=pacienti)


@app.route('/pacient/<id>', methods=['GET'])  
@login_required
def view_pacient(id):
    pacient = get_pacient_by_id(id)
    if pacient is None:
        return render_template("pacienti/eroare_view_pacient.html")
    else:
        return render_template("pacienti/view_pacient.html", pacient=pacient)
    

@app.route('/adaugare_pacient')
@login_required
def adaugare_pacient_page():
    return render_template("pacienti/insert_pacient.html")


@app.route('/adaugare_pacient_form', methods=['POST']) 
@login_required  
def adaugare_pacient_form():
    # Access form data using request.form
    nume = request.form.get('nume')
    prenume = request.form.get('prenume')
    data_nasterii = request.form.get('data_nasterii')
    sex = request.form.get('sex')
    adresa = request.form.get('adresa')
    telefon = request.form.get('telefon')
    cnp = request.form.get('cnp')
    parola = request.form.get('parola')

    result = adaugare_pacient(nume, prenume, data_nasterii, sex, adresa, telefon, cnp, parola)
    if result is None:
        return render_template("pacienti/eroare_adaugare.html")
    else:
        pacienti = lista_pacienti()

        return render_template("pacienti/lista_pacienti.html", name=nume, id=id, pacienti=pacienti)


@app.route('/pacient/update/<id>', methods=['GET'])   
@login_required
def update_pacient(id):
    pacient = get_pacient_by_id(id)
    if pacient is None:
        return render_template("pacienti/eroare_update_pacient.html")
    else:
        return render_template("pacienti/update_pacient.html", pacient=pacient)


@app.route('/editare_pacient_form/<id>', methods=['POST'])   
@login_required
def editare_pacient_form(id):
    # Access form data using request.form
    nume = request.form.get('nume')
    prenume = request.form.get('prenume')
    data_nasterii = request.form.get('data_nasterii')
    sex = request.form.get('sex')
    adresa = request.form.get('adresa')
    telefon = request.form.get('telefon')
    cnp = request.form.get('cnp')

    result = editare_pacient(id, nume, prenume, data_nasterii, sex, adresa, telefon, cnp)
    if result is None:
        return render_template("pacienti/eroare_editare.html")
    else:
        pacienti = lista_pacienti()

        return render_template("pacienti/lista_pacienti.html", name=nume, id=id, pacienti=pacienti)


@app.route('/lista_medici' , methods=['GET'])
@login_required
def dashboard_medici():
    medici = lista_medici()
    return render_template("medici/lista_medici.html", medici=medici)

@app.route('/medic/<id>', methods=['GET'])   
@login_required
def view_medic(id):
    medic = get_medic_by_id(id)
    laboratoare = lista_dropdown_laboratoare()

    if medic is None:
        return render_template("medici/eroare_view_medic.html")
    else:
        return render_template("medici/view_medic.html", medic=medic, laboratoare = laboratoare)
    
    
@app.route('/medic/update/<id>', methods=['GET'])  
@login_required 
def update_medic(id):
    medic = get_medic_by_id(id)
    laboratoare = lista_dropdown_laboratoare()
    
    if medic is None:
        return render_template("medici/eroare_update_medic.html")
    else:
        return render_template("medici/update_medic.html", medic=medic, laboratoare=laboratoare)
    
@app.route('/editare_medic_form/<id>', methods=['POST'])   
@login_required
def editare_medic_form(id):
    # Access form data using request.form
    nume = request.form.get('nume')
    prenume = request.form.get('prenume')
    laborator = request.form.get('laborator')

    result = editare_medic(id, nume, prenume, laborator)
    if result is None:
        return render_template("medici/eroare_editare.html")
    else:
        medici = lista_medici()
        

        return render_template("medici/lista_medici.html", name=nume, id=id, medici=medici)


@app.route('/pacient/delete/<id>', methods=['POST']) 
@login_required  
def delete_pacient(id):
    result = delete_pacient_by_id(id)

    if result is None:
        return render_template("pacienti/eroare_delete.html")
    else:
        pacienti = lista_pacienti()
        return render_template("pacienti/lista_pacienti.html", pacienti=pacienti)


@app.route('/medic/delete/<id>', methods=['POST'])  
@login_required 
def delete_medic(id):
    result = delete_medic_by_id(id)

    if result is None:
        return render_template("medici/eroare_delete.html")
    else:
        medici = lista_medici()
        return render_template("medici/lista_medici.html", medici=medici)
    

@app.route('/adaugare_medic')
@login_required
def adaugare_medic_page():
    laboratoare = lista_dropdown_laboratoare()

    return render_template("medici/insert_medic.html", laboratoare=laboratoare)


@app.route('/adaugare_medic_form', methods=['POST']) 
@login_required  
def adaugare_medic_form():
    # Access form data using request.form
    nume = request.form.get('nume')
    prenume = request.form.get('prenume')
    laborator = request.form.get('laborator_id')

    result = adaugare_medic(nume, prenume, laborator)
    if result is None:
        print("Adaugare medic")
        return render_template("medici/eroare_adaugare.html")
    else:
        medici = lista_medici()
        

        return render_template("medici/lista_medici.html", name=nume, medici=medici)
    
    
@app.route('/lista_analize' , methods=['GET'])
@login_required
def dashboard_analize():
    analize = lista_analize()
    return render_template("analize/lista_analize.html", analize=analize)


@app.route('/lista_categorii' , methods=['GET'])
@login_required
def dashboard_categorii():
    categorii = lista_categorii()
    return render_template("categorii/lista_categorii.html", categorii=categorii)

@app.route('/adaugare_categorie')
@login_required
def adaugare_categorie_page():
    return render_template("categorii/insert_categorie.html" )


@app.route('/categorie/delete/<id>', methods=['POST'])
@login_required
def delete_categorie(id):
    result = delete_categorie_by_id(id)

    if result is None:
        return render_template("categorii/eroare_delete.html")
    else: 
        categorii = lista_categorii()
        return render_template("categorii/lista_categorii.html", categorii=categorii)
    
@app.route('/adaugare_categorie_form', methods=['POST'])
@login_required
def adaugare_categorie_form():
    nume_categorie = request.form.get('nume_categorie')

    result = adaugare_categorie(nume_categorie)
    if result is None:
        print("Adaugare categorie")
        return render_template("categorii/eroare_adaugare.html")
    else:
        categorii = lista_categorii()
        return render_template("categorii/lista_categorii.html", nume_categorie=nume_categorie, categorii=categorii)
    
@app.route('/categorie/update/<id>',  methods=['GET'])
@login_required
def update_categorie(id):
    categorie = get_categorie_by_id(id)

    if categorie is None:
        return render_template("categorii/eroare_update_categorie.html")
    else:
        return render_template("categorii/update_categorie.html", categorie=categorie)

    
@app.route('/editare_categorie_form/<id>', methods=['POST'])
@login_required
def editare_categorie_form(id):
    nume_categorie = request.form.get('nume_categorie')

    result = editare_categorie(id, nume_categorie)
    if result is None:
        return render_template("categorii/eroare_editare.html")
    else:
        categorii = lista_categorii()

        return render_template("categorii/lista_categorii.html", id=id, nume_categorie=nume_categorie, categorii=categorii)


@app.route('/lista_buletine' , methods=['GET'])
@login_required
def dashboard_buletine():
    buletine = lista_buletine()
    return render_template("buletine/lista_buletine.html", buletine=buletine)

@app.route('/lista_laboratoare' , methods=['GET'])
@login_required
def dashboard_laboratoare():
    laboratoare = lista_laboratoare()
    return render_template("laboratoare/lista_laboratoare.html", laboratoare=laboratoare)

@app.route('/laborator/<id>', methods=['GET'])   
@login_required
def view_laborator(id):
    laborator = get_laborator_by_id(id)
    

    if laborator is None:
        return render_template("laboratoare/eroare_view_laborator.html")
    else:
        return render_template("laboratoare/view_laborator.html", laborator=laborator)
    
    
@app.route('/laborator/update/<id>', methods=['GET'])   
@login_required
def update_laborator(id):
    laborator = get_laborator_by_id(id)
    
    if laborator is None:
        return render_template("laboratoare/eroare_update_laborator.html")
    else:
        return render_template("laboratoare/update_laborator.html", laborator=laborator)
    
@app.route('/editare_laborator_form/<id>', methods=['POST'])   
@login_required
def editare_laborator_form(id):
    nume = request.form.get('nume')
    adresa = request.form.get('adresa')
    telefon = request.form.get('telefon')

    result = editare_laborator(id, nume, adresa, telefon)
    if result is None:
        return render_template("laboratoare/eroare_editare.html")
    else:
        laboratoare = lista_laboratoare()
        
        return render_template("laboratoare/lista_laboratoare.html", id=id, nume=nume, adresa=adresa, telefon=telefon, laboratoare=laboratoare)
    
@app.route('/laborator/delete/<id>', methods=['POST']) 
@login_required  
def delete_laborator(id):
    result = delete_laborator_by_id(id)

    if result is None:
        return render_template("laboratoare/eroare_delete.html")
    else:
        laboratoare = lista_laboratoare()
        return render_template("laboratoare/lista_laboratoare.html", laboratoare=laboratoare)
    

@app.route('/adaugare_laborator')
@login_required
def adaugare_laborator_page():
    return render_template("laboratoare/insert_laborator.html") 


@app.route('/adaugare_laborator_form', methods=['POST'])  
@login_required 
def adaugare_laborator_form():
    nume = request.form.get('nume')
    adresa = request.form.get('adresa')
    telefon = request.form.get('telefon')

    result = adaugare_laborator(nume, adresa, telefon)
    if result is None:
        print("Adaugare laborator")
        return render_template("laboratoare/eroare_adaugare.html")
    else:
        laboratoare = lista_laboratoare()
        return render_template("laboratoare/lista_laboratoare.html", nume=nume, laboratoare=laboratoare)

@app.route('/medic/search/', methods=['GET'])   
@login_required
def search_medic():
    lab = request.args.get('search')
    result = get_medic_by_lab(lab)

    if result is None:
        return render_template("medici/eroare_cautare.html")
    else:
        return render_template("medici/lista_cautare.html", medici=result)
    
    
@app.route('/analiza/search/', methods=['GET'])  
@login_required 
def search_analiza():
    categorie = request.args.get('search')
    result = get_analiza_by_categorie(categorie)

    if result is None:
        return render_template("analize/eroare_cautare.html")
    else:
        return render_template("analize/lista_cautare.html", analize=result)
    

@app.route('/buletin/search/', methods=['GET'])   
@login_required
def search_buletin():
    year = request.args.get('search')
    result = get_pacient_by_year(year)

    if result is None:
        return render_template("buletine/eroare_cautare.html")
    else:
        return render_template("buletine/lista_cautare.html", buletine=result)


@app.route('/buletin/<id>', methods=['GET'])   
@login_required
def view_buletin(id):
    lista_analize = lista_analize_by_id(id)

    if lista_analize is None:
        return render_template("buletine/eroare_view_buletine.html")
    else:
        return render_template("buletine/view_buletine.html", lista_analize=lista_analize)
    

@app.route('/buletin/medic/', methods=['GET'])
@login_required   
def search_buletin_medic():
    nume = request.args.get('search')
    names = nume.split() 
    result = get_analize_by_medic(names[0], names[1])
    

    if result is None:
        return render_template("buletine/eroare_cautare.html")
    else:
        return render_template("buletine/lista_cautare_medic.html", analize=result)
    

@app.route('/buletin/analize/', methods=['GET'])  
@login_required 
def search_buletin_analize():
    month = request.args.get('search')
    result = get_analize_by_month(month)
    
    if result is None:
        return render_template("buletine/eroare_cautare.html")
    else:
        return render_template("buletine/lista_cautare_analize.html", analize=result)
    

@app.route('/date_personale' , methods=['GET'])
@login_required
def date_pacient():
    cookie = request.cookies.get("LOGIN_COOKIE")
    id, cnp = LOGINS.get(cookie, (None, None))

    pacient = get_pacient_by_id(id)
    return render_template("date_personale.html", pacient=pacient)


@app.route('/lista_analize_pacient/<id>' , methods=['GET'])
@login_required
def lista_analize_pacient(id):
    analize = get_analize_by_id(id)
    pacient = get_pacient_by_id(id)
    cost_total = get_cost_total(id)
    return render_template("lista_analize_pacient.html", analize=analize, pacient=pacient, cost_total=cost_total)

@app.route('/analiza/<id>', methods=['GET'])  
@login_required 
def view_analiza(id):
    analiza = get_analiza_by_id1(id)
    categorii = lista_dropdown_categorii()

    if analiza is None:
        return render_template("analize/eroare_view_analize.html")
    else:
        return render_template("analize/view_analize.html", analiza=analiza, categorii = categorii)

@app.route('/analiza/update/<id>', methods=['GET']) 
@login_required  
def update_analiza(id):
    analiza = get_analiza_by_id1(id)
    categorii = lista_dropdown_categorii()
    
    if analiza is None:
        return render_template("analize/eroare_update_analiza.html")
    else:
        return render_template("analize/update_analize.html", analiza=analiza, categorii=categorii)

@app.route('/editare_analiza_form/<id>', methods=['POST']) 
@login_required  
def editare_analiza_form(id):
    # Access form data using request.form
    nume_analiza = request.form.get('nume_analiza')
    categorie_id = request.form.get('categorie_id')
    cost_analiza = request.form.get('cost_analiza')
    rezultat = request.form.get('rezultat')
    unitate_masura = request.form.get('unitate_masura')

    result = editare_analiza(id, nume_analiza, categorie_id, cost_analiza, rezultat, unitate_masura)
    if result is None:
        return render_template("analize/eroare_editare_analiza.html")
    else:
        analize = lista_analize()  

        return render_template("analize/lista_analize.html", id=id, nume_analiza=nume_analiza, analize=analize)

@app.route('/adaugare_analiza')
@login_required
def adaugare_analiza_page():
    categorii = lista_dropdown_categorii()

    return render_template("analize/insert_analize.html", categorii=categorii)  

@app.route('/adaugare_analiza_form', methods=['POST'])  
@login_required 
def adaugare_analiza_form():
    # Access form data using request.form
    nume_analiza = request.form.get('nume_analiza')
    categorie_id = request.form.get('categorie_id')
    cost_analiza = request.form.get('cost_analiza')
    rezultat = request.form.get('rezultat')
    unitate_masura = request.form.get('unitate_masura')

    result = adaugare_analiza(nume_analiza, categorie_id, cost_analiza, rezultat, unitate_masura)
    if result is None:
        print("Adaugare analiza")
        return render_template("analize/eroare_adaugare_analize.html")
    else:
        analize = lista_analize()      

        return render_template("analize/lista_analize.html", nume_analiza=nume_analiza, analize=analize)

@app.route('/analiza/delete/<id>', methods=['POST']) 
@login_required  
def delete_analiza(id):
    result = delete_analiza_by_id(id)

    if result is None:
        return render_template("analize/eroare_delete_analiza.html")
    else:
        analize = lista_analize()
        return render_template("analize/lista_analize.html", analize=analize)
    
@app.route('/programare/<id>', methods=['GET', 'POST'])
@login_required
def programare(id):
    if request.method == 'POST':
        pacient_id = id 
        medic_id = request.form.get('medic_id')

        data_programare = request.form.get('data_programare')

        result = adaugare_programare(pacient_id, medic_id, data_programare)
        
        return redirect(url_for('dashboard_pacient'))

    medici = lista_medici()
    pacient = get_pacient_by_id(id)
    return render_template('programare.html', medici=medici, pacient=pacient)


@app.route('/lista_programari_pacient/<pacient_id>', methods=['GET'])
@login_required
def lista_programari_pacient(pacient_id):
    programari = get_programari_by_pacient(pacient_id)
    return render_template('lista_programari_pacient.html', programari=programari)

    

if __name__=='__main__': 
    app.run(debug = True)

