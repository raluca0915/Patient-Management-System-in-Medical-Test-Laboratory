from sqlalchemy import create_engine, text

DATABASE_URL=''
engine = create_engine(DATABASE_URL, echo=True)

def start():
    connection = engine.connect()

    raw_sql_query = text("SELECT * FROM proiect")
    result = connection.execute(raw_sql_query)

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'nume_proiect': i[0], 
                'nume_materie':i[1]
                } for i in result]
    print(result)
    connection.close()

    return result


def login_pacient(CNP, password):
    connection = engine.connect()

    raw_sql_query = text("SELECT * FROM pacient WHERE CNP = :cnp AND parola = :password")
    result = connection.execute(raw_sql_query, {"cnp":CNP, "password":password})

    # prelucrare rezultat
    result = list(result.fetchall())
    if len(result) == 0:
        id_login = None
    else:
        id_login = result[0][0]

    connection.close()

    return id_login


def login_administrator(nume, password):
    connection = engine.connect()

    raw_sql_query = text("SELECT * FROM administrator WHERE nume = :nume AND parola = :password")
    result = connection.execute(raw_sql_query, {"nume":nume, "password":password})

    # prelucrare rezultat
    result = list(result.fetchall())
    if len(result) == 0:
        id_login = None
    else:
        id_login = result[0][0]

    connection.close()

    return id_login


def lista_pacienti():
    connection = engine.connect()

    raw_sql_query = text("SELECT * FROM pacient ORDER BY pacient_id")
    result = connection.execute(raw_sql_query)

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'pacient_id': i[0], 
                'nume':i[1],
                'prenume':i[2],
                'data_nasterii':i[3],
                'sex':i[4],
                'telefon':i[5],
                'cnp':i[6],
                'adresa':i[7]
                
                } for i in result]
    print(result)
    connection.close()

    return result


def get_pacient_by_id(id):
    connection = engine.connect()

    raw_sql_query = text("SELECT * FROM pacient WHERE pacient_id = :id")
    result = connection.execute(raw_sql_query, {"id":id})

    pacient = {}

    # prelucrare rezultat
    result = list(result.fetchall())
    if len(result) == 0:
        pacient = None
    else:
        pacient['id'] = result[0][0]
        pacient['nume'] = result[0][1]
        pacient['prenume'] = result[0][2]
        pacient['data_nasterii'] = result[0][3]
        pacient['sex'] = result[0][4]
        pacient['telefon'] = result[0][5]
        pacient['cnp'] = result[0][6]
        pacient['adresa'] = result[0][7]

    connection.close()

    return pacient


def adaugare_pacient(nume, prenume, data_nasterii, sex, adresa, telefon, cnp, parola):
    connection = engine.connect()

    try:
        raw_sql_query = text("INSERT INTO pacient (nume, prenume, data_nasterii, sex, telefon, cnp, adresa, parola) VALUES (:nume, :prenume, :data_nasterii, :sex, :telefon, :cnp, :adresa, :parola)")
        result = connection.execute(raw_sql_query, {"nume":nume, "prenume":prenume, "data_nasterii":data_nasterii, "sex":sex, "telefon":telefon, "cnp":cnp, "adresa":adresa, "parola":parola})
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return False
    
    return True


def editare_pacient(id, nume, prenume, data_nasterii, sex, adresa, telefon, cnp):
    connection = engine.connect()

    try:
        raw_sql_query = text("UPDATE pacient SET nume = :nume, prenume = :prenume, data_nasterii = :data_nasterii, sex = :sex, telefon = :telefon, cnp = :cnp, adresa = :adresa WHERE pacient_id = :id")
        result = connection.execute(raw_sql_query, {"id":id, "nume":nume, "prenume":prenume, "data_nasterii":data_nasterii, "sex":sex, "telefon":telefon, "cnp":cnp, "adresa":adresa})
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return False
    
    return True


def lista_medici():
    connection = engine.connect()

    raw_sql_query = text("SELECT medic.medic_id, medic.nume, medic.prenume, laborator.nume FROM medic INNER JOIN laborator ON medic.laborator_id = laborator.laborator_id ORDER BY medic.medic_id")
    result = connection.execute(raw_sql_query)

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'medic_id': i[0], 
                'nume':i[1],
                'prenume':i[2],
                'laborator':i[3]
                } for i in result]
    print(result)
    connection.close()

    return result


