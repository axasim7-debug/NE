# 02 — دليل كتابة السكريبت (Voice DNA)

> هذا الدليل مستخرج من 40 نص كامل لقناة Dr Insanity. **أي سكريبت نكتبه لازم يمر على كل بنود هذا الملف.**
> **قناتنا إنجليزية بالكامل** (السرد والعناوين والترجمة). القسم 9 (العربي) للاحتياط فقط.

---

## 1. معادلة الوقت

| العنصر | القيمة |
|---|---|
| ما يظهر على الشاشة | **لقطات حقيقية من 80 إلى 100% من الوقت.** الراوي يتكلم فوق اللقطات نفسها، وما فيه شاشة منفصلة للسرد (شوف `06_editing_style.md` §1) |
| نسبة الفويس أوفر إلى صوت اللقطات | **تقريباً 1 إلى 2**: ثلث المدة صوت الراوي فوق اللقطات، والثلثين صوت اللقطات الأصلي بدون راوي |
| عدد كلمات الفويس في فيديو 35 دقيقة | تقريباً **1,800 إلى 2,500 كلمة** |
| طول كتلة الفويس الواحدة | **2 إلى 5 جمل (30 إلى 80 كلمة، أي 10 إلى 30 ثانية)**، وبعدها نرجع للقطات مباشرة |
| أطول مقطع لقطات بدون سرد | 2 إلى 4 دقائق، وفي ذروة المشهد ممكن أكثر (مثل اقتحام البيت أو مواجهة العلية) |
| سرعة الإلقاء | تقريباً 150 إلى 160 كلمة في الدقيقة، ونبرة هادئة وجادة ما فيها مبالغة |

**القاعدة الذهبية:** الراوي **يمهّد** للقطة أو **يفسّرها**. ما يكرر اللي المشاهد شافه وسمعه.
**وكل كتلة VO لازم يكون لها `(on: C### time)`**، يعني لقطة حقيقية تظهر تحتها. الرسومات تكون فقط في الحالات اللي ما فيها لقطة.

---

## 2. الهيكل الثابت (7 فصول)

```
00:00 ┃ ① COLD OPEN / TRAILER        (45–90 ث)  ← أقوى 4–8 مقتطفات من الفيديو كله
      ┃ ② THE HOOK                    (20–40 ث)  ← "This is X... What officers don't realize..."
01:30 ┃ ③ THE SETUP                   (2–5 د)    ← "It's [time] on [date] in [city]..." + 911 call
      ┃ ④ FIRST RESPONSE              (5–10 د)   ← بودي كام أول وصول، شهود، أول شك
~8–15 ┃ ⑤ THE TWIST + SPONSOR         ← cliffhanger → "But before we get to that," → الراعي → "With that said, let's return to..."
      ┃ ⑥ THE HUNT / ESCALATION       (10–20 د)  ← تفتيش، مطاردة، مداهمة، مواجهة (الذروة البصرية)
      ┃ ⑦ INTERROGATION               (5–10 د)   ← غرفة التحقيق: كذب ← مواجهة بالأدلة ← انهيار أو "I want a lawyer"
النهاية┃ ⑧ EVIDENCE & VERDICT          (1–3 د)    ← الأدلة الجنائية → التهم → الحكم بالأرقام → ملاحظة ختامية قصيرة
```
ما فيه مقدمة للقناة، وما فيه "Hey guys"، وما فيه "Subscribe". **الفيديو يبدأ في منتصف الحدث، وينتهي بالحكم.**

### ① Cold Open — التريلر
- نبدأ **بصوت اللقطات نفسها، مو بالراوي**. نختار جملة صادمة من البودي كام: *"There's bloody gloves on the passenger seat."*
- بين المقتطفات، الراوي يقول جملة أو جملتين تحدد المكان والرهان:
  > *"Michigan cops are in the middle of a statewide manhunt for a dangerous killer believed to be driving this exact car."*
- **ونختم التريلر بجملة "الوعد":**
  > *"...eventually leading to some of the strangest and most disturbing footage ever captured on body cam."*
  > *"What follows is amongst the most disturbing collections of criminal case files ever uploaded to YouTube."*

### ② The Hook — صيغة "This is"
هذي أكثر صيغة تتكرر في القناة، وموجودة في كل الفيديوهات الـ40:
> *"**This is** 42-year-old Amy Valardi. And for the last 8 years, she's been living with a terrifying secret that these detectives are about to expose."*
> *"**This is** the mother of 43-year-old Crystal Krug. In a few seconds, she's going to find Crystal's lifeless body inside this very garage. **And this is** Daniel Krug, the man who killed her."*

