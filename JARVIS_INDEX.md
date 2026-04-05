# JARVIS_INDEX — الفهرس الأم للمشروع

**هذا الملف هو نقطة البحث الأولى** لأي مسار، اسم ملف، أو جزء من النظام. عند إعادة تسمية ملف أو نقل مجلد، حدّث هذا الفهرس و**[`README.md`](./README.md)** (إنجليزي) و**[`README.ar.md`](./README.ar.md)** (عربي) معًا.

---

## كيف تستخدم الفهرس

| تريد أن… | اذهب إلى… |
|----------|-----------|
| تشغيل المشروع | **`run/dev.bat`**, **`run/web.bat`**, **`run/pm2.bat`** — و**`run/stop-pm2.bat`** قبل التطوير إن كان PM2 يشغّل `jarvis` (تجنب خطأ Telegram 409). تفاصيل: **`run/README.txt`**. يوجد أيضًا `dev.bat` في الجذر. |
| تغيير المجلدات الافتراضية (DB، رفع، سجلات، رموز) | **`paths.json`** ثم **`more_paths.json`** (يستهلكهما `src/project-paths.ts`) |
| تغيير سلوك الوكيل أو المفاتيح | `src/config.ts` + `.env` |
| فهم حلقة التفكير والأدوات | `src/agent/loop.ts` |
| إضافة أداة للنموذج | `src/tools/` ثم سطر في `src/tools/index.ts` |
| واجهة الويب | `src/interfaces/web/public/index.html` + `src/interfaces/web/server.ts` |
| تيليجرام | `src/interfaces/telegram.ts` |

---

## شجرة `src/` (الكود المصدري)

```
src/
├── index.ts                 نقطة الدخول (Telegram دائمًا؛ الويب اختياري بـ --web)
├── project-paths.ts         قراءة paths.json + more_paths.json ومسارات مطلقة
├── config.ts                إعدادات البيئة والـ system prompt (مسارات من project-paths)
├── agent/
│   ├── types.ts             أنواع الوكيل
│   ├── loop.ts              حلقة الوكيل (LLM ↔ أدوات ↔ ذاكرة)
│   ├── planner.ts           تخطيط مسبق عند الحاجة
│   ├── reflection.ts        مراجعة النتائج
│   └── context.ts           ضبط طول السياق وقص رسائل الأدوات
├── engine/
│   └── manager.ts           وضع المحرك: auto / local / api ونماذج Ollama المحلية
├── llm/
│   ├── provider.ts          واجهات الرسائل والأدوات للمزوّدين
│   ├── index.ts             تسجيل المزوّدين والتوجيه والـ fallback
│   ├── groq.ts              Groq
│   ├── gemini.ts            Google Gemini
│   ├── local-llm.ts         نموذج محلي (OpenAI-compatible API)
├── memory/
│   └── store.ts             SQLite + اختياري Firebase
├── security/
│   └── auth.ts              قائمة المستخدمين المسموحين (Telegram)
├── google/
│   └── auth.ts              OAuth2 لخدمات Google
├── voice/
│   └── transcribe.ts        صوت → نص (Groq Whisper)
├── interfaces/
│   ├── telegram.ts          بوت Grammy
│   └── web/
│       ├── server.ts        Express + WebSocket + REST
│       └── public/
│           └── index.html   واجهة المحادثة
├── skills/
│   └── index.ts             مهارات إضافية إن وُجدت
└── tools/
    ├── index.ts             استيراد كل الأدوات (side effects)
    ├── registry.ts          تسجيل وتنفيذ الأدوات
    ├── pipeline.ts          مساعد لملخصات الطرفية/البحث
    ├── time.ts              الوقت الحالي
    ├── memory.ts            ذاكرة مفتاحية
    ├── image-gen.ts         توليد صور
    ├── video-gen.ts         توليد فيديو
    ├── web-search.ts        بحث ويب
    ├── terminal.ts          أوامر الطرفية
    ├── screenshot.ts        لقطة شاشة
    ├── gmail.ts             Gmail
    ├── gcal.ts              Google Calendar
    ├── gcontacts.ts         جهات الاتصال
    ├── gdrive.ts            Drive
    ├── youtube.ts           YouTube Analytics
    ├── browser.ts           Playwright
    ├── screen.ts            تحليل الشاشة
    ├── desktop.ts           تحكم سطح المكتب
    ├── files.ts             إدارة الملفات
    ├── sysinfo.ts           معلومات النظام
    ├── clipboard.ts         الحافظة
    ├── notification.ts      إشعارات
    └── ollama.ts            تكامل Ollama كأداة
```

---

## جذر المشروع (ملفات التشغيل والإعداد)

