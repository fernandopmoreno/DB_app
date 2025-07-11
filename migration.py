import os
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
from supabase import create_client

from aux_functions import resource_path
from models import User

# Function to connect to the Supabase database and authenticate the user
def login(app, user, password):
    if user != "" and password != "":
        try:
            response = app.supabase.auth.sign_in_with_password(
                {
                    "email": user,
                    "password": password
                }
            )
            if hasattr(response, "error") and response.error:
                messagebox.showerror("Error de autenticación", "No se pudo autenticar al usuario. Por favor, verifique sus credenciales.")
                return
            else:
                messagebox.showinfo("Conexión exitosa", "Conexión exitosa a la base de datos")
                for widget in app.login_widgets:
                    widget.destroy()
                app.main_window()
                return
        except Exception as e:
            messagebox.showerror("Error de autenticación", f"No se pudo autenticar al usuario. Error: {e}")
            return
    else:
        messagebox.showwarning("Credenciales faltantes", "Por favor, ingrese su usuario y contraseña para conectarse a la base de datos.")
        return

# Function to format date strings to "YYYY-MM-DD"
def format_fecha(fecha):
    if fecha is None or fecha == "":
        fecha_str = None
    elif isinstance(fecha, pd.Timestamp):
        fecha_str = fecha.strftime("%Y-%m-%d")
    else:
        try:
            fecha_str = pd.to_datetime(fecha).strftime("%Y-%m-%d")
        except Exception:
            fecha_str = None
    return fecha_str

# Function to replace "De", "De L" and "Del" with "de", "de l" and "del" in names
def dels_to_minus(dato):
    dato = dato.title()
    dato = dato.replace(" De L", " de l").replace(" De ", " de ").replace(" Del ", " del ")
    return dato

# Function to read an Excel file and add users to the database
def read_excel(app):
    filename = askopenfilename(filetypes=[("Archivos Excel", "*.xlsx"), ("Archivos Excel", "*.xls")])
    if filename:
        def add_users_from_excel(app):
            df = pd.read_excel(filename)
            df = df.replace(np.nan, None)
            data_to_tables(app, df)
            app.progress_window.after(0, app.main_window)
        app.progress_bar(add_users_from_excel)

# Function to read a CSV file and add users to the database
def read_csv(app):
    filename = askopenfilename(filetypes=[("Archivos csv", "*.csv")])
    if filename:
        def process_csv(app):
            with open(filename, 'r', encoding='utf-8') as file:
                df = pd.read_csv(file, encoding='utf-8')
                df = df.replace(np.nan, None)
                data_to_tables(app, df)
            app.progress_window.after(0, app.main_window)

        app.progress_bar(process_csv)

# Function to convert DataFrame rows to User objects and insert them into the database
def data_to_tables(app, df):
    total_rows = len(df)
    step = 100 / total_rows if total_rows > 0 else 1
    for i in range(total_rows):
        if getattr(app, 'cancel_flag', False):
            break
        user_dict = df.loc[i].to_dict()
        # Create a User object from the DataFrame row
        # Ensure that the fields are properly formatted and handle missing values
        user = User(
            name=dels_to_minus(user_dict["nombre"].strip().title()),
            surname=dels_to_minus(user_dict["apellidos"].strip().title()),
            dni=user_dict["dni"].strip().upper(),
            email = user_dict["email"].strip() if pd.notna(user_dict["email"]) else None,
            phone = str(user_dict["teléfono"]).strip().replace(" ", "") if pd.notna(user_dict["teléfono"]) else None,
            birth_date = format_fecha(user_dict["fecha de nacimiento"]) if pd.notna(user_dict["fecha de nacimiento"]) else None,
            papel=user_dict["papel"],
            agrupacion=user_dict["agrupación"],
            seccion=user_dict["sección"],
            atril = int(user_dict["atril"]) if pd.notna(user_dict["atril"]) else None,
            activo=user_dict["activa"],
            isla = user_dict["isla"].strip().title() if pd.notna(user_dict["isla"]) else None,
            municipio = user_dict["municipio"].strip().title() if pd.notna(user_dict["municipio"]) else None,
            empadronamiento = user_dict["empadronamiento"].strip().title() if pd.notna(user_dict["empadronamiento"]) else None,
            trabajo = user_dict["trabajo"].strip() if pd.notna(user_dict["trabajo"]) else None,
            estudios = user_dict["estudios"].strip() if pd.notna(user_dict["estudios"]) else None,
            matricula_number=user_dict["matrícula"] if pd.notna(user_dict["matrícula"]) else None,
        )
        try:
            app.supabase.table("all_data").insert(user.__dict__).execute()
            print(f"{user.name} {user.surname} agregado con éxito")
        except Exception:
            pass
        step_percent = step * (i + 1)
        # Update the progress bar in the GUI
        app.progress_window.after(0, app.update_progress, i + 1, step_percent, total_rows)

# Function to export all tables from the database to CSV files
def export(app):
    tablas = ["agrupaciones", "empleos", "estructura", "matriculas", "papeles", "residencia", "secciones", "users"]

    for t in tablas:
        data = app.supabase.table(t).select("*").execute()
        df = pd.DataFrame(data.data)
        path = resource_path(f"tables/tabla_{t}.csv")
        df.to_csv(path, index=False)
    messagebox.showinfo("Exportación completada", 
                        f"Las tablas se han exportado correctamente a archivos CSV en {path}.")