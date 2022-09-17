from tkinter import *
from PIL import Image,ImageTk
import speech_recognition as sr
import datetime
import pyaudio
import pyttsx3
import pywhatkit as kt
from PyDictionary import PyDictionary
from threading import Thread
import pyjokes


######## VOICE INIT ########

engine=pyttsx3.init('sapi5')
engine.setProperty("rate",145)

######## SPEAK ########

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

######## TAKING VOICE FROM THE USER ########

def record():
    r=sr.Recognizer()
    with sr.Microphone() as mic:
        print("Listeninng")
        bot_status(True)
        uservoice=r.listen(mic)
        query=""
        try:
            print("Recognizing")
            bot_status(False,True)
            query=r.recognize_google(uservoice)
            message(text=f"{query}")
        except Exception as e:
            print(e)
            message(text="Could Not Hear You. Please Try Again",bot=True)
    return query.lower()


######## CONVERTING VOICES TO STRINGS ########

def runAssitant():
    query=record()
    if "thank you" in query:
        message(text="Your most welcome",bot=True)
        speak("Your most welcome.")
        return
    else:
        command(query)
        return



######## ACTION TO BE TAKEN FOR THE COMMANDS TAKEN FROM THE USER ########
def having(text,subtext):
    for i in subtext:
        if i in text:
            return True
    return False

def command(query):


    """ Interactions : """

    if having(query,["who are you","who made you"]):
        message(text="Hii, I am a voice assistant namely D.D.X made by Biswaranjan", bot=True)
        speak("Hii, I am a voice assistant namely DDX made by Biswaranjan")
        bot_status(False,False,True)

    if having(query,["you are good","you are nice","you are awesome"]):
        message(text="Aww thank you, I appreciate that", bot=True)
        speak("Aww thank you, I appreciate that")
        bot_status(False,False,True)

    if having(query,["tell me some jokes","make me laugh"]):
        jokes=pyjokes.get_joke()
        message(text=f"{jokes}", bot=True)
        speak(f"{jokes}")
        bot_status(False,False,True)


    if having(query,["how are you"]):
        message(text="I am good. Thank You. What about You?", bot=True)
        speak("I am good. Thank You. What about you?")
        uservoice1=record()
        if having(uservoice1,["not feeling good","sad","not fine","not good"]):
            message("Dont worry, Everything will be fine soon",True)
            speak("Dont worry, Everything will be fine soon")
        else:
            message("Thats really nice. Have a great day ", True)
            speak("Thats really nice. Have a great day")
        bot_status(False, False, True)

    """ PLAYING VIDEO OR SEARCHING ON YOUTUBE """

    if having(query,["on youtube","video","play"]):
        if "play" in query:
            query=query.replace('play','')
        if "video" in query:
            query=query.replace('video','')
        if "on youtube" in query:
            query=query.replace('on youtube','')
        message(text=f"Opening Youtube and playing {query}", bot=True)
        speak(f"Hold on, Loading Youtube and playing {query}.")
        kt.playonyt(query)
        bot_status(False, False, True)

    """ SEARCHING ON GOOGLE """

    if having(query,["search","google","on google"]):
        if "search" in query:
            query=query.replace('search','')
        if "on google" in query:
            query = query.replace('on google', '')
        if "google" in query:
            query = query.replace('google', '')

        message(text=f"Searching:{query} on Google", bot=True)
        speak(f"Hold on, I am searching {query} on Google.")
        kt.search(query)
        bot_status(False, False, True)

    """ DICTIONARY USE """

    if having(query,["what is the meaning of","what is the definition of","define"]):
        if "what is the meaning of" in query:
            query=query.replace('what is the meaning of ','')
        if "what is the definition of" in query:
            query = query.replace('what is the definition of ', '')
        if "define " in query:
            query=query.replace('define','')
        message(text=f"{query.capitalize()}: It is ..", bot=True)
        speak(f"{query}: It is ")
        word=PyDictionary()
        meaning=word.meaning(f"{query}")
        count=len(meaning['Noun'])
        if count>4:
            count=4
        for i in range(count):
            message(text=f"{meaning['Noun'][i]}", bot=True)
            speak(f"{meaning['Noun'][i]}")
        bot_status(False, False, True)



########  MIC BUTTON TASK  ########

def mic():
    clearchats()
    try:
        t1=Thread(target=runAssitant)
        t1.start()
    except Exception as e:
        print(e)
        if "you are offline" in e.lower():
            Label(text="You are Off line").pack()


######## INTERACTIONS ON SCREEN ########

def message(text,bot=False):
    if bot:
        ddx = Label(chat_frm, text=f"{text}.", bg="light grey", wraplength=250, justify=LEFT,font="Calisto 10 bold",fg='black')
        ddx.pack(anchor="w", pady=2)
    else:
        usr = Label(chat_frm, text=text.capitalize(), wraplength=250, justify=LEFT, bg="black",font="Calisto 10 bold",fg='white')
        usr.pack(anchor="e", pady=2)

######## CLEARING THE CHAT SCREEN ########

def clearchats():
    for win in chat_frm.winfo_children():
        win.destroy()

######### STATUS MESSAGE ########

