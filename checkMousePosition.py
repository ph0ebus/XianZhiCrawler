import pyautogui
import time

try:
    while True:
        # 获取当前鼠标位置
        x, y = pyautogui.position()
        
        # 实时输出鼠标坐标
        print(f"\rMouse position: X={x}, Y={y}",end="")
        
        # 暂停0.1秒以避免过快输出
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nScript stopped.")
