import customtkinter as ctk
from tkinter import ttk, messagebox

from click import confirm

MAX_NOMBRE_LEN = 100
MAX_DESC_LEN = 255


class MarcasView(ctk.CTkFrame):
    def __init__(self, parent, app=None, controller=None):
        super().__init__(parent)

        self.app = app
        self.controller = controller

        self._build_ui()

    # ---------------- UI ----------------
    def _build_ui(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ---------- TABLAS ----------
        tablas_frame = ctk.CTkFrame(self)
        tablas_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        tablas_frame.grid_columnconfigure((0, 1), weight=1)

        # Marcas
        frame_marcas, self.tv_marcas = self._create_treeview(
            tablas_frame,
            columns=("nombre", "descripcion", "id_compania", "compania"),
            headers=("Nombre de la marca", "Descripción", "id_compania", "Compañia a la que pertenece"),
            title="Marcas"
        )
        frame_marcas.grid(row=0, column=0, sticky="nsew", padx=5)
        # Vinculandolo al evento

        self.tv_marcas.bind("<Double-Button-1>", self._rellenar_entries)

        # ---- Scrollers
        yscroll = ctk.CTkScrollbar(frame_marcas, orientation="vertical", command=self.tv_marcas.yview)
        self.tv_marcas.config(yscrollcommand=yscroll.set)
        yscroll.grid(row=1, column = 2, sticky= "ns")

        xscroll = ctk.CTkScrollbar(frame_marcas, orientation="horizontal", command=self.tv_marcas.xview)
        self.tv_marcas.config(xscrollcommand=xscroll.set)
        xscroll.grid(row=2, column = 0, sticky= "ew")

        self.tv_marcas.column("id_compania", width=0, stretch=False)

        # Companias
        frame_companias, self.tv_companias = self._create_treeview(
            tablas_frame,
            columns=("nombre",),
            headers=("Nombre",),
            title="Compañías"
        )
        frame_companias.grid(row=0, column=1, sticky="nsew", padx=5)

        # ---- Scrollers
        yscroll = ctk.CTkScrollbar(frame_companias, orientation="vertical", command=self.tv_companias.yview)
        self.tv_companias.config(yscrollcommand=yscroll.set)
        yscroll.grid(row=1, column = 2, sticky= "ns")

        # ---------- FORM ----------
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form_frame, text="Nombre").grid(row=0, column=0, sticky="w")
        self.nombre_entry = ctk.CTkEntry(form_frame)
        self.nombre_entry.grid(row=0, column=1, sticky="ew")

        ctk.CTkLabel(form_frame, text="Descripción").grid(row=1, column=0, sticky="w")
        self.desc_text = ctk.CTkTextbox(
            form_frame,
            height=100,
            wrap="word"
        )
        self.desc_text.grid(row=1, column=1, sticky="ew")

        # ---------- BOTONES ----------
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=1, column=1, sticky="n", padx=10, pady=10)

        ctk.CTkButton(btn_frame, text="Crear", command=self.crear).pack(fill="x", pady=2)
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.actualizar).pack(fill="x", pady=2)
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.eliminar).pack(fill="x", pady=2)
        ctk.CTkButton(btn_frame, text="Limpiar", command=self.limpiar).pack(fill="x", pady=2)

    def _create_treeview(self, parent, columns, headers, title):
        frame = ctk.CTkFrame(parent)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text=title).grid(row=0, column=0, sticky="w")

        tv = ttk.Treeview(frame, columns=columns, show="headings", height=8)
        for col, header in zip(columns, headers):
            tv.heading(col, text=header)
            tv.column(col, anchor="w")

        tv.grid(row=1, column=0, sticky="nsew")

        return frame, tv

    # ---------------- VALIDACIÓN ----------------
    def _validar_form(self):
        nombre = self.nombre_entry.get().strip()
        desc = self.desc_text.get("1.0","end").strip()

        if not nombre or not desc:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos")
            return None

        if len(nombre) > MAX_NOMBRE_LEN:
            messagebox.showerror("Error", f"Nombre demasiado largo ({MAX_NOMBRE_LEN})")
            return None

        if len(desc) > MAX_DESC_LEN:
            messagebox.showerror("Error", f"Descripción demasiado larga ({MAX_DESC_LEN})")
            return None

        sel_compania = self.tv_companias.selection()
        if not sel_compania:
            messagebox.showerror("Error", "Seleccione una compañía")
            return None

        return nombre, desc, sel_compania[0]  # iid = id_compania

    # ---------------- ACCIONES ----------------
    def crear(self):
        data = self._validar_form()
        if not data:
            return

        nombre, desc, id_compania = data
        tv = self.tv_companias
        comp = tv.item(tv.selection()[0], "values")[0]

        msg = f"""
                Se creará una nueva marca con la siguiente información:
                Nombre de la marca: {nombre},
                Descripción: {desc},
                Compania a la que pertenece: {comp}
                
                ¿Proseguir?
            """

        confirm = messagebox.askyesno("Confirmar creación", msg)
        if self.controller and confirm:
            self.controller.crear_marca(nombre, desc, id_compania)

    def actualizar(self):
        sel = self.tv_marcas.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione una marca")
            return

        data = self._validar_form()
        if not data:
            return

        id_marca = sel[0]
        nombre, desc, id_compania = data

        name_ant = self.tv_marcas.item(id_marca, "values")[0]

        tv = self.tv_companias
        comp = tv.item(tv.selection()[0], "values")[0]

        msg = f"""
                        Se actualizará la marca {name_ant} con la siguiente información:
                        Nombre de la marca: {nombre},
                        Descripción: {desc},
                        Compania a la que pertenece: {comp}
                        
                        ¿Proseguir?
                    """

        confirm = messagebox.askyesno("Confirmar actualización", msg)

        if self.controller and confirm:
            self.controller.actualizar_marca(id_marca, nombre, desc, id_compania)

    def eliminar(self):
        sel = self.tv_marcas.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione una marca")
            return

        marca = self.tv_marcas.item(sel[0], "values")[0]

        msg = f"""
                Se eliminará la marca "{marca}"
                ¿Está seguro?
            """
        confirm = messagebox.askyesno("Confirmar eliminacion", msg)
        if self.controller and confirm:
            self.controller.eliminar_marca(sel[0])

    def limpiar(self, marca= True, comp = True):
        self.nombre_entry.delete(0, "end")

        # si usas CTkTextbox
        if hasattr(self, "desc_text"):
            self.desc_text.delete("1.0", "end")

        # opcional: limpiar selección de tablas
        if marca:
            self.tv_marcas.selection_remove(self.tv_marcas.selection())
        if comp:
            self.tv_companias.selection_remove(self.tv_companias.selection())

    # ---------------- EVENTOS ----------------
    def _rellenar_entries(self, event):
        # Capturar seleccion
        tv = event.widget
        sel = tv.selection()

        # Recoger valores
        item_id = sel[0]
        val = tv.item(item_id, "values")

        # Limpiamos
        self.limpiar(marca= False)

        # Orden de columnas: nombre, descripcion, id_compania, nombre_compania
        self.nombre_entry.insert(0, val[0])
        self.desc_text.insert("1.0", val[1])

        tv2 = self.tv_marcas
        id_comp = int(val[2])

        for iid in tv2.get_children():
            if iid == id_comp:
                tv2.selection_set(iid)
                tv2.focus(iid)
                tv2.see(iid)

    # ---------------- HELPERS PARA CARGA ----------------
    def cargar_marcas(self, marcas=None):

        if self.controller and not marcas:
            marcas = self.controller.listar_marcas()

        self.tv_marcas.delete(*self.tv_marcas.get_children())

        if len(marcas) == 0:
            self.tv_marcas.insert(
                "",
                "end",
                values=("No hay marcas",) + ("",) * (len(self.tv_marcas["columns"]) - 1)
            )
        else:
            for m in marcas:
                self.tv_marcas.insert(
                    "",
                    "end",
                    iid=m["id_marca"],
                    values=(m["nombre"], m["descripcion"], m["id_compania"], m["compania"])
                )

    def cargar_companias(self, companias=None):

        if self.controller and not companias:
            companias = self.controller.listar_companias()

        self.tv_companias.delete(*self.tv_companias.get_children())

        if len(companias) == 0:
            self.tv_companias.insert(
                "",
                "end",
                values = ("No hay compañias",) + ("",) * (len(self.tv_marcas["columns"]) - 1)
            )
        else:
            for c in companias:
                self.tv_companias.insert(
                    "",
                    "end",
                    iid=c["id_compania"],
                    values=(c["nombre"],)
                )


# ---------------- TEST LOCAL DE LA VISTA ----------------
if __name__ == "__main__":
    ctk.set_appearance_mode("System")

    class DummyController:
        def crear_marca(self, *args): print("crear", args)
        def actualizar_marca(self, *args): print("actualizar", args)
        def eliminar_marca(self, *args): print("eliminar", args)
        def listar_marcas(self): return ()
        def listar_companias(self): return ()

    app = ctk.CTk()
    app.geometry("900x500")

    view = MarcasView(app, controller=DummyController())
    view.pack(fill="both", expand=True)

    view.cargar_companias([
        {"id_compania": "1", "nombre": "Comp A"},
        {"id_compania": "2", "nombre": "Comp B"},
    ])

    view.cargar_marcas([
        {"id_marca": "10", "nombre": "Marca X", "descripcion": "Desc", "id_compania": "1", "compania": "Comp A"},
    ])

    app.mainloop()
