import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="44038930",
    database="agenda"
)
cursor = db.cursor()

# Clase para manejar la localidad
class Localidades:
    def __init__(self, id, id_provincia, localidad):
        self.id = id
        self.id_provincia = id_provincia
        self.localidad = localidad

    def guardar(self):
        query = "INSERT INTO localidades (id_provincia, localidad) VALUES (%s, %s)"
        values = (self.id_provincia,self.localidad,)
        cursor.execute(query, values)
        db.commit()  

    def borrar(self):
        query = "DELETE FROM localidades WHERE id = %s"
        values = (self.id,)
        cursor.execute(query, values)
        db.commit()

    def editar(self, nueva_localidad):
        query = "UPDATE localidades SET id_provincia = %s, localidad = %s WHERE id = %s"
        values = (nueva_localidad.id_provincia, nueva_localidad.localidad, self.id)
        cursor.execute(query, values)
        db.commit()

    @staticmethod
    def obtener_todas():
        query = "SELECT * FROM localidades"
        cursor.execute(query)
        localidades = cursor.fetchall()
        return [Localidades(id, id_provincia, localidad) for (id, id_provincia, localidad) in localidades]
    
    def cargar_localidades(idProvincia):
        query = "SELECT * FROM localidades where id_provincia=%s"
        cursor.execute(query, (idProvincia,))
        localidades = cursor.fetchall()
        if len(localidades)>0:
            return [Localidades(id, id_provincia, localidad) for (id, id_provincia, localidad) in localidades]      
        else:
            return None
    
    def obtiene_nom_localidad(id):
        query = "SELECT localidad from localidades where id=%s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        nom_localidad = result[0] if result else None
        return nom_localidad
    
    def obtiene_id_localidad(nom_localidad, id_provincia):
        query = "SELECT id from localidades where localidad=%s and id_provincia=%s"
        cursor.execute(query, (nom_localidad, id_provincia))
        result = cursor.fetchone()
        id = result[0] if result else None
        return id

    def obtiene_id_provincia(self, id_localidad):
        query = "SELECT id_provincia from localidades where id=%s"
        cursor.execute(query, id_localidad)
        result = cursor.fetchone()
        id = result[0] if result else None
        return id 

    


# Clase para manejar la entidad Provincia
class Provincia:
    def __init__(self, id, provincia):
        self.id = id
        self.provincia = provincia
    
    def guardar(self):
        query = "INSERT INTO provincias (provincia) VALUES (%s)"
        values = (self.provincia,)
        cursor.execute(query, values)
        db.commit()  

    def borrar(self):
        query = "DELETE FROM provincias WHERE id = %s"
        values = (self.id,)
        cursor.execute(query, values)
        db.commit()

    def editar(self, nueva_provincia):
        query = "UPDATE provincias SET provincia = %s WHERE id = %s"
        values = (nueva_provincia, self.id)
        cursor.execute(query, values)
        db.commit()
    

    @staticmethod
    def obtener_todas():
        query = "SELECT * FROM provincias"
        cursor.execute(query)
        provincias = cursor.fetchall()
        return [Provincia(id, provincia) for (id, provincia) in provincias]
    
    @staticmethod
    def obtiene_nom_provincia(id):
        query = "SELECT provincia from provincias where id=%s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        nom_provincia = result[0] if result else None
        return nom_provincia
    
    def obtiene_id_segun_provincia(provincia):
        query = "SELECT id from provincias where provincia=%s"
        cursor.execute(query, (provincia,))
        result = cursor.fetchone()
        id_provincia = result[0] if result else None
        return id_provincia      


