import cv2
import os
import mediapipe as mp
import math
import sqlite3
import numpy as np
import datetime

data = sqlite3.connect("Registro.db")
cursor = data.cursor()

column_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS registro(
        "EMOCIÓN PERCIBIDA" VARCHAR (15)
        )
""")

if os.path.exists("Registro.db"):
    try:
        cursor.execute(f"""
            ALTER TABLE registro ADD COLUMN "{column_name}" VARCHAR (100)
        """)

    except sqlite3.OperationalError as e:
        pass

AddData = [
    ("Neutral")
    ]


Emociones = np.array([0, 0, 0, 0])
last_emotion = None

mp_mascara = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
config = mp_drawing.DrawingSpec(thickness = 1, circle_radius = 1)

capture =cv2.VideoCapture(0, cv2.CAP_DSHOW)

with mp_mascara.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5) as face_mesh:

    while True:
        ret, frame = capture.read()
        if ret == False:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        px = []
        py = []
        listado = []
        r = 5
        t = 3

        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, face_landmarks,
                    mp_mascara.FACEMESH_CONTOURS,
                    mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))
                for id,puntos in enumerate(face_landmarks.landmark):
                    al, an, c = frame.shape
                    x,y = int(puntos.x*an), int(puntos.y*al)
                    px.append(x)
                    py.append(y)
                    listado.append([id, x, y])
                    if len(listado) == 468:
                        #región: Ceja Derecha
                        x1, y1 = listado [65] [1:]
                        x2, y2 = listado [158] [1:]
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                        longitud1 = math.hypot(x2 - x1, y2 - y1)
                        

                        #región: Ceja Izquierda
                        x3, y3 = listado [295] [1:]
                        x4, y4 = listado [385] [1:]
                        cx2, cy2 = (x3 + x4) // 2, (y3 + y4) // 2
                        longitud2 = math.hypot(x4 - x3, y4 - y3)
                        

                        #región: Bordes de la boca
                        x5, y5 = listado [78] [1:]
                        x6, y6 = listado [308] [1:]
                        cx3, cy3 = (x5 + x6) // 2, (y5 + y6) // 2
                        longitud3 = math.hypot(x6 - x5, y6 - y5)


                        #región: Líneas de apertura de la boca
                        x7, y7 = listado [13] [1:]
                        x8, y8 = listado [14] [1:]
                        cx4, cy4 = (x7 + x8) // 2, (y7 + y8) // 2
                        longitud4 = math.hypot(x8 - x7, y8 - y7)

                        #Emoción: Enojo
                        if longitud1 < 19 and longitud2 < 19 and longitud3 > 80 and longitud3 < 95 and longitud4 < 5:
                            current_emotion = "Enojo"
                            if current_emotion != last_emotion:
                                cv2.putText(frame, 'Enojado', (480, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 0, 255), 3)
                                AddData = [
                                            ("Enojo")
                                            ]
                                insert_query = f"INSERT INTO registro (\"EMOCIÓN PERCIBIDA\", \"{column_name}\") VALUES (?, ?)"
                                cursor.execute(insert_query, (AddData[0], current_emotion))
                                data.commit()
                                last_emotion = current_emotion

                        #Emoción: Felicidad
                        if longitud1 > 20 and longitud1 < 30 and longitud2 > 20 and longitud2 < 30 and longitud3 > 109 and longitud4 > 10 and longitud4 < 20:
                            current_emotion = "Felicidad"
                            if current_emotion != last_emotion:
                                cv2.putText(frame, 'Feliz', (480, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 255, 255), 3)
                                AddData = [
                                            ("Felicidad")
                                            ]
                                insert_query = f"INSERT INTO registro (\"EMOCIÓN PERCIBIDA\", \"{column_name}\") VALUES (?, ?)"
                                cursor.execute(insert_query, (AddData[0], current_emotion))
                                data.commit()
                                last_emotion = current_emotion

                        #Emoción: Sorpresa
                        if longitud1 > 35 and longitud2 > 35 and longitud3 > 80 and longitud3 < 90 and longitud4 >20:
                            current_emotion = "Sorpresa"
                            if current_emotion != last_emotion:
                                cv2.putText(frame, 'Sorprendido', (480, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 255, 0), 3)
                                AddData = [
                                            ("Sorpresa")
                                            ]
                                insert_query = f"INSERT INTO registro (\"EMOCIÓN PERCIBIDA\", \"{column_name}\") VALUES (?, ?)"
                                cursor.execute(insert_query, (AddData[0], current_emotion))
                                data.commit()
                                last_emotion = current_emotion

                        #Emoción: Tristeza
                        if longitud1 > 20 and longitud1 < 35 and longitud2 > 20 and longitud2 < 35 and longitud3 > 80 and longitud3 < 95 and longitud4 < 5:
                            current_emotion = "Tristeza"
                            if current_emotion != last_emotion:
                                cv2.putText(frame, 'Triste', (480, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (255, 0, 0), 3)
                                AddData = [
                                            ("Tristeza")
                                            ]
                                insert_query = f"INSERT INTO registro (\"EMOCIÓN PERCIBIDA\", \"{column_name}\") VALUES (?, ?)"
                                cursor.execute(insert_query, (AddData[0], current_emotion))
                                data.commit()
                                last_emotion = current_emotion


        cv2.imshow('frame', frame)
        if (cv2.waitKey(1) == ord('s')):
         break


data.close()

capture.release()
cv2.destroyAllWindows()
