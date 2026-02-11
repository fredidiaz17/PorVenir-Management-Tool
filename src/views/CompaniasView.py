import customtkinter as ctk
from tkinter import ttk, messagebox

from customtkinter import CTkScrollbar

MAX_NOMBRE_LEN = 100
# Si, este codigo es un copia y pega de MarcasView, pero adaptado.

class CompaniasView(ctk.CTkFrame):
    def __init__(self, parent, app=None, controller=None):
        super().__init__(parent)

        self.app = app
        self.controller = controller

        self._build_ui()

    # ---------------- UI ----------------
    def _build_ui(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ---------- TABLA ----------
        tablas_frame = ctk.CTkFrame(self)
        tablas_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        tablas_frame.grid_columnconfigure((0, 1), weight=1)

        frame_companias, self.tv_companias = self._create_treeview(
            tablas_frame,
            columns=("nombre",),
            headers=("Nombre",),
            title="Compañías"
        )
        frame_companias.grid(row=0, column=0, sticky="nsew", padx=5)
        # Vinculandolo al evento para rellenar entries
        self.tv_companias.bind("<Double-Button-1>", self._rellenar_entries)

        # ---------- Scroller ---------
         # todo: Hacer cambios (adaptados) a CompaniasView, repetir lo mismo con marcas, probar todo junto
        yscroll = CTkScrollbar(frame_companias, orientation="vertical", command=self.tv_companias.yview)
        self.tv_companias.configure(yscrollcommand= yscroll.set)
        yscroll.grid(row=1, column=2, sticky="ns")


        # ---------- FORM ----------
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form_frame, text="Nombre").grid(row=0, column=0, sticky="w")
        self.nombre_entry = ctk.CTkEntry(form_frame)
        self.nombre_entry.grid(row=0, column=1, sticky="ew")


        # ---------- BOTONES ----------
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)

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

        if not nombre:
            messagebox.showerror("Error", "El campo no puede estar vacío")
            return None

        if len(nombre) > MAX_NOMBRE_LEN:
            messagebox.showerror("Error", f"Nombre demasiado largo ({MAX_NOMBRE_LEN})")
            return None

        return nombre

    # ---------------- ACCIONES ----------------
    def crear(self):
        data = self._validar_form()
        if not data:
            return

        nombre = data

        msg = f"""
                        Se creará la compañia "{nombre}".
                        ¿Proseguir?
                """

        confirm = messagebox.askokcancel("Confirmar creación", msg)

        if self.controller and confirm:
            self.controller.crear_compania(nombre)

    def actualizar(self):
        sel = self.tv_companias.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione una compañia")
            return

        data = self._validar_form()
        if not data:
            return

        id_compania = sel[0]
        nombre = data
        name_anterior = self.tv_companias.item(id_compania)["values"][0]

        msg = f"""
            Se actualizará la compañia "{name_anterior}"
            a "{nombre}".
            ¿Proseguir?
        """

        confirm = messagebox.askokcancel("Confirmar actualización", msg)

        if self.controller and confirm:
            self.controller.actualizar_compania(id_compania, nombre)

    def eliminar(self):
        sel = self.tv_companias.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione una compañia")
            return
        nombre = self.tv_companias.item(sel[0], "values")[0]

        msg = f"""
            Se eliminará la compañia "{nombre}"
            ¿Seguro?
        """

        confirm = messagebox.askokcancel("Confirmar eliminación", msg)

        if self.controller and confirm:
            self.controller.eliminar_compania(sel[0])

    def limpiar(self, comp = True):
        self.nombre_entry.delete(0, "end")

        # opcional: limpiar selección de tablas
        if comp:
            self.tv_companias.selection_remove(self.tv_companias.selection())

    # ---------------- EVENTOS ----------------

    def _rellenar_entries(self, event):
        # Capturamos el widget y la seleccion
        tv = event.widget
        sel = tv.selection()

        # Recogemos valores de la selección.
        id = sel[0]
        val = tv.item(id, "values")

        # Limpiamos las entries para evitar acumulamiento
        self.limpiar(comp = False)

        # Rellenamos
        self.nombre_entry.insert(0, val[0])


    # ---------------- HELPERS PARA CARGA ----------------

    def cargar_companias(self, companias=None):

        if self.controller and not companias:
            companias = self.controller.listar_companias()

        self.tv_companias.delete(*self.tv_companias.get_children())

        if len(companias) == 0:
            self.tv_companias.insert(
                "",
                "end",
                values = ("No hay compañias",) + ("",) * (len(self.tv_companias["columns"]) - 1)
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
        def crear_compania(self, *args): print("crear", args)
        def actualizar_compania(self, *args): print("actualizar", args)
        def eliminar_compania(self, *args): print("eliminar", args)
        def listar_companias(self): return ()

    app = ctk.CTk()
    app.geometry("900x500")

    view = CompaniasView(app, controller=DummyController())
    view.pack(fill="both", expand=True)

    view.cargar_companias([
        {"id_compania": "1", "nombre": "Comp A"},
        {"id_compania": "2", "nombre": "Comp B"},
    ])

    app.mainloop()