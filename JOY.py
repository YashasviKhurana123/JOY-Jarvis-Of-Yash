import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime
import json
from groq import Groq
import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pywhatkit as kit
import pygame
import yt_dlp
import threading
import webbrowser

client = Groq(
    api_key="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",
)

update_frame_id = None
type_text_id = None
delete_text_id = None
type_new_text_id = None
delete_new_text_id = None
blink_cursor_id = None

window = tk.Tk()

window.title("JOY Login")

window.geometry("800x600") 

window.configure(bg="black")

image = Image.open("ai.gif")
frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(image)]

gif_label = tk.Label(window, bd=0, highlightthickness=0)
gif_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

def update_frame(frame_index):
    frame = frames[frame_index]
    gif_label.config(image=frame)
    frame_index = (frame_index + 1) % len(frames)
    global update_frame_id
    update_frame_id = window.after(50, update_frame, frame_index)

update_frame(0)

text_label = tk.Label(window, text="", font=("Lucida Calligraphy", 24), fg="#1E90FF", bg="black")
text_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

current_hour = datetime.now().hour
if current_hour < 12:
    full_text = "Good morning. I am JOY (Jarvis Of Yash)!"
elif 12 <= current_hour < 18:
    full_text = "Good afternoon. I am JOY (Jarvis Of Yash)!"
else:
    full_text = "Good evening. I am JOY (Jarvis Of Yash)!"

cursor = "|"
new_text = "Created By Yashasvi Khurana!"

def type_text(index=0):
    if index < len(full_text):
        current_text = full_text[:index + 1]
        text_label.config(text=current_text + cursor)
        global type_text_id
        type_text_id = window.after(150, type_text, index + 1)
    else:
        global delete_text_id
        delete_text_id = window.after(2000, delete_text)

def delete_text():
    current_text = text_label.cget("text")
    if len(current_text) > 1:
        text_label.config(text=current_text[:-2] + cursor)
        global delete_text_id
        delete_text_id = window.after(50, delete_text)
    else:
        type_new_text()

def type_new_text(index=0):
    if index < len(new_text):
        current_text = new_text[:index + 1]
        text_label.config(text=current_text + cursor)
        global type_new_text_id
        type_new_text_id = window.after(150, type_new_text, index + 1)
    else:
        global delete_new_text_id
        delete_new_text_id = window.after(2000, delete_new_text)

def delete_new_text():
    current_text = text_label.cget("text")
    if len(current_text) > 1:
        text_label.config(text=current_text[:-2] + cursor)
        global delete_new_text_id
        delete_new_text_id = window.after(50, delete_new_text)
    else:
        reset_cycle()

def reset_cycle():
    text_label.config(text="")
    type_text()

def blink_cursor():
    current_text = text_label.cget("text")
    if current_text.endswith(cursor):
        text_label.config(text=current_text[:-1] + "\u00A0")
    else:
        text_label.config(text=current_text[:-1] + cursor)
    global blink_cursor_id
    blink_cursor_id = window.after(500, blink_cursor)

type_text()

username_label = tk.Label(window, text="Username:", font=("Lucida Calligraphy", 24), fg="#1E90FF", bg="black")
username_label.place(relx=0.35, rely=0.75, anchor=tk.CENTER)
username_entry = tk.Entry(window, font=("Helvetica", 14), highlightbackground="white", highlightcolor="white", background="black", fg="white", insertbackground="white")
username_entry.place(relx=0.65, rely=0.75, anchor=tk.CENTER)

password_label = tk.Label(window, text="Password:", font=("Lucida Calligraphy", 24), fg="#1E90FF", bg="black")
password_label.place(relx=0.35, rely=0.82, anchor=tk.CENTER)
password_entry = tk.Entry(window, font=("Helvetica", 14), show="*", highlightbackground="white", highlightcolor="white", background="black", fg="white", insertbackground="white")
password_entry.place(relx=0.65, rely=0.82, anchor=tk.CENTER)

credentials = {
    "yash": "creator of joy",
    "user2": "password2",
}

ctrl_pressed = False

from PIL import Image, ImageTk, ImageSequence