| الملف | الغرض |
|--------|--------|
| `package.json` / `package-lock.json` | الحزم والسكربتات |
| `tsconfig.json` | TypeScript → `dist/` |
| `.env` | أسرار التشغيل (لا ترفع للمستودع) |
| `.env.example` | قالب المتغيرات |
| `ecosystem.config.cjs` | PM2 |
| `Dockerfile` / `docker-compose.yml` / `.dockerignore` | حاويات |
| `deploy.sh` | نشر سيرفر (bash) |
| `dev.bat` | تشغيل تطويري سريع (Telegram) |
| `web.bat` | بناء + ويب + تيليجرام |
| `pm2.bat` | بناء + PM2 |
| `run/dev.bat` / `run/web.bat` / `run/pm2.bat` | تشغيل من جذر المشروع (`cd ..` داخل السكربت) |
| `memory.db` | قاعدة SQLite للمحادثات |
| `google-credentials.json` (موصى به) | OAuth Google — المسار من `GOOGLE_CREDENTIALS_PATH` |
| `google-token.json` | رموز OAuth بعد الربط |
| `client_secret_*.json` | قد تكون نسخًا من Console؛ يفضّل توحيد الاسم عبر `GOOGLE_CREDENTIALS_PATH` |
| `tokens/firebase.json` | حساب خدمة Firebase (اختياري) — الاسم القصير الموصى به |
| `tokens/google-oauth.json` | OAuth Google (عميل سطح المكتب/الويب) |
| `tokens/google-oauth-alt.json` | عميل OAuth ثانٍ اختياري |
| `tokens/google-token.json` | رموز OAuth بعد الربط |
| `paths.json` | **فهرس المسارات الأساسية** (مجلدات + ملف DB) |
| `more_paths.json` | **مسارات فرعية** (Google، Firebase، مصدر الواجهة) |
| `SKILL.md` | إرشادات مهارة منفصلة عن تشغيل Node |
| `README.md` | الدليل الطويل |
| **`JARVIS_INDEX.md`** | **هذا الملف — الفهرس الأم** |
| `dist/` | مخرجات `npm run build` + نسخ `public` للويب |
| `uploads/` | مرفوعات الويب (يُنشأ عند التشغيل) |
| `logs/` | سجلات PM2 عند الاستخدام |

---

## أسماء الأدوات للنموذج (API) ↔ الملف

أسماء الاستدعاء كما يراها الـ LLM — **لا تتغير** عند إعادة تسمية الملف إلا إذا عدّلت `registerTool` داخل الملف.

| اسم الأداة للنموذج | ملف التنفيذ |
|---------------------|-------------|
| `get_current_time` | `src/tools/time.ts` |
| `set_memory`, `get_memory`, … | `src/tools/memory.ts` |
| `generate_image` | `src/tools/image-gen.ts` |
| `generate_video` | `src/tools/video-gen.ts` |
| `web_search` | `src/tools/web-search.ts` |
| `execute_command` | `src/tools/terminal.ts` |
| `take_screenshot` | `src/tools/screenshot.ts` |
| `gmail` | `src/tools/gmail.ts` |
| `google_calendar` | `src/tools/gcal.ts` |
| `google_contacts` | `src/tools/gcontacts.ts` |
| `google_drive` | `src/tools/gdrive.ts` |
| `youtube_analytics` | `src/tools/youtube.ts` |
| `browser` | `src/tools/browser.ts` |
| `analyze_screen` | `src/tools/screen.ts` |
| `desktop_control` | `src/tools/desktop.ts` |
| `file_manager` | `src/tools/files.ts` |
| `system_info` | `src/tools/sysinfo.ts` |
| `clipboard` | `src/tools/clipboard.ts` |
| `notification` | `src/tools/notification.ts` |

(أي أداة في `ollama.ts` تتبع التسمية المعرفة داخل نفس الملف.)

---

## مسارات REST و WebSocket (ويب)

- ملف الخادم: `src/interfaces/web/server.ts`
- الواجهة: `src/interfaces/web/public/index.html`
- عادة: `http://localhost:3000` (من `WEB_PORT`)

---

## مرجع سريع للوكيل (Agent)

1. `src/index.ts` يحمّل الإعداد والذاكرة والأدوات ويشغّل Telegram (واختياريًا الويب).
2. رسالة المستخدم → `runAgentLoop` في `loop.ts`.
3. يُبنى السياق من SQLite؛ يُضاف لاحق للوضع (بحث عميق / تفكير / مساعد فقط).
4. `chatWithRouting` في `llm/index.ts` يختار المزوّد.
5. إن وُجدت `tool_calls` يُنفَّذ عبر `executeTool` في `registry.ts` ويُعاد للنموذج حتى رد نهائي أو بلوغ `MAX_AGENT_ITERATIONS`.

التفاصيل السردية والمتغيرات البيئية: راجع `README.md`.

---

*آخر تحديث هيكل: أبريل 2026 — أسماء ملفات الأدوات والوكيل مبسّطة كما في الجدول أعلاه.*
