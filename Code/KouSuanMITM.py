import threading
from mitmproxy import http
import json
import os
import time
import cv2
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import ttk
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

# 匹配的 URL 前缀
url_prefix = "https://xyks.yuanfudao.com/leo-game-pk/android/math/pk/match"

template_image = cv2.imread('QQ20241008-195310.png', 0)  
template_image2 = cv2.imread('QQ20241008-201026.png', 0)  
template_image3 = cv2.imread('continue.png', 0) 
template_image4 = cv2.imread('continuepk.png', 0) 
def perform_actions(questions):
    '''已经是最佳参数，请勿随意调整'''
    print("等待12.1秒...")
    time.sleep(12.2)

    print("开始根据答案执行操作，每0.2秒间隔一次...")
    for idx, question in enumerate(questions):  # 遍历所有题目
        answer = question.get("answer", None)

        # 根据答案执行相应的滑动操作
        if answer == ">":
            print(f"题目 {idx + 1}: 执行 '>' 滑动操作")
            os.system("adb shell input swipe 600 800 1000 900 0")
            os.system("adb shell input swipe 1000 900 600 1000 0")
        elif answer == "<":
            print(f"题目 {idx + 1}: 执行 '<' 滑动操作")
            os.system("adb shell input swipe 1000 800 600 900 0")
            os.system("adb shell input swipe 600 900 1000 1000 0")
        elif answer == "=":
            print(f"题目 {idx + 1}: 执行 '=' 滑动操作")
            os.system("adb shell input swipe 600 850 1000 850 0")
            os.system("adb shell input swipe 600 900 1000 900 0")
        else:
            print(f"题目 {idx + 1}: 未知答案 {answer}")

        time.sleep(0.2) 





# 定义模板匹配函数
def match_template(screen_image_gray, template_image, threshold=0.8):
    result = cv2.matchTemplate(screen_image_gray, template_image, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        return max_loc  # 返回匹配的左上角坐标
    return None

# Opencv进行灰度比较和OCR数字的识别
def process_image_and_control(stop_event):
    while not stop_event.is_set():
        try:

            os.system("adb exec-out screencap -p > screenshot.png")
            image = Image.open("screenshot.png")
            screen_image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            screen_image_gray = cv2.cvtColor(screen_image_np, cv2.COLOR_BGR2GRAY)

            # 模板匹配并点击
            for template, name in [(template_image, "template_image"),
                                   (template_image2, "template_image2"),
                                   (template_image3, "template_image3"),
                                   (template_image4, "template_image4")]:
                matched_location = match_template(screen_image_gray, template)
                if matched_location:
                    print(f"Matched {name} at: {matched_location}")
                    click_x = matched_location[0] + 25
                    click_y = matched_location[1] + 25
                    os.system(f"adb shell input tap {click_x} {click_y}")
        except Exception as e:
            print(f"Error in process_image_and_control: {e}")

        time.sleep(0.3)  # 最佳
        
        
        
        
def response(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_url.startswith(url_prefix):
        os.system('cls')  # 清除屏幕
        print(f"匹配到目标请求: {flow.request.pretty_url}")
        
        response_data = flow.response.text
        
        try:
            data = json.loads(response_data)
            
            point_name = data.get("examVO", {}).get("pointName", "未知")
            print(f"比赛名称: {point_name}")
            

            other_user_name = data.get("otherUser", {}).get("userName", "未知")
            other_user_id = data.get("otherUser", {}).get("userId", "未知")
            
            print(f"对手用户名: {other_user_name} ID: {other_user_id}")
            

            questions = data.get("examVO", {}).get("questions", [])
            print("题目答案：")
            for idx, question in enumerate(questions):
                answer = question.get("answer", "未知")
                content = question.get("content", "未知题目")
                print(f"题目 {idx + 1}: {content}，答案: {answer}")
            
            # 启动一个新线程来执行倒计时和操作，避免阻塞主线程
            action_thread = threading.Thread(target=perform_actions, args=(questions,))
            action_thread.start()

        except json.JSONDecodeError:
            print("响应数据不是合法的 JSON 格式")
        except Exception as e:
            print(f"解析响应数据时发生错误: {str(e)}")


stop_event = threading.Event()

def check_control_state(control_var):
    if control_var.get():
        print("Starting image control...")
        stop_event.clear()
        image_thread = threading.Thread(target=process_image_and_control, args=(stop_event,))
        image_thread.start()
    else:
        print("Stopping image control...")
        stop_event.set()

# 创建Tkinter界面
def create_gui():
    root = tk.Tk()
    root.wm_attributes("-topmost", True)
    root.resizable(0,0)
    root.attributes("-toolwindow", 2) 
    root.title("中间人mitm口算刷分")

    control_var = tk.BooleanVar(value=False)


    check_button = ttk.Checkbutton(root, text="启用自动比赛             ", variable=control_var, command=lambda: check_control_state(control_var))
    check_button.grid(row=0, column=0, padx=10, pady=10)


    root.mainloop()
    

threading.Thread(target=create_gui, daemon=True).start()