def create_new_window(username):
    new_window = tk.Tk()
    new_window.geometry("800x600")
    new_window.configure(bg="#212121")
    new_window.title("Jarvis Of Yash")

    sidebar = tk.Frame(new_window, width=200, bg="black")
    sidebar.pack(side="left", fill="y")

    image = Image.open("ai.gif")
    frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(image)]

    gif_label = tk.Label(sidebar, bd=0, highlightthickness=0, bg="black")
    gif_label.pack(pady=10)

    def update_frame(frame_index):
        frame = frames[frame_index]
        gif_label.config(image=frame)
        frame_index = (frame_index + 1) % len(frames)
        new_window.after(50, update_frame, frame_index)

    update_frame(0)

    joy_label = tk.Label(sidebar, text="JOY", font=("Lucida Calligraphy", 14), fg="#1E90FF", bg="black")
    joy_label.place(x=110, y=80)

    typing_label = tk.Label(sidebar, text="", font=("Helvetica", 24), fg="#1E90FF", bg="black")
    typing_label.pack(pady=20)
    
    new_conversation_button = tk.Button(sidebar, text="New Conversation", font=("Lucida Calligraphy", 14), fg="#1E90FF", bg="black", highlightbackground="blue", highlightcolor="blue", bd=2)
    new_conversation_button.pack(pady=10, fill="x")

    pre_prompt_button = tk.Button(sidebar, text="Pre-defined Prompts", font=("Lucida Calligraphy", 14), fg="#1E90FF", bg="black", highlightbackground="blue", highlightcolor="blue", bd=2)
    pre_prompt_button.pack(pady=10, fill="x")

    previous_prompt_button = tk.Button(sidebar, text="Previous Conversations", font=("Lucida Calligraphy", 14), fg="#1E90FF", bg="black", highlightbackground="blue", highlightcolor="blue", bd=2)
    previous_prompt_button.pack(pady=10, fill="x")

    creator_label = tk.Label(sidebar, text="Created by Yashasvi Khurana", font=("Helvetica", 14), fg="#1E90FF", bg="black")
    creator_label.pack(side="bottom", pady=10)

    welcome_text = f"Welcome {username.upper()}!"
    cursor_visible = True
    typing_speed = 100
    deleting_speed = 50
    pause_time = 1000

    def type_text(index=0, typing=True):
        nonlocal cursor_visible
        if typing:
            if index <= len(welcome_text):
                typing_label.config(text=welcome_text[:index] + ("|" if cursor_visible else ""))
                cursor_visible = not cursor_visible
                new_window.after(typing_speed, type_text, index + 1, True)
            else:
                new_window.after(pause_time, type_text, len(welcome_text), False)
        else:
            if index >= 0:
                typing_label.config(text=welcome_text[:index] + ("|" if cursor_visible else ""))
                cursor_visible = not cursor_visible
                new_window.after(deleting_speed, type_text, index - 1, False)
            else:
                new_window.after(pause_time, type_text, 0, True)

    type_text()

    label_frame = tk.Frame(new_window, bg="#212121")
    label_frame.pack(expand=True)

    creator_label1 = tk.Label(label_frame, text="JOY", font=("Helvetica", 54), fg="#1E90FF", bg="#212121")
    creator_label1.pack()

    creator_label2 = tk.Label(label_frame, text="It's not just an AI!", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
    creator_label2.pack()

    creator_label3 = tk.Label(label_frame, text="It's a feeling!", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
    creator_label3.pack()

    def show_predefined_prompts():
        for widget in new_window.winfo_children():
            if widget != sidebar:
                widget.destroy()

        button_frame = tk.Frame(new_window, bg="#212121")
        button_frame.pack(expand=True)

        button1 = tk.Button(button_frame, text="Open an Application", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
        button1.pack(pady=10, anchor="center")

        button2 = tk.Button(button_frame, text="Send an E-mail", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
        button2.pack(pady=10, anchor="center")

        button3 = tk.Button(button_frame, text="Send a Whatsapp Message", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
        button3.pack(pady=10, anchor="center")

        button4 = tk.Button(button_frame, text="Play a Song", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
        button4.pack(pady=10, anchor="center")

        button5 = tk.Button(button_frame, text="Do a Google Search", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
        button5.pack(pady=10, anchor="center")

        def send_email(subject, body, to_email):
            from_email = "yashkhurana2911@gmail.com"
            password = "jmfk rlqp oxps zkhg"

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(from_email, password)
                server.send_message(msg)
                print("Email sent successfully")
            except Exception as e:
                print(f"Failed to send email: {e}")
            finally:
                server.quit()

        def send_whatsapp_message(phone_number, message):
            try:
                kit.sendwhatmsg_instantly(phone_number, message)
                print("Message sent successfully")
            except Exception as e:
                print(f"Failed to send message: {e}")

        def fetch_and_play_song(song_name):
            def play_song():
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'noplaylist': True,
                    'quiet': True,
                    'outtmpl': 'song.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
                    filename = ydl.prepare_filename(info['entries'][0])
                    filename = os.path.splitext(filename)[0] + ".mp3"

                pygame.mixer.init()
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

            threading.Thread(target=play_song).start()

        def play_song():
            pygame.mixer.music.unpause()

        def pause_song():
            pygame.mixer.music.pause()

        def google_search(query):
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)

        def open_application():
            button2.pack_forget()
            button3.pack_forget()
            button4.pack_forget()
            button5.pack_forget()

            for widget in new_window.winfo_children():
                if widget != sidebar and widget != button_frame:
                    widget.destroy()

            input_frame = tk.Frame(button_frame, bg="#212121")
            input_frame.pack(pady=20, padx=20, anchor="center")

            label = tk.Label(input_frame, text="Enter the name of the application", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
            label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            app_name_entry = tk.Entry(input_frame, font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            app_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

            open_button = tk.Button(input_frame, text="Open", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            open_button.grid(row=1, columnspan=2, pady=20)

            def open_app():
                app_name = app_name_entry.get()
                if app_name:
                    try:
                        subprocess.run([app_name], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"Failed to open {app_name}: {e}")

            open_button.config(command=open_app)

        def send_email_prompt():
            button1.pack_forget()
            button3.pack_forget()
            button4.pack_forget()
            button5.pack_forget()

            for widget in new_window.winfo_children():
                if widget != sidebar and widget != button_frame:
                    widget.destroy()

            input_frame = tk.Frame(button_frame, bg="#212121")
            input_frame.pack(pady=20, padx=20, anchor="center")

            to_label = tk.Label(input_frame, text="To:", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
            to_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            to_entry = tk.Entry(input_frame, font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            to_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

            subject_label = tk.Label(input_frame, text="Subject:", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
            subject_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

            subject_entry = tk.Entry(input_frame, font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            subject_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

            body_label = tk.Label(input_frame, text="Body:", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
            body_label.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

            body_text = tk.Text(input_frame, font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2, height=10, width=40)
            body_text.grid(row=2, column=1, padx=10, pady=10, sticky="w")

            send_button = tk.Button(input_frame, text="Send", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            send_button.grid(row=3, columnspan=2, pady=20)

            def send_email_action():
                to_email = to_entry.get()
                subject = subject_entry.get()
                body = body_text.get("1.0", tk.END)
                send_email(subject, body, to_email)

            send_button.config(command=send_email_action)

        def send_whatsapp_prompt():
            button1.pack_forget()
            button2.pack_forget()
            button4.pack_forget()
            button5.pack_forget()

            for widget in new_window.winfo_children():
                if widget != sidebar and widget != button_frame:
                    widget.destroy()

            input_frame = tk.Frame(button_frame, bg="#212121")
            input_frame.pack(pady=20, padx=20, anchor="center")

            phone_label = tk.Label(input_frame, text="Phone Number:", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
            phone_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            phone_entry = tk.Entry(input_frame, font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            phone_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

            message_label = tk.Label(input_frame, text="Message:", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
            message_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

            message_text = tk.Text(input_frame, font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2, height=10, width=40)
            message_text.grid(row=1, column=1, padx=10, pady=10, sticky="w")

            send_button = tk.Button(input_frame, text="Send", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            send_button.grid(row=2, columnspan=2, pady=20)

            def send_whatsapp_action():
                phone_number = phone_entry.get()
                message = message_text.get("1.0", tk.END)
                send_whatsapp_message(phone_number, message)

            send_button.config(command=send_whatsapp_action)

        def play_song_prompt():
            button1.pack_forget()
            button2.pack_forget()
            button3.pack_forget()
            button5.pack_forget()

            for widget in new_window.winfo_children():
                if widget != sidebar and widget != button_frame:
                    widget.destroy()

            input_frame = tk.Frame(button_frame, bg="#212121")
            input_frame.pack(pady=20, padx=20, anchor="center")

            song_label = tk.Label(input_frame, text="Enter the name of the song:", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
            song_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            song_entry = tk.Entry(input_frame, font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            song_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

            play_button = tk.Button(input_frame, text="Play", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            play_button.grid(row=1, columnspan=2, pady=20)

            pause_button = tk.Button(input_frame, text="Pause", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            pause_button.grid(row=2, column=0, pady=20)

            resume_button = tk.Button(input_frame, text="Resume", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            resume_button.grid(row=2, column=1, pady=20)

            def play_song_action():
                song_name = song_entry.get()
                fetch_and_play_song(song_name)

            play_button.config(command=play_song_action)
            pause_button.config(command=pause_song)
            resume_button.config(command=play_song)

        def google_search_prompt():
            button1.pack_forget()
            button2.pack_forget()
            button3.pack_forget()
            button4.pack_forget()

            for widget in new_window.winfo_children():
                if widget != sidebar and widget != button_frame:
                    widget.destroy()

            input_frame = tk.Frame(button_frame, bg="#212121")
            input_frame.pack(pady=20, padx=20, anchor="center")

            search_label = tk.Label(input_frame, text="Enter search query:", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
            search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            search_entry = tk.Entry(input_frame, font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

            search_button = tk.Button(input_frame, text="Search", font=("Helvetica", 14), fg="#1E90FF", bg="black", bd=2)
            search_button.grid(row=1, columnspan=2, pady=20)

            def search_action():
                query = search_entry.get()
                google_search(query)

            search_button.config(command=search_action)

        button1.config(command=open_application)
        button2.config(command=send_email_prompt)
        button3.config(command=send_whatsapp_prompt)
        button4.config(command=play_song_prompt)
        button5.config(command=google_search_prompt)


    pre_prompt_button.config(command=show_predefined_prompts)

    def show_conversation_details(question, answer):
        for widget in new_window.winfo_children():
            if widget != sidebar:
                widget.destroy()

        question_frame = tk.Frame(new_window, bg="#333333", bd=2, relief="groove")
        question_frame.pack(pady=10, padx=220, fill="x")

        question_canvas = tk.Canvas(question_frame, bg="#333333")
        question_scrollbar = tk.Scrollbar(question_frame, orient="vertical", command=question_canvas.yview)
        question_scrollable_frame = tk.Frame(question_canvas, bg="#333333")

        question_scrollable_frame.bind(
            "<Configure>",
            lambda e: question_canvas.configure(
                scrollregion=question_canvas.bbox("all")
            )
        )

        question_canvas.create_window((0, 0), window=question_scrollable_frame, anchor="nw")
        question_canvas.configure(yscrollcommand=question_scrollbar.set)

        question_canvas.pack(side="left", fill="both", expand=True)
        question_scrollbar.pack(side="right", fill="y")

        question_label = tk.Label(question_scrollable_frame, text=f"Question: {question}", font=("Helvetica", 14), fg="#1E90FF", bg="#333333", wraplength=500, anchor="w", justify="left")
        question_label.pack(pady=10, padx=10)

        answer_frame = tk.Frame(new_window, bg="#333333", bd=2, relief="groove")
        answer_frame.pack(pady=10, padx=220, fill="x")

        answer_canvas = tk.Canvas(answer_frame, bg="#333333")
        answer_scrollbar = tk.Scrollbar(answer_frame, orient="vertical", command=answer_canvas.yview)
        answer_scrollable_frame = tk.Frame(answer_canvas, bg="#333333")

        answer_scrollable_frame.bind(
            "<Configure>",
            lambda e: answer_canvas.configure(
                scrollregion=answer_canvas.bbox("all")
            )
        )

        answer_canvas.create_window((0, 0), window=answer_scrollable_frame, anchor="nw")
        answer_canvas.configure(yscrollcommand=answer_scrollbar.set)

        answer_canvas.pack(side="left", fill="both", expand=True)
        answer_scrollbar.pack(side="right", fill="y")

        answer_label = tk.Label(answer_scrollable_frame, text=f"Answer: {answer}", font=("Helvetica", 14), fg="#1E90FF", bg="#333333", wraplength=500, anchor="w", justify="left")
        answer_label.pack(pady=10, padx=10)

    def show_previous_conversations():
        file_path = f"{username}_history.json"
        
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, "r") as file:
                conversations = json.load(file)
        else:
            conversations = []

        for widget in new_window.winfo_children():
            if widget != sidebar:
                widget.destroy()

        canvas = tk.Canvas(new_window, bg="#212121")
        scrollbar = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#212121")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if conversations:
            for conversation in conversations:
                button_text = f"{conversation['timestamp']} - {conversation['user']}"
                conversation_button = tk.Button(scrollable_frame, text=button_text, font=("Helvetica", 12), fg="#1E90FF", bg="black", bd=2, command=lambda c=conversation: show_conversation_details(c['user'], c['joy']))
                conversation_button.pack(pady=5, anchor="center", expand=True, fill=tk.X)
        else:
            no_conversations_label = tk.Label(scrollable_frame, text="No previous conversations found.", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
            no_conversations_label.pack(anchor="center", padx=10, pady=10)

    def start_new_conversation():
        creator_label1.pack_forget()
        creator_label2.pack_forget()
        creator_label3.pack_forget()

        for widget in new_window.winfo_children():
            if widget != sidebar:
                widget.destroy()
        
        input_frame = tk.Frame(new_window, bg="#212121")
        input_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        text_box = tk.Text(input_frame, height=4, bg="#212121", fg="#1E90FF", font=("Helvetica", 14))
        text_box.pack(side="left", fill="x", expand=True)

        send_image = Image.open("send.png")

        new_height = int(text_box.winfo_reqheight() * 0.9)
        new_width = int(send_image.width * (new_height / send_image.height))

        send_image = send_image.resize((new_width, new_height), Image.LANCZOS)

        send_image = send_image.crop((0, 0, new_width, new_height))

        send_photo = ImageTk.PhotoImage(send_image)

        send_button = tk.Button(input_frame, image=send_photo, bg="#212121", bd=0)
        send_button.image = send_photo
        send_button.pack(side="right")

        def handle_specific_commands(input_text):
            name_questions = [
                "what is your name?",
                "what are you called?",
                "who are you?",
                "can you tell me your name?",
                "may i know your name?",
                "what's your name?",
                "what do people call you?",
                "how should I address you?",
                "who am I talking to?",
                "what do you go by?",
                "what should I call you?",
                "what is your full name?",
                "could you tell me your name?",
                "do you have a name?",
                "what is your designation?",
                "what name were you given?",
                "what's your official name?",
                "how do people refer to you?",
                "what name do you respond to?",
                "under what name are you known?",
                "what's your identity?",
                "how can I refer to you?",
                "what's your moniker?",
                "what's your alias?",
                "what's your handle?",
                "what's your tag?",
                "what's your title?",
                "what's your label?",
                "what's your nickname?",
                "what's your appellation?",
                "what's your sobriquet?",
                "what's your byname?",
                "what's your pseudonym?",
                "what's your nom de plume?",
                "what's your nom de guerre?",
                "what's your assumed name?",
                "what's your pen name?",
                "what's your stage name?",
                "what's your screen name?",
                "what's your user name?",
                "what's your internet name?",
                "what's your online name?",
                "what's your virtual name?",
                "what's your avatar name?",
                "what's your character name?",
                "what's your persona?",
                "what's your identity?",
                "what's your identifier?",
                "what's your unique identifier?",
                "what's your unique name?",
                "what's your unique tag?",
                "what's your unique handle?",
                "what's your unique label?",
                "what's your unique title?",
                "what's your unique nickname?",
                "what's your unique appellation?",
                "what's your unique sobriquet?",
                "what's your unique epithet?",
                "what's your unique byname?",
                "what's your unique pseudonym?",
                "what's your unique nom de plume?",
                "what's your unique nom de guerre?",
                "what's your unique assumed name?",
                "what's your unique pen name?",
                "what's your unique stage name?",
                "what's your unique screen name?",
                "what's your unique user name?",
                "what's your unique internet name?",
                "what's your unique online name?",
                "what's your unique virtual name?",
                "what's your unique avatar name?",
                "what's your unique character name?",
                "what's your unique persona?",
            ]
                        
            if input_text.lower() in name_questions:
                return "My name is JOY (Jarvis Of Yash). I was created by Yashasvi Khurana. He is a student at St. Columba's School, New Delhi. He is a passionate coder and I am one of his greatest creations. He is a great person and I am proud to be his creation."
            return None

        def show_accept_reject_buttons():
            entered_text = text_box.get("1.0", tk.END).strip()

            specific_response = handle_specific_commands(entered_text)
            if specific_response:
                answer = specific_response
            else:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": entered_text,
                        }
                    ],
                    model="llama3-8b-8192",
                )
                answer = chat_completion.choices[0].message.content

            send_button.pack_forget()
            text_box.pack_forget()

            button_frame = tk.Frame(new_window, bg="#212121")
            button_frame.pack(side="bottom", pady=20) 

            accept_button = tk.Button(button_frame, text="Accept", font=("Lucida Calligraphy", 14), fg="#1E90FF", bg="black", bd=2)
            accept_button.pack(side="left", padx=20)

            reject_button = tk.Button(button_frame, text="Reject", font=("Lucida Calligraphy", 14), fg="#1E90FF", bg="black", bd=2)
            reject_button.pack(side="left", padx=20)

            answer_frame = tk.Frame(new_window, bg="#212121")
            answer_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

            answer_text = tk.Text(answer_frame, wrap="word", bg="#212121", fg="#1E90FF", font=("Helvetica", 14))
            answer_text.insert(tk.END, answer)
            answer_text.config(state=tk.DISABLED)  
            answer_text.pack(side="left", fill="both", expand=True)

            scrollbar = tk.Scrollbar(answer_frame, command=answer_text.yview)
            scrollbar.pack(side="right", fill="y")
            answer_text.config(yscrollcommand=scrollbar.set)

            def accept_action():
                conversation_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "user": entered_text,
                    "joy": answer
                }
                
                file_path = f"{username}_history.json"
                
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    with open(file_path, "r") as file:
                        conversations = json.load(file)
                else:
                    conversations = []

                conversations.append(conversation_entry)

                with open(file_path, "w") as file:
                    json.dump(conversations, file, indent=4)

                for widget in new_window.winfo_children():
                    if widget != sidebar:
                        widget.destroy()

                label_frame = tk.Frame(new_window, bg="#212121")
                label_frame.pack(expand=True)

                creator_label1 = tk.Label(label_frame, text="JOY", font=("Helvetica", 54), fg="#1E90FF", bg="#212121")
                creator_label1.pack()

                creator_label2 = tk.Label(label_frame, text="It's not just an AI!", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
                creator_label2.pack()

                creator_label3 = tk.Label(label_frame, text="It's a feeling!", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
                creator_label3.pack()

                print("Answer Accepted")

            def reject_action():
                for widget in new_window.winfo_children():
                    if widget != sidebar:
                        widget.destroy()

                label_frame = tk.Frame(new_window, bg="#212121")
                label_frame.pack(expand=True)

                creator_label1 = tk.Label(label_frame, text="JOY", font=("Helvetica", 54), fg="#1E90FF", bg="#212121")
                creator_label1.pack()

                creator_label2 = tk.Label(label_frame, text="It's not just an AI!", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
                creator_label2.pack()

                creator_label3 = tk.Label(label_frame, text="It's a feeling!", font=("Helvetica", 14), fg="#1E90FF", bg="#212121")
                creator_label3.pack()

                print("Answer Rejected")

            accept_button.config(command=accept_action)
            reject_button.config(command=reject_action)

            print(f"Entered text: {entered_text}")

        send_button.config(command=show_accept_reject_buttons)

    new_conversation_button.config(command=start_new_conversation)
    previous_prompt_button.config(command=show_previous_conversations)

    new_window.mainloop()

def on_submit():
    
    username = username_entry.get().lower()
    password = password_entry.get()
    if username in credentials and credentials[username] == password:
        login_label.config(text="Login Successful", fg="green")
        if update_frame_id is not None:
            window.after_cancel(update_frame_id)
        if type_text_id is not None:
            window.after_cancel(type_text_id)
        if delete_text_id is not None:
            window.after_cancel(delete_text_id)
        if type_new_text_id is not None:
            window.after_cancel(type_new_text_id)
        if delete_new_text_id is not None:
            window.after_cancel(delete_new_text_id)
        if blink_cursor_id is not None:
            window.after_cancel(blink_cursor_id)
        window.after(1000, lambda: [window.destroy(), create_new_window(username)])
    else:
        login_label.config(text="Login Failed", fg="red")

button_image = Image.open("button.png")
button_photo = ImageTk.PhotoImage(button_image)

canvas = tk.Canvas(window, width=button_photo.width(), height=button_photo.height(), bg="black", highlightthickness=0)
canvas.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

canvas.create_image(0, 0, anchor=tk.NW, image=button_photo)

canvas.bind("<Button-1>", lambda event: on_submit())

login_label = tk.Label(window, text="", font=("Helvetica", 14), bg="black")
login_label.place(relx=0.5, rely=0.98, anchor=tk.CENTER)

window.mainloop()