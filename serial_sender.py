import serial
import time

class SerialSender:
    """
    Clase para manejar la comunicación con el microcontrolador ESP32
    a través del puerto serial.
    """
    def __init__(self, port, baudrate=115200):
        """
        Inicializa la conexión.
        
        :param port: Cadena con el nombre del puerto (ej: 'COM3' o '/dev/ttyUSB0').
        :param baudrate: Tasa de baudios. Debe coincidir con la del ESP32.
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_inst = None
        self.is_connected = False
        
        try:
            self.serial_inst = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Dar tiempo al ESP32 para reiniciar si es necesario tras abrir la conexión
            self.is_connected = True
            print(f"Conexión serial establecida en {self.port} a {self.baudrate} baudios.")
        except serial.SerialException as e:
            print(f"Error abriendo el puerto serial {self.port}: {e}")
            print("El sistema continuará sin enviar datos físicos (Modo Simulación).")

    def send_angles(self, angles):
        """
        Envía los 5 ángulos de los dedos mediante un string formateado:
        'thumb,index,middle,ring,pinky\n'
        
        :param angles: Lista de 5 enteros representando los ángulos.
        """
        if not self.is_connected or len(angles) != 5:
            return

        # Formatear el string
        # Ejemplo: "90,180,180,0,0\n"
        data_string = f"{angles[0]},{angles[1]},{angles[2]},{angles[3]},{angles[4]}\n"
        
        try:
            self.serial_inst.write(data_string.encode('utf-8'))
        except serial.SerialException as e:
            print(f"Error escribiendo en el puerto serial: {e}")
            self.is_connected = False

    def close(self):
        """Cierra la conexión serial de forma segura."""
        if self.is_connected and self.serial_inst:
            self.serial_inst.close()
            print("Conexión serial cerrada.")
