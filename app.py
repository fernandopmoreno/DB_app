import threading
from tkinter import ttk
from tkinter import *
from dotenv import load_dotenv

from aux_functions import obtener_tabla, on_double_click, on_write, resource_path
from list_files import listado_pdf, listado_word
from migration import *
from orders import all_data_columns_dictionary, all_data_columns_dictionary_inv


class App:

    def __init__(self, root):

        self.connect()

        # Login window
        self.root = root
        self.root.withdraw()
        self.ventana_login = Toplevel(root)
        self.ventana_login.title("Inicio de sesión")
        screen_width = self.ventana_login.winfo_screenwidth()
        screen_height = self.ventana_login.winfo_screenheight()
        self.ventana_login.geometry(f"+{int(screen_width/2) - 100}+{int(screen_height/2) - 100}")
        #self.ventana_login.iconbitmap(resource_path("images/logo.ico"))

        user_label = Label(self.ventana_login, text="Usuario:")
        user_label.pack(padx=10)
        self.user_entry = Entry(self.ventana_login, width=30)
        self.user_entry.pack(padx=10)
        password_label = Label(self.ventana_login, text="Contraseña:")
        password_label.pack(padx=10)
        self.password_entry = Entry(self.ventana_login, width=30, show="*")
        self.password_entry.pack(padx=10)
        button_remote = Button(self.ventana_login, text="Conectar", command=lambda: login(self, 
                                                                                        self.user_entry.get(), 
                                                                                        self.password_entry.get()))
        button_remote.pack(padx=10, pady=10)
        self.login_widgets = [user_label, self.user_entry, password_label, self.password_entry, button_remote]

    def connect(self):
        load_dotenv(override=True)
        self.supabase = create_client(
            # .env in project must contain URL and KEY for Supabase
            os.getenv("URL"),
            os.getenv("KEY")
        )

    def main_window(self):
        # Main window
        if hasattr(self, 'ventana_main') and self.ventana_main.winfo_exists():
            for widget in self.ventana_main.winfo_children():
                widget.destroy()
        else:
            self.ventana_main = Toplevel(self.root)
            self.ventana_login.destroy()
        self.ventana_main.title("DB")
        screen_width = self.ventana_main.winfo_screenwidth()
        screen_height = self.ventana_main.winfo_screenheight()
        window_width = int(screen_width)
        window_height = int(screen_height)
        self.ventana_main.geometry(f"{window_width}x{window_height}+{int((screen_width-window_width)/2)}+{int((screen_height-window_height)/2)}")
        self.ventana_main.resizable(True, True)
        #self.ventana_main.iconbitmap(resource_path("images/logo.ico"))
        self.ventana_main.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())

        self.actualizar_columnas()

        # Frame to hold the filter options and buttons
        self.frame_options = Frame(self.ventana_main)
        frame_act_tabla = Frame(self.frame_options)

        # Agrupaciones in database
        frame_group = Frame(frame_act_tabla)        
        sections_label = Label(frame_group, text="Agrupaciones")
        sections_label.pack(anchor=W)
        col_agrupaciones_tabla = Listbox(frame_group, selectmode=MULTIPLE, width=30, height=len(self.agrupaciones), exportselection=0)
        for value in self.agrupaciones:
            col_agrupaciones_tabla.insert(END, value)
        col_agrupaciones_tabla.pack()
        frame_group.pack(padx=5, pady=5)

        # Secciones in database
        frame_sec = Frame(frame_act_tabla)        
        sections_label = Label(frame_sec, text="Secciones")
        sections_label.pack(anchor=W)
        col_secciones_tabla = Listbox(frame_sec, selectmode=MULTIPLE, width=30, height=10, exportselection=0)
        for value in self.secciones:
            col_secciones_tabla.insert(END, value)
        col_secciones_tabla.pack()
        frame_sec.pack(padx=5, pady=5)
        
        # Data in database
        frame_datos = Frame(frame_act_tabla)
        datos_label = Label(frame_datos, text="Datos")
        datos_label.pack(anchor=W)
        self.col_datos = Listbox(frame_datos, selectmode=MULTIPLE, width=30, height=10, exportselection=0)
        for key in all_data_columns_dictionary_inv:
            self.col_datos.insert(END, key)
        self.col_datos.pack()
        frame_datos.pack(padx=5, pady=5)

        # Options for active/inactive members
        activos_box = ttk.Combobox(frame_act_tabla, state="readonly", values=["Solo activos", "Solo inactivos", "Todos"])
        activos_box.set("Solo activos")
        activos_box.pack(padx=5, pady=5, fill=X)

        # Options for order
        orden_box = ttk.Combobox(frame_act_tabla, state="readonly", values=["Apellidos", "Agrupación", "Sección", "Atril", "Agrupación, Sección, Atril"])
        orden_box.set("Apellidos")
        orden_box.pack(padx=5, pady=5, fill=X)

        # Frame to hold the action buttons
        frame_buttons = Frame(frame_act_tabla)

        # Update table according to the selected filters
        button_actualizar = Button(frame_buttons, text="Actualizar tabla", 
                                        command=lambda: obtener_tabla(
                                            agrupaciones=[col_agrupaciones_tabla.get(i) for i in col_agrupaciones_tabla.curselection()],
                                            secciones=[col_secciones_tabla.get(i) for i in col_secciones_tabla.curselection()], 
                                            columnas=[all_data_columns_dictionary_inv[self.col_datos.get(i)] for i in self.col_datos.curselection()],
                                            activos=activos_box.get(),
                                            orden=orden_box.get(),
                                            app=self
                                        ))
        button_actualizar.grid(row=0, column=0, pady=5)

        # Create PDF or Word document
        button_pdf = Button(frame_buttons, text="Crear listado", command=self.create_file)
        button_pdf.grid(row=0, column=1, pady=5)

        # Export all tables to CSV
        button_export = Button(frame_buttons, text="Exportar tablas", command=lambda: export(self))
        button_export.grid(row=0, column=2, pady=5)

        # Add user or read from Excel/CSV
        button_add_user = Button(frame_buttons, text="Añadir usuario", command=self.add_user)
        button_add_user.grid(row=1, column=0, pady=5)

        button_read_excel = Button(frame_buttons, text="Leer Excel", command=lambda: read_excel(self))
        button_read_excel.grid(row=1, column=1, pady=5)

        button_read_csv = Button(frame_buttons, text="Leer CSV", command=lambda: read_csv(self))
        button_read_csv.grid(row=1, column=2, pady=5)

        frame_buttons.pack()
        frame_act_tabla.pack(expand=True, fill=BOTH, anchor=NW)
        self.frame_options.grid(row=1, column=0, padx=5)

        # Initialize the table frame
        self.frame_tabla = Frame(self.ventana_main)
        self.frame_buscar = LabelFrame(self.frame_tabla)
        self.tabla = ttk.Treeview(self.frame_tabla, columns=[], show="headings")
        self.scrollbar_tabla = Scrollbar(self.frame_tabla)
        self.frame_tabla.grid(row=1, column=1, padx=5, pady=5)

    def create_table(self, rows, columnas):
        # Destroy previous table
        self.frame_buscar.destroy()
        self.tabla.destroy()
        self.scrollbar_tabla.destroy()

        # Search frame
        self.frame_buscar = LabelFrame(self.frame_tabla, text="Buscar")
        name_search_label = Label(self.frame_buscar, text="Nombre")
        name_search_label.grid(row=0, column=0)
        self.name_search_entry = Entry(self.frame_buscar, width=20)
        self.name_search_entry.bind("<Return>", lambda event: on_write(event, "name", self))
        self.name_search_entry.grid(row=0, column=1, padx=5)
        surname_search_label = Label(self.frame_buscar, text="Apellidos")
        surname_search_label.grid(row=0, column=2)
        self.surname_search_entry = Entry(self.frame_buscar, width=20)
        self.surname_search_entry.grid(row=0, column=3, padx=5)
        self.surname_search_entry.bind("<Return>", lambda event: on_write(event, "surname", self))
        self.frame_buscar.pack(padx=16, pady=5, anchor=E)

        # New table
        self.scrollbar_tabla = Scrollbar(self.frame_tabla, orient="vertical")
        self.scrollbar_tabla.pack(side=RIGHT, fill=Y)
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, height=43, show="headings", yscrollcommand=self.scrollbar_tabla.set)
        self.scrollbar_tabla.config(command=self.tabla.yview)
        self.tabla.bind("<Double-1>", lambda event: on_double_click(self, event))
        self.tabla.pack()
        for key in columnas:
            self.tabla.heading(key, text=all_data_columns_dictionary[key])
            self.tabla.column(key, width=int((self.ventana_main.winfo_width()-self.frame_options.winfo_width()-50)/len(columnas)))
        for row in rows:
            self.tabla.insert("", "end", values=row)
        return

    def actualizar_datos(self, old_values, new_text, column_index):
        # Convert old values to string if they are not None
        old_values = [str(item) for item in old_values]

        # Column names from the Listbox
        columnas = [all_data_columns_dictionary_inv[self.col_datos.get(i)] for i in self.col_datos.curselection()]

        # Create a dictionary to match the old values with the column names
        filters = {}
        for i in range(len(old_values)):
            value = old_values[i]
            col = columnas[i]
            if value == "None":
                filters[col] = None
            else:
                filters[col] = value

        # Query the database to find the estructura_id that matches the filters
        result = self.supabase.table("all_data").select("estructura_id").match(filters).execute()
        if result.data and len(result.data) > 0:
            estructura_id = result.data[0]["estructura_id"]
            # Update the specific column with the new text
            update_col = columnas[column_index]
            self.supabase.table("all_data").update({update_col: new_text}).eq("estructura_id", estructura_id).execute()
        return


    def add_user(self):
        # Add user window
        self.ventana_add = Toplevel()
        self.ventana_add.title("Añadir nuevo usuario")
        screen_width = self.ventana_add.winfo_screenwidth()
        self.ventana_add.geometry(f"+{int(screen_width/2)}+50")
        #self.ventana_add.iconbitmap(resource_path("images/logo.ico"))

        # labels and inputs for each field in the all_data_columns_dictionary
        labels = []
        inputs = []
        for value in list(all_data_columns_dictionary.values())[1:]:
            label = Label(self.ventana_add, text=value)
            input = Entry(self.ventana_add, width=30)
            i = list(all_data_columns_dictionary.values()).index(value)
            label.grid(sticky="W", row=i, column=0, padx=5)
            input.grid(sticky="W", row=i, column=1, padx=5)
            labels.append(label)
            inputs.append(input)

        # Button to submit the data
        add_button = Button(
            self.ventana_add,
            text="Añadir datos",
            command=lambda: self.add_user_manual_app(
                {all_data_columns_dictionary_inv[label.cget("text")]: input.get()
                for label, input in zip(labels, inputs)}
            )
        )
        add_button.grid(row=i+1, column=0, columnspan=2, pady=5)
        return

    def add_user_manual_app(self, data):
        # Check if the required fields are filled
        if data["name"] == "" or data["surname"] == "" or data["dni"] == "" or data["agrupacion"] == "" or data["seccion"] == "" or data["papel"] == "":
            messagebox.showerror("Error", "Los campos Nombre, Apellidos, DNI, Agrupación, Sección y Papel son obligatorios")
            return
        else:
            for key in data:
                # Convert empty strings to None
                if data[key] == "":
                    data[key] = None
            # Insert the data into the database
            self.supabase.table("all_data").insert(data).execute()
            messagebox.showinfo("Usuario añadido", "El usuario ha sido añadido con éxito")

    def create_file(self):
        # Create file window
        self.ventana_listado = Toplevel()
        self.ventana_listado.title("Crear listado")
        screen_width = self.ventana_listado.winfo_screenwidth()
        screen_height = self.ventana_listado.winfo_screenheight()
        window_width = int(screen_width * 0.25)
        window_height = int(screen_height * 0.8)
        self.ventana_listado.geometry(f"{window_width}x{window_height}+{int((screen_width-window_width)/2)}+{int((screen_height-window_height)/2)}")
        #self.ventana_listado.iconbitmap(resource_path("images/logo.ico"))

        frame_pdf_agroup_sec = Frame(self.ventana_listado)

        # Selection of agrupaciones, secciones and papeles for the PDF
        col_agrupaciones_pdf = Listbox(frame_pdf_agroup_sec, selectmode=MULTIPLE, width=30, height=4, exportselection=0)
        for value in self.agrupaciones:
            col_agrupaciones_pdf.insert(END, value)
        col_agrupaciones_pdf.pack(pady=5)

        scrollbar_pdf_2 = Scrollbar(frame_pdf_agroup_sec, orient="vertical")
        scrollbar_pdf_2.pack(side=RIGHT, fill=Y)
        col_secciones_pdf = Listbox(frame_pdf_agroup_sec, selectmode=MULTIPLE, width=30, height=20, yscrollcommand=scrollbar_pdf_2.set, exportselection=0)
        scrollbar_pdf_2.config(command=col_secciones_pdf.yview)
        for value in self.secciones:
            col_secciones_pdf.insert(END, value)
        col_secciones_pdf.pack(pady=5)

        frame_pdf_agroup_sec.grid(row=1, column=0, pady=5)

        frame_pdf_papeles_datos = Frame(self.ventana_listado)

        col_papeles_pdf = Listbox(frame_pdf_papeles_datos, selectmode=MULTIPLE, width=30, height=4, exportselection=0)
        for value in self.papeles:
            col_papeles_pdf.insert(END, value)
        col_papeles_pdf.pack(pady=5)

        # Selection of data columns for the file
        scrollbar_pdf_3 = Scrollbar(frame_pdf_papeles_datos, orient="vertical")
        scrollbar_pdf_3.pack(side=RIGHT, fill=Y)
        col_datos_pdf = Listbox(frame_pdf_papeles_datos, selectmode=MULTIPLE, width=30, height=20, yscrollcommand=scrollbar_pdf_3.set, exportselection=0)
        scrollbar_pdf_3.config(command=col_datos_pdf.yview)
        for value in all_data_columns_dictionary.values():
            col_datos_pdf.insert(END, value)
        col_datos_pdf.pack(pady=5)
        frame_pdf_papeles_datos.grid(row=1, column=1, pady=5)

        # Sorting options
        orden = LabelFrame(self.ventana_listado, text="Ordenar por")
        orden_box = ttk.Combobox(orden, state="readonly", values=["Apellidos", "Sección", "Atril"])
        orden_box.set("Apellidos")
        orden.grid(sticky="W", row=25, column=0, padx=5)
        orden_box.grid(sticky="W",row=26, column=0, padx=5)

        # Option to separate by sections, agrupations, papers or not
        separar = LabelFrame(self.ventana_listado, text="Separar por")
        separar_box = ttk.Combobox(separar, state="readonly", values=["Secciones", "Agrupaciones", "Papeles", "No separar"])
        separar_box.set("Secciones")
        separar.grid(sticky="W", row=25, column=1, padx=5)
        separar_box.grid(sticky="W",row=26, column=1, padx=5)

        # Option to select active, inactive or all members
        activos = LabelFrame(self.ventana_listado, text="Seleccionar")
        activos_box_pdf = ttk.Combobox(activos, state="readonly", values=["Solo activos", "Solo inactivos", "Todos"])
        activos_box_pdf.set("Solo activos")
        activos.grid(sticky="W", row=27, column=0, padx=5)
        activos_box_pdf.grid(sticky="W",row=28, column=0, padx=5)

        # Option to union name and surname
        union = LabelFrame(self.ventana_listado, text="Unir nombre y apellidos")
        union_box = ttk.Combobox(union, state="readonly", values=["Nombre,Apellidos", "Apellidos,Nombre"])
        union_box.set("")
        union.grid(sticky="W", row=27, column=1, padx=5)
        union_box.grid(sticky="W",row=28, column=1, padx=5)

        # checkboxes for additional settings
        ajustes = LabelFrame(self.ventana_listado, text="Ajustes")
        self.numerar_var = BooleanVar()
        numerar_box = Checkbutton(ajustes, text="Filas numeradas", variable=self.numerar_var, command=lambda: self.clicked(value=self.numerar_var.get()))
        numerar_box.grid(sticky="W", row=29, column=0, padx=5)
        self.destacados_secc = BooleanVar()
        destacados_secc = Checkbutton(ajustes, text="Separar cabeza y destacados de sección", variable=self.destacados_secc, command=lambda: self.clicked(value=self.destacados_secc.get()))
        destacados_secc.grid(sticky="W", row=30, column=0, padx=5)
        ajustes.grid(sticky="W", row=30, column=0, padx=5)

        # Width of columns in the PDF
        ancho_columnas = LabelFrame(self.ventana_listado, text="Ancho de columnas")
        ancho_columnas_entry = Entry(ancho_columnas)
        ancho_columnas_entry.insert(0, "10, 60, 60, 30, 30")
        ancho_columnas_entry.grid(sticky="W", row=29, column=1, padx=5)
        ancho_columnas.grid(sticky="W", row=30, column=1, padx=5)

        # Text box for the header
        cabecera = LabelFrame(self.ventana_listado, text="Texto de cabecera")
        cabecera_pdf_box = Text(cabecera, height=5, width=50)
        cabecera_pdf_box.grid(sticky="W", row=32, column=0, columnspan=2, padx=5, pady=5)
        cabecera.grid(sticky="W", row=33, column=0, columnspan=2, padx=5, pady=5)

        # File name input
        nombre_pdf = LabelFrame(self.ventana_listado, text="Nombre del archivo pdf")
        nombre_pdf_box = Entry(nombre_pdf)
        nombre_pdf_box.insert(0, "prueba")
        nombre_pdf.grid(sticky="W", row=34, column=0, columnspan=2, padx=5, pady=5)
        nombre_pdf_box.grid(sticky="W", row=35, column=0, columnspan=2, padx=5, pady=5)

        # Buttons to create PDF or Word document
        pdf_button = Button(self.ventana_listado, text="Crear PDF", command=lambda: listado_pdf(
                                                                                                    self,
                                                                                                    [col_agrupaciones_pdf.get(i) for i in col_agrupaciones_pdf.curselection()],
                                                                                                    [col_secciones_pdf.get(i) for i in col_secciones_pdf.curselection()], 
                                                                                                    [col_papeles_pdf.get(i) for i in col_papeles_pdf.curselection()],
                                                                                                    [all_data_columns_dictionary_inv[col_datos_pdf.get(i)] for i in col_datos_pdf.curselection()],
                                                                                                    all_data_columns_dictionary_inv[orden_box.get()],
                                                                                                    separar_box.get(),
                                                                                                    activos_box_pdf.get(),
                                                                                                    union_box.get(),
                                                                                                    self.numerar_var.get(),
                                                                                                    self.destacados_secc.get(),
                                                                                                    ancho_columnas_entry.get(),
                                                                                                    cabecera_pdf_box.get("1.0", "end"),
                                                                                                    nombre_pdf_box.get())
                                                                                                    )
        pdf_button.grid(sticky="W", row=35, column=0, padx=20, pady=5, columnspan=2)
        word_button = Button(self.ventana_listado, text="Crear word", command=lambda: listado_word(
                                                                                                    self,
                                                                                                    [col_agrupaciones_pdf.get(i) for i in col_agrupaciones_pdf.curselection()],
                                                                                                    [col_secciones_pdf.get(i) for i in col_secciones_pdf.curselection()], 
                                                                                                    [col_papeles_pdf.get(i) for i in col_papeles_pdf.curselection()],
                                                                                                    [all_data_columns_dictionary_inv[col_datos_pdf.get(i)] for i in col_datos_pdf.curselection()],
                                                                                                    all_data_columns_dictionary_inv[orden_box.get()],
                                                                                                    separar_box.get(),
                                                                                                    activos_box_pdf.get(),
                                                                                                    union_box.get(),
                                                                                                    self.numerar_var.get(),
                                                                                                    self.destacados_secc.get(),
                                                                                                    ancho_columnas_entry.get(),
                                                                                                    cabecera_pdf_box.get("1.0", "end"),
                                                                                                    nombre_pdf_box.get())
                                                                                                    )
        word_button.grid(sticky="W", row=35, column=1, padx=20, pady=5, columnspan=2)
        return
    
    # Function to handle checkbox clicks
    def clicked(self, value):
        value.set(not value.get())
        return

    # Function to update the columns in the Listbox widgets
    def actualizar_columnas(self):
        result_papeles = self.supabase.table("papeles").select("papel").order("papel").execute()
        self.papeles = [item["papel"] for item in result_papeles.data] if result_papeles.data else []

        result_agrupaciones = self.supabase.table("agrupaciones").select("agrupacion").order("agrupacion").execute()
        self.agrupaciones = [item["agrupacion"] for item in result_agrupaciones.data] if result_agrupaciones.data else []

        result_secciones = self.supabase.table("secciones").select("seccion").order("seccion").execute()
        self.secciones = [item["seccion"] for item in result_secciones.data] if result_secciones.data else []

    def progress_bar(self, function):
        # Create the progress window
        self.cancel_flag = False
        self.progress_window = Toplevel()
        self.progress_window.title("Progreso")
        screen_width = self.progress_window.winfo_screenwidth()
        screen_height = self.progress_window.winfo_screenheight()
        self.progress_window.geometry(f"+{int(screen_width/2) - 100}+{int(screen_height/2) - 100}")
        #self.progress_window.iconbitmap(resource_path("images/logo.ico"))
        self.progress_window.resizable(False, False)
        text_progress = Label(self.progress_window, text="Cargando datos...")
        text_progress.pack()
        self.progressbar_widget = ttk.Progressbar(self.progress_window, orient="horizontal", length=200, mode="determinate", maximum=100)
        self.progressbar_widget.pack(padx=20, pady=20)
        self.percent_label = Label(self.progress_window, text="0%")
        self.percent_label.pack()
        cancel_button = Button(self.progress_window, text="Cancelar", command=self.cancel_progress)
        cancel_button.pack(pady=5)
        # Start the thread
        threading.Thread(target=function, args=(self,), daemon=True).start()

    # Function to cancel the progress bar
    def cancel_progress(self):
        self.cancel_flag = True
        self.progress_window.destroy()
        messagebox.showinfo("Cancelado", "La operación ha sido cancelada.")

    # Function to update the progress bar
    def update_progress(self, step, step_percent, total_steps):
        if getattr(self, 'cancel_flag', False):
            return
        self.progressbar_widget["value"] = step_percent
        self.percent_label.config(text=f"{self.progressbar_widget['value']:.1f}% ({step}/{total_steps})")
        self.progress_window.update_idletasks()
        if self.progressbar_widget['value'] >= 100:
            self.progressbar_widget.stop()
            self.progress_window.destroy()
            messagebox.showinfo("Carga completa", "Los datos se han cargado correctamente.")
            self.main_window()