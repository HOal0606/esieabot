
import discord
import threading
import pigpio
import atexit
import time
import socket
# from esieabot-webcamera import StreamingOutput

TOKEN = "MTAyNzkwNjkyNzcwOTE0NzIxOA.GjFUzw.XPEJZD42EtMxe9Rku5lGmr2JVa5SUtTS9D2Dzo"


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

client_user = "legentil#0432"

pass_tour = 0
adrIp = str(socket.gethostbyname(socket.gethostname()))

pi = pigpio.pi()
if not pi.connected:
    print("Error, can't connect to pigpiod service")
    exit()

atexit.register(pi.stop)

# affectation des constante pour les pins
pin_enable_gauche = 24
pin_enable_droite = 4
pin_reculer_gauche = 25
pin_reculer_droite = 17
pin_avancer_gauche = 23
pin_avancer_droite = 22
pin_servo_pitch = 18
current_pitch = 1200

pi.set_mode(pin_enable_gauche, pigpio.OUTPUT)
pi.set_mode(pin_enable_droite, pigpio.OUTPUT)
pi.set_mode(pin_avancer_gauche, pigpio.OUTPUT)
pi.set_mode(pin_avancer_droite, pigpio.OUTPUT)
pi.set_mode(pin_reculer_gauche, pigpio.OUTPUT)
pi.set_mode(pin_reculer_droite, pigpio.OUTPUT)

pi.set_mode(pin_servo_pitch, pigpio.OUTPUT)
pi.set_PWM_frequency(pin_servo_pitch, 50)
pi.set_servo_pulsewidth(pin_servo_pitch, current_pitch)

pi.set_PWM_frequency(pin_avancer_gauche, 50)
pi.set_PWM_dutycycle(pin_avancer_gauche, 0)
pi.set_PWM_frequency(pin_avancer_droite, 50)
pi.set_PWM_dutycycle(pin_avancer_droite, 0)
pi.set_PWM_frequency(pin_reculer_gauche, 50)
pi.set_PWM_dutycycle(pin_reculer_gauche, 0)
pi.set_PWM_frequency(pin_reculer_droite, 50)
pi.set_PWM_dutycycle(pin_reculer_droite, 0)

