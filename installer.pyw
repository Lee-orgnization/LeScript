import os
import sys
import shutil
import zipfile
import threading
import requests
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox
import winshell
from win32com.client import Dispatch

# =========================================================
#  GLOBAL STATE
# =========================================================
INSTALL_STATE = {
    "path": None,
    "all_users": False
}

root = tk.Tk()
root.title("LeScript Installer")
root.geometry("600x400")

current_frame = None

def switch_frame(new_frame):
    global current_frame
    if current_frame is not None:
        current_frame.destroy()
    current_frame = new_frame
    current_frame.pack(fill="both", expand=True)

# =========================================================
#  ADMIN CHECK
# =========================================================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# =========================================================
#  ERROR HANDLING
# =========================================================
def translate_error(e):
    msg = str(e).lower()

    if "permission" in msg or "access" in msg or "denied" in msg:
        return (
            "The installer does not have permission to write to the selected folder.\n\n"
            "Try selecting a different install location or run the installer as administrator."
        )

    if "zip" in msg or "extract" in msg:
        return (
            "The installer could not extract the installation package.\n\n"
            "The downloaded ZIP may be corrupted or incomplete."
        )

    if "network" in msg or "connection" in msg:
        return (
            "The installer could not download required files.\n\n"
            "Please check your internet connection and try again."
        )

    if "disk" in msg or "space" in msg:
        return (
            "There is not enough disk space to complete the installation.\n\n"
            "Free some space and try again."
        )

    return f"An unexpected error occurred:\n\n{str(e)}"

def screen_error(message):
    frame = tk.Frame(root, padx=20, pady=20)

    tk.Label(frame, text="Installation Error", font=("Arial", 22), fg="red").pack(pady=20)

    tk.Label(
        frame,
        text=message,
        font=("Arial", 14),
        justify="center",
        wraplength=500
    ).pack(pady=10)

    tk.Button(
        frame,
        text="Back",
        font=("Arial", 14),
        width=12,
        command=lambda: screen_install_location()
    ).pack(pady=20)

    tk.Button(
        frame,
        text="Exit Installer",
        font=("Arial", 14),
        width=12,
        command=root.destroy
    ).pack(pady=10)

    switch_frame(frame)

# =========================================================
#  START MENU SHORTCUT
# =========================================================
def create_start_menu_shortcut(install_path, all_users=False):
    try:
        import os
        import winshell
        from win32com.client import Dispatch
        import sys

        if all_users:
            start_menu = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
        else:
            start_menu = winshell.start_menu()

        shortcut_path = os.path.join(start_menu, "LeScript.lnk")

        script = os.path.join(install_path, "launcher.py")
        python = sys.executable  # uses current Python install

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)

        shortcut.Targetpath = python
        shortcut.Arguments = f'"{script}"'
        shortcut.WorkingDirectory = install_path
        shortcut.IconLocation = python
        shortcut.save()

        return True

    except Exception as e:
        print("Shortcut creation failed:", e)
        return False

# =========================================================
#  SCREENS
# =========================================================
def screen_admin():
    frame = tk.Frame(root, padx=20, pady=20)

    tk.Label(
        frame,
        text="Administrator privileges are recommended.\n\n"
             "Without admin rights, installation may fail\n"
             "when writing to protected folders.",
        font=("Arial", 14),
        justify="center"
    ).pack(pady=20, fill="x")

    btns = tk.Frame(frame)
    btns.pack(pady=10)

    def exit_app():
        root.destroy()

    def run_as_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

    def continue_anyway():
        screen_home()

    tk.Button(btns, text="Exit", width=12, command=exit_app).grid(row=0, column=0, padx=10)

    admin_btn = tk.Button(btns, text="Run as Admin", width=15, command=run_as_admin)
    admin_btn.grid(row=0, column=1, padx=10)

    if is_admin():
        admin_btn.config(state="disabled")

    tk.Button(
        frame,
        text="Continue Anyway (NOT RECOMMENDED)",
        fg="red",
        width=35,
        command=continue_anyway
    ).pack(pady=10)

    switch_frame(frame)

