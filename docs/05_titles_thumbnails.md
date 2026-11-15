# 05 — هيكلة العناوين والصور المصغرة (Packaging)

> **العينة:** صور ثمبنيل أعلى 30 فيديو مشاهدة (من 18 مليون إلى 42 مليون) + أحدث 6 فيديوهات، مع عناوينها. المجموع 36 صورة.
> **الهدف:** معايير واضحة نطبقها على كل فيديو عشان نرفع نسبة النقر (CTR).
> العنوان والصورة **وحدة واحدة**: كل واحد يكمل الثاني، وما يكرر اللي في الثاني.

---

## الجزء الأول: الثمبنيل

### 1. التوقيع البصري الثابت (موجود في 36 من 36 صورة)
كل صورة عليها **إطار كاميرا فيديو (Camcorder / Viewfinder HUD)**. هذا هو "البراند" حقهم:

| العنصر | المكان | ملاحظة |
|---|---|---|
| 🔴 **REC** (نقطة حمراء + كلمة REC) | أعلى اليسار، وأحياناً أعلى اليمين | موجود في كل الصور |
| 🔋 أيقونة البطارية | أعلى اليمين | أحياناً تكون شبه فاضية، يعني ضغط وتوتر |
| ⌐ ¬ زوايا الإطار الأربع (خطوط بيضاء رفيعة) | الأركان | تحدد الكادر |
| 🎥 أيقونة الكاميرا (ꝏ◁) | أسفل اليمين | |
| `F/2.8 1/120` + `00:00:13:80` | أسفل اليسار وأسفل اليمين | في حوالي 25% من الصور |
| `AXON 1` و`cam 01` | أعلى اليمين وأسفل اليمين | في حوالي 10% من الصور (اسم شركة البودي كام الحقيقية) |

**ليش هذا مهم؟** الإطار يقول للمشاهد في نص ثانية: "هذي لقطات حقيقية من كاميرا". وهذا هو الـ niche كله.
**قرارنا:** نصمم إطار خاص فينا (نفس الفكرة، بس بتصميم مختلف: لون مختلف وخط مختلف وعناصر مختلفة)، ونطبقه على **كل** الصور. الأداة `tools/make_thumbnail.py` تسويه تلقائياً.

### 2. الصورة نفسها: لقطة حقيقية بعد معالجة قوية
- **91% من الصور (33 من 36) فريم حقيقي من البودي كام أو CCTV.** ما فيه رسومات ولا فوتوشوب واضح.
- لكن الفريم **معالج بقوة**:
  - زيادة الحدة (Sharpen) والوضوح (Clarity).
  - تشبع ألوان عالي.
  - شكل قريب من HDR.
  - رفع جودة الوجوه (Upscale).
  - هذي المعالجة تخلي الفريم الضبابي يطلع "سينمائي" على الجوال.
- **قليل من الصور مركّبة:** أشخاص من لقطات مختلفة جنب بعض، وأحياناً بحواف بيضاء (Cutout).
  - #8 (عائلة من 3)، #11 (مراهقين في سيارة الشرطة)، #15 (أب وابن)، #27 (زوجين).
