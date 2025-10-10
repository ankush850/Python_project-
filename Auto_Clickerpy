import threading
import time
import sys
import tkinter as tk
from tkinter import ttk, StringVar, IntVar, BooleanVar
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode

# Hotkeys
HOT_TOGGLE = KeyCode(char='t')
HOT_QUIT = KeyCode(char='q')
HOT_DOUBLE = KeyCode(char='d')
HOT_HOLD = KeyCode(char='h')
HOT_BTN1 = KeyCode(char='1')
HOT_BTN2 = KeyCode(char='2')
HOT_BTN3 = KeyCode(char='3')
HOT_SPEED_UP = KeyCode.from_vk(0x26)   # Up arrow
HOT_SPEED_DOWN = KeyCode.from_vk(0x28) # Down arrow

MOUSE = Controller()

class AutoClickerCore:
    def __init__(self):
        self._running = False
        self._hold_mode = False
        self._double_click = False
        self._button = Button.left
        self._cps = 10.0
        self._interval = 1.0 / self._cps
        self._lock = threading.Lock()
        self._exit_flag = False
        self._hold_key_down = False

    def set_cps(self, cps):
        with self._lock:
            self._cps = max(0.1, float(cps))
            self._interval = 1.0 / self._cps

    def get_cps(self):
        with self._lock:
            return self._cps

    def set_button(self, btn_id):
        with self._lock:
            self._button = {1: Button.left, 2: Button.middle, 3: Button.right}[btn_id]

    def set_double(self, val: bool):
        with self._lock:
            self._double_click = val

    def set_hold_mode(self, val: bool):
        with self._lock:
            self._hold_mode = val
            if not val: self._hold_key_down = False

    def toggle_running(self):
        with self._lock:
            self._running = not self._running
            return self._running

    def set_running(self, val: bool):
        with self._lock:
            self._running = val

    def is_running(self):
        with self._lock:
            return self._running

    def set_exit(self):
        with self._lock:
            self._exit_flag = True

    def should_exit(self):
        with self._lock:
            return self._exit_flag

    def notify_hold_key(self, is_down: bool):
        with self._lock:
            self._hold_key_down = is_down

    def hold_key_is_down(self):
        with self._lock:
            return self._hold_key_down

    def run_click_loop(self, status_callback=None):
        while not self.should_exit():
            active = self.hold_key_is_down() if self._hold_mode else self.is_running()
            if active:
                if self._double_click:
                    MOUSE.click(self._button, 2)
                else:
                    MOUSE.click(self._button, 1)
            interval = None
            with self._lock:
                interval = self._interval
            time.sleep(max(0.001, interval))
            if status_callback:
                status_callback()
        self.set_running(False)

class AutoClickerApp(tk.Tk):
    def __init__(self, core: AutoClickerCore):
        super().__init__()
        self.core = core
        self.title("Autoclicker GUI")
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.resizable(False, False)
        self.var_cps = tk.DoubleVar(value=self.core.get_cps())
        self.var_button = tk.IntVar(value=1)
        self.var_double = tk.BooleanVar(value=False)
        self.var_hold = tk.BooleanVar(value=False)
        self.var_status = tk.StringVar(value="Idle")
        frm = ttk.Frame(self, padding=12)
        frm.grid(row=0, column=0)
        ttk.Label(frm, text="CPS (Clicks Per Second)").grid(row=0, column=0, sticky="w")
        self.slider = ttk.Scale(frm, from_=0.5, to=200, variable=self.var_cps, command=self._on_cps_change)
        self.slider.grid(row=1, column=0, columnspan=3, sticky="we", pady=(0,8))
        ttk.Radiobutton(frm, text="Left (1)", variable=self.var_button, value=1, command=self._on_button_change).grid(row=2,column=0)
        ttk.Radiobutton(frm, text="Middle (2)", variable=self.var_button, value=2, command=self._on_button_change).grid(row=2,column=1)
        ttk.Radiobutton(frm, text="Right (3)", variable=self.var_button, value=3, command=self._on_button_change).grid(row=2,column=2)
        ttk.Checkbutton(frm, text="Double Click (D)", variable=self.var_double, command=self._on_double_toggle).grid(row=3,column=0)
        ttk.Checkbutton(frm, text="Hold Mode (H)", variable=self.var_hold, command=self._on_hold_toggle).grid(row=3,column=1)
        self.btn_toggle = ttk.Button(frm, text="Start (T)", command=self._gui_toggle)
        self.btn_toggle.grid(row=4,column=0)
        self.btn_quit = ttk.Button(frm, text="Quit (Q)", command=self._on_close)
        self.btn_quit.grid(row=4,column=1)
        ttk.Label(frm, text="Status:").grid(row=5,column=0)
        ttk.Label(frm, textvariable=self.var_status).grid(row=5,column=1)
        self._worker_thread = threading.Thread(target=self.core.run_click_loop, args=(self._update_status,), daemon=True)
        self._worker_thread.start()
        self._kb_listener = Listener(on_press=self._on_key_press, on_release=self._on_key_release)
        self._kb_listener_thread = threading.Thread(target=self._kb_listener.run, daemon=True)
        self._kb_listener_thread.start()
        self.after(150, self._periodic_update)

    def _on_cps_change(self, *_):
        self.core.set_cps(self.var_cps.get())

    def _on_button_change(self):
        self.core.set_button(self.var_button.get())

    def _on_double_toggle(self):
        self.core.set_double(self.var_double.get())

    def _on_hold_toggle(self):
        self.core.set_hold_mode(self.var_hold.get())

    def _gui_toggle(self):
        running = self.core.toggle_running()
        self.btn_toggle.config(text="Stop (T)" if running else "Start (T)")

    def _update_status(self):
        with self.core._lock:
            status = "RUNNING" if self.core._running or (self.core._hold_mode and self.core._hold_key_down) else "IDLE"
            btn_map = {Button.left:"Left", Button.middle:"Middle", Button.right:"Right"}
            status += f" | {btn_map[self.core._button]} | {self.core._cps:.1f} CPS | {'DOUBLE' if self.core._double_click else 'SINGLE'} | {'HOLD' if self.core._hold_mode else 'TOGGLE'}"
            self.var_status.set(status)

    def _periodic_update(self):
        self._update_status()
        self.after(150, self._periodic_update)

    def _on_key_press(self, key):
        try:
            if key == HOT_TOGGLE:
                if self.var_hold.get(): self.core.notify_hold_key(True)
                else: self._gui_toggle()
            elif key == HOT_QUIT: self._on_close()
            elif key == HOT_DOUBLE: self.var_double.set(not self.var_double.get()); self._on_double_toggle()
            elif key == HOT_HOLD: self.var_hold.set(not self.var_hold.get()); self._on_hold_toggle()
            elif key == HOT_BTN1: self.var_button.set(1); self._on_button_change()
            elif key == HOT_BTN2: self.var_button.set(2); self._on_button_change()
            elif key == HOT_BTN3: self.var_button.set(3); self._on_button_change()
            elif key == HOT_SPEED_UP: self.var_cps.set(min(200,self.var_cps.get()+1)); self._on_cps_change()
            elif key == HOT_SPEED_DOWN: self.var_cps.set(max(0.5,self.var_cps.get()-1)); self._on_cps_change()
        except: pass

    def _on_key_release(self, key):
        if key == HOT_TOGGLE and self.var_hold.get(): self.core.notify_hold_key(False)

    def _on_close(self):
        self.core.set_exit()
        try: self._kb_listener.stop()
        except: pass
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    core = AutoClickerCore()
    app = AutoClickerApp(core)
    app.mainloop()