def delete_pacient_by_id(id):
    connection = engine.connect()

    #try:
    raw_sql_query = text("DELETE FROM pacient WHERE pacient_id = :id").execution_options(autocommit=True)
    result = connection.execute(raw_sql_query, {"id":id})
    connection.commit()
    connection.close()
    print(
        f"Deleted {result.rowcount} row(s) from ")
    #except:
    #    return False
    
    return True


def get_medic_by_id(id):
    connection = engine.connect()

    raw_sql_query = text("SELECT * FROM medic WHERE medic_id = :id")
    result = connection.execute(raw_sql_query, {"id":id})

    medic = {}

    # prelucrare rezultat
    result = list(result.fetchall())
    if len(result) == 0:
        medic = None
    else:
        medic['id'] = result[0][0]
        medic['nume'] = result[0][1]
        medic['prenume'] = result[0][2]
        medic['laborator'] = result[0][3]

    connection.close()

    return medic


def editare_medic(id, nume, prenume, laborator):
    connection = engine.connect()

    try:
        raw_sql_query = text("UPDATE medic SET nume = :nume, prenume = :prenume, laborator_id = :laborator WHERE medic_id = :id")
        result = connection.execute(raw_sql_query, {"id":id, "nume":nume, "prenume":prenume, "laborator":laborator})
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return False
    
    return True


def adaugare_medic(nume, prenume, laborator):
    connection = engine.connect()

    try:
        raw_sql_query = text("INSERT INTO medic (nume, prenume, laborator_id) VALUES (:nume, :prenume, :laborator)")
        result = connection.execute(raw_sql_query, {"nume":nume, "prenume":prenume, "laborator":laborator})
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return False
    
    return True


def lista_dropdown_laboratoare():
    connection = engine.connect()

    raw_sql_query = text("SELECT laborator_id, nume FROM laborator ORDER BY laborator_id")
    result = connection.execute(raw_sql_query)

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'laborator_id': i[0], 
                'nume':i[1]
                } for i in result]
    print(result)

    connection.close()

    return result


def delete_medic_by_id(id):
    connection = engine.connect()

    #try:
    raw_sql_query = text("DELETE FROM medic WHERE medic_id = :id").execution_options(autocommit=True)
    result = connection.execute(raw_sql_query, {"id":id})
    connection.commit()
    connection.close()
    print(
        f"Deleted {result.rowcount} row(s) from ")
    #except:
    #    return False
    
    return True


def lista_analize():
    connection = engine.connect()

    raw_sql_query = text("SELECT A.analiza_id, A.nume_analiza, C.nume_categorie, A.cost_analiza, A.rezultat, A.unitate_masura FROM analiza A INNER JOIN categorie C ON A.categorie_id = C.categorie_id ORDER BY cost_analiza")
    result = connection.execute(raw_sql_query)

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'analiza_id':i[0],
                'nume_analiza': i[1],
                'nume_categorie':i[2], 
                'cost_analiza':i[3],
                'rezultat':i[4],
                'unitate_masura':i[5]
                } for i in result]
    print(result)

    connection.close()

    return result


def lista_categorii():
    connection = engine.connect()

    raw_sql_query = text("SELECT * FROM categorie ORDER BY categorie_id")
    result = connection.execute(raw_sql_query)

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'categorie_id': i[0], 
                'nume_categorie':i[1]
                } for i in result]
    print(result)

    connection.close()

    return result

def get_categorie_by_id(id):
    connection = engine.connect()

    raw_sql_query = text("SELECT * FROM categorie WHERE categorie_id = :id")
    result = connection.execute(raw_sql_query, {"id":id})

    categorie = {}

    # prelucrare rezultat
    result = list(result.fetchall())
    if len(result) == 0:
        categorie = None
    else:
        categorie['id'] = result[0][0]
        categorie['nume_categorie'] = result[0][1]

    connection.close()

    return categorie

def get_laborator_by_id(id):
    connection = engine.connect()

    raw_sql_query = text("SELECT * FROM laborator WHERE laborator_id = :id")
    result = connection.execute(raw_sql_query, {"id":id})

    laborator = {}

    # prelucrare rezultat
    result = list(result.fetchall())
    if len(result) == 0:
        laborator = None
    else:
        laborator['id'] = result[0][0]
        laborator['nume'] = result[0][1]
        laborator['adresa'] = result[0][2]
        laborator['telefon'] = result[0][3]

    connection.close()

    return laborator