الصيغة: **This is + [العمر] + [الاسم أو الصفة] → [وش هو على وشك يكتشف أو يسوي]**.
وبعدها مباشرة جملة **السخرية الدرامية (Dramatic Irony)**:
> *"**What** [officers / he / the family] **don't realize is that** ..."*
> *"**He has no idea** the man about to step out of that car is a mass murderer in the middle of a deadly killing spree."*
> *"**But what makes this interesting is that** the son is in fact hiding this man..."*

### ③ The Setup — صيغة "It's [time]"
> *"**It's Saturday, May 20th in Kalamazoo, Michigan.** 28-year-old Taylor Dragovich has just returned to her mother's apartment... **Little does she know**, those few seconds alone are about to have devastating consequences."*
> *"**It's just before 5:00 a.m. on March 15th along Interstate 40 in New Mexico.**"*
> *"**It's 2:15 p.m. on October 24th, 2016.** 22-year-old Katie Blauvelt is captured on CCTV..."*

بعدها نشغّل **مكالمة 911** كاملة أو مختصرة، ونقدّم المتصل بجملة وحدة:
> *"**On the line is** Taylor's mother, Cindy, reporting that..."* · *"**That caller was** Caitlyn Cash, and she'd arrived home to find..."*

### ④ First Response
- **نشرح المصطلحات الشرطية والطبية بجملة وحدة** (هذا أسلوب ثابت في القناة):
  > *"officers noticed cerebral spinal fluid, or CSF for short, oozing onto the floor. This fluid surrounds the brain, meaning..."*
  > *"...after Allen entered an Alford plea, **meaning** he maintains his innocence while acknowledging..."*
- **نقرأ أفكار الشرطة:** *"From the detective's perspective, Melissa appears to be trying to cover up evidence..."*
- **ونعلّق على الكذب:** *"This response from Melissa sounds far from convincing."* · *"That was almost disturbingly simple."*

### ⑤ Twist + Sponsor
```
[حدث يتصاعد] → "But in reality, whoever is behind the wheel is about to pull officers into
a far more disturbing side of this investigation."
"But before we get to that, [قصة شخصية قصيرة مربوطة بالراعي]... [الراعي]... [الرابط]."
"With that said, let's return to [المشهد بالضبط], where officers are moments away from [وعد]."
```
بدون راعي، نستخدم نفس الـ cliffhanger وننتقل للمشهد اللي بعده مباشرة.

### ⑥ The Hunt — تصاعد الأحداث
- **نذكر الوقت قبل كل مرحلة:** *"Over an hour into the investigation..."* · *"Nearly 2 hours later..."* · *"10 hours would go past without any clues..."*
- **نذكر الأداة التقنية:** Flock (قارئ لوحات السيارات) · ping الجوال · درون · كاميرا حرارية · search warrant.
- **نرفع الرهان قبل كل اقتحام:** *"And every room officers clear could place them directly in his line of fire."*
- **ونترك الذروة للقطات نفسها بدون سرد.** الراوي يسكت هنا.

### ⑦ Interrogation
- نمهّد بسطر: *"While forensic analysts work to determine whether the blood is Taylor's... a confession is their only other shot. **But Jeffrey has other plans.**"*
- نعرض الفخ: *"What if I told you that your cell phone did ping somewhere other than where you say you were?"*
- **ونختم بجملة نتيجة:** *"With Jeffrey invoking his right to a lawyer, detectives' hopes of getting a confession come to an end. **Fortunately, they may no longer need one.**"*

### ⑧ Evidence & Verdict
- **نعيد بناء الخط الزمني بالدقيقة:** *"Around 5:00 p.m.... at 5:47 p.m.... by 5:49 p.m.... by roughly 6:15 p.m...."*
- **نذكر الدليل الحاسم:** *"But the final pieces of evidence would prove even more damaging, **completely sealing [X]'s fate.** DNA testing confirms..."*
- **نكتب الحكم بالأرقام:** *"In 2024, he pleads guilty to second-degree murder and is sentenced to 30 to 60 years in prison with the possibility of parole after serving the minimum 30 years."*
- نذكر مصير الأطراف الجانبية: *"As for Jeffrey's mother, investigators did not find sufficient evidence... So, no charges were filed."*
- **ممكن نختم بملاحظة واحدة لها عبرة** (اختياري، مرة في كل 3 فيديوهات تقريباً):
  > *"It sheds light on the importance of closely monitoring your children..."*
  > *"...there is a very real possibility he never leaves prison at all."*
- **ما نسوي أي خاتمة بعد الحكم.** الفيديو ينتهي هنا.

---

## 3. قواعد الجملة

