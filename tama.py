import tkinter
import tkinter.simpledialog
import tkinter.messagebox
import tkinter.ttk as ttk
import time
import random
import _thread

#
hunger = 100
fun = 100
health = 100
day = 0
money = 0
sick = False
alive = True
meatApplied = False

#
SICK_PERCENTAGE = 10
DAY_DURATION = 5 #
TAMA_NAME = "n/a"
HUNGER_UPDATE = 400 #
FUN_UPDATE = 400
HEALTH_UPDATE = 400
MONEY_ADD = 1
HUNGER_ADD = 10
FUN_ADD = 5
HEALTH_ADD = 8
MEAT_DURATION = 5 #

#
gameStarted = False

#-------------------------------------------------------------------

def startGame(event):
    start()

#-------------------------------------------------------------------

def start():
    global gameStarted, hunger, fun, health, alive, day, money

    if gameStarted == False:
        gameStarted = True
        hunger = 100
        fun = 100
        health = 100
        day = 0
        money = 0
        sick = False
        alive = True
        startLabel.config(text="tamagotchi")
        update()

#-------------------------------------------------------------------

def update():

    updateDay()
    updateDisplay()
    updateNeeds()

#-------------------------------------------------------------------

def updateDisplay():

    global hunger, fun, health, day
    
    if hunger <= 75:
        catPic.config(image = hungryphoto)
        imageLabel.config(text="Голоден")
    elif sick == True:
        catPic.config(image = deadphoto)
        imageLabel.config(text="Заболел")
    elif fun < 80:
        catPic.config(image = sadphoto)
        imageLabel.config(text="Грустит")
    else: 
        catPic.config(image = normalphoto)
        imageLabel.config(text="")

    progressBar() #
    hungerLabel.config(text=str(hunger))
    funLabel.config(text=str(fun))
    healthLabel.config(text=str(health))

    dayLabel.config(text="День: " + str(day) + "    Деньги: " + str(money))   

    catPic.after(100, updateDisplay)

#-------------------------------------------------------------------

def updateNeeds():

    updateHunger()
    updateFun()
    updateHealth()
    updateMoney()

    isAlive()

#-------------------------------------------------------------------

def updateHunger():

    global hunger, sick

    if meatApplied == False: hunger -= 1

    if alive == True:
        hungerLabel.after(HUNGER_UPDATE, updateHunger)

#-------------------------------------------------------------------

def updateFun():

    global fun, sick

    fun -= 1

    if alive == True:
        if sick == True: #
            funLabel.after(int(FUN_UPDATE / 2), updateFun)
        else:
            funLabel.after(FUN_UPDATE, updateFun)

#-------------------------------------------------------------------

def updateHealth():

    global health, sick

    isSick()

    if sick == True:
        health -= 1

    if alive == True:
        healthLabel.after(HEALTH_UPDATE, updateHealth)

#-------------------------------------------------------------------

def updateDay():

    global day

    if alive == True:
        day += 1
        dayLabel.after(DAY_DURATION * 1000, updateDay)

#-------------------------------------------------------------------

def updateMoney():

    global money

    if alive == True:
        money += MONEY_ADD
        dayLabel.after(300, updateMoney)

#-------------------------------------------------------------------

def updateLabel(turns, description):

    global day

    if alive == True:
        statusLabel.config(text=description)
        time.sleep(turns)
        statusLabel.config(text=" ")

#-------------------------------------------------------------------

def feed():

    global hunger, sick
    
    if hunger <= 88:
        if sick == True:
            hunger += HUNGER_ADD // 2
            _thread.start_new_thread(updateLabel, (3,TAMA_NAME + "Не хочет есть"))
        else:
            hunger += HUNGER_ADD
    else:
        _thread.start_new_thread(updateLabel, (3, "Не перекармливай" + TAMA_NAME))

#-------------------------------------------------------------------

def play():

    global fun, sick

    if sick == False:
        if fun <= 95:
            fun += FUN_ADD
        else:
            _thread.start_new_thread(updateLabel, (3, TAMA_NAME + "Не хочет играть"))
    else:
        _thread.start_new_thread(updateLabel, (3, TAMA_NAME + "Не хочет играть когда болеет"))

#-------------------------------------------------------------------

