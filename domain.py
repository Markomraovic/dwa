import sqlite3
from uuid import uuid4

def connection():
    try:
        conn=sqlite3.connect("baza.db")
        return conn
    except Error as e:
        print(e)

def close_connection(conn):
    conn.close()

def registracija(ime,prezime,mail,lozinka):

    korisnik_id=uuid4().hex

    conn=connection()

    c=conn.cursor()

    c.execute("INSERT INTO korisnik(id, ime, prezime, mail, lozinka) VALUES (?,?,?,?,?)", (korisnik_id, ime, prezime, mail, lozinka ))
    conn.commit()

    close_connection(conn)

    return korisnik_id

def prijava_u_sustav(mail, lozinka):
    
    conn=connection()

    c=conn.cursor()

    c.execute("SELECT * FROM korisnik WHERE mail = ? AND lozinka = ?", (mail, lozinka))
    
    korisnik = c.fetchone()
    print('KORISNIK: ', korisnik)
    
    close_connection(conn)

    return korisnik

def unos_troska(naziv_troska,iznos,opis,korisnik_id):

    conn=connection()
    c=conn.cursor()
    id=uuid4().hex
    c.execute("INSERT INTO troskovi(id,naziv_troska,iznos,opis,korisnik_id) VALUES (?,?,?,?,?)",(id,naziv_troska,iznos,opis,korisnik_id))
    conn.commit()
    close_connection(conn)
    return id

def obrisi(id):
    conn=connection()
    c=conn.cursor()
    c.execute("DELETE FROM troskovi WHERE id=?",(id,))
    conn.commit()
    close_connection(conn)

def listaj(korisnik_id):
    conn=connection()
    c=conn.cursor()
    c.execute("SELECT * FROM troskovi where korisnik_id=?",(korisnik_id,))
    svitroskovi = c.fetchall()
    close_connection(conn)
    return svitroskovi

def dohvati_korisnika(id):
    conn=connection()
    c=conn.cursor()
    c.execute("SELECT * from korisnik WHERE id=?",(id,))
    korisnik = c.fetchone()
    close_connection(conn)
    return korisnik