def editare_laborator(id, nume, adresa, telefon):
    connection = engine.connect()

    try:
        raw_sql_query = text("UPDATE laborator SET nume = :nume, adresa = :adresa, telefon = :telefon WHERE laborator_id = :id")
        result = connection.execute(raw_sql_query, {"id":id, "nume":nume, "adresa":adresa, "telefon":telefon})
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return False
    
    return True


def adaugare_laborator(nume, adresa, telefon):
    connection = engine.connect()

    try:
        raw_sql_query = text("INSERT INTO laborator (nume, adresa, telefon) VALUES (:nume, :adresa, :telefon)")
        result = connection.execute(raw_sql_query, {"nume":nume, "adresa":adresa, "telefon":telefon})
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return False
    
    return True

def delete_laborator_by_id(id):
    connection = engine.connect()

    #try:
    raw_sql_query = text("DELETE FROM laborator WHERE laborator_id = :id").execution_options(autocommit=True)
    result = connection.execute(raw_sql_query, {"id":id})
    connection.commit()
    connection.close()
    print(
        f"Deleted {result.rowcount} row(s) from ")
    #except:
    #    return False
    
    return True

def adaugare_categorie(nume_categorie):
    connection = engine.connect()

    try:
        raw_sql_query = text("INSERT INTO categorie (nume_categorie) VALUES (:nume_categorie)")
        result = connection.execute(raw_sql_query, {"nume_categorie":nume_categorie})
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return False
    
    return True

def editare_categorie(id, nume_categorie):
    connection = engine.connect()

    try:
        raw_sql_query = text("UPDATE categorie SET nume_categorie = :nume_categorie WHERE categorie_id = :id")
        result = connection.execute(raw_sql_query, {"id":id, "nume_categorie":nume_categorie})
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return False
    
    return True

def delete_categorie_by_id(id):
    connection = engine.connect()

    #try:
    raw_sql_query = text("DELETE FROM categorie WHERE categorie_id = :id").execution_options(autocommit=True)
    result = connection.execute(raw_sql_query, {"id":id})
    connection.commit()
    connection.close()
    print(
        f"Deleted {result.rowcount} row(s) from ")
    #except:
    #   return False
    return True



def lista_buletine():
    connection = engine.connect()

    raw_sql_query = text("SELECT B.buletin_id, concat(P.nume, ' ', P.prenume) AS nume_pacient, concat(M.nume, ' ', M.prenume) AS nume_medic, B.data_recoltarii FROM pacient P INNER JOIN buletin_analize B ON B.pacient_id = P.pacient_id INNER JOIN medic M ON B.medic_id = M.medic_id")
    result = connection.execute(raw_sql_query)

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'buletin_id': i[0],
               'nume_pacient': i[1],
               'nume_medic': i[2],
               'data_recoltarii': i[3]
                } for i in result]
    print(result)

    connection.close()

    return result


def lista_laboratoare():
    connection = engine.connect()

    raw_sql_query = text("SELECT laborator_id, nume, adresa, telefon FROM laborator ORDER BY laborator_id")
    result = connection.execute(raw_sql_query)

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'laborator_id': i[0],
               'nume': i[1],
               'adresa': i[2],
               'telefon': i[3]
                } for i in result]
    print(result)

    connection.close()

    return result


def get_medic_by_lab(lab):
    connection = engine.connect()

    raw_sql_query = text("SELECT M.nume, M.prenume FROM medic M INNER JOIN laborator L ON M.laborator_id = L.laborator_id WHERE L.nume = :lab ORDER BY M.medic_id")
    result = connection.execute(raw_sql_query, {"lab":lab})

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'nume': i[0],
               'prenume': i[1]
                } for i in result]
    print(result)

    connection.close()

    return result


def get_analiza_by_categorie(categorie):
    connection = engine.connect()

    raw_sql_query = text("SELECT A.nume_analiza, A.cost_analiza FROM analiza A INNER JOIN categorie C ON A.categorie_id = C.categorie_id WHERE C.nume_categorie = :categorie ORDER BY A.cost_analiza")
    result = connection.execute(raw_sql_query, {"categorie":categorie})

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'nume_analiza': i[0],
               'cost_analiza': i[1]
                } for i in result]
    print(result)

    connection.close()

    return result


