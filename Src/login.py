import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ----------------------------------------------------------------------------------------------------------------
conn = sqlite3.connect('hospital_datos.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS USUARIOS(
        id_usuario TEXT PRIMARY KEY,
        contraseña TEXT
    )
''')
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS PACIENTES(
        id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        apellido TEXT,
        fecha_de_nacimiento TEXT,
        edad INTEGER,
        telefono INTEGER,
        correo TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ESPECIALIDADES(
        id_especialidad INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS MEDICOS(
        id_medico INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        apellido TEXT,
        id_especialidad INTEGER,
        telefono INTEGER,
        FOREIGN KEY (id_especialidad) REFERENCES ESPECIALIDADES (id_especialidad)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS TURNOS(
        id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
        id_medico INTEGER,
        id_paciente INTEGER,
        fecha TEXT,
        hora TEXT,
        estado TEXT,
        FOREIGN KEY (id_medico) REFERENCES MEDICOS (id_medico),
        FOREIGN KEY (id_paciente) REFERENCES PACIENTES (id_paciente)
    )
''')

conn.commit()
# ----------------------------------------------------------------------------------------------------------------

app = tk.Tk()

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x400")
        self.root.configure(bg="#e2e8f3")
        
        marco = tk.Frame(app, width=600, height=600, bd=2, relief="solid",  background="white")
        marco.pack(pady=80)
        
        self.etiqueta = tk.Label(marco, text="Bienvenido al Sistema de Gestion de Clinicas", font=("Georgia", 15), fg="#486f99", background="white")
        self.etiqueta.pack(pady=20, padx=20)
        
        tk.Label(marco, text="Usuario", font=("Arial", 10), fg="black", background="white").pack(pady=5)
        self.entrada_usuario = tk.Entry(marco)
        self.entrada_usuario.pack(pady=5)
        
        tk.Label(marco, text="Contraseña", font=("Arial", 10), fg="black", background="white").pack(pady=5)
        self.entrada_contraseña = tk.Entry(marco, show="*")
        self.entrada_contraseña.pack(pady=5)
        
        btn_login = tk.Button(marco, text="Iniciar sesión", command=self.inicio, background="#e2e8f3")
        btn_login.pack(pady=10)

    def inicio(self):
        id_usuario = self.entrada_usuario.get()
        contraseña = self.entrada_contraseña.get()

        if id_usuario and contraseña:
            try:
                cursor.execute("INSERT INTO USUARIOS (id_usuario, contraseña) VALUES (?, ?)", (id_usuario, contraseña))
                conn.commit()
                messagebox.showinfo("Éxito", "Has logrado ingresar al sistema.")
                self.abrir_ventana_principal()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El usuario ya existe.")
                self.abrir_ventana_principal()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

# ----------------------------------------------------------------------------------------------------------------

    def abrir_ventana_principal(self):
        self.root.withdraw()

        self.nueva_ventana = tk.Toplevel(self.root)
        self.nueva_ventana.title("Sistema de Gestión")
        self.nueva_ventana.geometry("600x400")
        self.nueva_ventana.configure(bg="#e2e8f3")
        
        tk.Label(self.nueva_ventana, text="Grey Sloan Memorial Hospital", font=("Georgia", 15), fg="#486f99", background="#e2e8f3").pack(pady=10)
        
        imagen_original = Image.open("Src/portada-4.jpg")
        imagen_redimensionada = imagen_original.resize((400, 250)) 
        self.imagen = ImageTk.PhotoImage(imagen_redimensionada)
        self.imagen_label = tk.Label(self.nueva_ventana, image=self.imagen, bg="#e2e8f3")
        self.imagen_label.pack(pady=10)
        
        tk.Button(self.nueva_ventana, background="white",text="Salir", command=self.root.destroy).pack(pady=20)
        
        self.barra_menus = tk.Menu(self.nueva_ventana)
        self.nueva_ventana.config(menu=self.barra_menus)
        
        self.menu = tk.Menu(self.barra_menus, tearoff=0)
        self.crear_menus(self.menu)
        self.barra_menus.add_cascade(label="Opciones", menu=self.menu)
        
    def crear_menus(self, menu):
        menu.add_command(label="Pacientes", command=self.ventana_Pacientes)
        menu.add_command(label="Medicos", command=self.ventana_Doctores)
        menu.add_command(label="Especialidad", command=self.ventana_Especialidad)
        menu.add_command(label="Turnos", command=self.ventana_Turnos)

