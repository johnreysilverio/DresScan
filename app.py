import cv2
import tkinter as tk
from tkinter import Label, Listbox, Scrollbar, Frame, Menu
from PIL import Image, ImageTk
from ultralytics import YOLO
import threading
import pyttsx3

cloth_and_id_model = YOLO('clothes.pt')
hair_model = YOLO('haircolor.pt')

# Prohibited Item
not_allowed_clothing = [
    'tank_top', 'croptop', 'off_shoulder', 'strapless', 'shorts',
    'tattered_jeans', 'mini_skirt', 'leggings', 'jogger', 'crocs', 
    'slippers', 'exposed'
]
not_allowed_hair_colors = ['Blonde Hair', 'Gray_White', 'Red Hair']

# Mandatory Clothing
mandatory_clothing = 'id'

hair_confidence_threshold = 0.8

# Initialize Text-to-Speech engine
tts_engine = pyttsx3.init()
tts_active = False  # Flag to ensure TTS doesn't overlap
person_detected = False  # Flag to track if a person is detected

# Initialize the app and app size
root = tk.Tk()
root.title("Dress Code Detector")
root.attributes('-fullscreen', True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

themes = {
    "light": {
        "bg": "#FFFFFF",
        "fg": "#000000",
        "list_bg": "#F0F0F0",
        "list_fg": "#000000",
        "indicator_allowed": "#00FF00",
        "indicator_not_allowed": "#FF0000"
    },
    "dark": {
        "bg": "#2C2C2C",
        "fg": "#FFFFFF",
        "list_bg": "#3A3A3A",
        "list_fg": "#FFFFFF",
        "indicator_allowed": "#00FF00",
        "indicator_not_allowed": "#FF0000"
    }
}
current_theme = "light"

def apply_theme(theme_name):
    """Apply the chosen theme to the UI."""
    theme = themes[theme_name]
    root.config(bg=theme["bg"])
    video_frame.config(bg=theme["bg"])
    list_frame.config(bg=theme["bg"])
    list_label.config(bg=theme["bg"], fg=theme["fg"])
    allowed_label.config(bg=theme["bg"], fg=theme["indicator_allowed"])
    not_allowed_label.config(bg=theme["bg"], fg=theme["indicator_not_allowed"])
    not_allowed_listbox.config(bg=theme["list_bg"], fg=theme["list_fg"])
    menu_bar.config(bg=theme["bg"], fg=theme["fg"])

# Frame for video display
video_frame = Frame(root, width=int(screen_width * 0.7), height=screen_height)
video_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Frame for detected items display
list_frame = Frame(root, width=int(screen_width * 0.3), height=screen_height)
list_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Status indicator labels
status_frame = Frame(list_frame)
status_frame.pack(fill="x", pady=20)

allowed_label = Label(status_frame, text="All clothing allowed", font=("Arial", 16), fg="green")
not_allowed_label = Label(status_frame, text="Attention: Unauthorized dress code detected", font=("Arial", 16), fg="red")

# Listbox for prohibited items
list_label = Label(list_frame, text="Not Allowed Items Detected", font=("Arial", 16))
list_label.pack(pady=5)
not_allowed_listbox = Listbox(list_frame, font=("Arial", 14), width=30, height=20)
not_allowed_listbox.pack(side="left", fill="both", expand=True, padx=5)
scrollbar = Scrollbar(list_frame, orient="vertical", command=not_allowed_listbox.yview)
scrollbar.pack(side="right", fill="y")
not_allowed_listbox.config(yscrollcommand=scrollbar.set)

# Label for video feed
video_label = Label(video_frame)
video_label.pack(fill="both", expand=True)

# Initialize video capture
cap = cv2.VideoCapture(0)

def detect_dress_code():
    """Function to detect prohibited items in real time."""
    global person_detected

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (int(screen_width * 0.7), screen_height))
        prohibited_items_detected = set()
        id_present = False

        # Detect clothing and ID
        cloth_results = cloth_and_id_model(frame)
        person_detected = False  # Reset person detection flag
        for result in cloth_results:
            for box in result.boxes:
                class_id = int(box.cls)
                class_name = cloth_and_id_model.names[class_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                person_detected = True  # Person detected

                color = (0, 0, 255) if class_name in not_allowed_clothing else (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                if class_name in not_allowed_clothing:
                    prohibited_items_detected.add(class_name)
                if class_name == mandatory_clothing:
                    id_present = True

        # Detect hair color
        hair_results = hair_model(frame)
        for result in hair_results:
            for box in result.boxes:
                class_id = int(box.cls)
                class_name = hair_model.names[class_id]
                confidence = box.conf[0]
                if class_name in not_allowed_hair_colors and confidence >= hair_confidence_threshold:
                    prohibited_items_detected.add(class_name)

        # Handle prohibited items
        not_allowed_listbox.delete(0, tk.END)
        allowed_label.pack_forget()
        not_allowed_label.pack_forget()

        if not id_present and person_detected:
            prohibited_items_detected.add("No ID")

        if prohibited_items_detected and person_detected:
            for item in prohibited_items_detected:
                not_allowed_listbox.insert(tk.END, item)
            not_allowed_label.pack(pady=10)
            threading.Thread(target=announce_prohibited_items, args=(prohibited_items_detected,)).start()
        elif person_detected:
            allowed_label.pack(pady=10)
            threading.Thread(target=announce_allowed_clothing).start()

        # Update video feed
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        video_label.config(image=img_tk)
        video_label.image = img_tk

def announce_prohibited_items(items):
    """Announce detected prohibited items."""
    global tts_active, person_detected
    if not tts_active and person_detected:
        tts_active = True
        tts_engine.say(f"Detected prohibited items: {', '.join(items)}")
        tts_engine.runAndWait()
        tts_active = False

def announce_allowed_clothing():
    """Announce allowed clothing."""
    global tts_active, person_detected
    if not tts_active and person_detected:
        tts_active = True
        tts_engine.say("Your dress code is appropriate. Please proceed.")
        tts_engine.runAndWait()
        tts_active = False

def start_detection_thread():
    """Start the detection thread."""
    detection_thread = threading.Thread(target=detect_dress_code)
    detection_thread.daemon = True
    detection_thread.start()

# Toggle theme
def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme(current_theme)

# Menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Toggle Theme", command=toggle_theme)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="Options", menu=file_menu)

# Apply initial theme
apply_theme(current_theme)

# Start detection
start_detection_thread()

# Exit handler
def on_close():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()