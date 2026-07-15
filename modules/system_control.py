import os
import subprocess
import platform
import psutil

SYSTEM = platform.system()  # "Windows" / "Linux" / "Darwin"


# ── Volume ────────────────────────────────────────────────────
def set_volume(level: int):
    """level: 0–100"""
    if SYSTEM == "Windows":
        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            import comtypes
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        except Exception as e:
            print(f"Volume error: {e}")
    elif SYSTEM == "Linux":
        os.system(f"amixer sset Master {level}%")


def mute_volume():
    if SYSTEM == "Windows":
        os.system("nircmd.exe mutesysvolume 1")
    elif SYSTEM == "Linux":
        os.system("amixer sset Master toggle")


# ── Brightness ────────────────────────────────────────────────
def set_brightness(level: int):
    """level: 0–100"""
    try:
        import screen_brightness_control as sbc
        sbc.set_brightness(level)
    except Exception as e:
        print(f"Brightness error: {e}")


# ── Apps ──────────────────────────────────────────────────────
APP_MAP = {
    "notepad":   {"Windows": "notepad.exe",        "Linux": "gedit"},
    "browser":   {"Windows": "start chrome",       "Linux": "google-chrome"},
    "calculator":{"Windows": "calc.exe",           "Linux": "gnome-calculator"},
    "explorer":  {"Windows": "explorer.exe",       "Linux": "nautilus"},
    "spotify":   {"Windows": "spotify.exe",        "Linux": "spotify"},
    "vscode":    {"Windows": "code",               "Linux": "code"},
}


def open_app(app_name: str) -> str:
    app_name = app_name.lower()
    if app_name in APP_MAP:
        cmd = APP_MAP[app_name].get(SYSTEM, "")
        if cmd:
            subprocess.Popen(cmd, shell=True)
            return f"Opening {app_name}."
    return f"I don't know how to open {app_name} yet."


def close_app(app_name: str) -> str:
    for proc in psutil.process_iter(["name"]):
        if app_name.lower() in proc.info["name"].lower():
            proc.kill()
            return f"Closed {app_name}."
    return f"{app_name} is not running."


# ── Power ─────────────────────────────────────────────────────
def shutdown(delay: int = 30):
    if SYSTEM == "Windows":
        os.system(f"shutdown /s /t {delay}")
    elif SYSTEM == "Linux":
        os.system(f"shutdown -h +{delay//60}")


def restart():
    if SYSTEM == "Windows":
        os.system("shutdown /r /t 5")
    elif SYSTEM == "Linux":
        os.system("reboot")


def cancel_shutdown():
    if SYSTEM == "Windows":
        os.system("shutdown /a")
    elif SYSTEM == "Linux":
        os.system("shutdown -c")
