# 03 — من وين ننزل اللقطات (Footage Sourcing)

> **القاعدة الأولى:** نجيب اللقطة **من مصدرها الرسمي** (الجهة الحكومية) دايماً، مو من قناة يوتيوب ثانية رفعتها.
> اللقطة الحكومية الخام سجل عام (public record). لكن **نسخة قناة ثانية بعد ما مونتجوها** ممكن تكون مسجلة في Content ID، وتجيب لنا claim أو strike.

---

## الطبقة 1 — قنوات الجهات الرسمية (الأسرع والأكثر أماناً)
كثير من أقسام الشرطة تنشر **Critical Incident Videos** خلال 14 إلى 30 يوم من الحادثة، وأغلبها في حادثات إطلاق النار من الشرطة:

| الجهة | وين تنشر | ملاحظة |
|---|---|---|
| **Phoenix PD** (أريزونا) | YouTube + موقعهم الرسمي | "Critical Incident Briefings"، وهدفهم ينشرون خلال 14 يوم |
| **NYPD** | YouTube الرسمي + [Video Media Center](https://www.nyc.gov/site/nypd/media/video-media-center/video-media-center-landing.page) | ينشرون خلال 30 يوم |
| **San Antonio PD** (تكساس) | [Critical Incident Videos](https://www.sa.gov/Directory/Departments/SAPD/Transparency-Open-Data/Open-Data-Library/Critical-Incident-Videos) | ينشرون خلال 30 يوم |
| **Las Vegas Metro (LVMPD)** | YouTube الرسمي | مؤتمرات صحفية فيها بودي كام كاملة |
| **IMPD** (إنديانابوليس) | YouTube | من 2020 |
| **Vancouver PD** (واشنطن) | [cityofvancouver.us](https://cityofvancouver.us/critical-incident-videos/) | |
| **Seattle PD** | YouTube | من أوائل الأقسام اللي بدأت تنشر |
| **LAPD** | YouTube + موقع الشفافية | Critical Incident Community Briefings |
| **Charleston PD وGreenville County SO** | YouTube | |
| مكاتب الشريف (Sheriff) في فلوريدا: Polk وVolusia وPinellas وHillsborough | YouTube وفيسبوك | Polk County مشهور بالمؤتمرات الصحفية الطويلة |
| مكاتب المدعي العام (DA وState Attorney) ومكتب النائب العام للولاية (AG) | مواقعهم | تقارير قانونية عن إطلاق النار، وفيها فيديو وأدلة |

**طريقة البحث:** `"[اسم المدينة] police" critical incident video` أو `"[القسم]" bodycam released`.

## الطبقة 2 — طلبات السجلات العامة (FOIA / Open Records)
هذي **أهم طبقة لقضايا القتل** (911 والبودي كام وغرفة التحقيق)، لأن الأقسام نادراً تنشرها من نفسها:

1. نتأكد إن القضية **انتهت** (حكم أو إقرار بالذنب). لأن القضايا المفتوحة غالباً تُرفض بحجة "ongoing investigation".
2. ندوّر على بوابة السجلات للجهة: `"[agency] public records request"`. أغلبها تستخدم **JustFOIA** أو **GovQA** أو **NextRequest**.
3. نطلب **كل شي** في طلب واحد، بصيغة محددة:
   ```
   Pursuant to [State] [Open Records statute], I request copies of:
   1. All body-worn camera and dash camera video
   2. All 911 / dispatch audio recordings and CAD logs
   3. All recorded interviews/interrogations
   4. Incident report(s) and supplemental narratives
   related to Case/Incident #[...] on [date] at [location], involving [suspect name].
   Electronic format preferred. Please notify me of any fees exceeding $[X].
   ```
4. **[MuckRock](https://www.muckrock.com/tags/body-cams/)** يرتب الطلب ويتابعه نيابة عنك، وتقدر تشوف طلبات ناس ثانيين انقبلت قبل.
5. **ننتبه للمواعيد:** نسجل تاريخ كل طلب في `research/foia_log.csv` ونتابعه كل أسبوعين.

### الولايات حسب سهولة الحصول على اللقطات
| سهلة غالباً | صعبة |
|---|---|
| Georgia (البودي كام علني من الأساس)، Florida (قانون Sunshine)، Arizona، Texas (بعد إغلاق القضية)، Ohio، Michigan، Washington، Colorado، Utah، Minnesota | **North Carolina** (لازم أمر من القاضي)، **Pennsylvania** (قانون Act 22 شروطه صارمة)، Illinois (قانون خاص)، New York (الطلبات بطيئة) |

القوانين تتغير، فنراجع قانون كل ولاية قبل ما نقدم: [RCFP — Bodycam Access Guide](https://www.rcfp.org/bodycam-video-access/).

## الطبقة 3 — المحاكم
- **أدلة المحاكمة (Trial exhibits):** كثير من المحاكم تعرض البودي كام والتحقيق في جلسات علنية. ونطلب الأدلة نفسها **من مكتب الادعاء** (DA) بعد الحكم.
- **وثائق القضية:** الـ affidavit وشكوى الاتهام وحكم الإدانة:
  - القضايا الفيدرالية: PACER و[CourtListener](https://www.courtlistener.com/) (مجاني).
  - قضايا الولايات: بوابة المحكمة في كل ولاية (مثل Florida Clerk of Court وMaricopa وغيرها).
- ⚠️ **بث المحاكمات من Court TV وLaw&Crime** محمي بحقوق نشر. نستخدمه للبحث فقط، ولا ننشر منه شي.

## الطبقة 4 — مصادر ثانوية (للبحث فقط، مو للنشر)
| المصدر | وش نستفيد منه |
|---|---|
| قنوات تجميع البودي كام: Police Activity وCode Blue Cam وEWU Bodycam وReal World Police وLaw&Crime BodyCam | **نكتشف قضايا جديدة** ونعرف الجهة الأصلية من الوصف |
| الأخبار المحلية (المحطات التابعة لـ ABC وNBC وFox، والصحف المحلية) | الخط الزمني والأسماء وتصريحات الشرطة. **ما ننشر لقطاتهم** |
| Reddit: r/bodycam وr/TrueCrime وr/PublicFreakout | تنبيه مبكر بالقضايا الجديدة |
| أرشيف المحطات المحلية في يوتيوب | تواريخ المؤتمرات الصحفية |
| [Forensic Files — أرشيف نصوص Dr Insanity](https://forensicfiles.com/shows/drinsanitycrime) | نعرف وش غطى المنافس قبل، عشان **ما نكرر قضاياهم** ونقيس أسلوبنا عليهم |

## الطبقة 5 — مواد مساندة
- **صور الضحية والمتهم:** صفحات النعي (Legacy.com)، والصفحات العامة في السوشال ميديا، وصور الاعتقال (mugshots) من مكتب الشريف. ونسجل مصدر كل صورة.
- **الخرائط:** OpenStreetMap أو لقطة من Google Earth Studio (لازم نكتب الـ attribution في الفيديو).
- **الموسيقى:** من مكتبة مرخصة (Epidemic Sound أو Artlist أو YouTube Audio Library). **ما ننزل موسيقى من يوتيوب أبداً.**

---

## حماية القناة من حقوق النشر
- **التحويل (Transformative):** سرد وتحليل وشرح وخط زمني ورسومات. هذا اللي يقوّي موقفنا في الـ fair use. **ما نرفع لقطات بدون سرد طويل.**
- اللقطات الفيدرالية (FBI وATF) غالباً مو محمية بحقوق نشر. لكن **بعض الجهات المحلية وجهات الولايات ممكن تدّعي الحقوق**. والتفاصيل في [Copyright Law and BodyCam Video](https://www.vondranlegal.com/copyright-law-and-bodycam-video).
- الـ **Content ID** آلي، وما يفهم إن الاستخدام عادل. عشان كذا لازم ننزل اللقطة من الجهة الرسمية أو من طلب FOIA، ونحتفظ بإثبات المصدر (الرابط والتاريخ ورقم الطلب) في `assets.csv` عشان نعترض لو جانا claim.
- **ثلاث strikes خلال 90 يوم = حذف القناة.** فلو جانا claim من قناة تجميع، نعترض بالدليل.
- الوصف لازم يحتوي فقرة "educational / transparency / fact-checked" (موجودة في `templates/project/docs/metadata.md`).

## مراجع
- [RCFP — Police bodycam videos: The Wild West of open records requests](https://rcfp.org/?p=43852)
- [First Amendment Coalition — Is bodycam footage a public document?](https://firstamendmentcoalition.org/asked-and-answered/is-footage-taken-by-an-officer-wearing-a-body-camera-a-public-document)
- [MuckRock — Guide to FOIA for law enforcement records](https://www.muckrock.com/news/archives/2025/apr/08/guide-to-using-foia-for-access-to-law-enforcement-records)
- [BGA — How to FOIA for body camera footage](https://www.bettergov.org/2025/12/02/how-to-foia-for-body-camera-footage/)
- [The Week — YouTube's bodycam channels & exploitation concerns](https://theweek.com/tech/youtube-police-bodycam-channels-exploitation)
- [EFF — Copyright filters & police](https://www.eff.org/deeplinks/2021/07/what-cops-understand-about-copyright-filters-they-prevent-legal-speech)
