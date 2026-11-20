# ตั้งค่าบอท LINE เพื่อส่งไฟล์เข้ากลุ่ม

ทำครั้งเดียว ใช้เวลาประมาณ 15 นาที

## 1. สร้างบอท (Messaging API channel)
1. เข้า https://developers.line.biz/console/ แล้วล็อกอินด้วยบัญชี LINE
2. สร้าง **Provider** (ตั้งชื่ออะไรก็ได้)
3. กด **Create a new channel** → เลือก **Messaging API** → กรอกข้อมูลให้ครบ
4. ในแท็บ **Messaging API**:
   - เลื่อนลงไปที่ **Channel access token** → กด **Issue** → คัดลอกเก็บไว้ (นี่คือ `LINE_CHANNEL_ACCESS_TOKEN`)
   - ตรง **Allow bot to join group chats** → กด Edit → เปิดเป็น **Enabled**

## 2. หา Group ID
LINE ไม่แสดง Group ID ในแอป ต้องดูจาก webhook:
1. เปิด https://webhook.site แล้วคัดลอก URL ที่ได้ (Your unique URL)
2. ในแท็บ **Messaging API** → **Webhook URL** → วาง URL นั้น → เปิด **Use webhook**
3. ในแอป LINE เพิ่มบอทเป็นเพื่อน (สแกน QR ในหน้า Messaging API) แล้ว **เชิญบอทเข้ากลุ่ม**
4. พิมพ์อะไรก็ได้ในกลุ่ม
5. กลับไปที่ webhook.site จะเห็นข้อมูลเข้ามา ให้หา `"groupId": "C......"` → คัดลอกไว้ (นี่คือ `LINE_GROUP_ID`)
6. หาเสร็จแล้วปิด **Use webhook** ได้เลย

## 3. อัปโหลดไฟล์ให้มีลิงก์
บอทส่งไฟล์ทั่วไปตรงๆ ไม่ได้ เลยต้องส่งเป็นลิงก์:
- Google Drive: คลิกขวาที่ไฟล์ → แชร์ → **ทุกคนที่มีลิงก์** → คัดลอกลิงก์
- หรือ Dropbox / OneDrive ก็ได้

## 4. ตั้งเวลาส่ง
macOS / Linux:
```bash
export LINE_CHANNEL_ACCESS_TOKEN="token ที่ได้จากข้อ 1"
export LINE_GROUP_ID="Cxxxxxxxx"
python3 line_schedule_send.py --at "2026-11-21 08:00" --file-url "ลิงก์ไฟล์" --message "ข้อความ"
```

Windows (PowerShell):
```powershell
$env:LINE_CHANNEL_ACCESS_TOKEN="token ที่ได้จากข้อ 1"
$env:LINE_GROUP_ID="Cxxxxxxxx"
python line_schedule_send.py --at "2026-11-21 08:00" --file-url "ลิงก์ไฟล์" --message "ข้อความ"
```

**สำคัญ:** ต้องเปิดหน้าต่างนี้และเปิดเครื่องไว้จนถึงเวลาส่ง (อย่าให้เครื่องเข้าโหมด sleep)

## ข้อควรรู้
- ห้ามแชร์ token ให้คนอื่น และห้าม commit token ลง Git
- บัญชีฟรีส่งได้ประมาณ 200 ข้อความต่อเดือน (นับตามจำนวนสมาชิกในกลุ่ม: กลุ่ม 20 คน ส่ง 1 ครั้ง = ใช้ไป 20)
- ทดลองก่อนได้โดยเติม `--dry-run` (ไม่ส่งจริง)
