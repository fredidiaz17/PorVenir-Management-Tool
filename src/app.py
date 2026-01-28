import customtkinter as ctk

# Importar vistas
from views.CompaniasView import CompaniaView
from views.MarcasView import MarcasView

# Importar Controladores
from controllers.MarcasController import MarcasController

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración global de la app
        self.title("Sistema de Gestión")
        self.geometry("900x600")
        self.minsize(800, 500)

        # Contenedor principal (donde viven las vistas)
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Permitir que las vistas se expandan
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        # Controladores por vista
        self.marca_controller = MarcasController()

        # Diccionario de vistas
        self.vistas = {}

        # Crear vistas
        self._crear_vistas()

        # Mostrar vista inicial
        self.mostrar_vista("compañia")
        self.mostrar_vista("marca")


    def _crear_vistas(self):

        # Instanciar todas las vistas y dejarlas listas...aunque solo haya una por ahora :v
        self.vistas["compañia"] = CompaniaView(self.container) #agregar app al inicializador de la clase
        self.vistas["marca"] = MarcasView(parent=self.container, app= self, controller= self.marca_controller)


        # acomodandolas (grid), iterando por el diccionario (sus valores)
        for vista in self.vistas.values():
            vista.pack(side="bottom")

    def mostrar_vista(self, nombre_vista):
        # levantando (raise) la vista
        vista = self.vistas.get(nombre_vista)
        if vista:
            vista.tkraise()
        else:
            raise ValueError(f"La vista '{nombre_vista}' no existe")


if __name__ == "__main__":
    app = App()
    app.mainloop()

