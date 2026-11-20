"""ตั้งเวลาส่งไฟล์เข้ากลุ่ม LINE (ผ่าน LINE Messaging API)

บอท LINE ส่งไฟล์ทั่วไป (PDF, Excel, Word, zip ...) ตรงๆ ไม่ได้
สคริปต์นี้จึงส่ง "ลิงก์ไฟล์" เข้ากลุ่ม ซึ่งใช้ได้กับไฟล์ทุกประเภท
ถ้าเป็นรูป .jpg / .jpeg / .png จะส่งเป็นรูปให้เห็นในแชตด้วย

ก่อนใช้ ต้องตั้งค่า 2 อย่าง (ดูขั้นตอนใน LINE_SETUP.md):
    LINE_CHANNEL_ACCESS_TOKEN  = token ของบอท
    LINE_GROUP_ID              = รหัสกลุ่ม (ขึ้นต้นด้วย C...)

ตัวอย่าง:
    python3 line_schedule_send.py \
        --at "2026-11-21 08:00" \
        --file-url "https://drive.google.com/file/d/xxxx/view" \
        --message "ไฟล์รายงานประจำวันครับ"

ทดลองโดยไม่ส่งจริง: เติม --dry-run
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

PUSH_URL = "https://api.line.me/v2/bot/message/push"
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")


def build_messages(file_url, message):
    """สร้างรายการข้อความที่จะส่งเข้ากลุ่ม"""
    text = f"{message}\n📎 {file_url}" if message else f"📎 {file_url}"
    messages = [{"type": "text", "text": text}]

    # ถ้าลิงก์เป็นรูปโดยตรง ส่งเป็นรูปด้วย
    path = file_url.lower().split("?")[0]
    if path.endswith(IMAGE_EXTENSIONS):
        messages.append({
            "type": "image",
            "originalContentUrl": file_url,
            "previewImageUrl": file_url,
        })
    return messages


def push_to_group(token, group_id, messages):
    """ส่งข้อความเข้ากลุ่ม LINE"""
    body = json.dumps({"to": group_id, "messages": messages}).encode("utf-8")
    request = urllib.request.Request(
        PUSH_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            print(f"ส่งสำเร็จ (HTTP {response.status})")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        sys.exit(f"ส่งไม่สำเร็จ (HTTP {error.code}): {detail}")
    except urllib.error.URLError as error:
        sys.exit(f"เชื่อมต่อ LINE ไม่ได้: {error.reason}")


def wait_until(send_time):
    """รอจนถึงเวลาที่ตั้งไว้"""
    while True:
        remaining = (send_time - datetime.now()).total_seconds()
        if remaining <= 0:
            return
        hours, rest = divmod(int(remaining), 3600)
        minutes = rest // 60
        print(f"\rรออีก {hours} ชม. {minutes} นาที ... (กด Ctrl+C เพื่อยกเลิก)",
              end="", flush=True)
        time.sleep(min(remaining, 30))


def main():
    parser = argparse.ArgumentParser(description="ตั้งเวลาส่งไฟล์เข้ากลุ่ม LINE")
    parser.add_argument("--at", required=True,
                        help='เวลาส่ง เช่น "2026-11-21 08:00" (เวลาของเครื่องนี้)')
    parser.add_argument("--file-url", required=True,
                        help="ลิงก์ไฟล์ที่เปิดได้แบบสาธารณะ (https)")
    parser.add_argument("--message", default="", help="ข้อความที่จะส่งไปพร้อมไฟล์")
    parser.add_argument("--dry-run", action="store_true",
                        help="แสดงสิ่งที่จะส่ง แต่ไม่ส่งจริง")
    args = parser.parse_args()

    try:
        send_time = datetime.strptime(args.at, "%Y-%m-%d %H:%M")
    except ValueError:
        sys.exit('รูปแบบเวลาไม่ถูกต้อง ใช้แบบ "2026-11-21 08:00"')

    if not args.file_url.startswith("https://"):
        sys.exit("ลิงก์ไฟล์ต้องขึ้นต้นด้วย https://")

    messages = build_messages(args.file_url, args.message)
    print(f"จะส่งเวลา: {send_time:%d/%m/%Y %H:%M}")
    print("ข้อความ:", json.dumps(messages, ensure_ascii=False, indent=2))

    if args.dry_run:
        print("(dry-run: ไม่ได้ส่งจริง)")
        return

    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    group_id = os.environ.get("LINE_GROUP_ID")
    if not token or not group_id:
        sys.exit("ยังไม่ได้ตั้งค่า LINE_CHANNEL_ACCESS_TOKEN หรือ LINE_GROUP_ID "
                 "(ดู LINE_SETUP.md)")

    if send_time <= datetime.now():
        sys.exit("เวลาที่ตั้งผ่านไปแล้ว กรุณาเลือกเวลาในอนาคต")

    wait_until(send_time)
    print()
    push_to_group(token, group_id, messages)


if __name__ == "__main__":
    main()
