# เกมทายตัวเลข (แบบมีหน้าต่าง GUI)
# วิธีรัน:  python3 guess_number_gui.py
#
# สิ่งที่ได้เรียนจากไฟล์นี้:
#   - import      : ดึงเครื่องมือที่คนอื่นเขียนไว้มาใช้
#   - def         : สร้างฟังก์ชัน (ชุดคำสั่งที่ตั้งชื่อไว้เรียกใช้ซ้ำ)
#   - if/elif/else: ให้โปรแกรมตัดสินใจ
#   - try/except  : ดักจับข้อผิดพลาด เช่น ผู้ใช้พิมพ์ตัวอักษรแทนตัวเลข

import random            # ใช้สุ่มตัวเลข
import tkinter as tk     # ใช้สร้างหน้าต่างโปรแกรม

MIN_NUMBER = 1
MAX_NUMBER = 100

secret = random.randint(MIN_NUMBER, MAX_NUMBER)  # ตัวเลขลับที่ต้องทาย
tries = 0                                         # จำนวนครั้งที่ทายไปแล้ว


def check_guess(event=None):
    """ทำงานเมื่อกดปุ่ม "ทาย" หรือกด Enter"""
    global tries

    text = entry.get()
    entry.delete(0, tk.END)  # ล้างช่องกรอกให้พร้อมทายครั้งต่อไป

    # แปลงข้อความเป็นตัวเลข ถ้าแปลงไม่ได้ให้เตือนผู้ใช้
    try:
        guess = int(text)
    except ValueError:
        message.config(text="⚠️ กรุณาพิมพ์ตัวเลขเท่านั้น", fg="orange")
        return

    if guess < MIN_NUMBER or guess > MAX_NUMBER:
        message.config(text=f"⚠️ ต้องอยู่ระหว่าง {MIN_NUMBER} ถึง {MAX_NUMBER}", fg="orange")
        return

    tries = tries + 1
    tries_label.config(text=f"ทายไปแล้ว: {tries} ครั้ง")

    if guess < secret:
        message.config(text=f"{guess} น้อยไป ⬆️ ลองมากกว่านี้", fg="blue")
    elif guess > secret:
        message.config(text=f"{guess} มากไป ⬇️ ลองน้อยกว่านี้", fg="red")
    else:
        message.config(text=f"🎉 ถูกต้อง! เลขคือ {secret} ใช้ไป {tries} ครั้ง", fg="green")
        guess_button.config(state=tk.DISABLED)
        entry.config(state=tk.DISABLED)


def new_game():
    """เริ่มเกมใหม่: สุ่มเลขใหม่และรีเซ็ตทุกอย่าง"""
    global secret, tries
    secret = random.randint(MIN_NUMBER, MAX_NUMBER)
    tries = 0
    entry.config(state=tk.NORMAL)
    guess_button.config(state=tk.NORMAL)
    tries_label.config(text="ทายไปแล้ว: 0 ครั้ง")
    message.config(text="เริ่มเกมใหม่แล้ว! ลองทายดูเลย", fg="black")
    entry.focus()


# ---------- สร้างหน้าต่าง ----------
window = tk.Tk()
window.title("เกมทายตัวเลข")
window.geometry("380x260")

title = tk.Label(window, text=f"ทายตัวเลข {MIN_NUMBER} - {MAX_NUMBER}", font=("Arial", 18, "bold"))
title.pack(pady=10)

entry = tk.Entry(window, font=("Arial", 16), justify="center", width=8)
entry.pack()
entry.bind("<Return>", check_guess)  # กด Enter ก็ทายได้
entry.focus()

guess_button = tk.Button(window, text="ทาย", font=("Arial", 14), command=check_guess)
guess_button.pack(pady=8)

message = tk.Label(window, text="พิมพ์ตัวเลขแล้วกด ทาย", font=("Arial", 13))
message.pack()

tries_label = tk.Label(window, text="ทายไปแล้ว: 0 ครั้ง", font=("Arial", 11))
tries_label.pack(pady=4)

tk.Button(window, text="เล่นใหม่", command=new_game).pack(pady=6)

window.mainloop()  # เปิดหน้าต่างค้างไว้จนกว่าผู้ใช้จะปิด
