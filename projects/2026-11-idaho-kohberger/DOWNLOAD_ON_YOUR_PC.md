# تنزيل اللقطات على جهازك (يوتيوب يحجب السيرفر)

## 1) التجهيز (مرة وحدة)
```bash
pip install yt-dlp
# وثبّت ffmpeg: Windows: winget install ffmpeg | Mac: brew install ffmpeg
git clone <repo> && cd NE && git checkout ccr-51f18763-tkfo4g
```

## 2) التنزيل (54 فيديو، حوالي 40 ساعة)
```bash
python3 tools/download_assets.py projects/2026-11-idaho-kohberger
```
كل ملف ينحفظ باسم رقمه (مثل `C020.mp4`) داخل `projects/2026-11-idaho-kohberger/footage/raw/`.
لو فشل أي ملف، أعد التشغيل بهذا الأمر:
```bash
python3 tools/download_assets.py projects/2026-11-idaho-kohberger --retry-failed
```

## 3) ملفات شرطة ولاية آيداهو (ISP) — من المتصفح
افتح https://isp.idaho.gov/Moscow ثم "LINK TO PUBLIC RECORDS". نزّل كل الطلبات المنشورة الخاصة بالقضية (Moscow homicide): الوثائق وحوالي 2,780 صورة. حطها في مجلد اسمه `ISP`.

## 4) الرفع لي
ارفع مجلد `footage/raw` ومجلد `ISP` إلى Google Drive، وخل المشاركة "أي شخص لديه الرابط"، وأرسل لي الرابط. أنا أسحبها بالأمر:
`python3 tools/fetch_drive.py projects/2026-11-idaho-kohberger "<الرابط>"`

## 5) (مستحسن قبل النشر) طلب النسخ الأصلية
نموذج طلب السجلات العامة لمدينة موسكو: https://www.ci.moscow.id.us/1058/MPD-Public-Records-Request
اطلب نسخ لقطات البودي كام ومكالمة 911 وكاميرات المراقبة والمقابلات اللي سبق نشرها في القضية رقم MPD 22-M09903. بهذا تكون عندنا النسخ الأصلية بدل نسخ القنوات، ونحمي القناة من مطالبات حقوق النشر.

## 6) صوت قناة سامح سند (لدليل السكريبت العربي)
```bash
yt-dlp -x --audio-format mp3 -o "ref_ar/%(id)s.%(ext)s" 2X6fpu8naxc aFznUkx0E7g ZUpEgc3ojdo 5d4r2N2rtr8 pjOnkIB0qzU HLysEKojobI b4QHN5FKAJE uknuQhHg9A4
```
ارفع مجلد `ref_ar` في نفس مجلد Google Drive.