def bot_status(lsn=False,recgn=False,mic=False):
    if lsn:
        AI_status.config(text="Listening...",fg="red")
        return
    if recgn:
        AI_status.config(text="Recognizing...",fg="green")
        return
    if mic:
        AI_status.config(text="",bg="white")
        return



######## MAIN GUI ########

def destroyscreen():
    speak("Hii, I am DDX")
    splash.destroy()

def time():
    lvtime = datetime.datetime.now().strftime("%I:%M:%S %p")
    tm.config(text=lvtime)
    gui.after(1000,time)

def guide():
    guide = Tk()
    guide.title("D.D.X ASSISTANT GUIDEBOOK")
    wd, ht = 800, 500
    guide.geometry(f"{wd}x{ht}")
    guide.maxsize(width=wd, height=ht)
    guide.minsize(width=wd, height=ht)
    guide.configure(bg='black')

    ## TITLE ##

    page_title = Label(guide, text="VOICE COMMANDS", fg="white", bg='black', font='Calibri 28 bold')
    page_title.pack()

    ## ADDING FRAME ##

    text_frame = Frame(guide, bg='white', width=800, height=410)
    text_frame.pack()
    text_frame.pack_propagate()

    ## ADDING SCROLLBAR ##
    scl_bar = Scrollbar(text_frame, orient=VERTICAL, bg='black')
    scl_bar.pack(side=RIGHT, fill=Y)

    ## ADDING TEXT BOX TO THE WINDOW ##

    text_box = Text(text_frame, bg="black", font="Calibri 14 bold", fg='white', width=75, height=17, borderwidth=5,
                    wrap='word', yscrollcommand=scl_bar.set,relief="sunken")
    text_box.pack(fill='both')

    text_box.insert(END,open('GUIDE_BOOK', 'r').read())
    scl_bar.config(command=text_box.yview)

    ## BUTTON TO CLOSE THE WINDOW ##

    close_button = Button(guide, text='CLOSE', font='calibri 10 bold', bg='red', fg='white', command=guide.destroy)
    close_button.pack(side=BOTTOM, pady=10)

    guide.mainloop()


if __name__=="__main__":


    # SPLASH SCREEN
    splash=Tk()
    splash.title("ASSISTANT - D.D.X")
    w,h=500,600
    splash.geometry(f"{w}x{h}")
    sp_pic = Image.open("SPLASH.jpg")
    sp_pic = sp_pic.resize((w, h))
    sp_image = ImageTk.PhotoImage(sp_pic)
    bgn = Label(splash, image=sp_image)
    bgn.place(x=-2, y=0)
    splash.after(100,destroyscreen)
    splash.mainloop()




    ### MAIN WORKING INTERFACE
    gui=Tk()
    gui.title("ASSISTANT - D.D.X")
    wd,ht=800,500
    gui.geometry(f"{wd}x{ht}")
    gui.maxsize(width=wd,height=ht)
    gui.minsize(width=wd, height=ht)

    bg_pic=Image.open("img_1.png")
    bg_pic=bg_pic.resize((wd,ht))
    bgn_image=ImageTk.PhotoImage(bg_pic)
    bgn=Label(gui,image=bgn_image)
    bgn.place(x=-2,y=0)

    ### ADDING LIVE TIME AND DATE ###
    tm=Label(gui,text="",font="calibri 15 bold",fg="#004E7B",bg="white")
    tm.place(x=472.5,y=46)
    dt=datetime.datetime.now().strftime("%a, %b %d")
    dte=Label(gui,text=dt,font="calibri 10 bold",fg="#004E7B",bg="white")
    dte.place(x=492,y=67.5)
    time()

    #### GUIDE ICON ######
    gd_pic = Image.open("dark-blue-book-icon_tcm12-256223.png")
    gd_pic = gd_pic.resize((45,39))
    gd_image = ImageTk.PhotoImage(gd_pic)
    gdic=Button(gui, image=gd_image, command=guide, activebackground="white", borderwidth=0, bg="white")
    gdic.place(x=392.5,y=46.5)

    ### CHAT FRAME ###
    chat_frm = Frame(gui,bg="white",width=267.5,height=300)
    chat_frm.place(x=394,y=106)
    chat_frm.pack_propagate(0)
    message(text="Tap the Mic to Speak. To Know more, Click 'info' button on the top left-hand side.",bot=True)

    #### STATUS FRAME AND MESSAGE ####
    st_frame=Frame(gui,bg="white",width=101,height=20)
    st_frame.place(x=485,y=405)
    st_frame.pack_propagate(0)
    AI_status=Label(st_frame,text="",fg="white",bg="white",font=("Calisto MT","11","bold"))
    AI_status.pack(anchor="center")



    #### MIC PLACEMENT #### #004E7B

    mic_pic = Image.open("img.png")
    mic_pic = mic_pic.resize((65,65))
    mic_image = ImageTk.PhotoImage(mic_pic)
    mic_btn = Button(gui,image=mic_image,command=mic,bg="#004E7B",activebackground="#004E7B",borderwidth=0)
    mic_btn.place(x=496.5, y=426)


    gui.mainloop()