def screen_home():
    frame = tk.Frame(root, padx=20, pady=20)

    tk.Label(
        frame,
        text="Welcome to the LeScript Installer",
        font=("Arial", 24),
        justify="center",
        anchor="center"
    ).pack(pady=40, fill="x")

    btns = tk.Frame(frame)
    btns.pack(pady=20)

    tk.Button(
        btns,
        text="Start",
        font=("Arial", 16),
        width=12,
        command=screen_terms
    ).pack(side="left", padx=20)

    tk.Button(
        btns,
        text="Exit",
        font=("Arial", 14),
        width=12,
        command=root.destroy
    ).pack(side="left", padx=20)

    switch_frame(frame)

def screen_terms():
    frame = tk.Frame(root, padx=20, pady=20)

    tk.Label(
        frame,
        text="Terms of Service",
        font=("Arial", 22)
    ).pack(pady=(5, 20), fill="x")

    tos_text = """LeScript Installer – Terms of Service (TOS)

These Terms govern your use of the LeScript Installer, LeScript Runtime, LeScript Language, and all
associated components, files, scripts, and services (“LeScript”). By installing, executing, or
interacting with LeScript in any capacity, you acknowledge that you have read, understood, and
agreed to these Terms. If you do not agree, you must not install or use LeScript.

1. License & Usage
LeScript is provided for personal, educational, and non-commercial use. You may install and run
LeScript on your device, but you may not redistribute the installer, runtime, or any modified
versions. You may not reverse-engineer, decompile, disassemble, or attempt to derive the source
code of any compiled components unless explicitly permitted. You may not claim LeScript as your
own work or represent it as an official product of any organization. You may not use LeScript in
any environment where failure, malfunction, or unexpected behavior could result in physical harm,
property damage, or significant financial loss.

2. Acceptable Use
You agree not to use LeScript for harmful, malicious, or illegal purposes. This includes, but is
not limited to: creating malware, exploiting systems, bypassing security mechanisms, distributing
harmful code, violating the terms of other platforms or services, or engaging in activities that
could disrupt networks, devices, or users. You are solely responsible for any actions performed
using LeScript. You acknowledge that misuse of LeScript may result in legal consequences, account
restrictions, or system damage.

3. No Warranty
LeScript is provided “AS IS” without any warranties, express or implied. This includes, but is not
limited to, warranties of performance, reliability, stability, compatibility, security, or fitness
for a particular purpose. The developer(s) make no guarantees that LeScript will function correctly,
remain available, or operate without errors. You acknowledge that software may contain bugs,
unexpected behavior, or limitations that could affect performance.

4. Limitation of Liability
Under no circumstances shall the developer(s) be held liable for any damages arising from the use
or inability to use LeScript. This includes, but is not limited to: data loss, corrupted files,
system instability, hardware damage, security breaches, financial loss, downtime, or any other
direct or indirect damages. You assume full responsibility for all risks associated with installing
and using LeScript. You agree that the total liability of the developer(s), if any, shall not
exceed zero dollars ($0.00).

5. System Modifications
The installer may create directories, write files, modify environment variables, adjust system
paths, or install runtime components. These actions are required for LeScript to function. By
continuing, you grant permission for the installer to perform these modifications. You understand
that uninstalling LeScript may not automatically revert all changes. You acknowledge that system
modifications may affect other software, scripts, or configurations on your device.

6. Updates, Changes, and Discontinuation
The developer(s) reserve the right to update, modify, or discontinue LeScript at any time without
notice. Features may be added, removed, or altered. Continued use of LeScript after updates implies
acceptance of any revised Terms. You acknowledge that updates may change functionality, behavior,
or compatibility with existing projects.

7. Data Handling
LeScript does not intentionally collect personal data. However, logs, crash reports, or diagnostic
information may be generated locally on your device. You are responsible for managing, deleting,
or securing these files. The developer(s) are not responsible for any data exposure resulting from
user actions, system vulnerabilities, or third-party software.

8. Third-Party Dependencies
LeScript may rely on third-party libraries, runtimes, or external services. These components are
subject to their own licenses and terms. You agree to comply with all third-party requirements and
acknowledge that the developer(s) are not responsible for issues arising from third-party software.
You acknowledge that third-party updates may affect LeScript’s functionality.

9. User Responsibility & Compliance
You agree to comply with all applicable laws, regulations, and platform rules when using LeScript.
You acknowledge that misuse of LeScript may result in legal consequences, account restrictions,
or system damage. You accept full responsibility for your actions and agree that the developer(s)
are not responsible for any misuse or violations committed using LeScript.

10. Security
You acknowledge that no software is completely secure. You agree to take reasonable precautions
when running scripts, installing packages, or interacting with external code. You understand that
LeScript cannot guarantee protection against malicious input, unsafe code, or harmful operations.

11. Termination
The developer(s) may revoke your permission to use LeScript at any time if you violate these Terms.
You may also terminate your agreement by uninstalling LeScript and deleting all related files.
Continued use of LeScript after termination is prohibited.

12. Agreement
By clicking Continue, you confirm that:
• You have read these Terms.
• You understand these Terms.
• You agree to be bound by these Terms.

If you do NOT agree, select “I do NOT accept” and exit the installer immediately.
"""

    terms_box = tk.Text(frame, width=60, height=10, wrap="word")
    terms_box.insert("end", tos_text)
    terms_box.config(state="disabled")
    terms_box.pack(fill="both", expand=True, pady=10)

    choice = tk.IntVar(value=0)

    radio_row = tk.Frame(frame)
    radio_row.pack(fill="x", pady=(10, 40))

    left = tk.Frame(radio_row)
    left.pack(side="left", padx=10)

    tk.Radiobutton(
        left,
        text="I accept the terms",
        variable=choice,
        value=1,
        font=("Arial", 12)
    ).pack(anchor="w", pady=5)

    tk.Radiobutton(
        left,
        text="I do NOT accept the terms",
        variable=choice,
        value=0,
        font=("Arial", 12)
    ).pack(anchor="w", pady=5)

    def continue_if_accepted():
        if choice.get() == 1:
            screen_install_location()
        else:
            messagebox.showwarning("Terms Required", "You must accept the terms to continue.")

    tk.Button(
        radio_row,
        text="Continue",
        font=("Arial", 14),
        width=12,
        command=continue_if_accepted
    ).pack(side="right", padx=20)

    switch_frame(frame)