# Clase para manejar la entidad DatosPersonales
class DatosPersonales:
    def __init__(self, nombre, apellidos, direccion, telefono, localidad_id):
        self.nombre = nombre
        self.apellidos = apellidos
        self.direccion = direccion
        self.telefono = telefono
        self.localidad_id = localidad_id
    
    def guardar(self):
        query = "INSERT INTO datos (nombre, apellidos, direccion, telefono, localidad_id) VALUES (%s, %s, %s, %s, %s)"
        values = (self.nombre, self.apellidos, self.direccion, self.telefono, self.localidad_id)
        cursor.execute(query, values)
        db.commit()

    def borrar_registro(self):
        query = "DELETE FROM datos WHERE apellidos = %s AND nombre = %s"
        values = (self.apellidos, self.nombre, )
        cursor.execute(query, values)
        db.commit()

    @staticmethod
    def obtener_dp_agenda():
        query = "SELECT * FROM datos"
        cursor.execute(query)
        listaagenda = cursor.fetchall()
        return [DatosPersonales(nombre, apellidos, direccion, telefono, localidad_id) for (nombre, apellidos, direccion, telefono, localidad_id) in listaagenda]
    
    def modificar_registro(self, nuevoregistro):
        query = "UPDATE datos SET nombre=%s, apellidos=%s, direccion=%s, telefono=%s, localidad_id=%s WHERE apellidos=%s and nombre=%s"
        values = (nuevoregistro.nombre, nuevoregistro.apellidos, nuevoregistro.direccion, nuevoregistro.telefono, nuevoregistro.localidad_id, self.apellidos, self.nombre)
        cursor.execute(query, values)
        db.commit()

# Ventana principal de la aplicación
class PrincipalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda Telefónica")

        center_window(self, 600, 400)
        # self.geometry("600x400")  # Ajusta las dimensiones de la ventana

        # Cargar la imagen de fondo
        imagen_fondo = Image.open("bk_main.jpg")
        imagen_fondo = imagen_fondo.resize((600, 400),  Image.Resampling.LANCZOS)  # Ajustar tamaño según la ventana
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

        # Crear un canvas para colocar la imagen de fondo
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.grid(row=0, column=0, rowspan=4, columnspan=4, sticky='nsew')
        self.canvas.create_image(0, 0, image=imagen_fondo_tk, anchor="nw")



        #         # Contenedor para los botones de navegación
        # contenedor_botones = tk.Frame(self)
        # contenedor_botones.grid(row=0, column=0, rowspan=4, sticky='nsew')

        # Botones para ir a la ventana de Categorías y Datos Personales
        btn1=tk.Button(self.canvas, text="Provincias", command=self.abrir_provincias, width=13, height=2)
        btn2=tk.Button(self.canvas, text="Localidades", command=self.abrir_localidades, width=13, height=2)
        btn3=tk.Button(self.canvas, text="Datos Personales", command=self.abrir_datos_personales, width=13, height=2)


        # Colocar los botones en el Canvas
        self.canvas.create_window(100, 20, window=btn1)  # Ajustar coordenadas X, Y según sea necesario
        self.canvas.create_window(300, 20, window=btn2)
        self.canvas.create_window(500, 20, window=btn3)

        # # Agregar widgets encima del fondo (Ejemplo: un botón)
        # boton = tk.Button(self, text="¡Haz clic aquí!", command=lambda: print("Botón clickeado"))
        # boton_canvas = canvas.create_window(400, 300, window=boton)  # Coordenadas X, Y del botón

        # boton1 = tk.Button(self, text="Provincias", command=self.abrir_provincias).grid(row=1, column=4, padx=10, pady=10, sticky='nsew')
        # boton1_canvas = canvas.create_window(400, 300, window=boton1)  # Coordenadas X, Y del botón

        # Mantener una referencia a la imagen para evitar que sea recolectada por el garbage collector
        self.canvas.imagen_fondo_tk = imagen_fondo_tk

        # Botones para ir a la ventana de Categorías y Datos Personales
      #  tk.Button(self, text="Provincias", command=self.abrir_provincias).grid(row=1, column=4, padx=10, pady=10, sticky='nsew')
      #  tk.Button(self, text="Localidades", command=self.abrir_localidades).grid(row=2, column=4, padx=10, pady=10, sticky='nsew')
      #  tk.Button(self, text="Datos Personales", command=self.abrir_datos_personales).grid(row=3, column=4, padx=10, pady=10, sticky='nsew')

        
        # # Botones para ir a la ventana de Categorías y Datos Personales
        # tk.Button(self, text="Provincias", command=self.abrir_provincias).pack(pady=10)
        # tk.Button(self, text="Localidades", command=self.abrir_localidades).pack(pady=10)
        # tk.Button(self, text="Datos Personales", command=self.abrir_datos_personales).pack(pady=10)
    
    def abrir_provincias(self):
        provincia_app = ProvinciasApp(self)
        provincia_app.grab_set()
    
    def abrir_datos_personales(self):
        datos_personales_app = DatosPersonalesApp(self)
        datos_personales_app.grab_set()

    def abrir_localidades(self):
        localidades_app = LocalidadesApp(self)
        localidades_app.grab_set()

