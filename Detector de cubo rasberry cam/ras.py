import webbrowser
import cv2
import numpy as np
import kociemba
import itertools
from collections import Counter


# ------------------------
# DETECCION COLOR
# ------------------------

def detectar_color(h,s,v):
    
    # BLANCO
    if s < 50 and v > 180:
        return "W"

        # ROJO (solo extremos del HSV)
    if (h <= 7 or h >= 170) and s > 90:
        return "R"

    # NARANJA (rango más grande)
    if 8 <= h <= 35 and s > 80:
        return "O"

    # AMARILLO
    if 23 <= h <= 40 and s > 90:
        return "Y"

    # VERDE
    if 41 <= h <= 85:
        return "G"

    # AZUL
    if 90 <= h <= 130:
        return "B"

    return "?"


# ------------------------
# COLORES BGR
# ------------------------

color_bgr={
"W":(255,255,255),
"R":(0,0,255),
"O":(0,150,255),
"Y":(0,255,255),
"G":(0,255,0),
"B":(255,0,0),
"?":(50,50,50)
}

orden_colores=["W","R","O","Y","G","B"]


# ------------------------
# ROTAR CARA
# ------------------------

def rotar_cara(cara):

    r0=cara

    r1=[
    cara[6],cara[3],cara[0],
    cara[7],cara[4],cara[1],
    cara[8],cara[5],cara[2]
    ]

    r2=[
    cara[8],cara[7],cara[6],
    cara[5],cara[4],cara[3],
    cara[2],cara[1],cara[0]
    ]

    r3=[
    cara[2],cara[5],cara[8],
    cara[1],cara[4],cara[7],
    cara[0],cara[3],cara[6]
    ]

    return [r0,r1,r2,r3]


# ------------------------
# ORDENAR POR CENTROS
# ------------------------

def ordenar_por_centros(cubo):

    caras=[cubo[i*9:(i+1)*9] for i in range(6)]

    mapa={}

    for cara in caras:
        centro=cara[4]
        mapa[centro]=cara

    orden=["W","O","G","Y","B","R"]

    cubo_ordenado=[]

    for c in orden:

        if c not in mapa:
            print("Falta cara con centro:",c)
            exit()

        cubo_ordenado+=mapa[c]

    return cubo_ordenado


# ------------------------
# ORDEN SOLVER
# ------------------------

def ordenar_caras_para_solver(cubo):

    U=cubo[0:9]
    L=cubo[9:18]
    F=cubo[18:27]
    D=cubo[27:36]
    B=cubo[36:45]
    R=cubo[45:54]

    return U + R + F + D + L + B


# ------------------------
# CONVERTIR A KOCIEMBA
# ------------------------

def convertir_a_kociemba(cubo):

    centros=[
    cubo[4],
    cubo[13],
    cubo[22],
    cubo[31],
    cubo[40],
    cubo[49]
    ]

    mapa={
    centros[0]:"U",
    centros[1]:"R",
    centros[2]:"F",
    centros[3]:"D",
    centros[4]:"L",
    centros[5]:"B"
    }

    resultado=""

    for c in cubo:
        resultado+=mapa[c]

    return resultado


# ------------------------
# INSTRUCCIONES
# ------------------------

instrucciones=[
"Escanear cara BLANCA",
"Girar DERECHA -> cara NARANJA",
"Girar ABAJO -> cara VERDE",
"Girar DERECHA -> cara AMARILLA",
"Girar DERECHA -> cara AZUL",
"Girar ABAJO -> cara ROJA"
]


# ------------------------
# IMAGEN GIRO
# ------------------------

