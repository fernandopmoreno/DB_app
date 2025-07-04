import os
import sys
from orders import all_data_columns_dictionary_inv
from tkinter import Entry, messagebox
from tooltip import ToolTip

def on_write(event, column, app):
    columnas = [all_data_columns_dictionary_inv[app.col_datos.get(i)] for i in app.col_datos.curselection()]
    texto = event.widget.get()
    query = app.supabase.table("all_data").select(",".join(columnas))
    query = query.ilike(column, f"%{texto}%")
    response = query.execute()
    rows = response.data if hasattr(response, "data") else []
    data = [tuple(row[col] for col in columnas) for row in rows]
    app.create_table(data, columnas)
    return

def on_double_click(app, event):
    # Get the selected row
    region_clicked = app.tabla.identify_region(event.x, event.y)
    # Check if the clicked region is a cell
    if region_clicked != "cell":
        return
    
    # Get the column index and selected item
    column = app.tabla.identify_column(event.x)
    column_index = int(column[1:]) - 1
    selected_iid = app.tabla.focus()
    selected_values = app.tabla.item(selected_iid)["values"]
    column_box = app.tabla.bbox(selected_iid, column)
    
    # Create an Entry widget for editing
    entry_edit = Entry(app.tabla)
    entry_edit.editing_column_index = column_index
    entry_edit.editing_item_iid = selected_iid
    entry_edit.insert(0, selected_values[column_index])
    entry_edit.select_range(0, "end")
    entry_edit.focus()
    entry_edit.bind("<FocusOut>", lambda event: on_focus_out(event))
    entry_edit.bind("<Return>", lambda event: on_enter_pressed(app, event))
    entry_edit.place(x=column_box[0], y=column_box[1], w=column_box[2], h=column_box[3])
    return

# Function to handle closing the application
def on_closing(app):
    if messagebox.askokcancel("Quit", "¿Quiere salir del programa?"):
        app.ventana_main.destroy()

# Delete the Entry widget when focus is lost
def on_focus_out(event):
    event.widget.destroy()
    return

# Function to handle pressing Enter in the Entry widget
def on_enter_pressed(app, event):
    # Save the new text from the Entry widget
    new_text = event.widget.get()

    # Get the selected item ID and column index
    selected_iid = event.widget.editing_item_iid
    column_index = event.widget.editing_column_index

    # Update the selected item in the table
    old_values = app.tabla.item(selected_iid)["values"]
    new_values = old_values.copy()
    new_values[column_index] = new_text
    app.tabla.item(selected_iid, values=new_values)
    event.widget.destroy()

    # Update the database with the new value
    if old_values != new_values:
        app.actualizar_datos(old_values, new_text, column_index)
    return

# Function to obtain the table data based on selected filters
def obtener_tabla(agrupaciones, secciones, columnas, activos, orden, app):
    if activos == "Solo activos":
        activos_list = ["true"]
    elif activos == "Solo inactivos":
        activos_list = ["false"]
    else:
        activos_list = ["true", "false"]
    orden = [all_data_columns_dictionary_inv[item] for item in orden.split(", ")]
    if columnas == [] or (secciones == [] and agrupaciones == []):
        messagebox.showwarning("Ausencia de datos", "Se debe seleccionar al menos una agrupación o sección y un dato para las columnas")
        return

    # Build the query based on the selected filters
    query = app.supabase.table("all_data").select(",".join(columnas))
    query = query.in_("activo", activos_list)
    if agrupaciones:
        query = query.in_("agrupacion", agrupaciones)
    if secciones:
        query = query.in_("seccion", secciones)
    if orden:
        for col in orden:
            query = query.order(col)
    response = query.execute()
    rows = response.data if hasattr(response, "data") else []
    data = [tuple(row[col] for col in columnas) for row in rows]
    app.create_table(data, columnas)
    return

# Function to get the resource path for bundled files
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Function to create a tooltip for a widget
def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    return