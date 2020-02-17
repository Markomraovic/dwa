from flask import Flask
from flask import render_template,url_for,request, jsonify
import domain as db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registracija',methods=['GET'])
def registracija():
    return render_template('registracija.html')

@app.route('/novi_korisnik',methods=['POST'])
def novi_korisnik():
    ime = request.form['ime']
    prezime = request.form['prezime']
    mail = request.form['mail']
    lozinka = request.form['lozinka']
    odg = db.registracija(ime,prezime,mail,lozinka)
    if odg:
        return render_template('index.html')
    else:
        return print('Nesto ne valja.')


@app.route('/prijava',methods=['POST'])
def home():
    mail = request.form['mail']
    lozinka = request.form['lozinka']
    korisnik = db.prijava_u_sustav(mail,lozinka)
    svitroskovi=db.listaj(korisnik[0])
    if korisnik:
        return render_template('home.html', korisnik=korisnik, svitroskovi=svitroskovi)
    else:
        return print('korisnik nije pronaden')

@app.route('/odjava')
def odjava():
    return render_template('index.html')

@app.route('/povratak/<korisnik_id>',methods=['GET'])
def povratak(korisnik_id):
    korisnik = db.dohvati_korisnika(korisnik_id)
    svitroskovi=db.listaj(korisnik[0])
    return render_template('home.html', korisnik=korisnik, svitroskovi=svitroskovi)

@app.route('/novi_trosak/<id>',methods=['GET','POST'])
def novi_trosak(id):
    if request.method == 'GET':
        return render_template('unos_troska.html', korisnik_id=id)
    elif request.method == 'POST':
        naziv_troska = request.form['naziv_troska']
        iznos = request.form['iznos']
        opis = request.form['opis']
        trosak = db.unos_troska(naziv_troska,iznos,opis,id)
        svitroskovi=db.listaj(id)
        korisnik = db.dohvati_korisnika(id)
        print("korisnik:",korisnik)
        if trosak:
            return render_template('home.html', korisnik=korisnik, svitroskovi=svitroskovi)
        else:
            return print("Nesto nije dobro")

@app.route('/brisanje_template/<korisnik_id>', methods=['GET'])
def brisanje_template(korisnik_id):
    svitroskovi=db.listaj(korisnik_id)
    return render_template('brisanje_troska.html', svitroskovi=svitroskovi, korisnik_id=korisnik_id)


@app.route('/brisanje_troska/<trosak_id>/<korisnik_id>', methods=['POST'])
def brisanje_troska(trosak_id,korisnik_id):
    print(request.method)
    if request.method == 'POST':
        db.obrisi(trosak_id)
        svitroskovi=db.listaj(korisnik_id)
        korisnik = db.dohvati_korisnika(korisnik_id)
        return render_template('home.html', korisnik=korisnik, svitroskovi=svitroskovi)
    else:
        print('fuk')
    

if __name__=='__main__':
    app.debug = True
    app.run()