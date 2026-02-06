import customtkinter as ctk
from tkinter import ttk, messagebox

MAX_NOMBRE_LEN = 100
MEDIDAS = ["GRAMOS","KILOGRAMOS", "LIBRAS", "LITROS", "MILILITROS", "UNIDADES", "DOCENAS", "PAQUETES"]

# Si, otro copia y pega del MarcasView jejeje

class ProductosView(ctk.CTkFrame):
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

        # Productos
        frame_productos, self.tv_productos = self._create_treeview(
            tablas_frame,
            columns=("nombre", "cantidad_stock", "unidad_medida", "precio_compra", "precio_venta", "porcentaje_iva", "id_marca", "nombre_marca"),
            headers=("Nombre", "Cantidad en stock", "Unidad de medida", "Precio de compra según el mercado",
                     "Precio base de venta", "Porcentaje de IVA", "Idmarca", "Marca a la que pertenece"),
            title="Productos"
        )
        frame_productos.grid(row=0, column=0, sticky="nsew", padx=5)
        self.tv_productos.column("id_marca", width=0, stretch=False)

        # Scroller de la tabla de productos

        xscroll = ttk.Scrollbar(frame_productos, orient="horizontal", command=self.tv_productos.xview)
        self.tv_productos.configure(xscrollcommand=xscroll.set)
        xscroll.grid(row=2, column=0, sticky="ew")

        # Marcas

        frame_marcas, self.tv_marcas = self._create_treeview(
            tablas_frame,
            columns=("nombre", "descripcion", "id_compania"), #Todo: No me interesa el id de la compañia de la Marca, necesito el nombre. Cambiar el select y la vista de Marca para retornar nombre de la compañia
            headers=("Nombre", "Descripción", "Compañía"),
            title="Marcas"
        )
        frame_marcas.grid(row=0, column=1, sticky="nsew", padx=5)



        # ---------- FORM ----------
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form_frame, text="Nombre del producto").grid(row=0, column=0, sticky="w")
        self.nombre_entry = ctk.CTkEntry(form_frame)
        self.nombre_entry.grid(row=0, column=1, sticky="ew")

        ctk.CTkLabel(form_frame, text="cantidad en stock").grid(row=1, column=0, sticky="w")
        self.cantidad_stock_entry = ctk.CTkEntry(form_frame)
        self.cantidad_stock_entry.grid(row=1, column=1, sticky="ew")

        ctk.CTkLabel(form_frame, text="unidad de medida").grid(row=2, column=0, sticky="w")
        self.unidad_medida_opm = ctk.CTkOptionMenu(form_frame, values=MEDIDAS)
        self.unidad_medida_opm.grid(row=2, column=1, sticky="ew")

        ctk.CTkLabel(form_frame, text="precio compra").grid(row=3, column=0, sticky="w")
        self.precio_compra_entry = ctk.CTkEntry(form_frame)
        self.precio_compra_entry.grid(row=3, column=1, sticky="ew")

        ctk.CTkLabel(form_frame, text="precio de venta").grid(row=4, column=0, sticky="w")
        self.precio_venta_entry = ctk.CTkEntry(form_frame)
        self.precio_venta_entry.grid(row=4, column=1, sticky= "ew")

        ctk.CTkLabel(form_frame, text="porcentaje de IVA").grid(row=5, column=0, sticky="w")
        self.porcentaje_iva_entry = ctk.CTkEntry(form_frame)
        self.porcentaje_iva_entry.grid(row=5, column=1, sticky= "ew")

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
        cantidad_stock = self.cantidad_stock_entry.get().strip()
        precio_compra = self.precio_compra_entry.get().strip()
        precio_venta = self.precio_venta_entry.get().strip()
        porcentaje_iva = self.porcentaje_iva_entry.get().strip()

        if not nombre or not cantidad_stock or not precio_compra or not precio_venta or not porcentaje_iva:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos")
            return None

        if len(nombre) > MAX_NOMBRE_LEN:
            messagebox.showerror("Error", f"Nombre demasiado largo ({MAX_NOMBRE_LEN})")
            return None

        unidad_medida = self.unidad_medida_opm.get()

        # todo: validaciones de tipo de datos en controller

        sel_marca = self.tv_marcas.selection()
        if not sel_marca:
            messagebox.showerror("Error", "Seleccione una marca")
            return None

        return nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, sel_marca[0]  # iid = id_compania

    # ---------------- ACCIONES ----------------
    def crear(self):
        data = self._validar_form()
        if not data:
            return

        nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, id_marca = data

        if self.controller:
            self.controller.crear_producto(nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, id_marca)

    def actualizar(self):
        sel = self.tv_productos.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione un producto")
            return

        data = self._validar_form()
        if not data:
            return

        id_producto = sel[0]
        nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, id_marca = data

        if self.controller:
            self.controller.actualizar_producto(id_producto, nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, id_marca)

    def eliminar(self):
        sel = self.tv_productos.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione un producto")
            return

        if self.controller:
            self.controller.eliminar_producto(sel[0])

    def limpiar(self):
        self.nombre_entry.delete(0, "end")

        # si usas CTkTextbox
        if hasattr(self, "desc_text"):
            self.desc_text.delete("1.0", "end")

        # opcional: limpiar selección de tablas
        self.tv_productos.selection_remove(self.tv_productos.selection())
        self.tv_marcas.selection_remove(self.tv_marcas.selection())

    # ---------------- HELPERS PARA CARGA ----------------
    def cargar_productos(self, productos=None):

        if self.controller and not productos:
            productos = self.controller.listar_productos()

        self.tv_productos.delete(*self.tv_productos.get_children())

        if len(productos) == 0:
            self.tv_productos.insert(
                "",
                "end",
                values=("No hay productos",) + ("",) * (len(self.tv_marcas["columns"]) - 1)
            )
        else:
            for p in productos:
                self.tv_productos.insert(
                    "",
                    "end",
                    iid=p["id_producto"],
                    values=(p["nombre"], p["cantidad_stock"], p["unidad_medida"], p["precio_compra"],
                            p["precio_venta"], p["porcentaje_iva"], p["id_marca"], p["marca"])
                ) # todo: Probar la interacción entre el optionmenu y el actualizar, la selección del producto y eso

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




# ---------------- TEST LOCAL DE LA VISTA ----------------
if __name__ == "__main__":
    ctk.set_appearance_mode("System")


    class DummyController:
        def crear_producto(self, *args): print("crear", args)

        def actualizar_productos(self, *args): print("actualizar", args)

        def eliminar_producto(self, *args): print("eliminar", args)

        def listar_productos(self): return ()

        def listar_marcas(self): return ()




    app = ctk.CTk()
    app.geometry("900x500")

    view = ProductosView(app, controller=DummyController())
    view.pack(fill="both", expand=True)

    view.cargar_marcas([
        {"id_marca": "10", "nombre": "Marca X", "descripcion": "Desc", "id_compania": "1"},
    ])

    view.cargar_productos([
        {"id_producto": "1","nombre": "Prod A" , "cantidad_stock": "3", "unidad_medida": "Litros", "precio_compra": "13000"
            ,"precio_venta": "14000", "porcentaje_iva": "0", "id_marca":"1", "marca": "Marca X"},
        {"id_producto": "2", "nombre": "Prod B", "cantidad_stock": "190", "unidad_medida": "Kilogramos",
         "precio_compra": "1200", "precio_venta": "1250", "porcentaje_iva": "3", "id_marca": "1", "marca": "Marca X"}
    ])


    app.mainloop()