def screen_warning_all_users(path):
    frame = tk.Frame(root, padx=20, pady=20)

    tk.Label(frame, text="Administrator Recommended", font=("Arial", 22)).pack(pady=20)

    tk.Label(
        frame,
        text="You selected 'Install for ALL users' but the installer\n"
             "is NOT running with administrator privileges.\n\n"
             "Installation may fail when writing to protected folders.\n"
             "You may continue, but admin rights are recommended.",
        font=("Arial", 14),
        justify="center"
    ).pack(pady=10)

    btns = tk.Frame(frame)
    btns.pack(pady=20)

    tk.Button(
        btns,
        text="Back",
        font=("Arial", 14),
        width=12,
        command=lambda: screen_install_location()
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        btns,
        text="Continue Anyway",
        font=("Arial", 14),
        width=18,
        fg="red",
        command=lambda: screen_ready()
    ).grid(row=0, column=1, padx=10)

    switch_frame(frame)

def screen_install_location():
    frame = tk.Frame(root, padx=20, pady=20)

    tk.Label(frame, text="Choose Install Location", font=("Arial", 22)).pack(pady=(40, 20), fill="x")

    default_path = "C:/LeScript"
    path_var = tk.StringVar(value=default_path)

    tk.Entry(frame, textvariable=path_var).pack(fill="x", padx=20, pady=20)

    install_user = tk.BooleanVar(value=True)
    install_all = tk.BooleanVar(value=False)

    def toggle_user():
        if install_user.get():
            install_all.set(False)

    def toggle_all():
        if install_all.get():
            install_user.set(False)

    tk.Checkbutton(
        frame,
        text="Install ONLY for this user",
        variable=install_user,
        command=toggle_user,
        font=("Arial", 12)
    ).pack(anchor="w", padx=20)

    tk.Checkbutton(
        frame,
        text="Install for ALL users",
        variable=install_all,
        command=toggle_all,
        font=("Arial", 12)
    ).pack(anchor="w", padx=20)

    def next_step():
        INSTALL_STATE["path"] = path_var.get()
        INSTALL_STATE["all_users"] = install_all.get()

        if INSTALL_STATE["all_users"] and not is_admin():
            screen_warning_all_users(INSTALL_STATE["path"])
            return

        screen_ready()

    tk.Button(
        frame,
        text="Next",
        font=("Arial", 14),
        command=next_step
    ).pack(pady=20)

    switch_frame(frame)

