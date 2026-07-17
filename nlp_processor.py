"""
نظام الترجمة الذكية من العربية إلى Blender باستخدام Windows AI APIs
Intelligent Arabic to Blender Translator using Windows Built-in AI
"""

import requests
import json
import re
from typing import Dict, List, Tuple, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArabicNLPProcessor:
    """معالج اللغة الطبيعية للعربية باستخدام خوارزميات محلية"""
    
    def __init__(self):
        # قاموس شامل للأوامر والمرادفات
        self.commands_db = self._initialize_commands_db()
        self.colors_db = self._initialize_colors_db()
        self.positions_db = self._initialize_positions_db()
        self.properties_db = self._initialize_properties_db()
    
    def _initialize_commands_db(self) -> Dict[str, str]:
        """قاعدة بيانات الأوامر الأساسية والمرادفات"""
        return {
            # إنشاء أشكال
            'مكعب': 'create_cube',
            'مكعب سداسي': 'create_cube',
            'كيوب': 'create_cube',
            'مربع ثلاثي': 'create_cube',
            
            'كرة': 'create_sphere',
            'الكرة': 'create_sphere',
            'كره': 'create_sphere',
            'sphere': 'create_sphere',
            
            'اسطوانة': 'create_cylinder',
            'الاسطوانة': 'create_cylinder',
            'اسطوانه': 'create_cylinder',
            'cylinder': 'create_cylinder',
            
            'مخروط': 'create_cone',
            'المخروط': 'create_cone',
            'مخروطي': 'create_cone',
            'cone': 'create_cone',
            
            'تورس': 'create_torus',
            'الدائرة المجوفة': 'create_torus',
            'حلقة': 'create_torus',
            
            # تحريك
            'حرك': 'move',
            'انقل': 'move',
            'تحريك': 'move',
            'اضغط': 'move',
            
            'دوّر': 'rotate',
            'دير': 'rotate',
            'تدوير': 'rotate',
            'أدر': 'rotate',
            
            'كبّر': 'scale',
            'غيّر الحجم': 'scale',
            'تكبير': 'scale',
            'حجّم': 'scale',
            'صغّر': 'scale_down',
            
            # حذف وتعديل
            'احذف': 'delete',
            'امسح': 'delete',
            'حذف': 'delete',
            'استبدل': 'delete',
            
            'نسخ': 'duplicate',
            'انسخ': 'duplicate',
            'كرر': 'duplicate',
            'ضاعف': 'duplicate',
            
            'الصق': 'paste',
            'الصقها': 'paste',
            'أضف': 'paste',
            
            # الظهور والإخفاء
            'اخف': 'hide',
            'أخف': 'hide',
            'إخفاء': 'hide',
            'اختبئ': 'hide',
            
            'اظهر': 'show',
            'أظهر': 'show',
            'إظهار': 'show',
            'اطلع': 'show',
            
            # التجميع
            'جمّع': 'group',
            'تجميع': 'group',
            'جمع': 'group',
            
            'فك': 'ungroup',
            'افصل': 'ungroup',
            'فصل': 'ungroup',
        }
    
    def _initialize_colors_db(self) -> Dict[str, Tuple[float, float, float, float]]:
        """قاعدة بيانات الألوان بصيغة RGBA"""
        return {
            'أحمر': (1.0, 0.0, 0.0, 1.0),
            'احمر': (1.0, 0.0, 0.0, 1.0),
            'الأحمر': (1.0, 0.0, 0.0, 1.0),
            'red': (1.0, 0.0, 0.0, 1.0),
            
            'أخضر': (0.0, 1.0, 0.0, 1.0),
            'اخضر': (0.0, 1.0, 0.0, 1.0),
            'الأخضر': (0.0, 1.0, 0.0, 1.0),
            'green': (0.0, 1.0, 0.0, 1.0),
            
            'أزرق': (0.0, 0.0, 1.0, 1.0),
            'ازرق': (0.0, 0.0, 1.0, 1.0),
            'الأزرق': (0.0, 0.0, 1.0, 1.0),
            'blue': (0.0, 0.0, 1.0, 1.0),
            
            'أصفر': (1.0, 1.0, 0.0, 1.0),
            'اصفر': (1.0, 1.0, 0.0, 1.0),
            'الأصفر': (1.0, 1.0, 0.0, 1.0),
            'yellow': (1.0, 1.0, 0.0, 1.0),
            
            'أبيض': (1.0, 1.0, 1.0, 1.0),
            'ابيض': (1.0, 1.0, 1.0, 1.0),
            'الأبيض': (1.0, 1.0, 1.0, 1.0),
            'white': (1.0, 1.0, 1.0, 1.0),
            
            'أسود': (0.0, 0.0, 0.0, 1.0),
            'اسود': (0.0, 0.0, 0.0, 1.0),
            'الأسود': (0.0, 0.0, 0.0, 1.0),
            'black': (0.0, 0.0, 0.0, 1.0),
            
            'برتقالي': (1.0, 0.5, 0.0, 1.0),
            'برتقالى': (1.0, 0.5, 0.0, 1.0),
            'orange': (1.0, 0.5, 0.0, 1.0),
            
            'بنفسجي': (1.0, 0.0, 1.0, 1.0),
            'بنفسجى': (1.0, 0.0, 1.0, 1.0),
            'purple': (1.0, 0.0, 1.0, 1.0),
            
            'رمادي': (0.5, 0.5, 0.5, 1.0),
            'رمادى': (0.5, 0.5, 0.5, 1.0),
            'gray': (0.5, 0.5, 0.5, 1.0),
            
            'سماوي': (0.0, 1.0, 1.0, 1.0),
            'سماوى': (0.0, 1.0, 1.0, 1.0),
            'cyan': (0.0, 1.0, 1.0, 1.0),
        }
    
    def _initialize_positions_db(self) -> Dict[str, Dict[str, float]]:
        """قاعدة بيانات المواضع والاتجاهات"""
        return {
            'يمين': {'x': 2.0, 'y': 0, 'z': 0},
            'اليمين': {'x': 2.0, 'y': 0, 'z': 0},
            'يساراً': {'x': -2.0, 'y': 0, 'z': 0},
            'يسار': {'x': -2.0, 'y': 0, 'z': 0},
            'اليسار': {'x': -2.0, 'y': 0, 'z': 0},
            'أمام': {'x': 0, 'y': 2.0, 'z': 0},
            'قدام': {'x': 0, 'y': 2.0, 'z': 0},
            'خلف': {'x': 0, 'y': -2.0, 'z': 0},
            'أعلى': {'x': 0, 'y': 0, 'z': 2.0},
            'فوق': {'x': 0, 'y': 0, 'z': 2.0},
            'أسفل': {'x': 0, 'y': 0, 'z': -2.0},
            'تحت': {'x': 0, 'y': 0, 'z': -2.0},
        }
    
    def _initialize_properties_db(self) -> Dict[str, Dict[str, Any]]:
        """قاعدة بيانات الخصائص الإضافية"""
        return {
            'كبير': {'scale': 2.0, 'size_level': 'large'},
            'الكبير': {'scale': 2.0, 'size_level': 'large'},
            'كبيرة': {'scale': 2.0, 'size_level': 'large'},
            'ضخم': {'scale': 3.0, 'size_level': 'huge'},
            'ضخمة': {'scale': 3.0, 'size_level': 'huge'},
            'عملاق': {'scale': 3.0, 'size_level': 'huge'},
            
            'صغير': {'scale': 0.5, 'size_level': 'small'},
            'الصغير': {'scale': 0.5, 'size_level': 'small'},
            'صغيرة': {'scale': 0.5, 'size_level': 'small'},
            'دقيق': {'scale': 0.3, 'size_level': 'tiny'},
            'دقيقة': {'scale': 0.3, 'size_level': 'tiny'},
            'صغرى': {'scale': 0.3, 'size_level': 'tiny'},
            
            'شفاف': {'transparency': 0.5, 'opacity': 0.5},
            'شفافة': {'transparency': 0.5, 'opacity': 0.5},
            'نصف شفاف': {'transparency': 0.3, 'opacity': 0.7},
            
            'معدني': {'material': 'metallic', 'roughness': 0.2},
            'معدنية': {'material': 'metallic', 'roughness': 0.2},
            'لامع': {'material': 'glossy', 'roughness': 0.1},
            'لامعة': {'material': 'glossy', 'roughness': 0.1},
            'غير لامع': {'material': 'matte', 'roughness': 0.8},
            'مطفي': {'material': 'matte', 'roughness': 0.8},
        }
    
    def tokenize_arabic(self, text: str) -> List[str]:
        """تقسيم النص العربي إلى كلمات"""
        # تنظيف النص
        text = text.strip()
        
        # تقسيم حسب المسافات والعلامات
        tokens = re.split(r'[\s\-\,\.]+', text)
        tokens = [t for t in tokens if t]  # إزالة الرموز الفارغة
        
        return tokens
    
    def find_matching_command(self, tokens: List[str]) -> Tuple[str, str]:
        """البحث عن أمر مطابق في قاعدة البيانات"""
        best_match = None
        best_score = 0
        
        for token in tokens:
            for db_command, command_id in self.commands_db.items():
                # مطابقة دقيقة
                if token == db_command:
                    return command_id, token
                
                # مطابقة جزئية
                similarity = self._calculate_similarity(token, db_command)
                if similarity > best_score:
                    best_score = similarity
                    best_match = (command_id, db_command)
        
        return best_match if best_match else (None, None)
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """حساب تشابه بين نصين"""
        if len(str1) == 0 or len(str2) == 0:
            return 0.0
        
        # Levenshtein distance
        matches = sum(1 for a, b in zip(str1, str2) if a == b)
        return matches / max(len(str1), len(str2))
    
    def extract_color(self, tokens: List[str]) -> Tuple[str, Tuple]:
        """استخراج اللون من الأوامر"""
        for token in tokens:
            if token in self.colors_db:
                return token, self.colors_db[token]
        return None, None
    
    def extract_position(self, tokens: List[str]) -> Tuple[str, Dict]:
        """استخراج الموضع/الاتجاه من الأوامر"""
        for token in tokens:
            if token in self.positions_db:
                return token, self.positions_db[token]
        return None, None
    
    def extract_properties(self, tokens: List[str]) -> List[Dict]:
        """استخراج الخصائص الإضافية"""
        properties = []
        for token in tokens:
            if token in self.properties_db:
                properties.append(self.properties_db[token])
        return properties
    
    def parse_command(self, arabic_text: str) -> Dict[str, Any]:
        """تحليل كامل للأمر العربي"""
        logger.info(f"🔍 تحليل الأمر: {arabic_text}")
        
        tokens = self.tokenize_arabic(arabic_text)
        logger.info(f"📝 الرموز: {tokens}")
        
        result = {
            'original_text': arabic_text,
            'tokens': tokens,
            'command': None,
            'command_name': None,
            'color': None,
            'color_value': None,
            'position': None,
            'position_value': None,
            'properties': [],
            'confidence': 0.0
        }
        
        # البحث عن الأمر الرئيسي
        command_id, command_name = self.find_matching_command(tokens)
        if command_id:
            result['command'] = command_id
            result['command_name'] = command_name
            result['confidence'] = 0.9
            logger.info(f"✅ تم العثور على أمر: {command_id}")
        else:
            result['confidence'] = 0.0
            logger.warning("❌ لم يتم العثور على أمر معروف")
            return result
        
        # استخراج اللون
        color_name, color_value = self.extract_color(tokens)
        if color_name:
            result['color'] = color_name
            result['color_value'] = color_value
            logger.info(f"🎨 اللون: {color_name} = {color_value}")
        
        # استخراج الموضع
        position_name, position_value = self.extract_position(tokens)
        if position_name:
            result['position'] = position_name
            result['position_value'] = position_value
            logger.info(f"📍 الموضع: {position_name} = {position_value}")
        
        # استخراج الخصائص
        properties = self.extract_properties(tokens)
        if properties:
            result['properties'] = properties
            logger.info(f"🔧 الخصائص: {properties}")
        
        return result


