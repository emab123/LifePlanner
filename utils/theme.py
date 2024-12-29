import sv_ttk
import ctypes

def set_theme(theme_name):
    sv_ttk.set_theme(theme_name)
    set_title_bar_color(theme_name)

def set_title_bar_color(theme_name):
    if theme_name == "dark":
        color = "#333333"
    else:
        color = "#FFFFFF"
    
    # Set the title bar color for Windows
    try:
        ctypes.windll.dwmapi.DwmSetWindowAttribute.argtypes = (ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.c_uint)
        hwnd = ctypes.windll.user32.GetParent(ctypes.windll.user32.GetForegroundWindow())
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = 1 if theme_name == "dark" else 0
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(value)), ctypes.sizeof(ctypes.c_int))
    except Exception as e:
        print(f"Failed to set title bar color: {e}")