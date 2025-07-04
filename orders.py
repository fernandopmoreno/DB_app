all_data_columns_dictionary = {
    "user_id": "ID",
    "surname": "Apellidos",
    "name": "Nombre",
    "dni": "DNI",
    "email": "Correo",
    "phone": "Telefono",
    "birth_date": "Fecha de nacimiento",
    "papel": "Papel",
    "agrupacion": "Agrupación",
    "seccion": "Sección",
    "isla": "Isla",
    "municipio": "Municipio",
    "empadronamiento": "Empadronamiento",
    "trabajo": "Trabajo",
    "estudios": "Estudios",
    "matricula_number": "Matricula",
    "activo": "Activo",
    "atril": "Atril"
}

all_data_columns_dictionary_inv = {v: k for k, v in all_data_columns_dictionary.items()}

papeles_order = ["Músico", "Invitado", "Colaborador", "Empresa Externa"]

agrupaciones_order = ["Orquesta", "Coro", "Ensemble", "Colaboradores", "Empresa Externa"]

secciones_order = [
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