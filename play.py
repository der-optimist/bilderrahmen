# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
import glob
import random
import tkinter as Tk
from datetime import datetime

class GUI:
    def __init__(self, mainwin, screen_width, screen_height):
        self.time_per_image = 10 # seconds
        self.image_folder = r'C:\Users\Bilder_bearbeitet\sichtbar\**\*.jpg'
        
        self.mainwin = mainwin
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.screen_aspect_ratio = screen_width / screen_height
        
        self.canvas = Tk.Canvas(self.mainwin, highlightthickness=0)
        self.canvas.place(relheight=1, relwidth=1, relx=0, rely=0)
        self.canvas.configure(background="black")
        
        # read source folder
        self.list_filepaths_all = []
        self.list_timestamps_all = []
        for filename in glob.glob(self.image_folder, recursive=True): #assuming gif
            im=Image.open(filename)
            self.list_filepaths_all.append(filename)
            try:
                self.list_timestamps_all.append(im._getexif()[36867])
            except:
                self.list_timestamps_all.append('0000:99:99 99:99:99')

        # go through list and sort in normal and anniversary
        self.today_day_str = datetime.today().strftime("%d")
        today_month_str = datetime.today().strftime("%m")
        today_year_str = datetime.today().strftime("%Y")
        self.list_filepaths_anniversary = []
        self.list_years_anniversary = []
        self.list_filepaths_rest = []
        for i in range(len(self.list_filepaths_all)):
            day_str = self.list_timestamps_all[i][8:10]
            month_str = self.list_timestamps_all[i][5:7]
            if (day_str == self.today_day_str) and (month_str == today_month_str):
                self.list_filepaths_anniversary.append(self.list_filepaths_all[i])
                years = int(today_year_str) - int(self.list_timestamps_all[i][0:4])
                self.list_years_anniversary.append(years)
            else:
                self.list_filepaths_rest.append(self.list_filepaths_all[i])
        
        # create and shuffle indices
        self.indices_anniversary_random = list(range(len(self.list_filepaths_anniversary)))
        random.shuffle(self.indices_anniversary_random)
        self.indices_rest_random = list(range(len(self.list_filepaths_rest)))
        random.shuffle(self.indices_rest_random)
        
        if len(self.list_filepaths_anniversary) == 0:
            self.anniversary_every = 1000000000
        elif len(self.list_filepaths_anniversary) <= 3:
            self.anniversary_every = 8
        elif len(self.list_filepaths_anniversary) <= 6:
            self.anniversary_every = 5
        elif len(self.list_filepaths_anniversary) <= 10:
            self.anniversary_every = 3
        else:
            self.anniversary_every = 2
        
        self.counter_all = 0
        self.counter_anniversary = 0
        self.counter_rest = 0

        self.slideShow()

    def slideShow(self):
        if datetime.today().strftime("%d") == self.today_day_str:
            if ((self.counter_all % self.anniversary_every) == 0) and (len(self.list_filepaths_anniversary) > 0):
                index = self.counter_anniversary % len(self.list_filepaths_anniversary)
                index_randomized = self.indices_anniversary_random[index]
                image = Image.open(self.list_filepaths_anniversary[index_randomized])
                year = self.list_years_anniversary[index_randomized]
                self.counter_anniversary += 1
                anniversary = True
            else:
                index = self.counter_rest % len(self.list_filepaths_rest)
                index_randomized = self.indices_rest_random[index]
                image = Image.open(self.list_filepaths_rest[index_randomized])
                self.counter_rest += 1
                anniversary = False
            self.counter_all += 1
            
            img_aspect = image.size[0]/image.size[1]
            if img_aspect < self.screen_aspect_ratio:
                wdt = int(img_aspect * self.screen_height)  
                image_resize = image.resize((wdt, self.screen_height))
            else:
                hgt = int(self.screen_width / img_aspect)
                image_resize = image.resize((self.screen_width, hgt))
            
            self.photo = ImageTk.PhotoImage(image_resize)
            self.canvas.create_image(int(self.screen_width / 2), int(self.screen_height / 2), image=self.photo)
            
            if anniversary:
                self.text = self.canvas.create_text(self.screen_width/2+2, 0.95*self.screen_height+2, text="heute vor {} Jahren...".format(year), fill='#202020', font=('garamond', 40, "bold italic"), anchor='s')
                self.text = self.canvas.create_text(self.screen_width/2, 0.95*self.screen_height, text="heute vor {} Jahren...".format(year), fill="white", font=('garamond', 40, "bold italic"), anchor='s')
            else:
                try:
                    self.canvas.delete(self.text)
                except:
                    pass
            
            root.after(1000*self.time_per_image, self.slideShow)
        else:
            root.destroy


# --- main ---

root = Tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.overrideredirect(True)
root.geometry('%dx%d' % (screen_width*1, screen_height*1))
root.configure(background='black')
root.configure(cursor="none")
myprog = GUI(root, screen_width, screen_height)
root.mainloop()
