import tkinter as tk
from tkinter import filedialog, messagebox
from pynput import keyboard, mouse


# ---------------------------------------------------------
# Bubble Button (non-draggable, clean)
# ---------------------------------------------------------
class BubbleButton(tk.Canvas):
    def __init__(self, master, text, command, size=120):
        super().__init__(master, width=size, height=size, highlightthickness=0, bg="black")

        self.size = size
        self.command = command

        # Draw circle
        self.circle = self.create_oval(
            5, 5, size - 5, size - 5,
            fill="black",
            outline="red",
            width=4
        )

        # Add text
        self.label = self.create_text(
            size // 2, size // 2,
            text=text,
            fill="red",
            font=("Arial", 16, "bold")
        )

        # LEFT CLICK = activate button
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        self.command()


# ---------------------------------------------------------
# LeLogger Main Class (with movement settle fix)
# ---------------------------------------------------------
class LeLogger:
    def __init__(self):
        self.section_count = 0
        self.current_section = None
        self.lines = []
        self.imports = set()
        self.recording = False

        # Movement settle system
        self.move_pending = None
        self.move_timer = None

        # GUI Setup
        self.root = tk.Tk()
        self.root.title("LeLogger")
        self.root.configure(bg="black")
        self.root.geometry("500x300")

        # Bubble buttons
        self.start_btn = BubbleButton(self.root, "START", self.start_section)
        self.start_btn.place(x=50, y=100)

        self.stop_btn = BubbleButton(self.root, "STOP", self.stop_recording)
        self.stop_btn.place(x=190, y=100)

        self.save_btn = BubbleButton(self.root, "SAVE", self.save_script_dialog)
        self.save_btn.place(x=330, y=100)

        # Status label
        self.status = tk.Label(self.root, text="Idle", fg="red", bg="black", font=("Arial", 12))
        self.status.pack(pady=10)

        # Start listeners
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)

        self.keyboard_listener.start()
        self.mouse_listener.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    # ---------------------------------------------------------
    # Recording Control (fixed)
    # ---------------------------------------------------------
    def start_section(self):
        if self.recording:
            self.status.config(text="Already recording — press STOP first")
            return

        self.section_count += 1
        self.current_section = f"Auto{self.section_count}"
        self.lines.append(f"\nSection:{self.current_section}()")

        self.recording = True
        self.status.config(text=f"Recording: {self.current_section}")

    def stop_recording(self):
        if not self.recording:
            self.status.config(text="Not recording")
            return

        self.recording = False
        self.current_section = None
        self.status.config(text="Stopped")

    # ---------------------------------------------------------
    # Event Handlers
    # ---------------------------------------------------------
    def on_key_press(self, key):
        if not self.recording or self.current_section is None:
            return

        try:
            if hasattr(key, "char") and key.char is not None:
                k = key.char.upper()
            else:
                k = str(key).replace("Key.", "").upper()
        except:
            k = str(key)

        cmd = f'press "{k}"'
        self.record_command(cmd)

    def on_click(self, x, y, button, pressed):
        if not self.recording or self.current_section is None:
            return
        if not pressed:
            return

        btn = str(button).replace("Button.", "").lower()
        cmd = f'click "{btn}" :{x},{y}'
        self.record_command(cmd)

    # ---------------------------------------------------------
    # Movement Settle System (final fix)
    # ---------------------------------------------------------
    def on_move(self, x, y):
        if not self.recording or self.current_section is None:
            return

        # Store latest mouse position
        self.move_pending = (x, y)

        # Reset timer
        if self.move_timer is not None:
            self.root.after_cancel(self.move_timer)

        # Wait 100ms after last movement
        self.move_timer = self.root.after(100, self.commit_move)

    def commit_move(self):
        if self.move_pending is None:
            return

        x, y = self.move_pending
        self.record_command(f"move :{x},{y}")

        # Reset
        self.move_pending = None
        self.move_timer = None

    # ---------------------------------------------------------
    # Core Logic
    # ---------------------------------------------------------
    def record_command(self, cmd):
        if cmd.startswith("press") or cmd.startswith("release"):
            self.imports.add('import "keyboard" : Key')

        if cmd.startswith("move") or cmd.startswith("click"):
            self.imports.add('import "mouse" : Mouse')

        if cmd.startswith("wait"):
            self.imports.add('import "Default"')

        if self.current_section:
            self.lines.append(f"    {cmd}")

    # ---------------------------------------------------------
    # Saving
    # ---------------------------------------------------------
    def save_script_dialog(self):
        if not self.lines:
            messagebox.showwarning("Nothing to save", "No recorded commands.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".les",
            filetypes=[("LeScript files", "*.les"), ("All files", "*.*")]
        )
        if not file_path:
            return

        self.save_script(file_path)

    def save_script(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            for imp in sorted(self.imports):
                f.write(imp + "\n")

            f.write("\n")

            for line in self.lines:
                f.write(line + "\n")

        messagebox.showinfo("Saved", f"Script saved as:\n{filename}")

    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------
    def on_close(self):
        try:
            self.keyboard_listener.stop()
            self.mouse_listener.stop()
        except:
            pass
        self.root.destroy()


# Run LeLogger
LeLogger()