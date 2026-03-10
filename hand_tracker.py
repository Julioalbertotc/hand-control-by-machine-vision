import cv2
import mediapipe as mp

class HandTracker:
    """
    Clase que encapsula la funcionalidad de MediaPipe para detectar y seguir
    las manos en un flujo de video.
    """
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, tracking_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.tracking_con = tracking_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.tracking_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        """
        Procesa la imagen para buscar manos. Si encuentra alguna, puede dibujarla.
        
        :param img: Imagen BGR de OpenCV.
        :param draw: Booleano para dibujar las conexiones de la mano.
        :return: Imagen procesada.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
        return img

    def get_landmarks(self, img, hand_no=0):
        """
        Obtiene las coordenadas (x, y) de cada uno de los 21 puntos clave de la mano.
        
        :param img: Imagen de OpenCV (utilizada para escalar los valores a píxeles).
        :param hand_no: Índice de la mano a analizar.
        :return: Lista de puntos landmarks, donde cada punto es [id, cx, cy].
        """
        lm_list = []
        if self.results.multi_hand_landmarks:
            hand_landmarks = self.results.multi_hand_landmarks[hand_no]
            h, w, c = img.shape
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list