# ----------------------------------------------------------------------------------------------------------------

    def ventana_Pacientes(self):
        if hasattr(self, 'nueva_ventana') and self.nueva_ventana:
            self.nueva_ventana.destroy()
        
        self.root.withdraw()
        
        self.conn = sqlite3.connect("hospital_datos.db")
        self.cursor = self.conn.cursor()
        
        pacientes_ventana = tk.Toplevel(self.root)
        pacientes_ventana.title("Sistema de Gestión")
        pacientes_ventana.geometry("600x400")
        pacientes_ventana.configure(bg="#e2e8f3")
        
        marco = tk.Frame(pacientes_ventana, bg="white", width=600, height=600, bd=2, relief="solid",  background="white")
        marco.pack(pady=40)
        
        self.etiqueta = tk.Label(marco, text="Gestión de Pacientes del Hospital", font=("Georgia", 15), fg="#486f99", background="white")
        self.etiqueta.pack(pady=10, padx=20)
        
        tk.Label(marco, text="Nombre del Paciente: ", bg="white").pack(pady=5)
        self.entrada_buscar = tk.Entry(marco)
        self.entrada_buscar.pack(pady=5, padx=10)
        
        tk.Button(marco, text="Buscar", command=self.buscar_Pacientes).pack(pady=5, padx=5)
        
        self.lista_pacientes = tk.Listbox(marco, width=50, height=5)
        self.lista_pacientes.pack(pady=20, padx=10)
        self.buscar_Pacientes()
        
        tk.Button(pacientes_ventana, text="Regresar", command=lambda: self.regresar_a_principal(pacientes_ventana)).pack(pady=5)
        
        barra_menus_pacientes = tk.Menu(pacientes_ventana)
        pacientes_ventana.config(menu=barra_menus_pacientes)
    
        menu_Pacientes = tk.Menu(barra_menus_pacientes, tearoff=0)
        menu_Pacientes.add_command(label="Agregar Paciente", command=self.agregar_Pacientes)
        menu_Pacientes.add_command(label="Eliminar Paciente", command=self.eliminar_Pacientes)
        menu_Pacientes.add_command(label="Modificar Informacion de Paciente", command=self.modificar_Pacientes)
        barra_menus_pacientes.add_cascade(label="Opciones", menu=menu_Pacientes)


    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def buscar_Pacientes(self):
        conn = sqlite3.connect('hospital_datos.db')
        cursor = conn.cursor()

        texto_buscar = self.entrada_buscar.get().strip()

        if texto_buscar:
            query = "SELECT * FROM PACIENTES WHERE nombre LIKE ?"
            cursor.execute(query, (f"%{texto_buscar}%",))
        else:
            query = "SELECT * FROM PACIENTES"
            cursor.execute(query)
    
        pacientes = cursor.fetchall()
    
        self.lista_pacientes.delete(0, tk.END)
    
    # Mostrar los pacientes encontrados
        for paciente in pacientes:
            texto_pacientes = (f"Id_Paciente: {paciente[0]}, Nombre: {paciente[1]}, "
                            f"Apellido: {paciente[2]}, Fecha Nacimiento: {paciente[3]}, "
                            f"Edad: {paciente[4]}, Telefono: {paciente[5]}, Correo: {paciente[6]}")
        self.lista_pacientes.insert(tk.END, texto_pacientes)

    def regresar_a_principal(self, ventana_actual):
        ventana_actual.destroy()
        self.abrir_ventana_principal()

    def agregar_Pacientes(self):
        def guardar_Paciente():
            nombre = entrada_nombre.get()
            apellido = entrada_apellido.get()
            fecha_de_nacimiento = entrada_fecha_de_nacimiento.get()
            edad = entrada_edad.get()
            telefono = entrada_telefono.get()
            correo = entrada_correo.get()

            if nombre and apellido and fecha_de_nacimiento and edad and telefono and correo:
                try:
                    telefono = int(telefono)
                    cursor.execute("INSERT INTO PACIENTES (nombre, apellido, fecha_de_nacimiento, edad, telefono, correo) VALUES (?, ?, ?, ?, ?, ?)", (nombre, apellido, fecha_de_nacimiento, edad, telefono, correo))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Paciente agregado correctamente.")
                    ventana_agregar.destroy()
                    self.buscar_Pacientes()
                except ValueError:
                    messagebox.showerror("Error", "El telefono debe ser un número entero.")
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")

        ventana_agregar = tk.Toplevel(app)
        ventana_agregar.title("Agregar Paciente")
        ventana_agregar.geometry("300x250")

        etiqueta_nombre = tk.Label(ventana_agregar, text="Nombre:")
        etiqueta_nombre.grid(row=0, column=0, padx=5, pady=5)

        entrada_nombre = tk.Entry(ventana_agregar)
        entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

        etiqueta_apellido = tk.Label(ventana_agregar, text="Apellido:")
        etiqueta_apellido.grid(row=1, column=0, padx=5, pady=5)

        entrada_apellido = tk.Entry(ventana_agregar)
        entrada_apellido.grid(row=1, column=1, padx=5, pady=5)

        etiqueta_nacimiento = tk.Label(ventana_agregar, text="Fecha de Nacimiento:")
        etiqueta_nacimiento.grid(row=2, column=0, padx=5, pady=5)

        entrada_fecha_de_nacimiento = tk.Entry(ventana_agregar)
        entrada_fecha_de_nacimiento.grid(row=2, column=1, padx=5, pady=5)
        
        etiqueta_edad = tk.Label(ventana_agregar, text="Edad:")
        etiqueta_edad.grid(row=3, column=0, padx=5, pady=5)

        entrada_edad = tk.Entry(ventana_agregar)
        entrada_edad.grid(row=3, column=1, padx=5, pady=5)
        
        etiqueta_telefono = tk.Label(ventana_agregar, text="Telefono:")
        etiqueta_telefono.grid(row=4, column=0, padx=5, pady=5)

        entrada_telefono = tk.Entry(ventana_agregar)
        entrada_telefono.grid(row=4, column=1, padx=5, pady=5)
        
        etiqueta_correo = tk.Label(ventana_agregar, text="Correo:")
        etiqueta_correo.grid(row=5, column=0, padx=5, pady=5)

        entrada_correo = tk.Entry(ventana_agregar)
        entrada_correo.grid(row=5, column=1, padx=5, pady=5)

        boton_guardar = tk.Button(ventana_agregar, text="Guardar", command=guardar_Paciente)
        boton_guardar.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
    
    def modificar_Pacientes(self):
        return
    
    def eliminar_Pacientes(self):
        return

