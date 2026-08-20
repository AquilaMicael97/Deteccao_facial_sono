import cv2
import mediapipe as mp
import numpy as np
import time
import os

from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python.vision import drawing_utils as mp_drawing

modelo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'face_landmarker.task')

p_olho_esq = [385, 380, 387, 373, 362, 263]
p_olho_dir = [160, 144, 158, 153, 33, 133]
p_olhos = p_olho_esq+p_olho_dir

def calculo_ear(face, p_olho_dir,p_olho_esq):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_esq = face[p_olho_esq,:]
        face_dir = face[p_olho_dir,:]

        ear_esq = (np.linalg.norm(face_esq[0]-face_esq[1])+np.linalg.norm(face_esq[2]-face_esq[3]))/(2*(np.linalg.norm(face_esq[4]-face_esq[5])))
        ear_dir = (np.linalg.norm(face_dir[0]-face_dir[1])+np.linalg.norm(face_dir[2]-face_dir[3]))/(2*(np.linalg.norm(face_dir[4]-face_dir[5])))
    except:
        ear_esq = 0.0
        ear_dir = 0.0
    media_ear = (ear_esq+ear_dir)/2
    return media_ear

p_boca = [82, 87, 13, 14, 312, 317, 78, 308]

def calculo_mar(face,p_boca):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_boca = face[p_boca,:]

        mar = (np.linalg.norm(face_boca[0]-face_boca[1])+np.linalg.norm(face_boca[2]-face_boca[3])+np.linalg.norm(face_boca[4]-face_boca[5]))/(2*(np.linalg.norm(face_boca[6]-face_boca[7])))
    except:
        mar = 0.0

    return mar

ear_limiar = 0.3
mar_limiar = 0.1
mar_bocejo = 0.4
piscadas_limiar = 5
t_bocejo = 1.0
alerta_bocejo = 3.0
dormindo = 0
bocejando = 0
bocejo_contado = False
contagem_bocejos = 0
t_boca = 0.0
t_ultimo_bocejo = None
contagem_piscadas = 0
c_tempo = 0
contagem_temporaria = 0
contagem_lista = []

t_piscadas = time.time()
carimbo = 0

cap = cv2.VideoCapture(0)

opcoes = mp_vision.FaceLandmarkerOptions(
    base_options=mp_python.BaseOptions(model_asset_path=modelo),
    running_mode=mp_vision.RunningMode.VIDEO,
    num_faces=1,
    min_face_detection_confidence=0.5,
    min_tracking_confidence=0.5)

with mp_vision.FaceLandmarker.create_from_options(opcoes) as facemesh:
    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            print('Ignorando o frame vazio da câmera.')
            continue
        comprimento, largura, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imagem_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        carimbo = max(int(time.time()*1000), carimbo+1)
        saida_facemesh = facemesh.detect_for_video(imagem_mp, carimbo)

        try:
            for face in saida_facemesh.face_landmarks:
                mp_drawing.draw_landmarks(frame, face, mp_vision.FaceLandmarksConnections.FACE_LANDMARKS_CONTOURS,
                    landmark_drawing_spec = mp_drawing.DrawingSpec(color=(255,102,102),thickness=1,circle_radius=1),
                    connection_drawing_spec = mp_drawing.DrawingSpec(color=(102,204,0),thickness=1,circle_radius=1))
                for id_coord, coord_xyz in enumerate(face):
                    if id_coord in p_olhos:
                       coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x,coord_xyz.y, largura, comprimento)
                       cv2.circle(frame, coord_cv, 2, (255,0,0), -1)
                    if id_coord in p_boca:
                       coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x,coord_xyz.y, largura, comprimento)
                       cv2.circle(frame, coord_cv, 2, (255,0,0), -1)

                ear = calculo_ear(face,p_olho_dir, p_olho_esq)
                mar = calculo_mar(face,p_boca)

                if ear < ear_limiar and mar < mar_limiar:
                    t_inicial = time.time() if dormindo == 0 else t_inicial
                    contagem_piscadas = contagem_piscadas+1 if dormindo == 0 else contagem_piscadas
                    dormindo = 1
                if (dormindo == 1 and ear >= ear_limiar) or (ear <= ear_limiar and mar>= mar_limiar):
                    dormindo = 0
                t_final = time.time()
                tempo_decorrido = t_final - t_piscadas

                if tempo_decorrido >= (c_tempo+1):
                    c_tempo = tempo_decorrido
                    piscadas_ps = contagem_piscadas-contagem_temporaria
                    contagem_temporaria = contagem_piscadas
                    contagem_lista.append(piscadas_ps)
                    contagem_lista = contagem_lista if (len(contagem_lista)<=60) else contagem_lista[-60:]
                piscadas_pm = sum(contagem_lista)
                janela_cheia = len(contagem_lista) >= 60

                tempo = (t_final-t_inicial) if dormindo == 1 else 0.0

                if mar >= mar_bocejo:
                    t_boca = t_final if bocejando == 0 else t_boca
                    bocejando = 1
                else:
                    bocejando = 0
                    bocejo_contado = False

                if bocejando == 1 and (t_final-t_boca) >= t_bocejo:
                    t_ultimo_bocejo = t_final
                    if not bocejo_contado:
                        contagem_bocejos = contagem_bocejos+1
                        bocejo_contado = True

                bocejo_recente = t_ultimo_bocejo is not None and (t_final-t_ultimo_bocejo) <= alerta_bocejo
                poucas_piscadas = janela_cheia and piscadas_pm < piscadas_limiar
                com_sonolencia = poucas_piscadas or tempo>=1.5 or bocejo_recente
                cor_caixa = (0, 0, 255) if com_sonolencia else (109, 233, 219)
                cor_texto = (255, 255, 255) if com_sonolencia else (58, 58, 55)

                cv2.rectangle(frame, (200, 355), (450, 395), (40, 40, 40), -1)
                cv2.putText(frame, f"MAR {mar:.2f}  PISC {piscadas_pm}/min{'' if janela_cheia else '?'}  BOC {contagem_bocejos}", (210, 383),
                                        cv2.FONT_HERSHEY_DUPLEX,
                                        0.6, (255, 255, 255), 1)

                cv2.rectangle(frame, (200, 400), (450, 440), cor_caixa, -1)
                cv2.putText(frame, f"{'COM SONOLENCIA' if com_sonolencia else 'SEM SONOLENCIA'}", (210, 430),
                                        cv2.FONT_HERSHEY_DUPLEX,
                                        0.85, cor_texto, 1)

        except:
            pass

        cv2.imshow('Camera',frame)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
cap.release()
cv2.destroyAllWindows()