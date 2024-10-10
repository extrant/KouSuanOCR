import os
import time
import re
import threading
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from cnocr import CnOcr


# 初始化OCR
ocr = CnOcr(det_model_name='naive_det')


left_image = None
right_image = None
left_num = None
right_num = None
result = None
template_image = cv2.imread('QQ20241008-195310.png', 0)  
template_image2 = cv2.imread('QQ20241008-201026.png', 0)  



# 提取图像区域中的数字
def extract_number(image_area):
    """使用OCR识别图像区域中的数字，并清理结果"""
    try:
        ocr_results = ocr.ocr(image_area)
        print(f"OCR Results: {ocr_results}")
        text = "".join([result['text'] for result in ocr_results if 'text' in result]) if ocr_results else ""
        clean_text = re.sub(r'\D', '', text)
        return clean_text
    except Exception as e:
        print(f"Error in extract_number: {e}")
        return ""

# 匹配图片并获取坐标
def match_template(screen_image, template):
    """在屏幕截图中查找模板图像的位置"""
    try:
        result = cv2.matchTemplate(screen_image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.8:  # 如果匹配度超过0.8，认为匹配成功
            return max_loc  # 返回匹配区域的左上角坐标
        else:
            return None
    except Exception as e:
        print(f"Error in match_template: {e}")
        return None





# Opencv进行灰度比较和OCR数字的识别
def process_image_and_control():
    global left_image, right_image, left_num, right_num, result, found_target
    while True:
        try:
            # 截图并保存
            os.system("adb exec-out screencap -p > screenshot.png")
            image = Image.open("screenshot.png")
            screen_image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # 转换为OpenCV格式
            screen_image_gray = cv2.cvtColor(screen_image_np, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像

            # 调整左右数字区域坐标1920X1080
            left_num_area = image.crop((800, 300, 890, 400))
            right_num_area = image.crop((1034, 300, 1200, 400))

            # 保存左右截图
            left_image = left_num_area
            right_image = right_num_area

            # OCR识别提取数字
            left_num_text = extract_number(left_num_area)
            right_num_text = extract_number(right_num_area)
            print(f"Left Number: {left_num_text}, Right Number: {right_num_text}")

            # 检查是否符合期望
            if left_num_text.isdigit() and right_num_text.isdigit():
                left_num = int(left_num_text)
                right_num = int(right_num_text)
            else:
                left_num, right_num = None, None

            # 根据识别结果执行相应的操作
            if left_num is not None and right_num is not None:
                if left_num > right_num:
                    result = ">"
                    os.system("adb shell input swipe 600 800 1000 900 0")
                    os.system("adb shell input swipe 1000 900 600 1000 0")
                elif left_num < right_num:
                    result = "<"
                    os.system("adb shell input swipe 1000 800 600 900 0")
                    os.system("adb shell input swipe 600 900 1000 1000 0")
                else:
                    result = "="
                    os.system("adb shell input swipe 600 850 1000 850 0")
                    os.system("adb shell input swipe 600 900 1000 900 0")

            # 如果启用了图片匹配功能，执行匹配进行自动点击再练一次
            if match_enabled.get():  
                matched_location = match_template(screen_image_gray, template_image)
                matched_location1 = match_template(screen_image_gray, template_image2)
                if matched_location:
                    print(f"Matched at: {matched_location}")
                    click_x = matched_location[0] + 25
                    click_y = matched_location[1] + 25
                    os.system(f"adb shell input tap {click_x} {click_y}")
                if matched_location1:
                    print(f"Matched at: {matched_location1}")
                    click_x = matched_location1[0] + 25
                    click_y = matched_location1[1] + 25
                    os.system(f"adb shell input tap {click_x} {click_y}")

        except Exception as e:
            print(f"Error in process_image_and_control: {e}")
            left_num, right_num, result = None, None, "OCR失败"

        time.sleep(0.3) #最佳间隔


# 初始化Tkinter窗口
root = tk.Tk()
root.wm_attributes("-topmost", True)

root.resizable(0,0)
root.attributes("-toolwindow", 2) 
root.title("OCR口算刷分")


match_enabled = tk.BooleanVar(value=True)  # 默认为True，即开启图片匹配


match_checkbox = tk.Checkbutton(root, text="启用自动刷分", variable=match_enabled)
match_checkbox.pack()



left_label = tk.Label(root, text="左数值: None", font=("Helvetica", 16))
left_label.pack()

right_label = tk.Label(root, text="右数值: None", font=("Helvetica", 16))
right_label.pack()

result_label = tk.Label(root, text="比较结果: None", font=("Helvetica", 16))
result_label.pack()

left_image_label = tk.Label(root)
left_image_label.pack()

right_image_label = tk.Label(root)
right_image_label.pack()


def update_ui():
    global left_image, right_image, left_num, right_num, result
    if left_num is not None:
        left_label.config(text=f"左数值: {left_num}")
    else:
        left_label.config(text="左数值: None")

    if right_num is not None:
        right_label.config(text=f"右数值: {right_num}")
    else:
        right_label.config(text="右数值: None")

    if result:
        result_label.config(text=f"比较结果: {result}")
    else:
        result_label.config(text="比较结果: None")

    if left_image:
        left_img = ImageTk.PhotoImage(left_image)
        left_image_label.config(image=left_img)
        left_image_label.image = left_img

    if right_image:
        right_img = ImageTk.PhotoImage(right_image)
        right_image_label.config(image=right_img)
        right_image_label.image = right_img

# 多线程——>OCR以及opencv，防止影响主线程UI
threading.Thread(target=process_image_and_control, daemon=True).start()

# 循环定时更新UI
def refresh_ui():
    update_ui()
    root.after(300, refresh_ui)  #这里是UI刷新的时间 300ms

# 开始UI刷新
refresh_ui()

# 启动Tkinter主循环
root.mainloop()
