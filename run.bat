@echo off
REM ملف البدء السريع للبرنامج على Windows
REM Quick Start Script for Arabic Blender Translator

echo.
echo ╯──────────────────────────────────────────────────────────────────╾
echo ║  🎨 مترجم الأوامر العربية إلى Blender                    ║
echo ║  Arabic Blender Translator v1.0.0                         ║
echo ╙──────────────────────────────────────────────────────────────────╚
echo.

REM التحقق من Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ خطأ: لم يتم العثور على Python!
    echo ⚠️  الرجاء تثبيت Python 3.7+ من https://www.python.org/
    pause
    exit /b 1
)

echo ✅ تم العثور على Python
echo.

echo 🔍 هل فتحت Blender بالفعل?
echo.
echo 📌 خطوات التثبيت:
echo 1. افتح Blender
echo 2. اذهب إلى Edit ^> Preferences ^> Add-ons
echo 3. اضغط Install
echo 4. اختر blender_addon_pro.py من هذا المجلد
echo 5. فعِّ الإضافة
echo.

:start_gui
echo 🚀 جاري تشغيل البرنامج...
echo.

python gui_pro.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ خطأ في تشغيل البرنامج!
    echo.
    pause
    exit /b 1
)

pause
