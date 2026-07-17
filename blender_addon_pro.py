"""
إضافة Blender المحسّنة مع خادم TCP
Enhanced Blender Add-on with TCP Server
"""

import bpy
import socket
import json
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bl_info = {
    "name": "Arabic Blender Translator Pro",
    "blender": (3, 0, 0),
    "version": (1, 0, 0),
    "location": "View3D > Sidebar",
    "description": "نظام متقدم لترجمة الأوامر العربية إلى Blender",
    "author": "Ahmed",
    "category": "Tools",
}


class BlenderServer:
    """خادم TCP للإضافة"""
    
    def __init__(self):
        self.socket = None
        self.is_running = False
        self.thread = None
    
    def start(self):
        """بدء الخادم"""
        self.is_running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        logger.info("✅ خادم Blender يعمل على المنفذ 9998")
    
    def _run_server(self):
        """تشغيل الخادم"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('localhost', 9998))
            self.socket.listen(5)
            
            while self.is_running:
                try:
                    client, addr = self.socket.accept()
                    self._handle_client(client)
                except:
                    pass
        except Exception as e:
            logger.error(f"❌ خطأ في الخادم: {e}")
    
    def _handle_client(self, client):
        """معالجة عميل"""
        try:
            data = client.recv(4096).decode('utf-8')
            message = json.loads(data)
            
            if message['type'] == 'execute_code':
                code = message['data']['code']
                try:
                    exec(code)
                    response = {'status': 'success', 'message': 'تم التنفيذ بنجاح'}
                except Exception as e:
                    response = {'status': 'error', 'message': str(e)}
            else:
                response = {'status': 'error', 'message': 'نوع رسالة غير معروف'}
            
            client.send(json.dumps(response).encode('utf-8'))
        except:
            pass
        finally:
            client.close()
    
    def stop(self):
        """إيقاف الخادم"""
        self.is_running = False
        if self.socket:
            self.socket.close()


# متغير عام للخادم
_server = None


class ARABIC_TRANSLATOR_PT_Panel(bpy.types.Panel):
    """لوحة الإضافة"""
    bl_label = "مترجم الأوامر العربية"
    bl_idname = "ARABIC_TRANSLATOR_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Arabic"
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="🎬 الخادم جاهز")
        layout.label(text="استخدم التطبيق الرسومي")
        layout.label(text="لإرسال الأوامر")


def register():
    """تسجيل الإضافة"""
    global _server
    
    bpy.utils.register_class(ARABIC_TRANSLATOR_PT_Panel)
    
    _server = BlenderServer()
    _server.start()
    
    logger.info("✅ تم تثبيت الإضافة بنجاح")


def unregister():
    """إلغاء الإضافة"""
    global _server
    
    if _server:
        _server.stop()
    
    bpy.utils.unregister_class(ARABIC_TRANSLATOR_PT_Panel)
    logger.info("🛑 تم إلغاء الإضافة")


if __name__ == "__main__":
    register()
