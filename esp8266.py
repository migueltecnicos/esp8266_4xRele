import socket


class ESP8266:
    def __init__(self, ip, puerto):
        self.ip = ip                # IP
        self.puerto = puerto        # Puerto
        self.conectado = False      # Indica si está conectado
        self.s : socket.socket = None               # Socket para conectar y enviar los comandos
        self.msg_error = ""

    def conectar(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.ip, self.puerto))
            self.conectado = True
            self.s.settimeout(3)
            resul = True
        except Exception as e:
            self.msg_error = str(e)
            resul = False

        return resul

    def desconectar(self):
        if self.conectado:
            self.s.close()
            self.conectado = False

    @staticmethod
    def crear_comando(num_rele, operacion):
        if num_rele < 1 or num_rele > 4:
            raise IndexError("Número de relé incorrecto")
        if operacion < 0 or operacion > 1:
            raise IndexError("Operación incorrecta")

        comando = bytearray.fromhex("a0")
        comando.append(num_rele)
        comando.append (operacion)      # 1 activar, 0 desactivar
        suma = 0
        for byte in comando:
            suma += byte
        suma = suma % 256
        comando.append(suma)
        return comando

    def encender(self, num_rele: int):
        comando = self.crear_comando(num_rele, 1)

        if self.conectado:
            self.s.send(comando)

    def apagar(self, num_rele: int):
        comando = self.crear_comando(num_rele, 0)

        if self.conectado:
            self.s.send(comando)

    def status(self):
        if self.conectado:
            self.s.send(b'\xFF')
            respuesta = self.s.recv(1024)
            print(self.s.recv(1024).hex())