def heal():

    global health, sick, HUNGER_UPDATE

    if sick == True:
        sick = False
        skullPhoto.config(image = skullNo)
        HUNGER_UPDATE //= 2
        if health <= 92:
            health += HEALTH_ADD
        else:
            health == 100
    else:
        _thread.start_new_thread(updateLabel, (3, TAMA_NAME + "Здороов"))

#------------------------------------------------------------------

def isSick():

    global sick, HUNGER_UPDATE

    if sick != True:
        if random.randint(1,100) <= SICK_PERCENTAGE: 
            sick = True
            skullPhoto.config(image = skull)
            HUNGER_UPDATE *= 2
            _thread.start_new_thread(updateLabel, (2, TAMA_NAME + "Заболел"))

#-------------------------------------------------------------------

def isAlive():

    global hunger, fun, health, alive

    if hunger <= 0 or fun <= 0 or health <= 0:
        catPic.config(image = deadphoto)
        _thread.start_new_thread(updateLabel, (2, TAMA_NAME + "Умер"))
        startLabel.config(text="Game Over!") 
        endGame()
        if tkinter.messagebox.askyesno("Давай ещё раз?", "Не хочешь сыграть ещё разок?"):
            start()
        return False

    if alive == True:
        hungerBar.after(100,isAlive)        
        
#-------------------------------------------------------------------

def endGame():

    global alive, gameStarted

    alive = False
    gameStarted = False

#-------------------------------------------------------------------

def progressBar():
    
    global hunger, fun, health

    hungerBar["value"] = hunger
    funBar["value"] = fun
    healthBar["value"] = health

    if alive == True:
        hungerBar.after(100,progressBar)

#-------------------------------------------------------------------

def meatFun():
    _thread.start_new_thread(meatFunction, (MEAT_DURATION,));

#-------------------------------------------------------------------

def meatFunction(delay):

    global HUNGER_UPDATE,meatApplied,money

    if money >= 15:
        if alive == True:
            btnFeed.config(state="disabled")
            money -= 15
            meatApplied = True
            
            _thread.start_new_thread(updateLabel, (3, TAMA_NAME + "Кушает"))
            time.sleep(delay)
            btnFeed.config(state="normal")
            meatApplied = False
    else:
        _thread.start_new_thread(updateLabel, (3, "У вас не достаточно денег для покупки еды"))

#-------------------------------------------------------------------

def ballFun():

    global FUN_UPDATE,money

    if money >= 50:
        FUN_UPDATE += int(FUN_UPDATE / 12)
        money -= 50
        _thread.start_new_thread(updateLabel, (3, "Улучшите ваши игрушки"))
    else:
        _thread.start_new_thread(updateLabel, (3, "У вас не достаточно денег на игрушки"))
    
#-------------------------------------------------------------------

def hospitalFun():

    global SICK_PERCENTAGE,money

    if money >= 25:
        SICK_PERCENTAGE -= 1
        money -= 25
        _thread.start_new_thread(updateLabel, (3, TAMA_NAME + "отныне будет здоровее!  "))

    else:
        _thread.start_new_thread(updateLabel, (3, "Не хватает денег на лечение!"))
#-------------------------------------------------------------------

def rules():
    tkinter.messagebox.showinfo( TAMA_NAME,
        "tamagotchi by abik" +  ", Это правила\n\n" + 
        "1. Не позволяй показателям" + TAMA_NAME + " упасть до нуля иначе, он умрёт\n" +
        "2. Если " + TAMA_NAME + " заболел, вылечи его как можно скорее! Он не будет есть и играть, пока вы не вылечите его \n" +
        "3. Не кормите" + TAMA_NAME + " Когда он сыт\n" +
        "4. Чем больше вы играете с " + TAMA_NAME + ", тем меньше удовольствия он получает. Попробуй немного изменить ситуацию " +
        "\n\nМагазин:\n"+
        "Мясо восполняет голод " + TAMA_NAME + " так что вам не нужно кормить его в течение определенного периода времени \n" + 
        "Игры снижают скорость грусти " + TAMA_NAME + "\n" + 
        "Лечение " + TAMA_NAME + "снижает процент заболеть\n")

#-------------------------------------------------------------------

#
root = tkinter.Tk()
root.title("tamagotchi by abik!")
root.geometry("500x500")
root.resizable(0,0)

#
s = ttk.Style()
s.theme_use("clam")
#
hungerBar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length="200", variable="hunger")
hungerBar.place(relx=0.75, rely=0.07, anchor="center")
funBar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length="200", variable="fun")
funBar.place(relx=0.75, rely=0.12, anchor="center")
healthBar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length="200", variable="health")
healthBar.place(relx=0.75, rely=0.17, anchor="center")
progressBar() #

