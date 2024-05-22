from tkinter import *
from tkinter import PhotoImage
#import math for converting seconds into minutes
import math 

# ---------------------------- CONSTANTS ----------------------------- #
PINK = "#DF8AA6"
RED = "#CB6E8D"
GREEN = "#90B697"
BACKGROUND = "#F1D3EC"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

WORK_SEC = WORK_MIN * 60
SHORT_BREAK_SEC = SHORT_BREAK_MIN * 60
LONG_BREAK_SEC = LONG_BREAK_MIN * 60

#initliaze TIME as WORK_SEC, the default
TIME = WORK_SEC
REPS = 1
CHECKMARKS = 0
timer = None


#-----------------------------TIMER BUTTONS ----------------------#
def set_timer(count):
  global TIME
  TIME = count
  if TIME == LONG_BREAK_SEC:
    timer_label.config(fg = RED, text="long break")
    canvas.itemconfig(tomato_img_id, image=tomato_red)
  elif TIME == SHORT_BREAK_SEC:
    timer_label.config(fg = PINK, text="short break")
    canvas.itemconfig(tomato_img_id, image=tomato_pink)
  else:
    timer_label.config(fg = GREEN, text="pomodoro")
    canvas.itemconfig(tomato_img_id, image=tomato_green)
  #need to format countdown to 00:00
  #.floor() round the count down to whole #
  count_min = math.floor(count / 60)
  #add leading 0 where needed by changing count_min to a string intermittently
  if count_min <10:
    count_min = f"0{count_min}"
  #the remainder of count/60 is the number of seconds
  count_sec = count % 60 
  #add leading 0 where needed by changing count_sec to a string intermittently
  if count_sec < 10:
    count_sec = f"0{count_sec}"
  #configure canvas using .itemconfig
  #.itemconfig(target_object, text=count)
  canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
  

# ---------------------------- TIMER RESET ---------------------- #
#reset button functionality
def reset_timer():
  window.after_cancel(timer)
  canvas.itemconfig(timer_text, text="25:00")
  timer_label.config(fg = GREEN, text="pomodoro")
  global CHECKMARKS
  CHECKMARKS = 0
  check_label.config(text=f"✔{CHECKMARKS}")
  global REPS
  REPS = 0
  global TIME
  TIME = WORK_SEC
  
  


# ---------------------------- TIMER MECHANISM ------------------------ #
#start button functionality
def start_timer():
  count_down(TIME)
  
# ---------------------------- COUNTDOWN MECHANISM ------------------ #
def count_down(count):
  if count == WORK_SEC:
    global CHECKMARKS
    CHECKMARKS +=1
    check_label.config(text=f"✔{CHECKMARKS}")
  #need to format countdown to 00:00
  #.floor() round the count down to whole #
  count_min = math.floor(count / 60)
  #add leading 0 where needed by changing count_min to a string intermittently
  if count_min <10:
    count_min = f"0{count_min}"
  #the remainder of count/60 is the number of seconds
  count_sec = count % 60 
  #add leading 0 where needed by changing count_sec to a string intermittently
  if count_sec < 10:
    count_sec = f"0{count_sec}"
  #configure canvas using .itemconfig
  #.itemconfig(target_object, text=count)
  canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
  #stops count down once it reaches 0
  if count >0:
  #subtracting 1 from count every 1000 miliseconds (1 sec)
    global timer
    timer = window.after(1000,count_down, count-1)
  else:
    global REPS
    REPS +=1
    if REPS % 8 == 0:
      set_timer(LONG_BREAK_SEC)
    elif REPS % 2 == 0:
      set_timer(SHORT_BREAK_SEC)
    else:
      set_timer(WORK_SEC)

#---------------------------CHECKMARK MECHANISM----------------------#
  

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("pomodoro timer")
window.config(padx=110, pady=50, bg=BACKGROUND)




#mode label
mode = Label(text="mode:", font=("courier", 22))
mode.config(bg=BACKGROUND, fg=GREEN)
mode.grid(column=1, row=0)

#timer label toggled by set_timer() function
timer_label = Label(text="pomodoro", font=("courier", 28))
timer_label.config(bg=BACKGROUND, fg=GREEN)
timer_label.grid(column=1, row=1, padx=15, pady=(0,20))

#pomodoro button triggers set_timer() w WORK_SEC as arg
button = Button(text="pomodoro", highlightthickness=0, command=lambda: set_timer(WORK_SEC))
button.grid(column=0, row=2)

#short_break button triggers set_timer() w SHORT_BREAK_SEC as arg
short_button = Button(text="short break", highlightthickness=0, command=lambda: set_timer(SHORT_BREAK_SEC))
short_button.grid(column=1, row=2)

#long_break button triggers set_timer() w LONG_BREAK_SEC as arg
button = Button(text="long break", highlightthickness=0, command=lambda: set_timer(LONG_BREAK_SEC))
button.grid(column=2, row=2)

canvas = Canvas(width=275, height=275, bg=BACKGROUND, highlightthickness=0)
#initialize each img variation as variables
tomato_green = PhotoImage(file="tomatogreen.png")
tomato_red = PhotoImage(file="tomatored.png")
tomato_pink = PhotoImage(file="tomatopink.png")
#tomato_img_id[image] toggled by set_timer()
tomato_img_id = canvas.create_image(125, 130, image=tomato_green)
# Configure the canvas properties
#store the count text as an obj variable timer_text so it can be
#passed into the count_down() function
canvas.itemconfig(tomato_img_id, image=tomato_pink)
timer_text = canvas.create_text(125,
                   140,
                   text="25:00",
                   fill="white",
                   font=(FONT_NAME, 30, "bold"))
canvas.grid(column=1, row=3, pady=(20,0))

#start button
#call the start_timer function --> calls count_down(TIME)
button = Button(text="start", highlightthickness=0, command=start_timer)
button.grid(column=0, row=4)

#reset button --> reset TIME, REPS, CHECKMARK, etc
button = Button(text="reset", highlightthickness=0, command=reset_timer)
button.grid(column=2, row=4)


#check label initialize
#if TIME = WORK_SEC --> count_down(TIME) adds 1
#to CHECKMARKS 
check_label = Label(text=f"✔{CHECKMARKS}", font=("courier", 19))
check_label.config(bg=BACKGROUND, fg=GREEN)
check_label.config(padx=10, pady=15)
check_label.grid(column=1, row=5)

window.mainloop()