class Config:
    def __init__(self):
        self.status = False # Modo cambiar rele
        self.ip = ""        # Sin IP
        self.puerto = 8080
        self.rele = 1       # Primer rele
        self.accion = True   # ON

    def print(self):
        print("Configuración cargada:\n")
        print("Estado:", self.status)
        print("IP:", self.ip)
        print("Rele:", self.rele)
        print("Accion:", self.accion)
