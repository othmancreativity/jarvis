Jarvis — مجلد التشغيل (Windows)
================================

الملفات:
  dev.bat   — تطوير: npx tsx src/index.ts (Telegram فقط)
  web.bat   — بناء + تشغيل الويب + Telegram
  pm2.bat   — بناء + تشغيل في الخلفية عبر PM2
  stop-pm2.bat — إيقاف عملية jarvis في PM2 (اقرأ السبب أدناه)

في جذر المشروع (مجلد أب لـ run) يوجد dev.bat و web.bat و pm2.bat
تستدعي نفس السكربتات أعلاه — لتشغيل مباشر دون الدخول إلى run/.

مهم جداً — خطأ 409 Conflict
---------------------------
Telegram لا يسمح بأكثر من برنامج يستدعي getUpdates لنفس توكن البوت في نفس الوقت.

إذا كان jarvis يعمل في PM2 وفتحت npm run dev في طرفية أخرى، سيظهر:
  Conflict: terminated by other getUpdates request

الحل:
  1) نفّذ stop-pm2.bat  أو  pm2 stop jarvis
  2) ثم شغّل dev.bat أو npm run dev

أو العكس: إذا أردت PM2 فقط، أغلق أي npm run dev مفتوح.

كل سكربت يضبط المجلد الحالي على جذر المشروع (المجلد الأب لـ run).
