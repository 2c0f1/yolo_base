import cv2,subprocess,time,os,re,sys#,multiprocessing
import tkinter as tk
from tkinter import *


#detecção de dispositivo
devs = os.listdir('/dev')
vid_indices = [int(dev[-1]) for dev in devs 
if dev.startswith('video')]
vid_indices = sorted(vid_indices)
#lipeza de numeração
clener = re.sub("[],*[\r\n]*","", str(vid_indices))
clear_number_cam = re.sub("[0-1] ","", str(clener))
clear_number_cam=[0]
#escala de resolução 
resolution_1440p=[2560,1440]#1440p
resolution_1080p=[1920,1080]#1080p
resolution_900p=[1600,900]#900p
resolution_768p=[1366,768]#768p
resolution_720p=[1280,720]#720p
resolution_600p=[1066,600]#600p
resolution_576p=[1024,576]#576p
resolution_540p=[960,540]#540p
resolution_480p=[854,480]#480p
resolution_360p=[640,360]#360p
resolution_240p=[426,240]#240p
#captura de image

resolução_inicial = resolution_360p
resolução_final = resolution_1080p
cap = cv2.VideoCapture(int(clear_number_cam[0]), cv2.CAP_V4L2)
cv2.UMat(cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV')))
cv2.UMat(cap.set(cv2.CAP_PROP_FPS, 30))
cv2.UMat(cap.set(cv2.CAP_PROP_BUFFERSIZE, -1)) #captura de video
cv2.UMat(cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolução_inicial[0])) #largura de captura
cv2.UMat(cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolução_inicial[1])) #altura de captura

img_counter = 0 #contador de imagens
ptime=0  # declaração de variavel para calculo de fps
nome = "placa de captura" #nome de janela
#reproduz o som do microfone

if 'True' in str(cap.isOpened()):
 #subprocess.call('pactl unload-module module-loopback', shell=True) #desativa o retorno de som
 #subprocess.call('pactl load-module module-loopback latency_msec=1', shell=True) #ativa o retorno de som
 while(cap.isOpened()):
    ret,frame = cap.read(0) #le a captura de video
    #calculo de fps
    ctime = time.time() 
    fps = 1//(ctime-ptime)
    ptime = ctime
    #processamento das cores do video 
    saida_video = cv2.UMat(cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA))         
    #upscale = cv2.UMat(cv2.pyrUp(saida_video))#, dstsize=(1270,720)))  
    resizer = cv2.UMat(cv2.resize(saida_video,(resolução_final[0],resolução_final[1]))) #seleção de resolução de tela final
    cv2.UMat(cv2.namedWindow(nome, cv2.WND_PROP_FULLSCREEN))
    cv2.UMat(cv2.setWindowProperty(nome,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN))    
    cv2.UMat(cv2.putText(resizer,f'fps:{int(fps)}',(10,55),cv2.FONT_HERSHEY_TRIPLEX,1,(0,160,28))) 
    #cv2.putText(resize,f'fps:{int(fps1)}',(10,30),cv2.FONT_HERSHEY_TRIPLEX,1,(0,160,28)) 
    #fps1 = cap.get(cv2.CAP_PROP_FPS)
    cv2.imshow(nome, resizer)

    
    k = cv2.waitKey(1)
    if k == 27:
     # ESC pressed
     subprocess.call('pactl unload-module module-loopback', shell=True) #desativa o retorno de som
     time.sleep(1)
     cv2.destroyAllWindows()
     break
 
    elif k%256 == 32:
     # SPACE pressed
     img_name = "opencv_frame_{}.png".format(img_counter)
     cv2.imwrite(img_name, frame)
     print("{} written!".format(img_name))
     img_counter += 1
 
if 'False' in str(cap.isOpened()):
 janela = Tk()
 janela.title("ops")
 janela.geometry('320x32')
 lbl = Label(janela, text=" erro de coneção da placa de captura")
 lbl.grid(column=1, row=0)
 
 def clicked(): #função
  #subprocess.call('pactl unload-module module-loopback', shell=True) #desativa o retorno de som
  time.sleep(0.2)
  cv2.destroyAllWindows()
  sys.exit(0)
  
 btn = Button(janela,text='fechar ', command=clicked)
 btn.grid(column=0, row=0)
 janela.mainloop()

cap.release()
cv2.destroyAllWindows()