- **منظور الضابط (POV)** موجود في حوالي 30% من الصور: يد الضابط أو مسدسه أو قلمه في مقدمة الكادر (#1 و#22 و#25 و#26). كأن المشاهد هو الضابط.

### 3. الأنماط السبعة للثمبنيل (من الأكثر تكراراً)

| # | النمط | أمثلة (الترتيب) | متى نستخدمه |
|---|---|---|---|
| **A** | **🫢 وجه مصدوم + يد على الفم** | #6 و#15 و#21 و#23 و#26 و#27 | عناوين "Realizes" و"Discovers" (لحظة الإدراك) |
| **B** | **😏 قاتل مبتسم أو هادي** في موقف المفروض يكون مرعب | #7 و#11 و#18 و#29 و#1 (نظارة شمسية ووقفة متكبرة) | عناوين "Thinks She Can Get Away" و"Smartest" و"Genius" |
| **C** | **📍 الشخص + المكان العادي** (ملحق، صندوق سيارة، علية، كراج) | #9 و#13 و#20 و#21 و#36 | عناوين فيها مكان: "Inside Grandmother's Shed" و"In Attic" |
| **D** | **👉 طفل يأشر** على باب أو مكان | #12 و#16 | عناوين "Daughter Leads Police To..." |
| **E** | **🔦 مواجهة ليلية** (أضواء الشرطة، كشاف، طريق مظلم) | #10 و#14 و#20 و#33 و#34 و#35 | المطاردات و"Highway" و"Pulled Over" |
| **F** | **🔫 تكتيكي**: SWAT أو مسدس الضابط يواجه شخص | #22 و#28 | "SWAT" و"Hostages" و"Hideout" |
| **G** | **🧑‍⚖️ غرفة التحقيق** | #4 و#18 و#24 | "Smarter Than The Detective" و"Being Recorded" |

### 4. النص على الصورة
- **حوالي 90% من الصور ما فيها أي نص.** العنوان هو اللي يحكي.
- **لما يكون فيه نص (#2 و#4 و#30):**
  - **من كلمتين إلى أربع كلمات.**
  - كلمة صغيرة بحروف صغيرة + **كلمة كبيرة بحروف كبيرة**: "genius **KILLER**" و"we found the **BODIES.**" و"secret genius".
  - خط أبيض عريض (Sans Bold)، وظل أسود ناعم. **بدون إطار ملون ولا خلفية للنص.**
  - النص يقول **شي ما يقوله العنوان**: إما اقتباس من اللقطة ("we found the bodies.")، أو وصف الشخص ("genius").
- **أدوات التوجيه:**
  - سهم مرسوم باليد (أبيض أو أحمر) يأشر على الشخص (#2 و#4).
  - **دائرة حمراء** حول تفصيلة مخفية، مثل المسدس في يد المشتبه به في #24.

### 5. الإخفاء (Blur) كأداة فضول
- الجثث والأشياء المروعة **ما تنعرض أبداً**. يغطونها بـ:
  - **بكسلة** (#9 و#18 و#19).
  - **مربع أسود** (#36).
  - ونفس الشي لوجوه الأطفال (#12 و#16).
- الإخفاء **يزيد الفضول**، ويحمي القناة من مشاكل الإعلانات وسياسات يوتيوب. **نطبقه دايماً.**

### 6. التكوين والألوان
- **عدد الأشخاص:** واحد إلى ثلاثة. **الوجه يغطي من 15% إلى 35% من مساحة الصورة**، ويكون واضح على الجوال.
- **قاعدة الأثلاث:** الشخص في جهة، والمكان أو الدليل في الجهة الثانية.
- **العيون:** نظرة للضابط أو للكاميرا. نظرة الذهول أو النظرة الفاضية أقوى من الصراخ.
- **الإضاءة:** نهار مشمس بألوان قوية (أخضر وأزرق)، **أو** ليل مع ضوء الشرطة الأحمر والأزرق. **ما فيه شي رمادي باهت.**
- **ما فيه:** شعار القناة، ولا إطار ملون حول الصورة، ولا إيموجي، ولا أكثر من سهم واحد.

---

## الجزء الثاني: العنوان (تحليل أعلى 30)

### 7. القوالب حسب الأداء
| القالب | الصيغة | عدد العناوين في أعلى 30 | أمثلة |
|---|---|---|---|
| **T1 الإدراك** | [علاقة أو صفة] + **Realizes** + [السر] | 8 | *Rich Mass Killer Realizes She's Been Caught 8 Years Later* (42 مليون)، *13 Year Old Realizes His Twin Brother Just Killed Someone* |
| **T2 الاكتشاف** | [Parents/Family/Police] + **Discover(s)** + [شي] + [مكان] | 5 | *Parents Discover Their Son Is A Wanted Killer*، *Family Discovers Missing Dad's Head Inside Garbage Bag* |
| **T3 القبض** | **How Police Captured** + [لقب] | 2 (لكنها من الأعلى) | *How Police Captured Colorado's Smartest Killer* (40 مليون) |
| **T4 الغرور** | [صفة] + **Thinks (S)he Can Get Away With** + [It/Murder] | 3 | *Spoiled Teen Thinks She Can Get Away With Murder* (30 مليون) |
| **T5 القيادة** | [شخص] + **Leads Police To** + [جثة أو مكان] | 2 | *Daughters Lead Police To Mother's Dead Body* |
| **T6 المكان** | [Cops/Police] + **Find** + [شي] + **In/Inside** + [مكان عادي] | 4 | *Police Find Dead Mother In Daughter's Garage*، *...Killer Is Living In Their Vents* |
| **T7 الكاميرا** | ... **Caught On Camera** / **Doesn't Realize He's Being Recorded** | 2 | *Colorado Hitman Caught On Camera Moments Before Executing Her Target* |

### 8. "مادة العنوان": الكلمات اللي تتكرر في أعلى 30
- **العلاقات (موجودة في 50% من العناوين):** Mom/Mother، Dad/Father، Son، Daughter(s)، Parents، Family، Wife، Husband، Girlfriend، Twin Brother، Couple.
- **الصفات قبل كلمة Killer:** Rich، Secret، Smartest، Spoiled، College، Psycho، Teen، Mass، Serial، Wanted، Genius، Clueless.
- **الأماكن العادية:** Garage، Attic، Vents، Backyard، Bedroom، Shed، River، Trash Can، Garbage Bag، Car، Mansion، House.
- **الأرقام:** 8 Years Later، 13 Year Old، 12 Year Old، $3,000,000، 50 SWAT Officers.
- **أفعال الإدراك:** Realizes، Discovers، Finds، Learns، Leads، Runs Into، Catches.

### 9. علاقة العنوان بالصورة (أهم درس)
| العنوان يقول | الصورة تعرض | مثال |
|---|---|---|
| **من** (العلاقة) و**وش** السر | **الوجه** + **المكان** | #6: *Man Horrified After Learning Girlfriend's Evil Secret* ← رجل يده على فمه في كراج |
| صفة القاتل ("Smartest") | القاتل نفسه بشكل عادي جداً (قميص وردي ونظارة) + كلمة "genius KILLER" | #2 |
| مكان الجثة ("Trash Can"، "Garbage Bag") | الكيس الأسود والمجرفة، **بدون الجثة** | #20 |
| "Leads Police To" | طفلة **تأشر** | #12 و#16 |
| "Thinks She Can Get Away" | المتهمة **تبتسم** | #7 و#29 |

**القاعدة:** الصورة تعرض **الشخص والمكان**، والعنوان يكشف **السر**. والمشاهد يضغط عشان يربط الاثنين ببعض.

---

## الجزء الثالث: معاييرنا (تقييم إلزامي قبل النشر)

### ✅ معيار الثمبنيل (من 100)، ونقبل من 75 وفوق
| البند | النقاط |
|---|---|
| إطار الكاميرا الخاص فينا (REC وبطارية وزوايا وأيقونة) | 10 |
| فريم حقيقي من اللقطات (مو صورة AI ولا ستوك) | 10 |
| وجه واضح يغطي من 15% إلى 35% من الصورة، ومقروء على حجم 160×90 | 15 |
| تعبير قوي: صدمة، أو هدوء مخيف، أو ابتسامة في وقت غلط | 15 |
| عنصر المكان أو الدليل من العنوان ظاهر في الصورة | 15 |
| معالجة الصورة (حدة وتشبع وتباين)، وما فيها أي منطقة باهتة | 10 |
| نص من 0 إلى 4 كلمات، وما يكرر العنوان (لو مافيه نص: 10 نقاط) | 10 |
| إخفاء الجثث والدم وأطفال القاصرين | 10 |
| يتميز عن آخر 3 ثمبنيلات عندنا (تكوين أو ألوان مختلفة) | 5 |

**اختبار الجوال:** نصغر الصورة إلى 160×90 ونسأل: هل نفهم **من** و**وين** خلال ثانية وحدة؟

### ✅ معيار العنوان (من 100)، ونقبل من 75 وفوق
| البند | النقاط |
|---|---|
| يتبع قالب من T1 إلى T7 | 15 |
| فيه علاقة عائلية أو صفة قوية للقاتل | 15 |
| فيه مكان عادي، أو رقم محدد، أو مدة زمنية ("8 Years Later") | 15 |
| فعل إدراك أو اكتشاف (Realizes وDiscovers وFinds وLeads) | 15 |
| من 6 إلى 11 كلمة، وطوله 60 حرف أو أقل، وكل كلمة تبدأ بحرف كبير | 10 |
| ما يحرق النهاية ولا الحكم | 10 |
| صادق: كل كلمة فيه مثبتة في القضية | 10 |
| ما فيه كلمات ضعيفة: Arrested وCaught Alone وShocking وInsane وأحرف من لغات ثانية | 10 |

الأداة `tools/title_check.py` تحسب هذا التقييم تلقائياً بشكل تقريبي.

### 🔁 بروتوكول الاختبار (A/B)
1. لكل فيديو نجهز **3 عناوين** (قوالب مختلفة) و**3 صور** (أنماط مختلفة: A وB وC مثلاً).
2. نفعّل **Test & Compare** في يوتيوب للصور. والعناوين ممكن نختبرها إذا كانت الميزة متاحة للقناة.
3. بعد 48 ساعة: نسجل الفائز في `research/postmortem.md`، ونحدّث جدول "الأنماط الرابحة" عندنا تحت.
4. **نفس الشي اللي تسويه القناة المرجعية:** يغيرون العنوان بعد النشر لو الأداء ضعيف. شفناهم غيروا عنوان فيديو `5kFYKil24A0` خلال يوم.

### 📒 الأنماط الرابحة عندنا (نحدّثه بعد كل فيديو)
| الفيديو | الثمبنيل الفائز (نمط) | العنوان الفائز (قالب) | CTR | ملاحظة |
|---|---|---|---|---|
| | | | | |

---

## ملحق: جدول أعلى 30 فيديو (العنوان + الثمبنيل)
| # | المشاهدات | العنوان | نمط الصورة | نص على الصورة |
|---|---|---|---|---|
| 1 | 42M | Rich Mass Killer Realizes She's Been Caught 8 Years Later | B: متهمة واثقة بنظارة شمسية قدام قصر + قلم الضابط POV | — |
| 2 | 40M | How Police Captured Colorado's Smartest Killer | B+G: CCTV للقاتل بقفازات زرقاء | "genius KILLER" + سهم |
| 3 | 35M | When Dumb Karens Try To Attack Cops | فعل عنيف: امرأة تُرش برذاذ الفلفل | — |
| 4 | 33M | When The Suspect Is Smarter Than The Detective | G: غرفة تحقيق | "secret genius" + سهم أحمر |
| 5 | 32M | Colorado Hitman Caught On Camera Moments Before... | CCTV: امرأة تمشي بشكل عادي | — |
| 6 | 31M | Man Horrified After Learning Girlfriend's Evil Secret | A: يد على الفم + ضابط | — |
| 7 | 30M | Spoiled Teen Thinks She Can Get Away With Murder | B: ابتسامة | — |
| 8 | 28M | Parents Discover Their Son Is A Wanted Killer | تركيب: أب وأم وابن | — |
| 9 | 28M | Police Find Dead Mother In Daughter's Garage | C: كراج + صندوق مبكسل | — |
| 10 | 27M | Cop Runs Into Secret Killer Dumping Body Parts In River | E: ليل، رجل ملطخ + سيارة الشريف | — |
| 11 | 25M | 13 Year Old Realizes His Twin Brother Just Killed Someone | B: توأم في سيارة الشرطة، واحد يبتسم | — |
| 12 | 25M | Daughters Lead Police To Mother's Dead Body | D: طفلة تأشر للباب | — |
| 13 | 24M | Hidden Camera Reveals Wanted Killer Living Inside Family's Attic | C: شاب في العلية ومعه سكين | — |
| 14 | 23M | How Police Captured Florida's Longest Active Serial Killer | E+F: ليل، مسدس الضابط | — |
| 15 | 23M | Family Realizes A Killer Is Living In Their Vents | A: تركيب أب وابن، يد على الفم | — |
| 16 | 22M | Daughter Leads Police To Her Father's Deadly Murder Rampage | D: طفلة تأشر داخل كراج | — |
| 17 | 22M | Killer Couple Realizes Cops Found Their Murder House | A: رجل مذهول + امرأة يدينها على رأسها | — |
| 18 | 22M | College Killer Thinks He Can Get Away With It | B+G: يبتسم في التحقيق | — |
| 19 | 21M | Teens Accidentally Run Into Secret Cult's Body Dump | C: نجمة شيطانية + جثة مبكسلة | — |
| 20 | 21M | Family Discovers Missing Dad's Head Inside Garbage Bag | C+E: كيس أسود + مجرفة، ليل | — |
| 21 | 21M | Cops Realize Psycho Daughters Car Is Filled With Bodies | A+C: يد على الفم + صندوق سيارة مليان أكياس | — |
| 22 | 21M | Police Discover A Mass Killer's Secret Hideout | F: مسدسات + غرفة فوضوية | — |
| 23 | 20M | Police Discover Car Filled With Serial Killer's Bodies | A+C: امرأة تغطي وجهها + سيارة حمراء | — |
| 24 | 20M | Teen Killer Doesn't Realize He's Being Recorded | G: دائرة حمراء على مسدس مخفي | — |
| 25 | 19M | Dad Realizes Children Hid A Dead Body In His Backyard | A: أب مصدوم + ابنة تصرخ + يد الضابط | — |
| 26 | 19M | Mom Realizes Her Daughter Just Decapitated Someone | A: أم يدينها على وجهها + ابنة مكبلة بنظرة فاضية | — |
| 27 | 19M | Parents Discover Their Daughter Is A Mass Killer | A: تركيب زوجين مصدومين، "AXON 1" | — |
| 28 | 19M | SWAT Team Faces Off Against An Active Shooter | F: فريق SWAT + درون + مدرعة | — |
| 29 | 18M | Student Kills Her Teacher, Thinks She Can Get Away With It | B: ابتسامة في سيارة الشرطة | — |
| 30 | 18M | Serial Killer Realizes Police Found His Body Collection | A: رجل مطروح على الأرض | "we found the BODIES." |