def screen_ready():
    path = INSTALL_STATE["path"]
    all_users = INSTALL_STATE["all_users"]

    frame = tk.Frame(root, padx=20, pady=20)

    tk.Label(frame, text="Ready to Install", font=("Arial", 22)).pack(pady=20, fill="x")

    mode = "All Users" if all_users else "Current User Only"

    tk.Label(
        frame,
        text=f"Install Location:\n{path}\n\nMode: {mode}",
        font=("Arial", 14),
        justify="center"
    ).pack(fill="x", pady=10)

    tk.Button(
        frame,
        text="Install",
        font=("Arial", 14),
        command=screen_install
    ).pack(pady=20)

    switch_frame(frame)

def screen_install():
    path = INSTALL_STATE["path"]
    all_users = INSTALL_STATE["all_users"]

    frame = tk.Frame(root, padx=20, pady=20)

    tk.Label(frame, text="Installing Components", font=("Arial", 22)).pack(pady=20, fill="x")

    status = tk.Label(frame, text="Starting...", font=("Arial", 14))
    status.pack(fill="x", pady=10)

    bar = ttk.Progressbar(frame, length=400, mode="determinate")
    bar.pack(fill="x", padx=20, pady=10)

    switch_frame(frame)

    ZIP_URL = "https://github.com/Lee-orgnization/LeScript/archive/refs/heads/main.zip"
    TEMP_ZIP = "lescript_temp.zip"

    def run():
        try:
            # Download
            status.config(text="Downloading package...")
            r = requests.get(ZIP_URL, stream=True)
            total = int(r.headers.get("content-length", 0))
            done = 0

            with open(TEMP_ZIP, "wb") as f:
                for chunk in r.iter_content(8192):
                    if chunk:
                        f.write(chunk)
                        done += len(chunk)
                        if total > 0:
                            bar["value"] = (done / total) * 33

            # Extract
            status.config(text="Extracting files...")
            with zipfile.ZipFile(TEMP_ZIP, "r") as z:
                files = z.namelist()
                for i, file in enumerate(files):
                    z.extract(file, "extract")
                    bar["value"] = 33 + (i / len(files)) * 33

            folder = os.path.join("extract", os.listdir("extract")[0])

            # Copy
            status.config(text="Copying files...")
            all_files = []
            for root_dir, dirs, files in os.walk(folder):
                for file in files:
                    all_files.append(os.path.join(root_dir, file))

            for i, src in enumerate(all_files):
                rel = os.path.relpath(src, folder)
                dest = os.path.join(path, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(src, dest)
                bar["value"] = 66 + (i / len(all_files)) * 34

            # Cleanup
            try:
                os.remove(TEMP_ZIP)
            except Exception:
                pass
            try:
                shutil.rmtree("extract")
            except Exception:
                pass

            # Create Start Menu shortcut
            create_start_menu_shortcut(path, all_users)

            screen_finish()

        except Exception as e:
            screen_error(translate_error(e))

    threading.Thread(target=run, daemon=True).start()

def screen_finish():
    frame = tk.Frame(root, padx=20, pady=20)

    tk.Label(
        frame,
        text="Installation Complete!",
        font=("Arial", 22),
        justify="center"
    ).pack(pady=20, fill="x")

    tk.Button(
        frame,
        text="Close",
        font=("Arial", 14),
        command=root.destroy
    ).pack(pady=20)

    switch_frame(frame)

# =========================================================
#  STARTUP
# =========================================================
if is_admin():
    screen_home()
else:
    screen_admin()

root.mainloop()