def get_pacient_by_year(year):
    connection = engine.connect()

    raw_sql_query = text("SELECT concat(P.nume, ' ', P.prenume) AS nume_pacient, concat(M.nume, ' ', M.prenume) AS nume_medic, B.data_recoltarii FROM pacient P INNER JOIN buletin_analize B ON B.pacient_id = P.pacient_id INNER JOIN medic M ON B.medic_id = M.medic_id WHERE EXTRACT(YEAR FROM B.data_recoltarii) = :year ORDER BY B.data_recoltarii")
    result = connection.execute(raw_sql_query, {"year":year})

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'nume_pacient': i[0],
               'nume_medic': i[1],
               'data_recoltarii': i[2]
                } for i in result]
    print(result)

    connection.close()

    return result


def lista_analize_by_id(id):
    connection = engine.connect()

    raw_sql_query = text("SELECT (SELECT nume_analiza FROM analiza WHERE analiza_id = LA.analiza_id) AS Nume_analiza,(SELECT rezultat FROM analiza WHERE analiza_id = LA.analiza_id) AS Rezultat, (SELECT unitate_masura FROM analiza WHERE analiza_id = LA.analiza_id) AS Unitate_masura FROM lista_analize LA WHERE LA.buletin_id = :id")
    result = connection.execute(raw_sql_query, {"id":id})

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'nume_analiza': i[0],
               'rezultat': i[1],
               'unitate_masura': i[2]
                } for i in result]
    print(result)

    connection.close()
    return result


def get_analize_by_medic(nume, prenume):
    connection = engine.connect()

    raw_sql_query = text("SELECT (SELECT nume_analiza FROM analiza WHERE analiza_id = LA.analiza_id) AS Nume_analiza, (SELECT rezultat FROM analiza WHERE analiza_id = LA.analiza_id) AS Rezultat, (SELECT unitate_masura FROM analiza WHERE analiza_id = LA.analiza_id) AS Unitate_masura FROM lista_analize LA WHERE LA.buletin_id IN (SELECT buletin_id FROM buletin_analize WHERE medic_id = (SELECT medic_id FROM medic WHERE nume = :nume AND prenume = :prenume))")
    result = connection.execute(raw_sql_query, {"nume":nume, "prenume":prenume})

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'nume_analiza': i[0],
               'rezultat': i[1],
               'unitate_masura': i[2]
                } for i in result]
    print(result)

    connection.close()

    return result


def get_analize_by_month(month):
    connection = engine.connect()

    raw_sql_query = text("SELECT A.nume_analiza, A.rezultat, A.unitate_masura FROM analiza A WHERE A.analiza_id IN (SELECT LA.analiza_id FROM lista_analize LA WHERE LA.buletin_id IN (SELECT BA.buletin_id FROM buletin_analize BA WHERE EXTRACT(MONTH FROM BA.data_recoltarii) = :month))")
    result = connection.execute(raw_sql_query, {"month":month})

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'nume_analiza': i[0],
               'rezultat': i[1],
               'unitate_masura': i[2]
                } for i in result]
    print(result)

    connection.close()

    return result


def get_analize_by_id(id):
    connection = engine.connect()

    raw_sql_query = text("SELECT A.nume_analiza, A.rezultat, A.unitate_masura, A.cost_analiza FROM analiza A WHERE A.analiza_id IN (SELECT LA.analiza_id FROM lista_analize LA WHERE LA.buletin_id IN (SELECT BA.buletin_id FROM buletin_analize BA WHERE BA.pacient_id = :id)) ORDER BY A.cost_analiza")
    result = connection.execute(raw_sql_query, {"id":id})

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'nume_analiza': i[0],
               'rezultat': i[1],
               'unitate_masura': i[2],
               'cost': i[3]
                } for i in result]
    print(result)

    connection.close()

    return result