def imagen_giro(paso):

    img=np.zeros((300,400,3),dtype=np.uint8)

    texto=instrucciones[paso]

    cv2.putText(img,texto,(20,80),
    cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

    if "DERECHA" in texto:
        cv2.arrowedLine(img,(120,200),(280,200),(0,255,0),8)

    if "ARRIBA" in texto:
        cv2.arrowedLine(img,(200,240),(200,100),(0,255,0),8)

    if "ABAJO" in texto:
        cv2.arrowedLine(img,(200,100),(200,240),(0,255,0),8)

    return img


# ------------------------
# DIBUJAR CARA
# ------------------------

def dibujar_cara(colores):

    img=np.zeros((400,300,3),dtype=np.uint8)

    size=100

    for y in range(3):
        for x in range(3):

            i=y*3+x
            c=colores[i]

            cv2.rectangle(img,(x*size,y*size),(x*size+size,y*size+size),color_bgr[c],-1)
            cv2.rectangle(img,(x*size,y*size),(x*size+size,y*size+size),(0,0,0),2)

    cv2.rectangle(img,(70,330),(230,380),(200,200,200),-1)

    cv2.putText(img,"SIGUIENTE",(85,365),
    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)

    return img


# ------------------------
# VARIABLES
# ------------------------

cara_actual=0
cubo=[]

frames_estables=0
ultimo=[]

cara_detectada=["?"]*9

# NUEVAS VARIABLES
pausa=False
frame_congelado=None

# ------------------------
# CLICK
# ------------------------

def click(event,x,y,flags,param):

    global cara_detectada

    if event==cv2.EVENT_LBUTTONDOWN:

        size=100

        if y<300:

            cx=x//size
            cy=y//size
            i=cy*3+cx

            c=cara_detectada[i]

            idx=orden_colores.index(c) if c in orden_colores else 0
            idx=(idx+1)%6

            cara_detectada[i]=orden_colores[idx]

        elif 70<x<230 and 330<y<380:
            confirmar_cara()


def confirmar_cara():

    global cara_actual,cubo,cara_detectada

    if "?" in cara_detectada:
        print("Hay colores sin detectar")
        return

    cubo.extend(cara_detectada)

    print("Cara guardada:",cara_detectada)

    cara_actual+=1

    cara_detectada=["?"]*9


# ------------------------
# CAMARA
# ------------------------

# ------------------------
# CAMARA - Raspberry Pi 5 oficial
# ------------------------

from picamera2 import Picamera2

picam2 = Picamera2()

# Configuración de resolución y preview
config = picam2.create_preview_configuration(
    main={"size": (1280,720)}
)
picam2.configure(config)
picam2.start()


# ------------------------
# ESCANEO
# ------------------------

while True:
    
    if cara_actual==6:
        break

    if not pausa:

        frame = picam2.capture_array()
        ret = True  # siempre True, ya que capture_array() devuelve la imagen directamente

        if not ret:
            print("Error leyendo camara")
            break

        frame=cv2.GaussianBlur(frame,(5,5),0)
        frame=cv2.bilateralFilter(frame,9,75,75)

        frame=cv2.flip(frame,1)

        frame=cv2.convertScaleAbs(frame, alpha=1.1, beta=-10)

        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        size=80
        startX=200
        startY=100

        colores=[]

        for y in range(3):
            for x in range(3):

                px=startX+x*size
                py=startY+y*size

                cv2.rectangle(frame,(px,py),(px+size,py+size),(255,255,255),2)

                roi=hsv[py+20:py+60,px+20:px+60]

                h=np.mean(roi[:,:,0])
                s=np.mean(roi[:,:,1])
                v=np.mean(roi[:,:,2])

                color_detectado=detectar_color(h,s,v)

                colores.append(color_detectado)

                cv2.putText(frame,color_detectado,(px+25,py+50),
                cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

        if colores==ultimo:
            frames_estables+=1
        else:
            frames_estables=0

        ultimo=colores

        # SI DETECTA CARA ESTABLE -> PAUSA
        if frames_estables>20:

            cara_detectada=colores.copy()

            # MODO ESPEJO
            cara_detectada=[
            cara_detectada[2],cara_detectada[1],cara_detectada[0],
            cara_detectada[5],cara_detectada[4],cara_detectada[3],
            cara_detectada[8],cara_detectada[7],cara_detectada[6]
            ]

            frame_congelado=frame.copy()

            pausa=True
            frames_estables=0

    else:

        frame=frame_congelado

        cv2.putText(frame,"PAUSA - ENTER para continuar",(40,50),
        cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),2)

    cv2.imshow("Camara",frame)

    giro=imagen_giro(cara_actual)
    cv2.imshow("Movimiento",giro)

    cara_img=dibujar_cara(cara_detectada)
    cv2.imshow("Caras",cara_img)
    cv2.setMouseCallback("Caras", click)

    key=cv2.waitKey(1)

    if key==27:
        break

    if key==13:   # ENTER
        pausa=False


# ------------------------
# VERIFICAR CUBO
# ------------------------

print("\nCaras detectadas:")

for i in range(6):
    print(cubo[i*9:(i+1)*9])

print("\nConteo colores:",Counter(cubo))


if len(cubo)!=54:
    print("Error: el cubo no tiene 54 stickers")
    exit()


# ordenar por centros
cubo=ordenar_por_centros(cubo)


# ------------------------
# BUSCAR ROTACION VALIDA
# ------------------------

caras=[cubo[i*9:(i+1)*9] for i in range(6)]

rotaciones=[rotar_cara(c) for c in caras]

encontrado=False

for combinacion in itertools.product(range(4), repeat=6):

    cubo_prueba=[]

    for i,r in enumerate(combinacion):
        cubo_prueba+=rotaciones[i][r]

    cubo_solver=ordenar_caras_para_solver(cubo_prueba)

    cube_string=convertir_a_kociemba(cubo_solver)

    try:

        solucion=kociemba.solve(cube_string,max_depth=20)

        encontrado=True
        break

    except:
        continue


if not encontrado:
    print("Cubo invalido")
    exit()


pasos=solucion.split()

print("\nPasos:",len(pasos))
print("Solucion:",solucion)


# ------------------------
# ABRIR VISOR 3D
# ------------------------

def invertir_mov(m):

    if "'" in m:
        return m.replace("'","")

    if "2" in m:
        return m

    return m+"'"


scramble=" ".join([invertir_mov(m) for m in pasos[::-1]])

url="https://alpha.twizzle.net/edit/?puzzle=3x3x3&alg="+scramble.replace(" ","%20")

print("\nAbriendo simulador 3D...")

webbrowser.open(url)