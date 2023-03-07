import ctypes
import  win32api
import  win32gui



def get_layout():
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    print(pf)
    if hex(pf(0)) == '0x4190419':
        print("ru-change(english)")
        window_handle = win32gui.GetForegroundWindow()
        result = win32api.SendMessage(window_handle, 0x0050, 0, 0x04090409)
        print(result)
        # keyboard.press_and_release('shift + alt')
        # return 'ru'
    if hex(pf(0)) == '0x4090409':
        print("en-normal")
        # return 'en'
get_layout()