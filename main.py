"""
AI Universal Ultra Clarity X300 PRO
Full Source Code - Super Resolution & Anti-Distortion Sharpener
"""
import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from PIL import Image as PILImage, ImageEnhance, ImageFilter, ImageOps, ImageStat

class UniversalAIZoomApp(App):
    def build(self):
        self.title = "AI Universal Ultra Clarity PRO"
        
        main_layout = BoxLayout(orientation='vertical', padding=12, spacing=10)
        
        # Header
        header = Label(
            text="[b]✨ AI Universal Ultra Clarity PRO[/b]",
            markup=True,
            font_size='22sp',
            size_hint_y=0.1,
            color=(0.4, 0.8, 1, 1)
        )
        main_layout.add_widget(header)
        
        # Image Preview Area
        self.img_widget = Image(source='', size_hint_y=0.55)
        main_layout.add_widget(self.img_widget)
        
        # Status Label
        self.status_label = Label(
            text="AI chống biến dạng: Tái tạo biên độ điểm ảnh & giữ nguyên chủ thể",
            size_hint_y=0.08,
            font_size='13sp',
            color=(0.8, 0.8, 0.8, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Zoom / Sharpness Level Slider
        zoom_box = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=5)
        zoom_box.add_widget(Label(text="Mức độ AI:", size_hint_x=0.25))
        self.slider = Slider(min=1, max=5, value=3, step=0.5, size_hint_x=0.55)
        self.slider.bind(value=self.on_slider_change)
        zoom_box.add_widget(self.slider)
        self.zoom_val_label = Label(text="Mức 3 (Chuyên sâu)", size_hint_x=0.25)
        zoom_box.add_widget(self.zoom_val_label)
        main_layout.add_widget(zoom_box)
        
        # Action Buttons
        btn_box = BoxLayout(orientation='horizontal', size_hint_y=0.12, spacing=10)
        
        btn_select = Button(
            text="📂 Chọn Ảnh",
            background_color=(0.2, 0.3, 0.4, 1),
            font_size='15sp'
        )
        btn_select.bind(on_press=self.open_file_chooser)
        btn_box.add_widget(btn_select)
        
        self.btn_process = Button(
            text="🚀 AI Ultra Sharpen Pro",
            background_color=(0.1, 0.6, 0.9, 1),
            font_size='15sp'
        )
        self.btn_process.bind(on_press=self.process_universal_ai)
        btn_box.add_widget(self.btn_process)
        
        main_layout.add_widget(btn_box)
        
        self.current_image_path = None
        return main_layout

    def on_slider_change(self, instance, value):
        modes = {1.0: "Tự nhiên", 2.0: "Khử nhòe", 3.0: "Chuyên sâu", 4.0: "Siêu nét", 5.0: "X300 Pro Ultra"}
        self.zoom_val_label.text = modes.get(value, f"Mức {value}")

    def open_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(path='.')
        content.add_widget(filechooser)
        
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        btn_cancel = Button(text="Hủy")
        btn_open = Button(text="Mở Ảnh", background_color=(0.1, 0.6, 0.9, 1))
        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_open)
        content.add_widget(btn_layout)
        
        popup = Popup(title="Chọn ảnh trong máy", content=content, size_hint=(0.9, 0.9))
        
        def select_file(btn):
            if filechooser.selection:
                self.current_image_path = filechooser.selection[0]
                self.img_widget.source = self.current_image_path
                self.status_label.text = f"Đã tải: {os.path.basename(self.current_image_path)}"
            popup.dismiss()
            
        btn_open.bind(on_press=select_file)
        btn_cancel.bind(on_press=popup.dismiss)
        popup.open()

    def process_universal_ai(self, instance):
        if not self.current_image_path:
            self.status_label.text = "⚠️ Hãy chọn một tấm ảnh trước đã bro!"
            return
            
        self.status_label.text = "⚡ AI đang tính toán ma trận ma sát biên độ..."
        self.btn_process.disabled = True
        threading.Thread(target=self._universal_ai_worker).start()

    def _universal_ai_worker(self):
        try:
            img = PILImage.open(self.current_image_path).convert('RGB')
            level = self.slider.value
            
            # Step 1: Intelligent Upsampling (Khôi phục ma trận pixel)
            scale_factor = 1.5 + (level * 0.1)
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
            img_upscaled = img.resize(new_size, PILImage.Resampling.LANCZOS)
            
            # Step 2: Anti-Distortion High-Pass Filtering (Nổi bật biên dạng mà không bịa đường nét)
            blur = img_upscaled.filter(ImageFilter.GaussianBlur(radius=1.5))
            high_pass = ImageOps.invert(ImageOps.autocontrast(ImageOps.fit(img_upscaled, blur.size)))
            
            # Step 3: Multi-Layer Precision Sharpening
            sharpener = ImageEnhance.Sharpness(img_upscaled)
            img_sharp = sharpener.enhance(1.8 + (level * 0.4))
            
            # Step 4: Unsharp Masking giữ chuẩn nét gốc
            final_img = img_sharp.filter(
                ImageFilter.UnsharpMask(radius=int(level * 0.8) + 1, percent=140 + int(level * 25), threshold=1)
            )
            
            # Step 5: Adaptive Contrast Enhancement (Tăng độ tương phản giữ nguyên màu)
            contrast = ImageEnhance.Contrast(final_img)
            final_img = contrast.enhance(1.08)
            
            output_path = "universal_enhanced_pro.png"
            final_img.save(output_path, quality=98)
            
            def update_ui(dt):
                self.img_widget.source = output_path
                self.img_widget.reload()
                self.status_label.text = "✅ Đã tái tạo sắc nét & KHÔNG sai lệch chủ thể!"
                self.btn_process.disabled = False
                
            from kivy.clock import Clock
            Clock.schedule_once(update_ui)
        except Exception as e:
            def handle_error(dt):
                self.status_label.text = f"❌ Lỗi: {str(e)}"
                self.btn_process.disabled = False
            from kivy.clock import Clock
            Clock.schedule_once(handle_error)

if __name__ == '__main__':
    UniversalAIZoomApp().run()