| القاعدة | التطبيق |
|---|---|
| **الزمن الحاضر** للأحداث | *"Officers immediately **begin** coordinating a stop..."*، *"Deputies **rush** to the property"* |
| **"would" للتلميح لما سيحدث** | *"where they **would** catch their first glimpse of the suspect"*، *"something about their response **would** feel off"* |
| **العمر قبل الاسم** دايماً | *"28-year-old Taylor Dragovich"* |
| **الأرقام بالتحديد** | *"28 mi"*، *"more than a dozen officers"*، *"4-hour standoff"*، *"1,300 m away"* |
| **جمل متوسطة** (12 إلى 25 كلمة)، وكل كتلة تنتهي بجملة دفع | *"...but they have no idea he's about to lead them into one of the strangest standoffs of their careers."* |
| **نهاية الكتلة = سؤال مفتوح أو وعد** | *"But when they arrive, the person who answers the door isn't who they're expecting."* |
| **ضمير "we" نادر** | فقط في الوعود: *"...the most dark and twisted body cam footage we've ever shown on this channel."* |
| **الراوي ما يعطي رأيه السياسي ولا يهاجم الشرطة** | ينتقد بهدوء أحياناً: *"despite nearly perfect detective work, his plan works exactly the way he intended."* |

### معجم الانتقالات (مرتّب حسب التكرار في الـ40 نص)
| العبارة | عدد الفيديوهات اللي فيها |
|---|---|
| `This is ...` | 40/40 |
| `no idea` | 33 |
| `At this point, ...` | 31 |
| `However, ...` | 31 |
| `disturbing` | 31 |
| `is/are about to ...` | 25 |
| `minutes/hours/days later` | 27 |
| `interesting(ly)` | 23 |
| `But what ...` | 22 |
| `unaware` | 20 |
| `sentenced to` | 20 |
| `horrifying` | 17 |
| `would go on to` | 14 |
| `would soon` | 13 |
| `just hours (earlier/later)` | 12 |
| `chilling` | 11 |
| `With this in mind,` | 10 |
| `What [X] don't realize (is)` | 8 |
| `Little does/did [X] know` | 8 |
| `Moments later` | 7 |
| `But in reality,` | 5 |
| `Worth noting is that` | 5 |

**تنبيه:** كلمات الرعب (disturbing وhorrifying وchilling) ما نستخدم منها أكثر من **مرة وحدة كل 3 دقائق تقريباً**. وكل كلمة منها نوزعها على الفيديو كله، ما نكررها ورا بعض.

---

## 4. معايير Non-AI (إلزامية)

السكريبت لازم يبان إنه مكتوب بيد إنسان باحث، مو مولّد آلياً. **نفحص كل سكريبت بـ `tools/script_lint.py` قبل التسليم.**

### ❌ ممنوع
- كليشيهات الذكاء الاصطناعي: `delve`، `tapestry`، `testament to`، `in a world where`، `it's important to note`، `a stark reminder`، `shrouded in mystery`، `sent shockwaves`، `little did anyone know what fate had in store`، `navigating`، `unwavering`، `palpable`، `in the realm of`، `a chilling reminder`، `the stakes have never been higher`.
- **الشرطة الطويلة (—):** القناة ما تستخدمها. نستخدم الفاصلة أو النقطة بدالها.
- **التكرار الثلاثي الآلي:** مثل "fear, uncertainty, and dread".
- **الأسئلة البلاغية المتتالية:** نسمح بسؤال واحد فقط في كل فصل.
- **الأخلاقيات والوعظ في وسط القصة.**
- **أي معلومة ما لها مصدر في `research/sources.md`.** ما نخترع حوار ولا تفاصيل ولا أفكار للضحية.
- **وصف دموي تفصيلي بالكلام.** القناة تخلي اللقطة تتكلم، والراوي يستخدم كلمات مثل "brutally" و"lifeless body" ويكمل.

### ✅ مطلوب
- **تفاصيل محددة** في كل كتلة: رقم أو وقت أو اسم شارع أو اسم أداة.
- **تنويع طول الجمل.** نحط جملة قصيرة جداً بعد جملة طويلة: *"But Jeffrey has other plans."*
- **ملاحظة "إنسانية" غريبة** من التفاصيل الحقيقية: *"I need my work stuff"*، و*"Oh, that might be my lipstick"*. الراوي يلتقطها ويعلّق عليها.
- **مصطلحات الشرطة الصحيحة:** felony stop، PPO، search warrant، Miranda، Alford plea، invoked his right to a lawyer.
- **التهجئة الصحيحة للأسماء.** القناة نفسها تغلط فيها، ونحن نتفوق عليهم في الدقة.

---

