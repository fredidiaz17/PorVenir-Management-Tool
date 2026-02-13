import customtkinter as ctk


# Importar vistas
from views.CompaniasView import CompaniasView
from views.MarcasView import MarcasView
from src.views.ProductosView import ProductosView

# Importar Controladores
from controllers.CompaniasController import CompaniasController
from controllers.MarcasController import MarcasController
from controllers.ProductosController import ProductoController

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración global de la app
        self.title("Sistema de Gestión")
        self.geometry("900x600")
        self.minsize(800, 500)

        # Configuración del grid principal
        self.grid_rowconfigure(0, weight=0) # El de la barra (no crece)
        self.grid_rowconfigure(1, weight=1)  # Vistas (si crece)
        self.grid_columnconfigure(0, weight=1)


        # -------- Contenedor principal (donde viven las vistas) --------
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=1, column=0, sticky="nsew")

        # Permitir que las vistas se expandan
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Controladores por vista
        self.compania_controller = CompaniasController()
        self.marca_controller = MarcasController(self.compania_controller)
        self.producto_controller = ProductoController(self.marca_controller)

        # Diccionario de vistas
        self.vistas = {}

        # Crear vistas
        self._crear_vistas()

        # -------- Barra de navegación --------
        self.navbar = ctk.CTkFrame(self, height=50)
        self.navbar.grid(row=0, column=0, sticky="ew")
        self.navbar.grid_propagate(False)

        # Botones para cambiar de vista
        self.botones_nav = {}
        self._crear_btns()

        # Mostrar vista inicial
        self.vista_actual  = None
        self.mostrar_vista("producto")


    def _crear_vistas(self):

        # Instanciar todas las vistas y dejarlas listas
        self.vistas["compañia"] = CompaniasView(parent=self.container, app=self, controller=self.compania_controller)
        self.vistas["marca"] = MarcasView(parent=self.container, app= self, controller= self.marca_controller)
        self.vistas["producto"] = ProductosView(parent=self.container, app= self, controller= self.producto_controller)


    def _crear_btns(self):

        for nombre_vista in self.vistas.keys():
            btn = ctk.CTkButton(
                self.navbar,
                text = nombre_vista,
                command = lambda n=nombre_vista: self.mostrar_vista(n)
            )

            btn.pack(side="left", padx=10, pady=10)

            self.botones_nav[nombre_vista] = btn


    def mostrar_vista(self, nombre_vista):
        # Destruyendo la vista actual
        if self.vista_actual is not None:
            self.vista_actual.grid_forget()

        # levantando (raise) la vista
        vista = self.vistas.get(nombre_vista)

        if vista:
            vista.grid(row=0, column=0, sticky= "nsew")
            self.vista_actual = vista

            # cargando registros
            if hasattr(vista, "on_show"):
                vista.on_show()
            # resetear colores de botones
            for btn in self.botones_nav.values():
                btn.configure(fg_color=("gray75", "gray25"))

            # Activar el seleccionado
            self.botones_nav[nombre_vista].configure(fg_color=("blue", "blue"))


        else:
            raise ValueError(f"La vista '{nombre_vista}' no existe")



if __name__ == "__main__":
    app = App()
    app.mainloop()

# todo: Agregar logs a los respectivos modulos, continuar con otras entidades