#
startLabel = tkinter.Label(root, text="Tamagotchi by abik! Нажмите пробел для старта.", font=("Helvetica", 12))
startLabel.pack()
hungerLabel = tkinter.Label(root, text=str(hunger), font=("Helvetica", 12))
hungerText = tkinter.Label(root, text="Голод: ", font=("Helvetica", 12))
hungerLabel.place(relx=0.35, rely=0.07, anchor="w")
hungerText.place(relx=0.35, rely=0.07, anchor="e")
funLabel = tkinter.Label(root, text=str(fun), font=("Helvetica", 12))
funText = tkinter.Label(root, text="Радость: ", font=("Helvetica", 12))
funLabel.place(relx=0.35, rely=0.12, anchor="w")
funText.place(relx=0.35, rely=0.12, anchor="e")
healthLabel = tkinter.Label(root, text=str(health), font=("Helvetica", 12))
healthText = tkinter.Label(root, text="Здоровье: ", font=("Helvetica", 12))
healthLabel.place(relx=0.35, rely=0.17, anchor="w")
healthText.place(relx=0.35, rely=0.17, anchor="e")
dayLabel = tkinter.Label(root, text="День: " + str(day) + "    Деньги: " + str(money), font=("Helvetica", 12))
dayLabel.place(relx=0.5, rely=0.22, anchor="center")
imageLabel = tkinter.Label(root, text="", font=("Helvetica", 12))
imageLabel.place(relx=0.5, rely=0.685, anchor="center")
statusLabel = tkinter.Label(root, text="", font=("Helvetica", 12))
statusLabel.place(relx=0.5, rely=0.27, anchor="center")

#Tamagotchi's pictures
hungryphoto = tkinter.PhotoImage(file="tama/tama_hungry.png")
normalphoto = tkinter.PhotoImage(file="tama/tama_normal.png")
sadphoto = tkinter.PhotoImage(file="tama/tama_sad.png")
deadphoto = tkinter.PhotoImage(file="tama/tama_dead.png")
playingphoto = tkinter.PhotoImage(file="tama/tama_playing.png")

meat = tkinter.PhotoImage(file = "emoji/meat.png")
ball = tkinter.PhotoImage(file = "emoji/ball.png")
hospital = tkinter.PhotoImage(file = "emoji/hospital.png")
skull = tkinter.PhotoImage(file = "emoji/skull.png")
skullNo = tkinter.PhotoImage(file = "emoji/skullNo.png")

#Adds the Tamagotchi image onto the canvas
catPic = tkinter.Label(root, image=normalphoto)
catPic.place(relx=0.5, rely=0.47, anchor="center")
skullPhoto = tkinter.Label(root, image=skullNo)
skullPhoto.place(relx=0.85, rely=0.325, anchor="center")

#Buttons
btnFeed = tkinter.Button(root, text="Feed Tama", command=feed, activebackground="lightblue")
btnFeed.place(relx=0.3, rely=0.75, anchor="center") 
btnPlay = tkinter.Button(root, text="Play with Tama", command=play, activebackground="lightblue")
btnPlay.place(relx=0.5, rely=0.75, anchor="center")
btnHeal = tkinter.Button(root, text="Heal Tama", command=heal, activebackground="lightblue")
btnHeal.place(relx=0.7, rely=0.75, anchor="center")
meatButton = tkinter.Button(root, command=meatFun,  image=meat, activebackground="lightblue")
meatButton.place(relx=0.3, rely=0.9, anchor="center")
ballButton = tkinter.Button(root, command=ballFun, image=ball ,activebackground="lightblue")
ballButton.place(relx=0.5, rely=0.9, anchor="center")
hospButton = tkinter.Button(root, command=hospitalFun, image=hospital , activebackground="lightblue")
hospButton.place(relx=0.7, rely=0.9, anchor="center")

#run the "startGame" function when the space key is pressed.
root.bind("<space>", startGame)

#User inputs
TAMA_NAME = tkinter.simpledialog.askstring("Имя", "Какое имя вашего tamagotchi?", initialvalue = "Tamagotchi")
if not TAMA_NAME:
    TAMA_NAME = "Tamagotchi"
else:
    TAMA_NAME = TAMA_NAME.upper()
rules()

#start the GUI
root.mainloop()
