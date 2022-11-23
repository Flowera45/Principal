#! /usr/bin/env python
import os, random, sys, math, pygame
from pygame.locals import *
from configuracion import *
from extras import *
from button import *
from pygame import mixer
from funcionesVACIAS import *

pygame.init()
pygame.font.init()
mixer.init()
clock = pygame.time.Clock()
clock.tick(60)

sonido= True
musica= True
fullscreen= False
contrarreloj = False

screen= pygame.display.set_mode((ANCHO, ALTO))

#Carga de recursos
BG_menu = pygame.image.load("recursos/Background.png")
BG_play = pygame.image.load("recursos/BG play.png")
BG_play_cuidado = pygame.image.load("recursos/BG play cuidado.png")
BG_play_peligro = pygame.image.load("recursos/BG play peligro.png")
BG_pausa = pygame.image.load("recursos/BG pausa.png")
BG_alt = pygame.image.load("recursos/BG Alt.png")

sonidoError = pygame.mixer.Sound("recursos/sonidoIncorrecto.mp3")
sonidoCorrecto = pygame.mixer.Sound("recursos/sonidoCorrecto.wav")
sonidoNoesta = pygame.mixer.Sound('recursos/try_again.wav')

mixer.music.load('recursos/BGmusic.mp3')
musicaMenu = pygame.mixer.Sound('recursos/mainMenu.mp3')
musicaPlay = pygame.mixer.Sound('recursos/BGmusic.mp3')
channel1 = pygame.mixer.Channel(0)
channelMusicPlay = pygame.mixer.Channel(1)
channelMusicMenu = pygame.mixer.Channel(2)

gameLogo = pygame.image.load("recursos/Menu Logo.png")
gameLogo = pygame.transform.scale(gameLogo, (930, 600))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("recursos/Montserrat-Medium.ttf", size)


