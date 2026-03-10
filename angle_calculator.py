import math

class AngleCalculator:
    """
    Calcula el grado de flexión de cada dedo basándose en los landmarks
    detectados por MediaPipe.
    Los ángulos se mapean a un rango de 0 a 180 para controlar servomotores.
    """
    def __init__(self):
        # Índices de MediaPipe para los extremos de cada dedo
        self.tip_ids = [4, 8, 12, 16, 20]
        # Índices de MediaPipe para las bases de cada dedo
        self.mcp_ids = [2, 5, 9, 13, 17]

    def _calculate_distance(self, p1, p2):
        """Calcula la distancia euclidiana entre dos puntos (x, y)"""
        return math.hypot(p2[1] - p1[1], p2[2] - p1[2])

    def get_finger_angles(self, lm_list):
        """
        Calcula el ángulo (0-180) para el pulgar, índice, medio, anular y meñique.
        
        :param lm_list: Lista de landmarks [id, x, y].
        :return: Lista de enteros con los 5 ángulos calculados.
        """
        if len(lm_list) == 0:
            return [0, 0, 0, 0, 0]

        angles = []
        
        # Referencia estática, la muñeca
        wrist = lm_list[0]

        # 1. Pulgar (Thumb)
        # Para el pulgar es más confiable medir la distancia entre la punta (4) y la base del índice o del propio pulgar
        thumb_tip = lm_list[self.tip_ids[0]]
        thumb_ip = lm_list[self.tip_ids[0] - 1]
        thumb_mcp = lm_list[self.mcp_ids[0]]
        
        # Distancia entre la punta del pulgar y la base (mcp)
        dist_thumb = self._calculate_distance(thumb_tip, thumb_mcp)
        # Rango empírico aproximado de distancias en pixeles para el pulgar
        # (Esto requeriría una normalización por tamaño de mano idealmente)
        max_thumb_dist = self._calculate_distance(thumb_mcp, wrist) * 1.5 
        min_thumb_dist = max_thumb_dist * 0.3
        
        thumb_angle = self._map_distance_to_angle(dist_thumb, min_thumb_dist, max_thumb_dist)
        angles.append(thumb_angle)

        # 2. Resto de los dedos (Índice, Medio, Anular, Meñique)
        for id in range(1, 5):
            tip = lm_list[self.tip_ids[id]]
            mcp = lm_list[self.mcp_ids[id]]
            
            # Distancia de la punta del dedo a la muñeca o base
            dist = self._calculate_distance(tip, wrist)
            
            # Distancia de la base del dedo a la muñeca (usado para normalizar proporciones)
            base_dist = self._calculate_distance(mcp, wrist)
            
            # Rango empírico: 
            # Dedo extendido -> dist es ~2.2x la base_dist
            # Dedo doblado -> dist es ~0.8x la base_dist
            max_dist = base_dist * 2.2
            min_dist = base_dist * 0.8
            
            angle = self._map_distance_to_angle(dist, min_dist, max_dist)
            angles.append(angle)

        return angles

    def _map_distance_to_angle(self, value, min_val, max_val):
        """
        Mapea linealmente un valor de un rango [min_val, max_val] a [0, 180].
        Asegura que el valor final esté entre 0 y 180.
        """
        # Limitar valor dentro del rango min y max
        value = max(min_val, min(value, max_val))
        
        # Mapeo: 180 es completamente abierto (max_val), 0 es cerrado (min_val)
        # Si quieres invertirlo (0 abierto, 180 cerrado), cambia esta línea.
        ratio = (value - min_val) / (max_val - min_val) if max_val > min_val else 0
        angle = int(ratio * 180)
        
        return angle