def get_cost_total(id):
    connection = engine.connect()

    raw_sql_query = text("SELECT (SELECT COUNT(A.analiza_id) FROM analiza A WHERE A.analiza_id IN (SELECT analiza_id FROM lista_analize WHERE buletin_id IN (SELECT buletin_id FROM buletin_analize WHERE pacient_id = :id))) AS numar_analize, (SELECT SUM(A.cost_analiza) FROM analiza A WHERE A.analiza_id IN (SELECT analiza_id FROM lista_analize WHERE buletin_id IN (SELECT buletin_id FROM buletin_analize WHERE pacient_id = :id))) AS cost_total")
    result = connection.execute(raw_sql_query, {"id":id})

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'numar_analize': i[0],
               'cost_total': i[1]
                } for i in result]
    print(result)

    connection.close()

    return result

def get_analiza_by_id1(id):
    connection = engine.connect()

    raw_sql_query = text("SELECT * FROM analiza WHERE analiza_id = :id")
    result = connection.execute(raw_sql_query, {"id":id})

    analiza = {}

    # prelucrare rezultat
    result = list(result.fetchall())
    if len(result) == 0:
        analiza = None
    else:
        analiza['id'] = result[0][0]
        analiza['nume_analiza'] = result[0][1]
        analiza['categorie_id'] = result[0][2]
        analiza['cost_analiza'] = result[0][3]
        analiza['rezultat'] = result[0][4]
        analiza['unitate_masura'] = result[0][5]

    connection.close()

    return analiza

def lista_dropdown_categorii():
    connection = engine.connect()

    raw_sql_query = text("SELECT categorie_id, nume_categorie FROM categorie ORDER BY categorie_id")
    result = connection.execute(raw_sql_query)

    # prelucrare rezultat
    result = list(result.fetchall())
    result = [{'categorie_id': i[0], 
                'nume_categorie':i[1]
                } for i in result]
    print(result)

    connection.close()

    return result

def editare_analiza(id, nume_analiza, nume_categorie, cost_analiza, rezultat, unitate_masura):
    connection = engine.connect()

    try:
        raw_sql_query = text("UPDATE analiza SET nume_analiza = :nume_analiza, categorie_id = :nume_categorie, cost_analiza = :cost_analiza, rezultat = :rezultat, unitate_masura = :unitate_masura WHERE analiza_id = :id")
        result = connection.execute(raw_sql_query, {"id":id, "nume_analiza":nume_analiza, "nume_categorie":nume_categorie, "cost_analiza":cost_analiza, "rezultat":rezultat, "unitate_masura":unitate_masura})
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return False
    
    return True

def adaugare_analiza(nume_analiza, categorie_id, cost_analiza, rezultat, unitate_masura):
    connection = engine.connect()

    try:
        raw_sql_query = text("INSERT INTO analiza (nume_analiza, categorie_id, cost_analiza, rezultat, unitate_masura) VALUES (:nume_analiza, :categorie_id, :cost_analiza, :rezultat, :unitate_masura)")
        result = connection.execute(raw_sql_query, {"nume_analiza":nume_analiza, "categorie_id":categorie_id, "cost_analiza":cost_analiza, "rezultat":rezultat, "unitate_masura":unitate_masura})
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return False
    
    return True

def delete_analiza_by_id(id):
    connection = engine.connect()

    #try:
    raw_sql_query = text("DELETE FROM analiza WHERE analiza_id = :id").execution_options(autocommit=True)
    result = connection.execute(raw_sql_query, {"id":id})
    connection.commit()
    connection.close()
    print(
        f"Deleted {result.rowcount} row(s) from ")
    #except:
    #    return False
    
    return True

    
def adaugare_programare(pacient_id, medic_id, data_programare):
    connection = engine.connect()

    try:
        raw_sql_query = text("INSERT INTO programare (pacient_id, medic_id, data_programare) VALUES (:pacient_id, :medic_id, :data_programare)")
        result = connection.execute(raw_sql_query, {"pacient_id": pacient_id, "medic_id": medic_id, "data_programare": data_programare})
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return False

def get_programari_by_pacient(pacient_id):
    connection = engine.connect()

    raw_sql_query = text("SELECT * FROM programare WHERE pacient_id = :pacient_id")
    result = connection.execute(raw_sql_query, {"pacient_id":pacient_id})

    programare = {}

    # prelucrare rezultat
    result = list(result.fetchall())
    if len(result) == 0:
        programare = None
    else:
        programare['programare_id'] = result[0][0]
        programare['pacient_id'] = result[0][1]
        programare['medic_id'] = result[0][2]
        programare['data_programarii'] = result[0][3]

    connection.close()

    return programare
