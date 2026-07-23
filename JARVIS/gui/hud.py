import customtkinter as ctk
import threading
import time
import math
import psutil
import sys
from datetime import datetime

if sys.platform == "win32":
    import winsound

# ── Theme ──────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

HUD_BG       = "#020B18"
ACCENT       = "#00D4FF"  # Cool Cyan (Ready Mode)
ACCENT2      = "#FF6B00"  # Danger Orange (Action/Process Mode)
DIM_BLUE     = "#0A2540"
TEXT_PRIMARY = "#E0F7FF"
TEXT_DIM     = "#4A7C99"
GRID_COLOR   = "#0D2035"


class JarvisHUD(ctk.CTk):
    def __init__(self, on_text_command):
        super().__init__()
        self.on_text_command = on_text_command

        self.title("J.A.R.V.I.S  —  Advanced Response Virtual Intelligence System")
        self.geometry("1100x720")
        self.configure(fg_color=HUD_BG)
        self.resizable(True, True)

        # Current state tracker for dynamic pulse animation colors
        self.current_state = "ready" # "ready", "processing", "listening"

        self._build_layout()
        
        # Safely start UI loops
        self._tick()
        self._pulse_angle = 0
        self._animate_pulse()
        
        # Start the Safe System Monitor inside GUI Loop!
        self._update_system_stats_loop()

    # ── Layout ─────────────────────────────────────────────────
    def _build_layout(self):
        top = ctk.CTkFrame(self, fg_color=DIM_BLUE, height=50, corner_radius=0)
        top.pack(fill="x")
        ctk.CTkLabel(top, text="⬡  J.A.R.V.I.S", font=("Courier", 18, "bold"),
                     text_color=ACCENT).pack(side="left", padx=20, pady=10)
        self.clock_lbl = ctk.CTkLabel(top, text="", font=("Courier", 13),
                                       text_color=TEXT_DIM)
        self.clock_lbl.pack(side="right", padx=20)
        ctk.CTkLabel(top, text="● ONLINE", font=("Courier", 11),
                     text_color="#00FF88").pack(side="right", padx=10)

        main = ctk.CTkFrame(self, fg_color=HUD_BG)
        main.pack(fill="both", expand=True, padx=10, pady=8)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=3)
        main.columnconfigure(2, weight=1)
        main.rowconfigure(0, weight=1)

        left = self._panel(main, "SYSTEM STATUS")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self._build_left_panel(left)

        center = self._panel(main, "COMMAND INTERFACE")
        center.grid(row=0, column=1, sticky="nsew", padx=6)
        self._build_center_panel(center)

        right = self._panel(main, "MEMORY LOG")
        right.grid(row=0, column=2, sticky="nsew", padx=(6, 0))
        self._build_right_panel(right)

        self._build_bottom_bar()

    def _panel(self, parent, title: str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(parent, fg_color=DIM_BLUE, corner_radius=8,
                              border_width=1, border_color=ACCENT)
        header = ctk.CTkFrame(frame, fg_color=ACCENT, height=28, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text=f"▸ {title}", font=("Courier", 11, "bold"),
                     text_color=HUD_BG).pack(side="left", padx=8)
        return frame

    def _build_left_panel(self, frame):
        self.status_items = {}
        metrics = [
            ("CPU", "Monitoring..."),
            ("RAM", "Monitoring..."),
            ("DISK", "Monitoring..."),
            ("NETWORK", "Active"),
            ("AI CORE", "Cloud ✓"),
            ("MIC", "Listening"),
        ]
        for key, val in metrics:
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=4)
            ctk.CTkLabel(row, text=key, font=("Courier", 10, "bold"),
                          text_color=TEXT_DIM, width=70, anchor="w").pack(side="left")
            lbl = ctk.CTkLabel(row, text=val, font=("Courier", 10),
                                text_color=ACCENT, anchor="w")
            lbl.pack(side="left", padx=6)
            self.status_items[key] = lbl

        self.pulse_canvas = ctk.CTkCanvas(frame, width=140, height=60,
                                           bg=DIM_BLUE, highlightthickness=0)
        self.pulse_canvas.pack(pady=10)

    def _build_center_panel(self, frame):
        self.log_box = ctk.CTkTextbox(
            frame, font=("Courier", 12), fg_color="#010D1A",
            text_color=TEXT_PRIMARY, corner_radius=6,
            border_width=1, border_color=GRID_COLOR
        )
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(8, 6))
        self.log_box.insert("end", "◈ JARVIS initialized. All systems nominal.\n")
        self.log_box.configure(state="disabled")

        inp_row = ctk.CTkFrame(frame, fg_color="transparent")
        inp_row.pack(fill="x", padx=10, pady=(0, 10))

        self.text_input = ctk.CTkEntry(
            inp_row, placeholder_text="Type command or speak...",
            font=("Courier", 12), fg_color="#010D1A",
            border_color=ACCENT, text_color=TEXT_PRIMARY, height=38
        )
        self.text_input.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.text_input.bind("<Return>", self._on_enter)

        send_btn = ctk.CTkButton(
            inp_row, text="SEND", font=("Courier", 12, "bold"),
            fg_color=ACCENT, text_color=HUD_BG, hover_color=ACCENT2,
            width=80, height=38, command=self._on_send
        )
        send_btn.pack(side="right")

        self.mic_btn = ctk.CTkButton(
            frame, text="🎙  ACTIVATE MIC",
            font=("Courier", 12, "bold"),
            fg_color="#0A3040", text_color=ACCENT,
            hover_color=ACCENT, border_width=1, border_color=ACCENT,
            height=36, command=self._on_mic
        )
        self.mic_btn.pack(fill="x", padx=10, pady=(0, 10))

    def _build_right_panel(self, frame):
        self.memory_box = ctk.CTkTextbox(
            frame, font=("Courier", 10), fg_color="#010D1A",
            text_color=TEXT_DIM, corner_radius=6, wrap="word"
        )
        self.memory_box.pack(fill="both", expand=True, padx=8, pady=8)
        self.memory_box.insert("end", "[ Memory Log ]\n\n")
        self.memory_box.configure(state="disabled")

    def _build_bottom_bar(self):
        bar = ctk.CTkFrame(self, fg_color=DIM_BLUE, height=30, corner_radius=0)
        bar.pack(fill="x", side="bottom")
        ctk.CTkLabel(bar, text="JARVIS v2.0  |  Cloud AI: Groq  |  STT: Google",
                     font=("Courier", 9), text_color=TEXT_DIM).pack(side="left", padx=12)
        ctk.CTkLabel(bar, text="© Stark Industries",
                     font=("Courier", 9), text_color=TEXT_DIM).pack(side="right", padx=12)

    # ── Event Handlers ─────────────────────────────────────────
    def _on_enter(self, event=None):
        self._on_send()

    def _on_send(self):
        text = self.text_input.get().strip()
        if text:
            self.text_input.delete(0, "end")
            self.add_user_message(text)
            threading.Thread(target=self._process_cmd, args=(text,), daemon=True).start()

    def _on_mic(self):
        # 🔊 Metallic activation sound play karein safely
        if sys.platform == "win32":
            threading.Thread(target=lambda: (
                winsound.Beep(1200, 80),
                winsound.Beep(1800, 100)
            ), daemon=True).start()

        self.mic_btn.configure(text="🔴  LISTENING...", fg_color=ACCENT2)
        self.current_state = "listening"
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _listen_thread(self):
        try:
            from modules.speech_input import listen_for_command
            text = listen_for_command()
        except ImportError:
            text = "Speech input module not found."
            
        self.mic_btn.configure(text="🎙  ACTIVATE MIC", fg_color="#0A3040")
        if text:
            # 🔊 Target acquired confirmation chime
            if sys.platform == "win32":
                threading.Thread(target=lambda: winsound.Beep(1500, 120), daemon=True).start()
                
            self.add_user_message(text)
            threading.Thread(target=self._process_cmd, args=(text,), daemon=True).start()
        else:
            self.current_state = "ready"

    def _process_cmd(self, text: str):
        try:
            from modules.command_router import route_command
            from modules.speech_output  import speak
            from core.memory             import remember_conversation
            
            self.set_status("Processing...")
            self.current_state = "processing"
            
            reply = route_command(text)
            
            self.add_jarvis_message(reply)
            remember_conversation(text, reply)
            self.add_memory_entry(text, reply)
            speak(reply)
            
            self.set_status("Listening")
            self.current_state = "ready"
        except Exception as e:
            self.add_jarvis_message(f"Error processing command: {e}")
            self.set_status("Error")
            self.current_state = "ready"

    # ── Public Methods ─────────────────────────────────────────
    def add_user_message(self, text: str):
        self._append_log(f"\n▶ YOU: {text}\n")

    def add_jarvis_message(self, text: str):
        self._append_log(f"◈ JARVIS: {text}\n")

    def set_status(self, msg: str):
        if "MIC" in self.status_items:
            self.status_items["MIC"].configure(text=msg)

    def add_memory_entry(self, user: str, jarvis: str):
        self.memory_box.configure(state="normal")
        ts = datetime.now().strftime("%H:%M")
        self.memory_box.insert("end", f"[{ts}] {user[:30]}…\n")
        self.memory_box.see("end")
        self.memory_box.configure(state="disabled")

    # ── Internal Loops ─────────────────────────────────────────
    def _append_log(self, text: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _tick(self):
        now = datetime.now().strftime("  %Y-%m-%d   %H:%M:%S  ")
        self.clock_lbl.configure(text=now)
        self.after(1000, self._tick)

    def _animate_pulse(self):
        c = self.pulse_canvas
        c.delete("all")
        cx, cy, r = 70, 30, 20
        
        # Decide core color depending on active system state
        if self.current_state == "processing":
            core_color = ACCENT2
            dot_color = ACCENT2
        elif self.current_state == "listening":
            core_color = "#FF3B30" # Alert Red
            dot_color = "#FF3B30"
        else:
            core_color = ACCENT
            dot_color = TEXT_DIM

        for i in range(3):
            a = self._pulse_angle + i * 60
            x1 = cx + (r + i*8) * math.cos(math.radians(a))
            y1 = cy + (r + i*8) * math.sin(math.radians(a)) * 0.4
            c.create_oval(x1-2, y1-2, x1+2, y1+2,
                          fill=core_color if i == 0 else dot_color, outline="")
                          
        c.create_text(cx, cy, text="◈", fill=core_color, font=("Courier", 14))
        self._pulse_angle = (self._pulse_angle + 3) % 360
        self.after(40, self._animate_pulse)

    def _update_system_stats_loop(self):
        """Safe internal GUI loop for performance metrics"""
        try:
            cpu  = f"{psutil.cpu_percent():.0f}%"
            ram  = f"{psutil.virtual_memory().percent:.0f}%"
            disk = f"{psutil.disk_usage('/').percent:.0f}%"
            
            self.status_items["CPU"].configure(text=cpu)
            self.status_items["RAM"].configure(text=ram)
            self.status_items["DISK"].configure(text=disk)
        except Exception as e:
            print(f"Stats Error: {e}")
            
        self.after(3000, self._update_system_stats_loop)