def play(screen, contrarreloj):

        pygame.time.set_timer(pygame.USEREVENT, 1000)

        #Centrar la ventana y despues inicializar pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"

        #carga los recursos

        defaultFont= pygame.font.Font('recursos/Montserrat-Medium.ttf', TAMANNO_LETRA)
        defaultFontGrande= pygame.font.Font('recursos/Montserrat-Medium.ttf', TAMANNO_LETRA_GRANDE)
        defaultFontBold= pygame.font.Font('recursos/Montserrat-Bold.ttf', TAMANNO_LETRA_GRANDE)


        #Preparar la ventana
        pygame.display.set_caption("WORDLEN'T")

        #tiempo total del juego
        gameClock = pygame.time.Clock()
        totaltime = 0
        if contrarreloj:
            segundos = TIEMPO_CONTRARELOJ
        else:
            segundos = TIEMPO_MAX
        fps = FPS_inicial

        #Datos
        puntos = 0
        palabraUsuario = ""
        aciertos = []
        listaDePalabrasUsuario = []
        incorrectasletras = []
        activo=True
        gano = False
        termino=False
        intentos = 5
        error=False
        premio=0
        palabraCorrecta=nuevaPalabra(aciertos,contrarreloj) #elige una palabra al azar
        listaPalabrasDiccionario=lectura(aciertos,2,contrarreloj,len(palabraCorrecta))# lista de palabras aceptadas
        sonido = True
        pausa=False



        print(palabraCorrecta)


        #dibuja la pantalla
        dibujar(screen, listaDePalabrasUsuario, palabraUsuario, puntos,segundos, intentos,palabraCorrecta,termino,listaPalabrasDiccionario,error,aciertos,incorrectasletras)

        while not termino:

        # 1 frame cada 1/fps segundos
            gameClock.tick(fps)
            totaltime += gameClock.get_time()

            if True:
            	fps = 3

            #Buscar la tecla apretada del modulo de eventos de pygame
            for e in pygame.event.get():

                #QUIT es apretar la X en la ventana
                if e.type == QUIT:
                    pygame.quit()
                    return()
                if activo:
                    if e.type == pygame.USEREVENT:

                            segundos -= 1

                #Ver si fue apretada alguna tecla

                if e.type == KEYDOWN:
                    if activo:
                        error=False
                        letra = dameLetraApretada(e.key)
                        palabraUsuario += letra #es la palabra que escribe el usuario
                        if e.key == K_BACKSPACE:
                                palabraUsuario = palabraUsuario[0:len(palabraUsuario)-1]

                #Pausa------------------------------------------------------------------------------------------------------

                    if e.key == K_ESCAPE:
                        if activo:
                            activo = False
                            pausa = True
                        else:
                            activo = True


                    while pausa:

                        screen.blit(BG_alt, (0, 0))

                        PAUSA_MOUSE_POS = pygame.mouse.get_pos()

                        PAUSA_TEXT = get_font(75).render("PAUSA", True, "White")

                        PAUSA_RECT = PAUSA_TEXT.get_rect(center=(640, 150))

                        REANUDAR_BUTTON = Button(image=pygame.image.load("recursos/On Rect.png"), pos=(640, 330),
                                            text_input="CONTINUAR", font=get_font(75), base_color="White", hovering_color="Black")
                        PAUSA_QUIT_BUTTON = Button(image=pygame.image.load("recursos/Off Rect.png"), pos=(640, 520),
                                            text_input="MENÚ", font=get_font(75), base_color="White", hovering_color="Black")

                        screen.blit(PAUSA_TEXT, PAUSA_RECT)

                        for button in [REANUDAR_BUTTON, PAUSA_QUIT_BUTTON]:
                            button.changeColor(PAUSA_MOUSE_POS)
                            button.update(screen)

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if REANUDAR_BUTTON.checkForInput(PAUSA_MOUSE_POS):
                                    activo = True
                                    pausa = False
                                if PAUSA_QUIT_BUTTON.checkForInput(PAUSA_MOUSE_POS):
                                    main(screen)

                        pygame.display.update()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

                    if e.key == K_RETURN:

                        if activo:

                            if len(palabraUsuario)!=len(palabraCorrecta): #Controla el largo de la palabra
                                pygame.mixer.Channel(0).play(sonidoNoesta)
                                error=True


                            elif palabraUsuario not in listaPalabrasDiccionario: #controla que la palabra este en el diccionario
                                pygame.mixer.Channel(0).play(sonidoNoesta)
                                error=True


                            #Controla si la palabra arriesgada ya la ingresó anteriormente
                            elif palabraUsuario in listaDePalabrasUsuario:
                                pygame.mixer.Channel(0).play(sonidoNoesta)
                                error = True

                            else:
                                    #controla si la palabra es correcta
                                gano = revision(palabraCorrecta, palabraUsuario)
                                    #acumula las letras incorrectas
                                incorrectasletras+=letrasincorrectas(palabraUsuario,palabraCorrecta)

                                     #guarda la palabra arriesgada
                                if palabraUsuario in listaPalabrasDiccionario:
                                    listaDePalabrasUsuario.append(palabraUsuario)

                                if gano:
                                    pygame.mixer.Channel(0).play(sonidoCorrecto)
                                    puntos+=calculoPuntos(intentos,aciertos,contrarreloj)
                                    aciertos.append(palabraUsuario)
                                    if len(aciertos) != PALABRAS_TOTALES:
                                        palabraCorrecta = nuevaPalabra(aciertos,contrarreloj)
                                        listaPalabrasDiccionario=lectura(aciertos,2,contrarreloj,len(palabraCorrecta))
                                        palabraUsuario = ""
                                        listaDePalabrasUsuario = []
                                        incorrectasletras=[]
                                        intentos=5
                                        if not contrarreloj:
                                            segundos +=30
                                        print(palabraCorrecta)

                                else:
                                    pygame.mixer.Channel(0).play(sonidoError)
                                    intentos -=1
                                    palabraUsuario = ""

            #Condicion de perder
            if not contrarreloj:
                if segundos == 0 or intentos==0 or len(aciertos)==PALABRAS_TOTALES: #avisa que el juego termino

                    termino=True
                    if  len(aciertos)==PALABRAS_TOTALES:
                         totalPuntos=puntos+segundos
                    else:
                         totalPuntos=puntos

                    listaPuntos=mejoresPuntajes(totalPuntos,contrarreloj)
                    screen.fill(COLOR_FONDO)
                    finDeJuego(screen,termino,aciertos,listaPuntos,puntos,segundos,totalPuntos,contrarreloj)
                    pygame.display.flip()

            elif segundos == 0:
                termino=True
                totalPuntos=puntos+(len(aciertos)*5)
                listaPuntos=mejoresPuntajes(totalPuntos,contrarreloj)
                screen.fill(COLOR_FONDO)
                finDeJuego(screen,termino,aciertos,listaPuntos,puntos,segundos,totalPuntos,contrarreloj)
                pygame.display.flip()



            if segundos>=15 and segundos<=40:
                screen.blit(BG_play_cuidado, (0, 0))
            elif segundos<15:
                screen.blit(BG_play_peligro, (0, 0))
            else:
                screen.blit(BG_play, (0, 0))

            dibujar(screen, listaDePalabrasUsuario, palabraUsuario, puntos,segundos, intentos,palabraCorrecta,termino,listaPalabrasDiccionario,error,aciertos,incorrectasletras)
            pygame.display.flip()



        print(gameClock)

        while 1:
            #Esperar el QUIT del usuario
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def options(screen, sonido, musica, fullscreen):

    sonido= True
    musica= True
    fullscreen= False

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG_alt, (0, 0))

        OPTIONS_TEXT = get_font(75).render("OPCIONES", True, "White")

        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 50))

        if sonido:
            MUTE_SOUND = Button(image=pygame.image.load("recursos/On Rect.png"), pos=(640,350), font=get_font(75), text_input="SONIDO", base_color="White", hovering_color="Black")
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        else:
            MUTE_SOUND = Button(image=pygame.image.load("recursos/Off Rect.png"), pos=(640,350), font=get_font(75), text_input="SONIDO", base_color="White", hovering_color="Black")
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        if musica:
            MUTE_MUSIC = Button(image=pygame.image.load("recursos/On Rect.png"), pos=(640,490), font=get_font(75), text_input="MUSICA", base_color="White", hovering_color="Black")
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        else:
            MUTE_MUSIC = Button(image=pygame.image.load("recursos/Off Rect.png"), pos=(640,490), font=get_font(75), text_input="MUSICA", base_color="White", hovering_color="Black")
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        if fullscreen:
            FULLSCREEN_BUTTON = Button(image=pygame.image.load("recursos/On Rect.png"), pos=(640,210), font=get_font(75), text_input="FULLSCREEN", base_color="White", hovering_color="Black")
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        else:
            FULLSCREEN_BUTTON = Button(image=pygame.image.load("recursos/Off Rect.png"), pos=(640,210), font=get_font(75), text_input="FULLSCREEN", base_color="White", hovering_color="Black")
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=pygame.image.load("recursos/Options Rect.png"), pos=(640, 650),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Black")

        for button in [OPTIONS_BACK, MUTE_SOUND, MUTE_MUSIC, FULLSCREEN_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main(screen)

                if MUTE_SOUND.checkForInput(OPTIONS_MOUSE_POS):
                    if sonido:
                        pygame.mixer.Channel(0).set_volume(0.0)
                        sonido = False
                    else:
                        pygame.mixer.Channel(0).set_volume(1.0)
                        pygame.mixer.Channel(0).play(sonidoCorrecto)
                        sonido = True
                    print(sonido)

                if MUTE_MUSIC.checkForInput(OPTIONS_MOUSE_POS):
                    if musica:
                        pygame.mixer.Channel(1).set_volume(0.0)
                        pygame.mixer.Channel(2).set_volume(0.0)
                        musica = False
                    else:
                        pygame.mixer.Channel(1).set_volume(1.0)
                        pygame.mixer.Channel(2).set_volume(1.0)
                        musica = True
                    print(musica)

                if FULLSCREEN_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    if fullscreen:
                        pygame.display.toggle_fullscreen()
                        fullscreen= False
                    else:
                        pygame.display.toggle_fullscreen()
                        fullscreen= True

        pygame.display.update()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def finDeJuego(screen, termino, aciertos,listaPuntos,puntos,segundos,totalPuntos,contrarreloj):

    screen.blit(BG_pausa, (0, 0))

    if len(aciertos)==PALABRAS_TOTALES:
        pygame.mixer.Channel(0).play(sonidoGano)
    else:
        pygame.mixer.Channel(0).play(sonidoPerdio)

    while True:

        #BOTONES

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("recursos/Options Rect.png"), pos=(ANCHO-ANCHO/4, 300),
                        text_input="REINTENTAR", font=get_font(55), base_color="White", hovering_color="Black")
        QUIT_BUTTON = Button(image=pygame.image.load("recursos/Quit Rect.png"), pos=(ANCHO-ANCHO/4, 450),
                            text_input="SALIR", font=get_font(55), base_color="White", hovering_color="Black")

        orden=["1º","2º","3º","4º","5º"]



        #DATOS DE EL ULTIMO JUEGO

        if contrarreloj:
            mensaje=letraFinjuego.render("¡FIN DEL JUEGO!",1,COLOR_JUEGO)
            bonus=defaultFont.render("BONUS:",1,COLOR_VERDE)
            valorbonus=defaultFont.render(str(len(aciertos)*5),1,COLOR_VERDE)

        elif len(aciertos)==PALABRAS_TOTALES:
            mensaje=letraFinjuego.render("¡GANASTE!",1,COLOR_GANASTE)
            bonus=defaultFont.render("BONUS:",1,COLOR_VERDE)
            valorbonus=defaultFont.render(str(segundos),1,COLOR_VERDE)
        else:
            mensaje=letraFinjuego.render("¡PERDISTE!",1,COLOR_PERDISTE)
            bonus=defaultFont.render("BONUS:",1,COLOR_ROJO)
            valorbonus=defaultFont.render(str(0),1,COLOR_ROJO)

        #UBICACION MENSAJE
        centro_x=(ANCHO//2)-(mensaje.get_width()//2)
        centro_y=(ALTO//12)-(mensaje.get_height()//12)
        screen.blit(mensaje,[centro_x,centro_y])

        # UBICACION BONUS

        centro_x=(ANCHO//5)-(bonus.get_width()//5)
        centro_y= (ALTO//3.1)
        screen.blit(bonus,[centro_x-0.9,centro_y])

        # UBICACION VALOR BONUS
        centro_x=(ANCHO//2.3)-(valorbonus.get_width()//2.3)
        centro_y= (ALTO//3.1)
        screen.blit(valorbonus,[centro_x-0.9,centro_y])

         #PUNTOS
        mensaje=defaultFont.render("PUNTOS:",1,COLOR_LETRAS)
        centro_x=(ANCHO//5)-(mensaje.get_width()//5)
        centro_y= (ALTO//4)
        screen.blit(mensaje,[centro_x,centro_y])

        mensaje=defaultFont.render(str(puntos),1,COLOR_LETRAS)
        centro_x=(ANCHO//2.3)-(mensaje.get_width()//2.3)
        centro_y= (ALTO//4)
        screen.blit(mensaje,[centro_x,centro_y])


         #TOTALPUNTO
        mensaje=defaultFont.render("TOTAL:",1,COLOR_BLANCO)
        centro_x=(ANCHO//5)-(mensaje.get_width()//5)
        centro_y= (ALTO//2.5)
        screen.blit(mensaje,[centro_x,centro_y])

        mensaje=defaultFont.render(str(totalPuntos),1,COLOR_BLANCO)
        centro_x=(ANCHO//2.3)-(mensaje.get_width()//2.3)
        centro_y= (ALTO//2.5)
        screen.blit(mensaje,[centro_x,centro_y])

        #DATOS DE LOS MEJORES 5 PUNTAJES

        mensaje=letraPuntos.render("RECORDS",1,COLOR_LETRAS)
        centro_x=(ANCHO//3.5)-(mensaje.get_width()//3.5)
        centro_y= (ALTO//2.1)
        screen.blit(mensaje,[centro_x,centro_y])

        a=0
        y=0
        for i in range (0,5):

               #MUSTRA SI EL ULTIMO PUNTAJE ESTA DENTRO DE LOS 5 MEJORES

            if listaPuntos[i]==totalPuntos and listaPuntos[i]!=0 and a==0:
                mensaje=letraPuntos.render("~·~"+orden[i]+"   "+ str(listaPuntos[i])+"~·~",1,COLOR_VERDE)
                centro_x=(ANCHO//4)-(mensaje.get_width()//4)
                centro_y= (ALTO//1.8+ y)
                screen.blit(mensaje,[centro_x,centro_y])
                y += TAMANNO_PUNTO
                a+=1

            else:

                mensaje=letraPuntos.render(orden[i]+"   "+ str(listaPuntos[i]),1,COLOR_LETRAS)
                centro_x=(ANCHO//3.5)-(mensaje.get_width()//3.5)
                centro_y=( ALTO//1.8 + y)
                screen.blit(mensaje,[centro_x,centro_y])
                y += TAMANNO_PUNTO

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        segundos=TIEMPO_MAX
                        play(screen,contrarreloj)

                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        main(screen)

        pygame.display.flip()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
def modoDeJuego():

    pygame.display.set_caption("MODO DE JUEGO")

    while True:
        screen.blit(BG_menu, (0, 0))

        MODE_MOUSE_POS = pygame.mouse.get_pos()

        MODE_TEXT = get_font(95).render("MODO DE JUEGO", True, "White")

        MODE_RECT = MODE_TEXT.get_rect(center=(640, 150))

        NORMAL_BUTTON = Button(image=pygame.image.load("recursos/Options Rect.png"), pos=(640, 320),
                            text_input="NORMAL", font=get_font(75), base_color="Black", hovering_color="White")

        TIMED_BUTTON = Button(image=pygame.image.load("recursos/On Rect.png"), pos=(640, 470),
                            text_input="CONTRARRELOJ", font=get_font(60), base_color="Black", hovering_color="White")

        VOLVER_BUTTON = Button(image=pygame.image.load("recursos/Off Rect.png"), pos=(640, 630),
                            text_input="Volver", font=get_font(75), base_color="Black", hovering_color="White")

        screen.blit(MODE_TEXT, MODE_RECT)

        for button in [TIMED_BUTTON, NORMAL_BUTTON, VOLVER_BUTTON]:
            button.changeColor(MODE_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TIMED_BUTTON.checkForInput(MODE_MOUSE_POS):
                    contrarreloj = True
                    play(screen, contrarreloj)
                if NORMAL_BUTTON.checkForInput(MODE_MOUSE_POS):
                    contrarreloj = False
                    play(screen, contrarreloj)
                if VOLVER_BUTTON.checkForInput(MODE_MOUSE_POS):
                    main(screen)

        pygame.display.update()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#MENU PRINCIPAL

def main(screen):

    pygame.display.set_caption("Menu")
    pygame.mixer.Channel(2).play(musicaPlay, loops=-1)

    while True:
        screen.blit(BG_menu, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = gameLogo
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 150))

        PLAY_BUTTON = Button(image=pygame.image.load("recursos/Play Rect.png"), pos=(640, 320),
                            text_input="JUGAR", font=get_font(75), base_color="White", hovering_color="Black")
        OPTIONS_BUTTON = Button(image=pygame.image.load("recursos/Options Rect.png"), pos=(640, 470),
                            text_input="OPCIONES", font=get_font(75), base_color="White", hovering_color="Black")
        QUIT_BUTTON = Button(image=pygame.image.load("recursos/Quit Rect.png"), pos=(640, 620),
                            text_input="SALIR", font=get_font(75), base_color="White", hovering_color="Black")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    modoDeJuego()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options(screen, sonido, musica, fullscreen)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main(screen)