# ----------------------------------------------------------------------------------------------------------------
    def ventana_Doctores(self):
        if hasattr(self, 'nueva_ventana') and self.nueva_ventana:
            self.nueva_ventana.destroy()
        
        self.root.withdraw()

        pacientes_ventana = tk.Toplevel(self.root)
        pacientes_ventana.title("Sistema de Gestión")
        pacientes_ventana.geometry("600x400")
        pacientes_ventana.configure(bg="#e2e8f3")
        
        tk.Label(pacientes_ventana, text="Gestión de Doctores", font=("Georgia", 15), fg="#486f99", background="#e2e8f3").pack(pady=10, padx=10)
        tk.Button(pacientes_ventana, text="Regresar", command=lambda: self.regresar_a_principal(pacientes_ventana)).pack(pady=50)

    def regresar_a_principal(self, ventana_actual):
        ventana_actual.destroy()
        self.abrir_ventana_principal()

    # Funciones para Doctores
    def mostrar_Doctores():
        return
    
    def agregar_Doctores():
        return
    
    def eliminar_Doctores():
        return
    
    def modificar_Doctores():
        return

# ----------------------------------------------------------------------------------------------------------------
    # Funciones para Especialidades 
    def ventana_Especialidad(self):
        if hasattr(self, 'nueva_ventana') and self.nueva_ventana:
            self.nueva_ventana.destroy()
        
        self.root.withdraw()

        pacientes_ventana = tk.Toplevel(self.root)
        pacientes_ventana.title("Sistema de Gestión")
        pacientes_ventana.geometry("600x400")
        pacientes_ventana.configure(bg="#e2e8f3")
        
        tk.Label(pacientes_ventana, text="Gestión de Especialidad", font=("Georgia", 15), fg="#486f99", background="#e2e8f3").pack(pady=10, padx=10)
        tk.Button(pacientes_ventana, text="Regresar", command=lambda: self.regresar_a_principal(pacientes_ventana)).pack(pady=50)

    def regresar_a_principal(self, ventana_actual):
        ventana_actual.destroy()

        self.abrir_ventana_principal()
    
    def mostrar_Especialidad():
        return
    
    def agregar_Especialidad():
        return
    
    def eliminar_Especialidad():
        return
    
    def modificar_Especialidad():
        return

# ----------------------------------------------------------------------------------------------------------------
    # Funciones para Turnos
    def ventana_Turnos(self):
        if hasattr(self, 'nueva_ventana') and self.nueva_ventana:
            self.nueva_ventana.destroy()
        
        self.root.withdraw()

        pacientes_ventana = tk.Toplevel(self.root)
        pacientes_ventana.title("Sistema de Gestión")
        pacientes_ventana.geometry("600x400")
        pacientes_ventana.configure(bg="#e2e8f3")
        
        tk.Label(pacientes_ventana, text="Gestión de Turnos", font=("Georgia", 15), fg="#486f99", background="#e2e8f3").pack(pady=10, padx=10)
        tk.Button(pacientes_ventana, text="Regresar", command=lambda: self.regresar_a_principal(pacientes_ventana)).pack(pady=50)

    def regresar_a_principal(self, ventana_actual):
        ventana_actual.destroy()

        self.abrir_ventana_principal()
    def mostrar_Turnos():
        return
    
    def agregar_Turnos():
        return
    
    def eliminar_Turnos():
        return
    
    def modificar_Turnos():
        return

login = Login(app)
app.mainloop()

conn.close()