pi.write(pin_enable_droite, pigpio.HIGH)
pi.write(pin_enable_gauche, pigpio.HIGH)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    global pass_tour

    if pass_tour == 0:
        pass_tour = 1
        await message.channel.send("================")
        await message.channel.send(f"{message.author}")
        await message.channel.send(f"{message.content}")        
        await message.channel.send(adrIp)
        await message.channel.send("- ss : arrêt robot")
        await message.channel.send("- les xxx = vitesse du robot")
        await message.channel.send("- ffxxx : avance robot tout droit")        
        await message.channel.send("- frxxx : robot tourne à droit")      
        await message.channel.send("- flxxx : robot tourne à gauche")      
        await message.channel.send("- bbxxx : robot recule")
        await message.channel.send("xxx = vitesse du robot de 0 à 999")
        
    if message.content.startswith("help"):
        pass_tour = 1
        await message.channel.send("================")
        await message.channel.send("================")
        await message.channel.send(adrIp)
        await message.channel.send("les commandes du robot sont : ")
        await message.channel.send("- ss : arrêt robot")
        await message.channel.send("- les xxx = vitesse du robot")
        await message.channel.send("- ffxxx : avance robot tout droit")        
        await message.channel.send("- frxxx : robot tourne à droit")      
        await message.channel.send("- flxxx : robot tourne à gauche")      
        await message.channel.send("- bbxxx : robot recule")
        await message.channel.send("xxx = vitesse du robot de 0 à 999")

    if (message.author == client_user and pass_tour == 0):  # client.user:
        pass_tour = 1
        await message.channel.send("================")
        await message.channel.send(f"{message.author}")
        await message.channel.send(f"{message.content}")        
        await message.channel.send(adrIp)
        await message.channel.send("- ss : arrêt robot")
        await message.channel.send("- les xxx = vitesse du robot")
        await message.channel.send("- ffxxx : avance robot tout droit")        
        await message.channel.send("- frxxx : robot tourne à droit")      
        await message.channel.send("- flxxx : robot tourne à gauche")      
        await message.channel.send("- bbxxx : robot recule")
        await message.channel.send("xxx = vitesse du robot de 0 à 999") 
        
    # stop stop ==> arrêt robot
    if message.content.startswith("ss"):
        pass_tour = 1
        pi.set_PWM_dutycycle(pin_avancer_gauche, 0)
        pi.set_PWM_dutycycle(pin_avancer_droite, 0)
        pi.set_PWM_dutycycle(pin_reculer_gauche, 0)
        pi.set_PWM_dutycycle(pin_reculer_droite, 0)
        await message.channel.send("fin for stop ")        
        
    # ff = front front ==> avance tout droit
    if message.content.startswith("ff"): 
        pass_tour = 1
        cmd = message.content
        
        cmdInt = abs(int(cmd[2:5]))
        if cmdInt > 255 : 
            cmdInt = 255
        if cmdInt < 50 : 
            cmdInt = 50

        pi.set_PWM_dutycycle(pin_avancer_gauche, cmdInt)
        pi.set_PWM_dutycycle(pin_avancer_droite, cmdInt)
        pi.set_PWM_dutycycle(pin_reculer_gauche, 0)
        pi.set_PWM_dutycycle(pin_reculer_droite, 0)

        time.sleep(1)
        pi.set_PWM_dutycycle(pin_avancer_gauche, 0)
        pi.set_PWM_dutycycle(pin_avancer_droite, 0)
        pi.set_PWM_dutycycle(pin_reculer_gauche, 0)
        pi.set_PWM_dutycycle(pin_reculer_droite, 0)
        await message.channel.send("fin for front front ")
        
        
    # fr = front right ==> tourne à droite    
    if message.content.startswith("fr"):
        pass_tour = 1
        cmd = message.content
        cmdInt = abs(int(cmd[2:5]))
        if cmdInt > 255 : 
            cmdInt = 255
        if cmdInt < 50 : 
            cmdInt = 50

        pi.set_PWM_dutycycle(pin_avancer_gauche, cmdInt)
        pi.set_PWM_dutycycle(pin_avancer_droite, 0)
        pi.set_PWM_dutycycle(pin_reculer_gauche, 0)
        pi.set_PWM_dutycycle(pin_reculer_droite, cmdInt)

        time.sleep(1)
        pi.set_PWM_dutycycle(pin_avancer_gauche, 0)
        pi.set_PWM_dutycycle(pin_avancer_droite, 0)
        pi.set_PWM_dutycycle(pin_reculer_gauche, 0)
        pi.set_PWM_dutycycle(pin_reculer_droite, 0)
        await message.channel.send("fin for front right ")
        
        
    # fl = front left ==> tourne à gauche    
    if message.content.startswith("fl"): 
        pass_tour = 1
        cmd = message.content
        cmdInt = abs(int(cmd[2:5]))
        if cmdInt > 255 : 
            cmdInt = 255
        if cmdInt < 50 : 
            cmdInt = 50

        pi.set_PWM_dutycycle(pin_avancer_gauche, 0) # map(0))
        pi.set_PWM_dutycycle(pin_avancer_droite, cmdInt)
        pi.set_PWM_dutycycle(pin_reculer_gauche, cmdInt)
        pi.set_PWM_dutycycle(pin_reculer_droite, 0) # map(0))

        time.sleep(1)
        pi.set_PWM_dutycycle(pin_avancer_gauche, 0)
        pi.set_PWM_dutycycle(pin_avancer_droite, 0)
        pi.set_PWM_dutycycle(pin_reculer_gauche, 0)
        pi.set_PWM_dutycycle(pin_reculer_droite, 0)
        await message.channel.send("fin for front left ")
        
        
    # bb = back back ==> reculer
    if message.content.startswith("bb"): 
        pass_tour = 1 
        cmd = message.content
        cmdInt = abs(int(cmd[2:5]))
        if cmdInt > 255 : 
            cmdInt = 255
        if cmdInt < 50 : 
            cmdInt = 50

        pi.set_PWM_dutycycle(pin_avancer_gauche, 0) # map(0))
        pi.set_PWM_dutycycle(pin_avancer_droite, 0)
        pi.set_PWM_dutycycle(pin_reculer_gauche, cmdInt)
        pi.set_PWM_dutycycle(pin_reculer_droite, cmdInt) # map(0))

        time.sleep(1)
        pi.set_PWM_dutycycle(pin_avancer_gauche, 0)
        pi.set_PWM_dutycycle(pin_avancer_droite, 0)
        pi.set_PWM_dutycycle(pin_reculer_gauche, 0)
        pi.set_PWM_dutycycle(pin_reculer_droite, 0)
        await message.channel.send("fin for back ")
        

# client.run('your token here')

client.run(TOKEN)

th_Stream = StreamingOutput()
th_Stream.start()
# client.run('1027906927709147218')

