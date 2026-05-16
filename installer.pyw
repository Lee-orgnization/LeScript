import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import time
import threading

root = tk.Tk()
root.title("LeScript Installer")
root.geometry("600x500")

current_frame = None

def switch_frame(new_frame):
    global current_frame
    if current_frame is not None:
        current_frame.destroy()
    current_frame = new_frame
    current_frame.pack(fill="both", expand=True)


# ---------------------------------------------------------
# 1. START SCREEN
# ---------------------------------------------------------
def screen_start():
    frame = tk.Frame(root)

    tk.Label(frame, text="Welcome to the LeScript Installer", font=("Arial", 24)).pack(pady=40)
    tk.Label(frame, text="Powered by LS", font=("Arial", 14)).pack(pady=5)

    tk.Button(
        frame,
        text="Start",
        width=20,
        height=2,
        font=("Arial", 16),
        command=screen_terms
    ).pack(pady=20)

    switch_frame(frame)


# ---------------------------------------------------------
# 2. TERMS OF SERVICE SCREEN
# ---------------------------------------------------------
def screen_terms():
    frame = tk.Frame(root)

    tk.Label(frame, text="Terms of Use", font=("Arial", 22)).pack(pady=15)

    # Scrollable TOS box
    text_frame = tk.Frame(frame)
    text_frame.pack(pady=10, padx=20, fill="both", expand=True)

    tos_scroll = tk.Scrollbar(text_frame)
    tos_scroll.pack(side="right", fill="y")

    tos_box = tk.Text(
        text_frame,
        height=12,
        width=60,
        font=("Arial", 12),
        wrap="word",
        yscrollcommand=tos_scroll.set
    )
    tos_box.pack(side="left", fill="both", expand=True)
    tos_scroll.config(command=tos_box.yview)

    # EXTENDED TOS TEXT
    tos_box.insert("end",
        "LeScript (LS) Terms of Use\n"
        "-----------------------------------------\n\n"

        "DEFINITIONS\n"
        "For the purposes of this agreement:\n"
        "- 'Software' refers to the LeScript (LS) runtime, tools, modules, installer, and any related files.\n"
        "- 'Developer' refers to the creator and distributor of LeScript (LS).\n"
        "- 'User' refers to any individual installing, executing, or interacting with the Software.\n"
        "- 'System' refers to any device, hardware, operating system, or environment on which the Software is used.\n\n"

        "1. GENERAL DISCLAIMER\n"
        "The Software is provided on an experimental, developmental, and non-commercial basis. The Developer "
        "makes no guarantees regarding stability, reliability, compatibility, safety, or performance. The "
        "Software may contain defects, bugs, or unintended behavior.\n\n"

        "2. NO WARRANTY\n"
        "The Software is provided 'AS IS' without any warranties, express or implied. This includes, but is not "
        "limited to, warranties of merchantability, fitness for a particular purpose, non-infringement, accuracy, "
        "security, or performance. The User acknowledges that the Software may malfunction or behave unpredictably.\n\n"

        "3. LIMITATION OF LIABILITY\n"
        "The Developer shall not be held liable for any damages arising from the installation, use, misuse, or "
        "inability to use the Software. This includes, but is not limited to:\n"
        "- Data loss or corruption\n"
        "- System instability or crashes\n"
        "- Hardware degradation or malfunction\n"
        "- Registry or configuration damage\n"
        "- Security vulnerabilities or exposure\n"
        "- Unintended script execution or behavior\n"
        "- Any direct, indirect, incidental, or consequential damages\n\n"

        "4. USER RESPONSIBILITY\n"
        "The User is solely responsible for safeguarding their System, backing up data, and ensuring stability. "
        "The User installs and uses the Software voluntarily and at their own risk.\n\n"

        "5. EXPERIMENTAL NATURE OF LESCRIPT (LS)\n"
        "LeScript (LS) is an evolving technology. Features may change, break, or be removed without notice. "
        "Scripts may behave differently across versions. No compatibility guarantees are provided.\n\n"

        "6. NO SUPPORT OR MAINTENANCE\n"
        "The Developer is not obligated to provide updates, patches, support, or maintenance. Any updates that "
        "may be provided are voluntary and without guarantee.\n\n"

        "7. USER CONDUCT\n"
        "The User agrees not to use the Software for malicious, harmful, illegal, or unethical purposes. The "
        "Developer is not responsible for how the User chooses to use the Software.\n\n"

        "8. THIRD-PARTY INTERACTIONS\n"
        "The Software may interact with third-party components. The Developer is not responsible for conflicts, "
        "incompatibilities, or damages resulting from such interactions.\n\n"

        "9. HIGH-RISK USE WARNING\n"
        "The Software is not intended for use in environments where failure could result in injury, property "
        "damage, financial loss, or other significant harm. This includes, but is not limited to:\n"
        "- Medical systems\n"
        "- Safety-critical systems\n"
        "- Industrial control systems\n"
        "- Financial or commercial systems\n\n"

        "10. NO REVERSE ENGINEERING\n"
        "The User agrees not to reverse engineer, decompile, modify, or attempt to derive the internal workings "
        "of the Software. This restriction applies to all components, including the runtime, modules, and installer.\n\n"

        "11. NOT FOR PUBLIC DISTRIBUTION\n"
        "This Software is provided for private, experimental, and non-commercial use only. Redistribution, "
        "repackaging, or public release is prohibited without explicit permission from the Developer.\n\n"

        "12. GOVERNING LAW\n"
        "This agreement shall be governed by and interpreted in accordance with the laws applicable to the "
        "Developer's region of residence. Any disputes shall be resolved under that jurisdiction.\n\n"

        "13. SEVERABILITY\n"
        "If any part of this agreement is found to be invalid or unenforceable, the remaining sections shall "
        "remain in full effect.\n\n"

        "14. ACCEPTANCE OF TERMS\n"
        "By clicking 'I agree to the terms' and continuing with installation, the User confirms that they have "
        "read, understood, and accepted all terms listed above. If the User does not agree, they must select "
        "'I don't agree to the terms' and discontinue installation.\n\n"

        "This software is powered by LeScript (LS). All rights reserved.\n"
    )

    tos_box.config(state="disabled")

    # Radio buttons
    agree_var = tk.StringVar(value="no")

    tk.Radiobutton(
        frame,
        text="I don't agree to the terms",
        variable=agree_var,
        value="no",
        font=("Arial", 14)
    ).pack(anchor="w", padx=30)

    tk.Radiobutton(
        frame,
        text="I agree to the terms",
        variable=agree_var,
        value="yes",
        font=("Arial", 14)
    ).pack(anchor="w", padx=30)

    continue_btn = tk.Button(
        frame,
        text="Continue",
        width=20,
        height=2,
        font=("Arial", 14),
        state="disabled",
        command=screen_location
    )
    continue_btn.pack(pady=20)

    def update_button(*args):
        continue_btn.config(state="normal" if agree_var.get() == "yes" else "disabled")

    agree_var.trace_add("write", update_button)

    switch_frame(frame)