class BlenderCommandGenerator:
    """توليد أوامر Blender Python من البيانات المستخرجة"""
    
    @staticmethod
    def generate_command(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """توليد أمر Blender من البيانات المحللة"""
        
        if not parsed_data['command']:
            return {
                'status': 'error',
                'message': 'لم يتم التعرف على الأمر',
                'code': None
            }
        
        command = parsed_data['command']
        code_lines = []
        
        # بناء كود Python لـ Blender
        if command == 'create_cube':
            code_lines.append("import bpy")
            code_lines.append("bpy.ops.mesh.primitive_cube_add()")
            code_lines.append("obj = bpy.context.active_object")
            
            if parsed_data['color_value']:
                r, g, b, a = parsed_data['color_value']
                code_lines.append(f"mat = bpy.data.materials.new(name='Material')")
                code_lines.append(f"mat.use_nodes = True")
                code_lines.append(f"mat.node_tree.nodes['Principled BSDF'].inputs[0].default_value = ({r}, {g}, {b}, {a})")
                code_lines.append(f"obj.data.materials.append(mat)")
            
            if parsed_data['position_value']:
                x = parsed_data['position_value'].get('x', 0)
                y = parsed_data['position_value'].get('y', 0)
                z = parsed_data['position_value'].get('z', 0)
                code_lines.append(f"obj.location = ({x}, {y}, {z})")
            
            if parsed_data['properties']:
                for prop in parsed_data['properties']:
                    if 'scale' in prop:
                        code_lines.append(f"obj.scale = ({prop['scale']}, {prop['scale']}, {prop['scale']})")
        
        elif command == 'create_sphere':
            code_lines.append("import bpy")
            code_lines.append("bpy.ops.mesh.primitive_uv_sphere_add()")
            code_lines.append("obj = bpy.context.active_object")
            
            if parsed_data['color_value']:
                r, g, b, a = parsed_data['color_value']
                code_lines.append(f"mat = bpy.data.materials.new(name='Material')")
                code_lines.append(f"mat.use_nodes = True")
                code_lines.append(f"mat.node_tree.nodes['Principled BSDF'].inputs[0].default_value = ({r}, {g}, {b}, {a})")
                code_lines.append(f"obj.data.materials.append(mat)")
        
        elif command == 'delete':
            code_lines.append("import bpy")
            code_lines.append("bpy.ops.object.delete(use_global=False)")
        
        elif command == 'duplicate':
            code_lines.append("import bpy")
            code_lines.append("bpy.ops.object.duplicate()")
        
        elif command == 'hide':
            code_lines.append("import bpy")
            code_lines.append("obj = bpy.context.active_object")
            code_lines.append("if obj: obj.hide_set(True)")
        
        elif command == 'show':
            code_lines.append("import bpy")
            code_lines.append("obj = bpy.context.active_object")
            code_lines.append("if obj: obj.hide_set(False)")
        
        code = "\n".join(code_lines)
        
        return {
            'status': 'success',
            'message': f'تم توليد الأمر بنجاح',
            'code': code,
            'command': command,
            'explanation': f"الأمر: {parsed_data['command_name']}",
            'parsed_data': parsed_data
        }
