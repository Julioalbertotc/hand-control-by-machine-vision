import cv2

class EMAFilter:
    """
    Filtro de Media Móvil Exponencial (Exponential Moving Average).
    Ayuda a suavizar los valores calculados de los ángulos de los dedos
    para evitar vibraciones (jitter) en los servomotores.
    """
    def __init__(self, alpha=0.3):
        """
        :param alpha: Factor de suavizado (0 < alpha <= 1).
                      Valores más bajos suavizan más pero introducen retraso.
                      Valores más cercanos a 1 son más rápidos pero filtran menos.
        """
        self.alpha = alpha
        self.current_value = None

    def filter(self, new_value):
        if self.current_value is None:
            self.current_value = new_value
        else:
            self.current_value = (self.alpha * new_value) + ((1 - self.alpha) * self.current_value)
        return self.current_value

def draw_info_overlay(image, fps, angles):
    """
    Dibuja un overlay en la imagen con los FPS y los ángulos calculados.
    
    :param image: Imagen de OpenCV (numpy array).
    :param fps: Valor de FPS (frames per second).
    :param angles: Lista con los 5 ángulos de los dedos [pulgar, índice, medio, anular, meñique].
    """
    # Mostrar FPS
    cv2.putText(image, f'FPS: {int(fps)}', (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    # Nombres de los dedos
    finger_names = ["Pulgar", "Indice", "Medio", "Anular", "Menique"]
    
    # Mostrar ángulos de cada dedo
    y_pos = 100
    for i, angle in enumerate(angles):
        text = f'{finger_names[i]}: {int(angle)} grados'
        cv2.putText(image, text, (20, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        y_pos += 40
        
    return image

def draw_close_button(image, x1, y1, x2, y2):
    """
    Dibuja un botón rojo visual para cerrar el sistema de forma segura.
    """
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), cv2.FILLED)
    cv2.putText(image, "Cerrar", (x1 + 35, y2 - 12), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    return image