# ---------------------------------------------------------
# 3. INSTALL LOCATION SCREEN
# ---------------------------------------------------------
def screen_location():
    frame = tk.Frame(root)

    tk.Label(frame, text="Choose Install Location", font=("Arial", 22)).pack(pady=20)

    path_var = tk.StringVar(value="C:/Program Files/LeScript")

    entry = tk.Entry(frame, textvariable=path_var, width=50, font=("Arial", 14))
    entry.pack(pady=10)

    def browse():
        folder = filedialog.askdirectory()
        if folder:
            path_var.set(folder)

    tk.Button(frame, text="Browse", font=("Arial", 14), width=15, command=browse).pack(pady=5)

    tk.Button(
        frame,
        text="Continue",
        width=20,
        height=2,
        font=("Arial", 14),
        command=lambda: screen_download(path_var.get())
    ).pack(pady=20)

    switch_frame(frame)


# ---------------------------------------------------------
# 4. DOWNLOAD + INSTALL SCREEN
# ---------------------------------------------------------
def screen_download(install_path):
    frame = tk.Frame(root)

    tk.Label(frame, text="Installing Components", font=("Arial", 22)).pack(pady=20)

    current_label = tk.Label(frame, text="Installing: (waiting...)", font=("Arial", 14))
    current_label.pack(pady=10)

    progress = ttk.Progressbar(frame, length=400, mode="determinate")
    progress.pack(pady=10)

    # Details toggle
    details_visible = False
    details_frame = tk.Frame(frame)
    details_text = tk.Text(details_frame, height=8, width=60, font=("Arial", 10))
    details_text.pack()
    details_frame.pack_forget()

    def toggle_details():
        nonlocal details_visible
        if details_visible:
            details_frame.pack_forget()
            details_btn.config(text="Show Details")
        else:
            details_frame.pack(pady=10)
            details_btn.config(text="Hide Details")
        details_visible = not details_visible

    details_btn = tk.Button(frame, text="Show Details", font=("Arial", 12), command=toggle_details)
    details_btn.pack(pady=5)

    switch_frame(frame)

    # File list
    files = [
        "LS-Core/engine.ls",
        "LS-Core/runtime.dll",
        "LS-Modules/std.ls",
        "LS-Modules/io.ls",
        "LS-Modules/math.ls",
        "LS-Tools/installer-helper.exe",
        "LS-Tools/config.json",
        "LS-VM/virtual-machine.ls",
        "LS-VM/bytecode-handler.ls",
        "LS-VM/memory-manager.ls"
    ]

    def run_install():
        total = len(files)

        for index, file in enumerate(files):
            current_label.config(text=f"Installing: {file}")
            details_text.insert("end", f"Installing {file} to {install_path}...\n")
            details_text.see("end")

            # Smooth progress
            for p in range(0, 101, 4):
                progress["value"] = ((index / total) * 100) + (p / total)
                time.sleep(0.03)

        current_label.config(text="Installation Complete!")
        progress["value"] = 100
        details_text.insert("end", "\nAll components installed successfully.\n")
        details_text.see("end")

        time.sleep(0.5)
        screen_finish()

    threading.Thread(target=run_install, daemon=True).start()


# ---------------------------------------------------------
# 5. FINISH SCREEN
# ---------------------------------------------------------
def screen_finish():
    frame = tk.Frame(root)

    tk.Label(frame, text="Installation Complete", font=("Arial", 24)).pack(pady=40)
    tk.Label(frame, text="LeScript (LS) has been successfully installed.", font=("Arial", 14)).pack(pady=10)

    tk.Button(
        frame,
        text="Finish",
        width=20,
        height=2,
        font=("Arial", 16),
        command=root.destroy
    ).pack(pady=20)

    switch_frame(frame)


# ---------------------------------------------------------
# START INSTALLER
# ---------------------------------------------------------
screen_start()
root.mainloop()