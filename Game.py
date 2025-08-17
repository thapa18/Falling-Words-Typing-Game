import tkinter as tk
import random
from PIL import ImageTk, Image
import os

WORDS = ["apple", "brisk", "cat", "drift", "eagle", "flame", "grape", "rainbow" , "hike", "inbox", "jolly", "knock", "lemon", "mint", "noble", "ocean", "pearl", "quake", "risky", "sheep", "track", "umbra", "vivid", "wrist", "xenon", "youth", "zebra", "angle", "bloom", "crisp", "delta", "entry", "fuzzy", "glide", "hatch", "image", "joker", "kites", "latch", "mango", "nerdy", "optic", "piano", "quill", "rumor", "scale", "tease", "ultra", "vapor", "witty", "xylem", "yield", "armor", "blast", "climb", "draft", "equip", "fancy", "giant", "honey", "ideal", "joint", "kneel", "lunar", "mirth", "ninth", "oxide", "pluck", "quiet", "raven", "speak", "toast", "upset", "valid", "woven", "xerox", "young", "zoned", "actor", "badge", "cabin", "dance", "elope", "flick", "grain", "honor", "issue", "jumps", "knees", "lobby", "metal", "nifty", "onset", "punch", "quote", "rebel", "shiny", "title", "unite", "voter", "naruto", "anime", "python", "laptop", "earpods", "room", "university", "campus"]
 
class FallingWordsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Falling Words Typing Game")
        self.root.geometry("1500x730")

        self.bg_image_path = os.path.abspath("C:\\Users\\rohan\\Documents\\Vs Code\python codes\\Falling words game\\images\\wall3.jpg")
        bg_image = Image.open(self.bg_image_path).resize((1380, 720), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.canvas = tk.Canvas(root, width=1000, height=550, highlightthickness=0, bd=1)
        self.canvas.place(x=200, y=80)

        image_path = os.path.abspath("C:\\Users\\rohan\\Documents\\Vs Code\python codes\\Falling words game\\images\\wallf.jpg")
        self.bg_canva = Image.open(image_path).resize((1000, 550),Image.Resampling.LANCZOS)
        self.bg_canva = ImageTk.PhotoImage(self.bg_canva)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_canva)

        # === Entry Field ===
        self.entry = tk.Entry(root, font=("Helvetica", 16), justify='center', bg="white", fg="black")
        self.entry.place(x=540, y=600, width=300)
        self.entry.bind("<Return>", self.check_word)

        # === Score Label ===
        self.score_label = tk.Label(root, text="SCORE: 0", font=("Helvetica", 14), fg="blue", bg=None)
        self.score_label.place(x=30, y=20,width=100)

        # === Start Button ===
        self.start_button = tk.Button(root, text="Start Game", font=("Helvetica", 14), bg="#4CAF50", fg="white", command=self.start_game)
        self.start_button.place(x=1205, y=100,width=117)
        #=== Exit Button ===#
        self.exit_button = tk.Button(root, text="Exit", font=("Helvetica", 14), bg="#F13A3A", fg="white", command=quit)
        self.exit_button.place(x=1207, y=150,width=115,height=30)
        
        self.word_speed = 150 #word speed
        self.words_on_screen = []
        self.score = 0
        self.running = False
        self.move_after_id = None
        self.spawn_after_id = None

    def start_game(self):
        self.running = True
        self.score = 0
        self.score_label.config(text="SCORE: 0")
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_canva)
        self.words_on_screen.clear()
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.word_speed = 150 #word speed

        if self.move_after_id:
            self.root.after_cancel(self.move_after_id)
        if self.spawn_after_id:
            self.root.after_cancel(self.spawn_after_id)

        self.spawn_word()
        self.move_words()

    def spawn_word(self):
        if not self.running:
            return

        word = random.choice(WORDS)
        x = random.randint(45, 830)
        color =random.choice ([
    "#0d0d0d", "#1a1a1a", "#262626", "#2e2e2e", "#333333",
    "#1c1c1c", "#141414", "#101010", "#1f1f1f", "#292929",
    "#121212", "#171717", "#1b1b1b", "#232323", "#2a2a2a",
    "#191919", "#151515", "#202020", "#242424", "#2c2c2c",
    "#111111", "#181818", "#1d1d1d", "#252525", "#2d2d2d",
    "#0f0f0f", "#0e0e0e", "#2b2b2b", "#222222", "#1e1e1e",
    "#2f2f2f", "#303030", "#313131", "#343434", "#353535",
    "#363636", "#383838", "#393939", "#3a3a3a", "#3b3b3b",
    "#3c3c3c", "#3d3d3d", "#3e3e3e", "#000000", "#404040",
    "#000000", "#26282c", "#1a1c1f", "#171a1e", "#1f2126"
    ])
        text = self.canvas.create_text(x, 0, text=word, fill=color, font=("Helvetica", 16, "bold"))
        self.words_on_screen.append((text, word))
        self.spawn_after_id = self.root.after(2000 , self.spawn_word)

    def move_words(self):
        if not self.running:
            return

        for word_data in self.words_on_screen[:]:
            text, word = word_data
            self.canvas.move(text, 0, 5)
            y = self.canvas.coords(text)[1]
            if y >= 420: # end line 
                self.end_game()
                return

        self.move_after_id = self.root.after(self.word_speed, self.move_words)

    def check_word(self, event):
        typed = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        for word_data in self.words_on_screen[:]:
            text, word = word_data
            if typed == word:
                self.canvas.delete(text)
                self.words_on_screen.remove(word_data)
                self.score += 1
                self.score_label.config(text=f"SCORE: {self.score}")

                if self.score % 10 == 0:
                    self.word_speed = max(50, self.word_speed - 10)
                break

    def end_game(self):
        self.running = False

        if self.move_after_id:
            self.root.after_cancel(self.move_after_id)
        if self.spawn_after_id:
            self.root.after_cancel(self.spawn_after_id)

        for text, word in self.words_on_screen:
            self.canvas.delete(text)
        self.words_on_screen.clear()

        self.canvas.create_text(450, 250, text="Game Over!", fill="red", font=("Helvetica", 40, "bold"))
        self.canvas.create_text(450, 280, text=f"Your Score is: {self.score}", fill="green", font=("Helvetica", 15, "bold"))
        self.start_button.config(text="Restart Game")

# Run the game
root = tk.Tk()
game = FallingWordsGame(root)
root.mainloop()