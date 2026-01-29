import customtkinter as ctk
from tkinter import ttk, messagebox


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

        frame_marcas, self.tv_marcas = self._create_treeview(
            tablas_frame,
            columns=("nombre", "descripcion", "id_compania"),
            headers=("Nombre", "Descripción", "Compañía"),
            title="Marcas"
        )
        frame_marcas.grid(row=0, column=0, sticky="nsew", padx=5)

        frame_companias, self.tv_companias = self._create_treeview(
            tablas_frame,
            columns=("nombre",),
            headers=("Nombre",),
            title="Compañías"
        )
        frame_companias.grid(row=0, column=1, sticky="nsew", padx=5)

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

        if self.controller:
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

        if self.controller:
            self.controller.actualizar_marca(id_marca, nombre, desc, id_compania)

    def eliminar(self):
        sel = self.tv_marcas.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione una marca")
            return

        if self.controller:
            self.controller.eliminar_marca(sel[0])

    def limpiar(self):
        self.nombre_entry.delete(0, "end")

        # si usas CTkTextbox
        if hasattr(self, "desc_text"):
            self.desc_text.delete("1.0", "end")

        # opcional: limpiar selección de tablas
        self.tv_marcas.selection_remove(self.tv_marcas.selection())
        self.tv_companias.selection_remove(self.tv_companias.selection())

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
                    values=(m["nombre"], m["descripcion"], m["id_compania"])
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
        {"id_marca": "10", "nombre": "Marca X", "descripcion": "Desc", "id_compania": "1"},
    ])

    app.mainloop()
