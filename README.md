# NE — نظام إنتاج قناة Bodycam True Crime

قناة وثائقية مبنية على لقطات كاميرات الشرطة (Bodycam) و911 وغرف التحقيق، مع فويس أوفر بين اللقطات.
**القناة المرجعية:** [Dr Insanity (@drinsanitycrime)](https://www.youtube.com/@drinsanitycrime) — تقريباً 5.8 مليون مشترك، ووسيط المشاهدات 10 مليون للفيديو.

## الملفات
| الملف | المحتوى |
|---|---|
| [`docs/01_channel_analysis.md`](docs/01_channel_analysis.md) | تحليل القناة: الأرقام، تطور المحتوى، معادلة العنوان، الوصف، الرعاة، المواضيع |
| [`docs/02_script_style_guide.md`](docs/02_script_style_guide.md) | **دليل كتابة السكريبت:** الهيكل (8 فصول)، الجمل الثابتة، معجم الانتقالات، ومعايير Non-AI |
| [`docs/03_footage_sources.md`](docs/03_footage_sources.md) | من وين نجيب اللقطات (الجهات الرسمية وFOIA والمحاكم)، وكيف نحمي القناة من حقوق النشر |
| [`docs/04_production_workflow.md`](docs/04_production_workflow.md) | **الورك فلو:** 8 مراحل، ومن يسوي وش في كل مرحلة |
| [`docs/05_titles_thumbnails.md`](docs/05_titles_thumbnails.md) | **هيكلة العناوين والثمبنيل:** تحليل أعلى 30 فيديو، والأنماط السبعة للصور، وقوالب العناوين، ومعايير تقييم من 100 |
| `research/reference_channel_videos.csv` | كل فيديوهات القناة المرجعية (143) بالمشاهدات والمدة |
| `research/topic_scorecard.md` | جدول تقييم القضايا المرشحة |
| `templates/project/` | قالب لكل مشروع جديد |

## الأدوات
```bash
tools/new_project.sh <slug>                               # مشروع جديد
python3 tools/download_assets.py projects/<p>             # تنزيل كل الأصول من assets.csv
tools/transcribe.sh projects/<p>                          # تفريغ اللقطات بـ Whisper
python3 tools/script_lint.py projects/<p>/docs/script.md --export   # فحص السكريبت + ملف EDL + نص الفويس
python3 tools/split_vo.py projects/<p>/vo/full_take.wav   # تقسيم تسجيل الفويس إلى كتل
python3 tools/assemble.py projects/<p>                    # نسخة مونتاج أولية + ترجمة + فصول
python3 tools/title_check.py "Title A" "Title B"           # تقييم العناوين (من 100)
python3 tools/make_thumbnail.py --video <clip> --at 00:14:41 --out export/thumb_A.jpg   # ثمبنيل بإطار الكاميرا
python3 tools/fetch_reference_transcripts.py 40           # نصوص القناة المرجعية للدراسة
python3 tools/fetch_reference_thumbs.py 30                # صور ثمبنيل القناة المرجعية للدراسة
```
المتطلبات: `python3` و`ffmpeg` و`yt-dlp` و`pillow`. والتفريغ يحتاج `openai-whisper`.

## دورة العمل باختصار
1. **Claude** يقترح 5 قضايا مع التقييم، و**أنت** تختار وحدة.
2. **Claude** يبحث بعمق، ويوثق المصادر، وينزل اللقطات، ويجهز طلبات FOIA.
3. **Claude** يفرغ اللقطات ويفرزها، ويكتب السكريبت ويفحصه، ويطلع `vo/VO_SCRIPT.txt`.
4. **أنت** تسجل الفويس.
5. **Claude** يجمع النسخة الأولية (`export/rough_cut.mp4`)، ويجهز العناوين والوصف والفصول.
6. **أنت** تلمّع المونتاج وتصمم الصورة المصغرة وتنشر.