# Ventana para ingresar categorías
class ProvinciasApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Provincias")
        center_window(self, 230, 330)
        # self.geometry("230x330")  # Ajusta las dimensiones de la ventana
        
        tk.Label(self, text="Provincia:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.provincia_entry = tk.Entry(self)
        self.provincia_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Crear un frame para los botones y alinearlos
        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Guardar", command=self.guardar_provincia).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Cambiar", command=self.editar_provincia).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Borrar", command=self.borrar_provincia).grid(row=0, column=2, padx=5)

        # Contenedor para el Treeview
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=2, column=0, columnspan=2, padx=15, pady=10, sticky="nsew")
        
        # Crear el árbol para mostrar los datos de las provincias
        self.tree = ttk.Treeview(tree_frame, columns=("Provincia"))

        self.carga_provincias()
        
        self.tree.heading("#0", text="", anchor="w")
        self.tree.column("#0", width=0, stretch=False)

        self.tree.heading("Provincia", text="Provincia")
        self.tree.column("Provincia", anchor="center", width=200)
        self.tree.pack(fill=tk.BOTH, expand=True)


        # Hacer que la ventana sea modal
        self.grab_set()

    def close(self):
        self.destroy()


    def carga_provincias(self):
        provincias = Provincia.obtener_todas()
        for provincia in provincias:
            # OJO, ESTO DE AQUI ABAJO NO VALE
            #  self.tree.insert("", "end", text=provincia.id, values=(provincia.provincia,))

            # LO QUE VALE ES ESTO, PRESTAR ATENCIÓN AL VALUES QUE VA ENTRE PARENTESIS
            # Y OJO A LA COMA, ES IMPRESCINDIBLE!!!
            self.tree.insert("", "end", text=provincia.id, values=(provincia.provincia,))
        self.tree.heading("#0", text="", anchor="w")
        self.tree.column("#0", width=0, stretch=False)
        
    
    def guardar_provincia(self):
        
        provincia = self.provincia_entry.get()
        
        if provincia:
            provincia_obj = Provincia(None, provincia)
            try:
                provincia_obj.guardar()
                messagebox.showinfo("Éxito", "Categoría guardada correctamente.", parent=self)
            except Exception as e:
                # Manejar la excepción y mostrar un mensaje de error
                messagebox.showerror("Error", f"Ocurrió un error al editar los datos: {str(e)}", parent=self)
        else:
            messagebox.showerror("Error", "Por favor, ingrese una categoría.", parent=self)

        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Recargar los datos
        self.carga_provincias()


    def editar_provincia(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una provincia para editar.", parent=self)
            return
        
        new_provincia = self.provincia_entry.get()
        if not new_provincia:
            messagebox.showerror("Error", "Ingrese el nuevo nombre de la provincia.", parent=self)
            return
        
        provincia_id = self.tree.item(selected_item, 'text')
        provincia_obj = Provincia(provincia_id, new_provincia)
        try:
            provincia_obj.editar(new_provincia)
            messagebox.showinfo("Éxito", "Provincia editada correctamente.", parent=self)
        except Exception as e:
            # Manejar la excepción y mostrar un mensaje de error
            messagebox.showerror("Error", f"Ocurrió un error al editar los datos: {str(e)}", parent=self)
        
        self.recargar_provincias()

    def borrar_provincia(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una provincia para borrar.", parent=self)
            return
        
        provincia_id = self.tree.item(selected_item, 'text')
        provincia_obj = Provincia(provincia_id, None)
        try:
            provincia_obj.borrar()
            messagebox.showinfo("Éxito", "Provincia borrada correctamente.", parent=self)
        except Exception as e:
            # Manejar la excepción y mostrar un mensaje de error
            messagebox.showerror("Error", f"Ocurrió un error al editar los datos: {str(e)}", parent=self)
        
        self.recargar_provincias()

    def recargar_provincias(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.carga_provincias()

# Ventana para ingresar localidades
class LocalidadesApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gest. Localidades")
        center_window(self, 275, 380)
        
        # # Frame para los controles
        controls_frame = ttk.Frame(self)
        controls_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=3)
        
        # Label y Combobox para Provincias
        ttk.Label(controls_frame, text="Provincia:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.provincia_var = tk.StringVar()
        self.provincia_dropdown = ttk.Combobox(controls_frame, textvariable=self.provincia_var, state="readonly")
        self.provincia_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.cargar_provincias()
        
        # Label y Entry para Localidad
        ttk.Label(controls_frame, text="Localidad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.localidad_entry = ttk.Entry(controls_frame)
        self.localidad_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        

        # Crear un frame para los botones y alinearlos
        button_frame = tk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        # Botones de Crear, Editar y Borrar
        ttk.Button(button_frame, text="Crear", command=self.crear_localidad).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Button(button_frame, text="Cambiar", command=self.editar_localidad).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(button_frame, text="Borrar", command=self.borrar_localidad).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        # Treeview para mostrar las localidades
        self.tree = ttk.Treeview(self, columns=("ID", "Provincia", "Localidad"), show="headings")
        self.tree.heading("ID", text="", anchor="w")
        self.tree.heading("Provincia", text="Provincia")
        self.tree.heading("Localidad", text="Localidad")

        # Así ocultamos el ID que no tiene por qué ver el usuario
        self.tree.column("ID", width=0, stretch=False)
        self.tree.column("Provincia", width=100)
        self.tree.column("Localidad", width=150)
        self.tree.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        
        self.cargar_localidades()

    def cargar_provincias(self):
        listaprovincias = Provincia.obtener_todas()
        self.provincia_dropdown['values'] =  [provincia.provincia for provincia in listaprovincias]
        #self.provincia_dropdown['values'] =  [Provincia(id,provincia) for (id,provincia) in listaprovincias]
    
    def cargar_localidades(self):
        localidades = Localidades.obtener_todas()
        for loc in localidades:
            self.tree.insert("", "end", values=(loc.id, Provincia.obtiene_nom_provincia(loc.id_provincia), loc.localidad))

    def crear_localidad(self):
        nom_provincia = self.provincia_var.get()
        localidad = self.localidad_entry.get()
        if nom_provincia and localidad:
            id_provincia = Provincia.obtiene_id_segun_provincia(nom_provincia)
            localidad_obj = Localidades(None, id_provincia, localidad)
            try:
                localidad_obj.guardar()
                messagebox.showinfo("Éxito", "Localidad creada correctamente.", parent=self)
                self.actualizar_treeview()
            except Exception as e:
                # Manejar la excepción y mostrar un mensaje de error
                messagebox.showerror("Error", f"Ocurrió un error al crear la localidad: {str(e)}", parent=self)
        else:
            messagebox.showerror("Error", "Debe completar todos los campos.", parent=self)

    def editar_localidad(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una localidad para editar.", parent=self)
            return
        item = selected_item[0]
        values = self.tree.item(item, "values")
        id_localidad = values[0]
       
        provincia_new = self.provincia_var.get()
        id_provincia_new = Provincia.obtiene_id_segun_provincia(provincia_new)
        nom_localidad_new = self.localidad_entry.get()
        localidadNew = Localidades(None, id_provincia_new, nom_localidad_new)
        if provincia_new and nom_localidad_new:
            localidad_obj = Localidades(id_localidad, id_provincia_new, localidadNew)
            try:
                localidad_obj.editar(localidadNew)
                messagebox.showinfo("Éxito", "Localidad editada correctamente.", parent=self)
                self.actualizar_treeview()
            except Exception as e:
                # Manejar la excepción y mostrar un mensaje de error
                messagebox.showerror("Error", f"Ocurrió un error al editar los datos: {str(e)}", parent=self)

        else:
            messagebox.showerror("Error", "Debe completar todos los campos.", parent=self)

    def borrar_localidad(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una localidad para borrar.", parent=self)
            return
        item = selected_item[0]
        values = self.tree.item(item, "values")
        id_localidad = values[0]
        localidad_obj = Localidades(id_localidad, None, None)
        try:
            localidad_obj.borrar()
            messagebox.showinfo("Éxito", "Localidad borrada correctamente.", parent=self)
            self.actualizar_treeview()
        except Exception as e:
            # Manejar la excepción y mostrar un mensaje de error
            messagebox.showerror("Error", f"Ocurrió un error al editar los datos: {str(e)}", parent=self)


    def actualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.cargar_localidades()


# Ventana para ingresar datos personales
class DatosPersonalesApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        center_window(self, 800, 500)
        # self.geometry("800x500")  # Ajusta las dimensiones de la ventana
        self.title("Datos Personales")


        # Añadir un título para el frame
        tk.Label(self, text="Formulario de Datos Personales", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=5, padx=20, pady=(10, 5), sticky="w")

        # Crear un frame para los datos personales
        datos_frame = tk.Frame(self)
        datos_frame.grid(row=1, column=0, columnspan=5, pady=10, padx=10, sticky="w")

        tk.Label(datos_frame, text="Nombre:").grid(row=0, column=0, pady=5, padx=(10, 2), sticky="w")
        self.nombre_entry = tk.Entry(datos_frame)
        self.nombre_entry.grid(row=0, column=1, pady=5, padx=(2, 10), sticky="w")
        
        tk.Label(datos_frame, text="Apellidos:").grid(row=0, column=2, pady=5, padx=(10, 2), sticky="w")
        self.apellidos_entry = tk.Entry(datos_frame)
        self.apellidos_entry.grid(row=0, column=3, pady=5, padx=(2, 10), sticky="w")
        
        tk.Label(datos_frame, text="Dirección:").grid(row=0, column=4, pady=5, padx=(10, 2), sticky="w")
        self.direccion_entry = tk.Entry(datos_frame)
        self.direccion_entry.grid(row=0, column=5, pady=5, padx=(2, 10), sticky="w")
        
        tk.Label(datos_frame, text="Teléfono:").grid(row=3, column=0, pady=5, padx=(10, 2), sticky="w")
        self.telefono_entry = tk.Entry(datos_frame)
        self.telefono_entry.grid(row=3, column=1, pady=5, padx=(2, 10), sticky="w")
        
        tk.Label(datos_frame, text="Provincia:").grid(row=3, column=2, pady=5, padx=(10, 2), sticky="w")
        self.provincia_var = tk.StringVar(self)
        self.provincia_dropdown = ttk.Combobox(datos_frame, textvariable=self.provincia_var, state="readonly")
        self.provincia_dropdown.grid(row=3, column=3, pady=5, padx=(2, 10), sticky="w")
        self.cargar_provincia()
        self.provincia_dropdown.bind("<<ComboboxSelected>>", self.actualiza_localidades)

        tk.Label(datos_frame, text="Localidad:").grid(row=3, column=4, pady=5, padx=(10, 2), sticky="w")
        self.localidad_var = tk.StringVar(self)
        self.localidad_dropdown = ttk.Combobox(datos_frame, textvariable=self.localidad_var, state="readonly")
        self.localidad_dropdown.grid(row=3, column=5, pady=5, padx=(2, 10), sticky="w")
        self.cargar_localidades(None)
        
        # tk.Button(self, text="Guardar", command=self.guardar_datos).grid(row=5, column=0, columnspan=2, pady=5)
        button_frame = tk.Frame(self)
        button_frame.grid(row=5, column=0, columnspan=3, pady=5)

        tk.Button(button_frame, text="Guardar", command=self.guardar_datos).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Editar", command=self.editar_datos).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Borrar", command=self.borrar_datos).grid(row=0, column=2, padx=5)
        
        # Crear el árbol para mostrar los datos de las provincias
        self.tree = ttk.Treeview(self, columns=("Nombre", "Apellidos", "Dirección", "Teléfono", "Localidad"), show="headings")

        # Insertar algunos datos de ejemplo
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Dirección", text="Dirección")
        self.tree.heading("Teléfono", text="Teléfono")
      #  self.tree.heading("Provincia", text="Provincia")
        self.tree.heading("Localidad", text="Localidad")

        # Ajustar el ancho de las columnas
        self.tree.column("Nombre", width=50)
        self.tree.column("Apellidos", width=100)
        self.tree.column("Dirección", width=150)
        self.tree.column("Teléfono", width=40)
     #   self.tree.column("Provincia", width=150)
        self.tree.column("Localidad", width=150)


        self.obtener_agenda()

        self.tree.grid(row=6, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

        # Configurar redimensionamiento de columnas
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

    def obtener_agenda(self):
        listaagenda = DatosPersonales.obtener_dp_agenda()
       
        for registro in listaagenda:
            # OJO, ESTO DE AQUI ABAJO NO VALE
            #  self.tree.insert("", "end", text=provincia.id, values=(provincia.provincia,))


            # LO QUE VALE ES ESTO, PRESTAR ATENCIÓN AL VALUES QUE VA ENTRE PARENTESIS
            # Y OJO A LA COMA, ES IMPRESCINDIBLE!!!
            # self.tree.insert("", "end", values=registro)
         #   self.tree.insert("", "end", values=(registro.nombre, registro.apellidos, registro.direccion, registro.telefono, Provincia.obtiene_nom_provincia(registro.provincia_id), Localidades.obtiene_nom_localidad(registro.localidad_id)))
         self.tree.insert("", "end", values=(registro.nombre, registro.apellidos, registro.direccion, registro.telefono, Localidades.obtiene_nom_localidad(registro.localidad_id)))

    def actualiza_localidades(self, event):
        # Obtener el índice de la provincia seleccionada
        #idProvincia = self.provincia_dropdown
        provincia = self.provincia_dropdown.get()

        idProvincia = Provincia.obtiene_id_segun_provincia(provincia)
    
        # Imprimir el índice seleccionado
        # print(f"Índice seleccionado: {idProvincia}")
    
        # Limpiar el combo de localidades
        self.localidad_dropdown['values'] = []

        if idProvincia:
            self.cargar_localidades(idProvincia)
            if self.localidad_dropdown['values'] == []:
                self.localidad_dropdown["values"] = "No Especificado", 
        else:
            self.localidad_dropdown["values"] = "No Especificado",
        #     ## AQUI HAY UN PROBLEMA.
        #     if listalocalidades!=None:
        #         self.localidad_dropdown["values"] =  [localidad.localidad for localidad in listalocalidades]
        #     else:
        #         self.localidad_dropdown["values"] = "No Especificado", 
        # else:
        #     self.localidad_dropdown["values"] = "No Especificado", 

    def cargar_localidades(self, idProvincia):
        if idProvincia:
            listalocalidades = Localidades.cargar_localidades(idProvincia)
            if listalocalidades!=None:
                self.localidad_dropdown["values"] =  [localidad.localidad for localidad in listalocalidades]
            else:
                messagebox.showerror("ERROR","Debe de especificar una localidad para dicha provincia ya que no existe",parent=self)
                self.localidad_dropdown["values"] = "No Especificado",
                
        else:
            self.localidad_dropdown["values"] = "No Especificado", 


    def cargar_provincia(self):
        # Obtener todas las categorías desde la base de datos
        listaprovincias = Provincia.obtener_todas()
        self.provincia_dropdown["values"] = [provincia.provincia for provincia in listaprovincias]

    def obtener_id_provincia(self, nombre_provincia):
        # Obtener el id de la categoría seleccionada
        # query = "SELECT id FROM provincias WHERE provincia = %s"
        # cursor.execute(query, (nombre_provincia,))
        # provincia_id = cursor.fetchone()
        # return provincia_id[0] if provincia_id else None
        id_provincia = Provincia.obtiene_id_segun_provincia(nombre_provincia)
        return id_provincia
    
    def obtener_id_localidad(self, nombre_localidad, provincia_id):
        id_localidad = Localidades.obtiene_id_localidad(nombre_localidad, provincia_id)
        return id_localidad
    
    
    def guardar_datos(self):
        nombre = self.nombre_entry.get()
        apellidos = self.apellidos_entry.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        provincia_nombre = self.provincia_var.get()
        provincia_id = self.obtener_id_provincia(provincia_nombre)
        localidad_nombre = self.localidad_var.get()
        localidad_id = self.obtener_id_localidad(localidad_nombre, provincia_id)
        
        if nombre and apellidos and direccion and telefono and provincia_id and localidad_id:
            datos_personales = DatosPersonales(nombre, apellidos, direccion, telefono, localidad_id)

            try:
                datos_personales.guardar()
                messagebox.showinfo("Éxito", "Datos guardados correctamente.", parent=self)
            except Exception as e:
                # Manejar la excepción y mostrar un mensaje de error
                messagebox.showerror("Error", f"Ocurrió un error al editar los datos: {str(e)}", parent=self)
            

        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos o seleccione una categoría.", parent=self)
        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)    
        self.obtener_agenda()

    def editar_datos(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un registro para editar.", parent=self)
            return
        
        nombreNew = self.nombre_entry.get()
        apellidosNew = self.apellidos_entry.get()
        direccionNew = self.direccion_entry.get()
        telefonoNew = self.telefono_entry.get()
        provinciaNew = self.provincia_var.get()
        localidadNew = self.localidad_var.get()
        id_provinciaNew = Provincia.obtiene_id_segun_provincia(provinciaNew)

        if not (nombreNew and apellidosNew and direccionNew and telefonoNew and provinciaNew and localidadNew):
            messagebox.showerror("Error", "Por favor, complete todos los campos.", parent=self)
            return

        item = selected_item[0]
        # self.tree.item(item, values=(nombre, apellidos, direccion, telefono, provincia, localidad))
        values = self.tree.item(item, 'values')
        

        nombre = values[0]
        apellidos = values[1]
        direccion = values[2]
        tlf = values[3]
        id_provincia = self.obtener_id_provincia(values[4])
        id_localidad = self.obtener_id_localidad(values[4], id_provincia)

        #   nombre, apellidos, direccion, telefono, provincia_id
        registro = DatosPersonales(nombre, apellidos, direccion, tlf, id_localidad)
        nuevoregistro = DatosPersonales(nombreNew, apellidosNew, direccionNew, telefonoNew, self.obtener_id_localidad(localidadNew, id_provinciaNew))
       
        try:
            registro.modificar_registro(nuevoregistro)

            for item in self.tree.get_children():
                self.tree.delete(item)    
            self.obtener_agenda()
        
            messagebox.showinfo("Éxito", "Datos editados correctamente.", parent=self)
        except Exception as e:
            # Manejar la excepción y mostrar un mensaje de error
            messagebox.showerror("Error", f"Ocurrió un error al editar los datos: {str(e)}", parent=self)

    def borrar_datos(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un registro para borrar.", parent=self)
            return

        item = selected_item[0]
        values = self.tree.item(item, 'values')

        nombre = values[0]
        apellidos = values[1]
        direccion = values[2]
        tlf = values[3]
        provincia = None

        #   nombre, apellidos, direccion, telefono, provincia_id
        registro = DatosPersonales(nombre, apellidos, direccion, tlf, provincia)
       
        try:
            registro.borrar_registro()

            for item in self.tree.get_children():
                self.tree.delete(item) 

            self.obtener_agenda()

            # self.tree.delete(item)
            messagebox.showinfo("Éxito", "Datos borrados correctamente.", parent=self)
        except Exception as e:
            # Manejar la excepción y mostrar un mensaje de error
            messagebox.showerror("Error", f"Ocurrió un error al borrar los datos: {str(e)}", parent=self)

def center_window(window, width, height):
    # Obtener el ancho y alto de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular las coordenadas x, y para que la ventana esté centrada
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    # Establecer la geometría de la ventana para centrarla
    window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

# Crear e iniciar la ventana principal
app = PrincipalApp()
app.mainloop()