import cv2
import time

from hand_tracker import HandTracker
from angle_calculator import AngleCalculator
from serial_sender import SerialSender
from utils import EMAFilter, draw_info_overlay, draw_close_button


running = True

def mouse_callback(event, x, y, flags, param):
    
    global running
    if event == cv2.EVENT_LBUTTONDOWN:
       
        if 440 <= x <= 620 and 20 <= y <= 60:
            print("Se hizo clic en el botón 'Cerrar'. Deteniendo ciclo principal...")
            running = False

def main():
    global running
   
    SERIAL_PORT = 'COM3' 
    BAUD_RATE = 115200

    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    tracker = HandTracker(detection_con=0.8, tracking_con=0.8)
    calculator = AngleCalculator()
    sender = SerialSender(port=SERIAL_PORT, baudrate=BAUD_RATE)

    filters = [EMAFilter(alpha=0.3) for _ in range(5)]

    pTime = 0

    print("\n--- Sistema iniciado ---")
    print("Presiona la tecla 'q' en la ventana de video para salir.")

    cv2.namedWindow("Control de Mano Robotica")
    cv2.setMouseCallback("Control de Mano Robotica", mouse_callback)

    try:
        while running:
            success, img = cap.read()
            if not success:
                print("Error capturando frame del video.")
                break
                
            img = cv2.flip(img, 1)

            img = tracker.find_hands(img, draw=True)
            
            lm_list = tracker.get_landmarks(img, hand_no=0)
            
            angles = [0, 0, 0, 0, 0]
            if len(lm_list) != 0:
                raw_angles = calculator.get_finger_angles(lm_list)
                
                for i in range(5):
                    filtered = filters[i].filter(raw_angles[i])
                    angles[i] = int(filtered)

                sender.send_angles(angles)

            cTime = time.time()
            fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
            pTime = cTime

            img = draw_info_overlay(img, fps, angles)
            
            img = draw_close_button(img, 440, 20, 620, 60)

            cv2.imshow("Control de Mano Robotica", img)
            
            if cv2.getWindowProperty("Control de Mano Robotica", cv2.WND_PROP_VISIBLE) < 1:
                print("Ventana cerrada mediante la 'X'. Saliendo de forma segura...")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Tecla 'q' presionada. Saliendo de forma segura...")
                break

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        sender.close()
        print("Fin de ejecución.")

if __name__ == "__main__":
    main()
