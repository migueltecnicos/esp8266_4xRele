from config import Config
from esp8266 import ESP8266


class Applicacion:
    def __init__(self):
        self.config = Config()
        self.esp = None

    def procesa_argumentos(self):
        import argparse
        parser = argparse.ArgumentParser(description="Control por ethernet de módulo 8266. By Miguel Á. Sánchez",
                                         add_help=False)
        group0 = parser.add_mutually_exclusive_group(required=True)
        group0.add_argument("-h", "--help", action="store_true", help="Muestra este mensaje de ayuda")
        parser.add_argument("-i", "--ip", required=True, type=str, help="Dirección IP del módulo a controlar")
        group0.add_argument("-s", "--status", action="store_true", help="Devuelve el estado de cada relé (depende de firmware)")
        group0.add_argument("-r", "--rele", help="Relé a encender/apagar", type=int, choices=[1,2,3,4])
        group1 = parser.add_mutually_exclusive_group()
        group1.add_argument("-1", "--on", action="store_true", help="Encender relé seleccionado")
        group1.add_argument("-0", "--off", action="store_true", help="Apagar relé seleccionado")

        args = parser.parse_args()

        if args.help:
            parser.print_help()
            exit(0)
        elif args.status:
            self.config.status = True
            print("Seleccionado status")
            if not args.ip:
                print("Error: Hay que especificar IP para ver el estado")
                parser.print_help()
                exit(1)
            else:
                self.config.ip = args.ip
        elif args.rele:
            # Comprueba que tenemos todos los datos
            if not args.ip or not args.rele or not (args.on or args.off):
                print("Error: Hay que especificar IP y relé para cambiar un relé")
                parser.print_help()
                exit(1)
            else:
                self.config.status = False
                self.config.ip = args.ip
                self.config.rele = args.rele
                self.config.accion = args.on
        else:
            parser.print_help()

    def main(self):
        self.procesa_argumentos()
        self.config.print()
        self.esp = ESP8266(self.config.ip, self.config.puerto)
        if self.esp.conectar():
            if self.config.status:
                self.esp.status()
            else:
                if self.config.accion:
                    self.esp.encender(self.config.rele)
                else:
                    self.esp.apagar(self.config.rele)

            self.esp.desconectar()
        else:
            print("Error al conectar:", self.esp.msg_error)
