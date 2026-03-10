# Controlador de Mano Robótica por Visión Artificial

Este proyecto es un sistema para controlar cinco servomotores MG90S (para los cinco dedos de una mano robótica) usando procesamiento de visión artificial en tiempo real con Python, OpenCV y MediaPipe, enviando instrucciones a un microcontrolador ESP32.

Elimina la necesidad de utilizar un guante con sensores de flexión y lo sustituye por el seguimiento en 3D de la mano utilizando simplemente una cámara web.

## Arquitectura

El proyecto consta de los siguientes ficheros:
- `requirements.txt`: Dependencias del sistema.
- `main.py`: Bucle principal que integra cámara, seguimiento, cálculo de ángulos y puerto serial.
- `hand_tracker.py`: Wrapper de MediaPipe Hands para la extracción de puntos clave.
- `angle_calculator.py`: Lógica matemática para determinar qué tan doblado está cada dedo.
- `serial_sender.py`: Wrapper de PySerial para enviar un string como `30,90,120,60,10` al ESP32.
- `utils.py`: Filtros matemáticos de suavizado (Exponential Moving Average) y funciones de pintado sobre OpenCV.

## Variables y Lógica del Sistema

1. **Captura:** OpenCV lee tu webcam a la máxima velocidad posible (ajustado para ~30 fps).
2. **Landmarks:** MediaPipe genera las 21 coordenadas (x,y,z) del esqueleto digital de tu mano.
3. **Cálculo de distancias:** `angle_calculator.py` analiza la distancia entre la yema de tus dedos (tip) y la palma de tu mano/muñeca frente a la distancia de tus nudillos (base_dist) permitiendo normalizar el tamaño de la mano frente a la cámara.
4. **Mapeo angular:** Esta proporción se mapea linealmente a grados del motor (0-180).
5. **Ajuste de fluctuación:** `utils.py` contiene un filtro de paso bajo EMA con ratio 'alfa'. Esto retarda infinitesimalmente la señal a cambio de evitar que los servos tiemblen debido a microrruidos del video.
6. **UART:** Se manda todo como texto base.

## Instalación y Configuración

Abre tu terminal en Windows e instala las dependencias (se requiere Python 3.8 - 3.11):
```bash
pip install -r requirements.txt
```

Luego, verifica qué puerto está utilizando tu ESP32:
1. Abre tu Administrador de Dispositivos en Windows (Device Manager).
2. Expande "Puertos (COM y LPT)".
3. Busca el puerto COM correspondiente (ej: `COM3`, `COM4`).
4. Abre `main.py` y edita la constante de la línea 15:
```python
SERIAL_PORT = 'COM3' # Sustituir por el COM que utilices 
```

## Ejecución

Simplemente ejecuta:
```bash
python main.py
```

## Calibración de Motores (Rangos de Flexión)

Si notas que los dedos no alcanzan a abrirse o cerrarse por completo en el brazo robótico, puedes ajustar empíricamente la matemática de los dedos en `angle_calculator.py`:

Dentro del método `get_finger_angles()`:
```python
max_dist = base_dist * 2.2 # Rango en el que considera que el dedo está completamente extendido
min_dist = base_dist * 0.8 # Rango en el que considera que el dedo está completamente cerrado
```
Si ves que necesitas doblar tu mano de manera muy exagerada, aumenta el factor `0.8`. Si por el contrario no cierra del todo, bújalo un poco.

El filtro de velocidad de los motores se ajusta en `main.py`:
```python
filters = [EMAFilter(alpha=0.3) for _ in range(5)]
```
- Si cambias **`alpha=1.0`**, los motores reaccionarán de forma instantánea pero puede vibrar.
- Si cambias **`alpha=0.1`**, los motores irán muy suaves, pero tendrán un leve retardo robótico.