## 5. أخلاقيات وتصنيف المحتوى (عشان نحمي القناة)
- **نخفي (Blur)** وجوه القاصرين، والجثث، والجروح الواضحة، وأرقام اللوحات والعناوين الخاصة اللي ما نشرتها الجهة الرسمية.
- **نصفّر الصوت (Bleep)** عند ذكر أسماء القاصرين لو كانت محجوبة رسمياً، وعند الشتائم القوية في أول 30 ثانية.
- **أول 30 ثانية تكون بدون دم واضح** (عشان الإعلانات).
- **ما نقول "قاتل" عن شخص ما صدر عليه حكم.** نستخدم "suspect" أو "accused" أو "allegedly"، إلا إذا القضية انتهت بحكم إدانة أو اعتراف.
- **نتأكد من حالة القضية:** هل فيه استئناف؟ هل البراءة ممكنة؟ ونضيف كل التصحيحات لصفحة corrections.

---

## 6. قالب كتلة السكريبت (الصيغة الإلزامية)
كل سكريبت نكتبه بهذي الصيغة عشان يتحول مباشرة لملف مونتاج:
```
[CLIP C012 00:14:22-00:14:41] bodycam — officer finds gloves  (vol 100)
[VO 07] (on: C012 00:14:41 / B-roll SUV)  ~18s
As Melissa learns Taylor has tragically succumbed to her injuries, officers face a troubling
possibility. If Melissa is really covering for her son, she's no longer just protecting her family.
[CLIP C013 00:00:00-00:01:12] bodycam — SUV search
[CARD] "MAY 20, 2023 · KALAMAZOO, MICHIGAN"  4s
```
- `C###` هو رقم اللقطة في `research/assets.csv`.
- `VO ##` هو رقم الكتلة. **أنت تسجل السكريبت كامل في ملف واحد متصل**، والأداة `align_vo.py` تقطع كل كتلة تلقائياً.
- **القطع في نص الجملة مسموح، ومطلوب في المواقف القوية:**
  ```
  [VO 12] (on: C020 00:03:10)
  But when deputies knock on the door,
  [CLIP C020 00:03:12-00:03:16] door opens (vol 100)
  [VO 13] (on: C020 00:03:16)
  the person who answers isn't who they're expecting.
  ```
- `hold=1.5` في سطر الـ VO يعني إن اللقطة تكمل ثانية ونص بعد ما يسكت الراوي، قبل العنصر اللي بعده.
- أسلوب المونتاج والرسومات كامل موجود في [`06_editing_style.md`](06_editing_style.md).

---

## 7. قائمة فحص قبل التسليم
- [ ] التريلر من 4 إلى 8 مقتطفات، وفيه جملة "وعد".
- [ ] فيه صيغة "This is [age] [name]" و"What X don't realize".
- [ ] فيه صيغة "It's [time] on [date] in [city]".
- [ ] كل كتلة VO من 30 إلى 80 كلمة، وتنتهي بدفع للأمام.
- [ ] فيه cliffhanger قبل الراعي وجملة رجوع بعده.
- [ ] الخط الزمني النهائي مكتوب بالدقيقة.
- [ ] الحكم مكتوب بالأرقام (السنة والتهمة والمدة والإفراج المشروط).
- [ ] `script_lint.py` يطلع 0 أخطاء.
- [ ] كل ادعاء له مصدر في `sources.md`.
- [ ] مجموع كلمات الـ VO بين 1,800 و2,500 لفيديو 35 دقيقة.

---

## 8. أمثلة "قبل وبعد"
**❌ نسخة AI:**
> *In a quiet Michigan town, a chilling tragedy would send shockwaves through the community — a stark reminder that danger can lurk anywhere.*

**✅ نسخة القناة:**
> *It's Saturday, May 20th in Kalamazoo, Michigan. 28-year-old Taylor Dragovich has just returned to her mother's apartment. As the family heads inside, Taylor stays behind in the parking lot. Little does she know, those few seconds alone are about to have devastating consequences.*

---

## 9. لو بنسرد بالعربي
- نمشي على نفس الهيكل ونفس نسبة الكتل.
- صيغة "This is" تصير: **"هذا هو [الاسم]، [العمر] سنة..."** أو **"هذه [الاسم]، وعمرها..."**.
- صيغة "What officers don't realize" تصير: **"ما لا يعرفه الضباط حتى هذه اللحظة..."**.
- صيغة "It's Saturday, May 20th" تصير: **"السبت، العشرين من مايو، مدينة كالامازو بولاية ميشيغان."** نبدأ بالتاريخ.
- نستخدم **فصحى مبسطة**، ومصطلحات الشرطة نكتبها بالعربي مع الإنجليزي أول مرة: "أمر تفتيش (search warrant)".
- اللقطات تبقى بصوتها الأصلي **مع ترجمة عربية مكتوبة على الشاشة**. هذا يضاعف شغل المونتاج، لكنه نقطة تميز قوية.
