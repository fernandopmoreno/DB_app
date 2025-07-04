import csv
import random
from faker import Faker
import pandas as pd

# This script generates a CSV file with user data for a fictional database.

fake = Faker('es_ES')

papeles = ["Músico", "Invitado", "Colaborador", "Empresa Externa"]
agrupaciones = ["Orquesta", "Coro", "Ensemble", "Colaboradores", "Empresa Externa"]
secciones = [
    "Dirección",
    "Violín primero", "Violín segundo", "Viola", "Violonchelo", "Contrabajo",
    "Flauta", "Oboe", "Clarinete", "Requinto", "Fagot", "Contrafagot", "Saxofón",
    "Trompeta", "Trompa", "Trombón", "Tuba", "Bombardino",
    "Arpa", "Piano", "Órgano", "Percusión",
    "Solista", 
    "Alto (coro)", "Soprano (coro)", "Bajo (coro)", "Tenor (coro)",  "Coach vocal",
    "Colaboradores", "Transportes", 
    "Invitados"
]

islas = [
    "Tenerife", "Gran Canaria", "Lanzarote", "Fuerteventura", "La Palma",
    "La Gomera", "El Hierro", "La Graciosa"
]
municipios = {
    "Tenerife": ["Santa Cruz de Tenerife", "La Laguna", "Arona", "Adeje"],
    "Gran Canaria": ["Las Palmas de Gran Canaria", "Telde", "Santa Lucía"],
    "Lanzarote": ["Arrecife", "Teguise", "San Bartolomé"],
    "Fuerteventura": ["Puerto del Rosario", "La Oliva", "Pájara"],
    "La Palma": ["Santa Cruz de La Palma", "Los Llanos de Aridane"],
    "La Gomera": ["San Sebastián de La Gomera", "Valle Gran Rey"],
    "El Hierro": ["Valverde", "La Frontera"],
    "La Graciosa": ["Caleta de Sebo"]
}

trabajos = [
    "Profesor/a", "Músico/a profesional", "Estudiante", "Ingeniero/a", "Administrativo/a",
    "Autónomo/a", "Desempleado/a", "Empresario/a", "Técnico/a de sonido", "Productor/a musical"
]

estudios = [
    "Grado en Música", "Máster en Interpretación", "Bachillerato", "Doctorado en Música",
    "Grado en Ingeniería", "Formación Profesional", "Educación Secundaria", "Sin estudios superiores"
]

def random_isla_municipio():
    isla = random.choice(islas)
    municipio = random.choice(municipios[isla])
    return isla, municipio

def random_matricula():
    return f"{random.randint(1000,9999)}{random.choice('BCDFGHJKLMNPRSTVWXYZ')}{random.choice('BCDFGHJKLMNPRSTVWXYZ')}{random.choice('BCDFGHJKLMNPRSTVWXYZ')}"

fieldnames = [
    "nombre", "apellidos", "dni", "email", "teléfono", "fecha de nacimiento",
    "sección", "agrupación", "papel", "atril", "isla",
    "municipio", "empadronamiento", "trabajo", "estudios", "matrícula", "activa"
]

section_atril = {section: set() for section in secciones}
rows = []

for _ in range(120):
    nombre = fake.first_name()
    apellidos = fake.last_name()
    dni = fake.unique.bothify(text='########?')
    email = fake.email()
    telefono = fake.phone_number()
    fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d')
    agrupacion = random.choice(agrupaciones)
    seccion = random.choice(secciones)
    papel = random.choice(papeles)
    # Unicidad de atril por sección
    atril = 1
    while str(atril) in section_atril[seccion]:
        atril += 1
    section_atril[seccion].add(str(atril))
    isla, municipio_nac = random_isla_municipio()
    municipio_emp = random.choice(municipios[isla])
    trabajo = random.choice(trabajos)
    estudio = random.choice(estudios)
    matricula = random_matricula()
    activa = random.choice(['True', 'False'])
    row = {
        "nombre": nombre,
        "apellidos": apellidos,
        "dni": dni,
        "email": email,
        "teléfono": telefono,
        "fecha de nacimiento": fecha_nacimiento,
        "sección": seccion,
        "agrupación": agrupacion,
        "papel": papel,
        "atril": str(atril),
        "isla": isla,
        "municipio": municipio_nac,
        "empadronamiento": municipio_emp,
        "trabajo": trabajo,
        "estudios": estudio,
        "matrícula": matricula,
        "activa": activa
    }
    rows.append(row)

# Eliminar datos con probabilidad 0.2
fields_to_keep = ['nombre', 'apellidos', 'dni', 'agrupación', 'sección', 'papel', 'activa']
for row in rows:
    if random.random() < 0.2:
        for key in row.keys():
            if key not in fields_to_keep:
                row[key] = ''

with open('c:/Users/kwgc0/Desktop/OCGC_DB_repo/csv/users.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    df = pd.read_csv('c:/Users/kwgc0/Desktop/OCGC_DB_repo/csv/users.csv')
    df.to_excel('c:/Users/kwgc0/Desktop/OCGC_DB_repo/excel/users.xlsx', index=False)