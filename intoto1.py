import tkinter
from datetime import datetime
import random

# Interfaz de transacciones (sin decoradores)
class Transacciones:
    def abonar(self, cantidad):
        pass

    def cargar(self, cantidad):
        pass

# Clase Cliente
class Cliente:
    def __init__(self, nombre, apellido_paterno, apellido_materno, fecha_nac, domicilio):
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.fecha_nac = fecha_nac
        self.domicilio = domicilio

# Clase Cuenta
class Cuenta(Transacciones):
    def __init__(self, numero):
        self.numero = numero
        self.saldo = 1000

    def abonar(self, cantidad):
        self.saldo += cantidad

    def cargar(self, cantidad):
        if self.saldo >= cantidad:
            self.saldo -= cantidad
            return True
        return False

# Clase Movimiento
class Movimiento:
    def __init__(self, fecha_mov, descripcion, cargo, abono, saldo):
        self.fecha_mov = fecha_mov
        self.descripcion = descripcion
        self.cargo = cargo
        self.abono = abono
        self.saldo = saldo

# Clase Estado de Cuenta
class EstadoCuenta:
    def __init__(self, cliente, cuenta, fecha_ingreso):
        self.cliente = cliente
        self.cuenta = cuenta
        self.fecha_ingreso = fecha_ingreso
        self.movimientos = []

    def agregar_movimiento(self, movimiento):
        self.movimientos.append(movimiento)

    def resumen(self):
        total_cargos = 0
        total_abonos = 0
        for mov in self.movimientos:
            total_cargos += mov.cargo
            total_abonos += mov.abono
        if len(self.movimientos) > 0:
            saldo_final = self.movimientos[-1].saldo
        else:
            saldo_final = self.cuenta.saldo
        return total_cargos, total_abonos, saldo_final

# Interfaz gráfica
class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Captura de Cliente y Cuenta")
        self.ventana.geometry("500x600")
        self.crear_pantalla_captura()

    def crear_pantalla_captura(self):
        self.entradas = {}

        campos = ["Nombre", "Apellido Paterno", "Apellido Materno", "Fecha de Nacimiento", "Domicilio", "Numero de Cuenta"]
        for campo in campos:
            etiqueta = tkinter.Label(self.ventana, text=campo)
            entrada = tkinter.Entry(self.ventana)
            etiqueta.pack()
            entrada.pack()
            self.entradas[campo] = entrada

        boton = tkinter.Button(self.ventana, text="Generar Movimientos", command=self.generar_estado)
        boton.pack(pady=10)

    def generar_estado(self):
        nombre = self.entradas["Nombre"].get()
        apellido1 = self.entradas["Apellido Paterno"].get()
        apellido2 = self.entradas["Apellido Materno"].get()
        fecha_nac = self.entradas["Fecha de Nacimiento"].get()
        domicilio = self.entradas["Domicilio"].get()
        numero_cuenta = self.entradas["Numero de Cuenta"].get()

        cliente = Cliente(nombre, apellido1, apellido2, fecha_nac, domicilio)
        cuenta = Cuenta(numero_cuenta)
        estado = EstadoCuenta(cliente, cuenta, datetime.today())

        for i in range(10):
            tipo = random.choice(["cargo", "abono"])
            cantidad = random.randint(50, 500)
            fecha = datetime.today().strftime("%Y-%m-%d")

            if tipo == "abono":
                cuenta.abonar(cantidad)
                mov = Movimiento(fecha, "Abono realizado", 0, cantidad, cuenta.saldo)
            else:
                if cuenta.cargar(cantidad):
                    mov = Movimiento(fecha, "Cargo realizado", cantidad, 0, cuenta.saldo)
                else:
                    continue

            estado.agregar_movimiento(mov)

        self.mostrar_consulta(estado)

    def mostrar_consulta(self, estado):
        ventana_nueva = tkinter.Toplevel(self.ventana)
        ventana_nueva.title("Consulta - Estado de Cuenta")
        ventana_nueva.geometry("600x600")

        cliente = estado.cliente
        cuenta = estado.cuenta
        total_cargos, total_abonos, saldo_final = estado.resumen()

        texto_cliente = "Cliente:\n"
        texto_cliente += "  Nombre: " + cliente.nombre + " " + cliente.apellido_paterno + " " + cliente.apellido_materno + "\n"
        texto_cliente += "  Fecha de nacimiento: " + cliente.fecha_nac + "\n"
        texto_cliente += "  Domicilio: " + cliente.domicilio + "\n\n"
        texto_cliente += "Cuenta:\n"
        texto_cliente += "  Numero: " + cuenta.numero + "\n"
        texto_cliente += "  Saldo inicial: 1000\n"

        etiqueta_cliente = tkinter.Label(ventana_nueva, text=texto_cliente, justify="left", font=("Courier", 10))
        etiqueta_cliente.pack(anchor="w", padx=10)

        titulo = tkinter.Label(ventana_nueva, text="Movimientos:", font=("Arial", 12, "bold"))
        titulo.pack(anchor="w", padx=10, pady=5)

        for i in range(len(estado.movimientos)):
            mov = estado.movimientos[i]
            texto = str(i+1) + ". Fecha: " + mov.fecha_mov + ", Desc: " + mov.descripcion + ", Cargo: " + str(mov.cargo) + ", Abono: " + str(mov.abono) + ", Saldo: " + str(mov.saldo)
            etiqueta = tkinter.Label(ventana_nueva, text=texto, justify="left", font=("Courier", 9))
            etiqueta.pack(anchor="w", padx=20)

        resumen = "\nResumen:\n"
        resumen += "  Total Cargos: " + str(total_cargos) + "\n"
        resumen += "  Total Abonos: " + str(total_abonos) + "\n"
        resumen += "  Saldo Final: " + str(saldo_final) + "\n"

        etiqueta_resumen = tkinter.Label(ventana_nueva, text=resumen, justify="left", font=("Courier", 10, "bold"))
        etiqueta_resumen.pack(anchor="w", padx=10, pady=10)

# Ejecución
ventana_principal = tkinter.Tk()
aplicacion = App(ventana_principal)
ventana_principal.mainloop()
