#!/bin/bash
# ملف البدء السريع للبرنامج على Linux/Mac
# Quick Start Script for Arabic Blender Translator

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🎨 مترجم الأوامر العربية إلى Blender                    ║"
echo "║  Arabic Blender Translator v1.0.0                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ خطأ: لم يتم العثور على Python!"
    echo "⚠️  الرجاء تثبيت Python 3.7+ من https://www.python.org/"
    exit 1
fi

echo "✅ تم العثور على Python"
echo ""

# التحقق من Blender
echo "🔍 هل فتحت Blender بالفعل؟"
echo ""
echo "📌 خطوات التثبيت:"
echo "1. افتح Blender"
echo "2. اذهب إلى Edit > Preferences > Add-ons"
echo "3. اضغط Install"
echo "4. اختر blender_addon_pro.py من هذا المجلد"
echo "5. فعّل الإضافة"
echo ""

echo "🚀 جاري تشغيل البرنامج..."
echo ""

python3 gui_pro.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ خطأ في تشغيل البرنامج!"
    echo ""
    exit 1
fi
