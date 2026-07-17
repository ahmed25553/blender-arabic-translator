"""
مثال على الاستخدام المباشر للمكتبة
Example Usage of the Arabic Blender Translator Library
"""

from nlp_processor import ArabicNLPProcessor, BlenderCommandGenerator

# ===== مثال 1: تحليل أمر بسيط =====
print("=" * 60)
print("مثال 1: تحليل أمر بسيط")
print("=" * 60)

nlp = ArabicNLPProcessor()
command = "مكعب أحمر"
parsed = nlp.parse_command(command)

print(f"الأمر الأصلي: {command}")
print(f"الأمر المعروف: {parsed['command']}")
print(f"اللون: {parsed['color']}")
print(f"الثقة: {parsed['confidence'] * 100}%")

# ===== مثال 2: توليد الكود =====
print("\n" + "=" * 60)
print("مثال 2: توليد كود Blender")
print("=" * 60)

result = BlenderCommandGenerator.generate_command(parsed)

print(f"الحالة: {result['status']}")
print(f"الشرح: {result['explanation']}")
print(f"\nالكود المولد:\n")
print(result['code'])

# ===== مثال 3: أمر معقد =====
print("\n" + "=" * 60)
print("مثال 3: أمر معقد مع عدة معاملات")
print("=" * 60)

command2 = "كرة زرقاء كبيرة جداً"
parsed2 = nlp.parse_command(command2)
result2 = BlenderCommandGenerator.generate_command(parsed2)

print(f"الأمر: {command2}")
print(f"الخصائص المكتشفة: {len(parsed2['properties'])} خاصية")
print(f"\nالكود:\n")
print(result2['code'])

# ===== مثال 4: قائمة الألوان المدعومة =====
print("\n" + "=" * 60)
print("مثال 4: الألوان المدعومة")
print("=" * 60)

colors = nlp.colors_db
print(f"عدد الألوان: {len(colors)}")
print("\nبعض الألوان:")
for i, (color_ar, color_rgb) in enumerate(list(colors.items())[:10]):
    print(f"  • {color_ar}: {color_rgb}")

# ===== مثال 5: قائمة الأوامر المدعومة =====
print("\n" + "=" * 60)
print("مثال 5: الأوامر المدعومة")
print("=" * 60)

commands = nlp.commands_db
print(f"عدد الأوامر: {len(commands)}")
print("\nأمثلة على الأوامر:")
for i, (cmd_ar, cmd_id) in enumerate(list(commands.items())[:15]):
    print(f"  • {cmd_ar} → {cmd_id}")

print("\n" + "=" * 60)
print("✅ انتهت الأمثلة!")
print("=" * 60)
