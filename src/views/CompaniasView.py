from customtkinter import CTkLabel

from src.controllers.CompaniasController import CompaniasController as CompC
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

class CompaniaView:

    def __init__(self, master):
        self.master = master
        self.frame = ctk.CTkFrame(master, width=400, height=400)
        self.frame.pack(fill= tk.BOTH)

        self.id_compania_var = tk.IntVar()
        self.nombre_compania_var = tk.StringVar()
        self.compania_selected_var = tk.StringVar()

        CTkLabel(self.frame, text= "--Menú de Creación de Companias--", anchor="center").grid(column=0, row=0, sticky=tk.W)



        self._crear_entries()
        self._crear_botones()
        self._crear_table()


    def _crear_entries(self):
        # Creando el frame contenedor de los entries
        entries_frame = ctk.CTkFrame(self.frame)
        entries_frame.grid(column=0, row= 1)

        # entry y label de la ultima compañia seleccionada
        self.label_selected = ctk.CTkLabel(entries_frame, text="Compañia seleccionada:")
        self.label_selected.grid(column=0, row=0)
        self.entry_selected = ctk.CTkEntry(entries_frame, textvariable=self.compania_selected_var, state='readonly')
        self.entry_selected.grid(column=1, row=0)

        # entry y label del nombre
        self.label_nombre = tk.Label(entries_frame, text="Nombre de la Compania a crear:")
        self.label_nombre.grid(column=0, row=1)
        self.entry_nombre = tk.Entry(entries_frame, textvariable=self.nombre_compania_var)
        self.entry_nombre.grid(column=1, row=1)

        # Aunque no es entry, interactua con ellos: Boton de refresh/eliminar lo diligenciado
        self.boton_refresh = ctk.CTkButton(entries_frame, text= "X",
                                           text_color='black', border_width= 4 ,border_color= 'black', fg_color='red',
                                           command= self.refrescar_campos)
        self.boton_refresh.grid(column=2, row=1)

    def _crear_botones(self):
        # Creando el frame contenedor
        botones_frame = ctk.CTkFrame(self.frame)
        botones_frame.grid(column=0, row=2)

        # Boton de Crear
        self.boton_crear = ctk.CTkButton(
            botones_frame,
            text='Crear Compania',
            command=self.crear_compania
        )
        self.boton_crear.pack(side="left", padx=3)

        # Boton de Eliminar
        self.boton_eliminar = ctk.CTkButton(
            botones_frame,
            text='Eliminar',
            command=self.eliminar_compania,
            fg_color= 'red'
        )
        self.boton_eliminar.pack(side="left", padx=3)

        # Boton de Actualizar
        self.boton_actualizar = ctk.CTkButton(
            botones_frame,
            text='actualizar',
            command=self.actualizar_compania,
            fg_color='yellow',
            text_color= 'black'
        )
        self.boton_actualizar.pack(side="left", padx=3)

    # FUNCION PARA CREAR LA TABLA Y SU ESTILO
    def _crear_table(self):
        # Definiendo el estilo del table (tree)
        style = ttk.Style()
        style.configure( # Estilo del table
            'Treeview',
            rowheight=20
        )
        style.configure( # Estilo del encabezado, no puedo usar background
            "Treeview.Heading",
            foreground='black'
        )

        # Creando la tabla (tree)
        columns = 'nombre'
        self.tree = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings",
            style='Treeview'
        )
        self.tree.heading(
            "nombre",
            text="Listado de Companias",
            anchor="center",
            # style='Treeview.Heading'
        )
        self.tree.column("nombre",width= 150, stretch=True)
        self.tree.grid(column=1, row=1)



        # Creando el vinculo de tabla-barra de texto
        self.tree.bind("<Double-1>", self.seleccionar_compania)
        self.rellenar_table()


    # CRUD

    def refrescar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.refrescar_campos()
        self.rellenar_table()

    def refrescar_campos(self):
        self.nombre_compania_var.set('')
        self.compania_selected_var.set('')

    def rellenar_table(self):
        # Datos a insertar en el table: Listado de companias
        # Todo: Los datos de la tabla se insertan incompletos, al menos cuando son mas de 1 palabra
        self.companias = CompC.listar_companias() #Listamos companias
        if len(self.companias) > 0:
            for i in self.companias:
                self.tree.insert('', 'end', iid= str(i['id_compania']), values=(i['nombre'],)) #El iid es un identificador por defecto de la fila, lo usaré para guardar el id del registra en la bd

        else:
            self.tree.insert('', 'end',values=['No hay companias existentes'])
            self.tree.insert('', 'end', values=["Prueba a crear una ahora mismo"])



    def seleccionar_compania(self, event):
        tree = event.widget
        seleccion = tree.selection()

        if seleccion:
            item = tree.item(seleccion[0])
            iid= seleccion[0]
            id_compania = int(iid)
            nombre_compania = item["values"][0]


            self.id_compania_var.set(id_compania)
            self.compania_selected_var.set(nombre_compania)


    def crear_compania(self):
        nombre_compania = self.nombre_compania_var.get()

        if nombre_compania == '' or len(nombre_compania) > 100:
            tk.messagebox.showwarning('Dato invalido', 'El nombre de la compañia debe estar entre los 1 y 100 caracteres')
        else:
            if CompC.crear_compania(nombre_compania):
                tk.messagebox.showinfo('Creación exitosa',f'Compania "{nombre_compania}" creada"')
                self.refrescar_tabla()
            else:
                tk.messagebox.showerror('Error al crear','¡Ups!, parece que hubo un error en la creación de la Compañia')


    def actualizar_compania(self):
        nombre_compania = self.compania_selected_var.get()
        id_comp = self.id_compania_var.get()

        if id_comp == 0:
            tk.messagebox.showwarning('Nada seleccionado',
                                      'Selecciona una compañia desde la lista de compañias para actualizar')
        elif nombre_compania == '' or len(nombre_compania) > 100:
            tk.messagebox.showwarning('Dato invalido','El nombre de la compañia debe estar entre los 1 y 100 caracteres')
        else:
            if CompC.actualizar_compania(id_comp, nombre_compania):
                tk.messagebox.showinfo('Actualización exitosa',f'Compañia "{nombre_compania}" actualizada')
                self.refrescar_tabla()
            else:
                tk.messagebox.showerror('Error al actualizar','¡Ups!, parece que hubo un error en la actualización de la Compañia')

    def eliminar_compania(self):
        nombre_compania = self.compania_selected_var.get()
        id_comp = self.id_compania_var.get()

        if id_comp == 0:
            tk.messagebox.showwarning('Nada seleccionado','Selecciona una compañia desde la lista de compañias para eliminar')
        else:
            if CompC.eliminar_compania(id_comp):
                tk.messagebox.showinfo('Eliminacion exitosa',f'Compañia {nombre_compania} eliminada')
                self.refrescar_tabla()
            else:
                tk.messagebox.showerror('Error al eliminar','¡Ups!, parece que hubo un error en la eliminación de la Compañia')




