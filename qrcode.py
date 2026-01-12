import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import os

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор QR-кодов")
        self.root.geometry("500x600")
        
        # Переменные
        self.qr_image = None
        self.last_qr_path = None
        
        # Цвета
        self.bg_color = "#f0f0f0"
        self.accent_color = "#4a6fa5"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Настройка стиля
        self.root.configure(bg=self.bg_color)
        
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="Генератор QR-кодов",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack(pady=20)
        
        # Фрейм для ввода данных
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10)
        
        # Метка и поле для текста/URL
        tk.Label(
            input_frame,
            text="Введите текст или URL:",
            font=("Arial", 12),
            bg=self.bg_color
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.text_entry = tk.Text(
            input_frame,
            height=4,
            width=40,
            font=("Arial", 10),
            wrap="word"
        )
        self.text_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Параметры QR-кода
        params_frame = tk.LabelFrame(
            self.root,
            text="Параметры QR-кода",
            font=("Arial", 12),
            bg=self.bg_color
        )
        params_frame.pack(pady=10, padx=20, fill="x")
        
        # Цвета
        tk.Label(
            params_frame,
            text="Цвет:",
            bg=self.bg_color
        ).grid(row=0, column=0, padx=5, pady=5)
        
        self.color_var = tk.StringVar(value="#000000")
        color_entry = tk.Entry(
            params_frame,
            textvariable=self.color_var,
            width=10
        )
        color_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Цвет фона
        tk.Label(
            params_frame,
            text="Фон:",
            bg=self.bg_color
        ).grid(row=0, column=2, padx=5, pady=5)
        
        self.bg_color_var = tk.StringVar(value="#FFFFFF")
        bg_color_entry = tk.Entry(
            params_frame,
            textvariable=self.bg_color_var,
            width=10
        )
        bg_color_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Размер
        tk.Label(
            params_frame,
            text="Размер:",
            bg=self.bg_color
        ).grid(row=1, column=0, padx=5, pady=5)
        
        self.size_var = tk.IntVar(value=10)
        size_scale = tk.Scale(
            params_frame,
            from_=1,
            to=20,
            variable=self.size_var,
            orient="horizontal",
            bg=self.bg_color
        )
        size_scale.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        # Фрейм для кнопок
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        # Кнопки
        self.generate_btn = tk.Button(
            button_frame,
            text="Сгенерировать QR-код",
            command=self.generate_qr,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 12),
            padx=20,
            pady=10
        )
        self.generate_btn.pack(side="left", padx=5)
        
        self.save_btn = tk.Button(
            button_frame,
            text="Сохранить",
            command=self.save_qr,
            bg="#2e7d32",
            fg="white",
            font=("Arial", 12),
            padx=20,
            pady=10,
            state="disabled"
        )
        self.save_btn.pack(side="left", padx=5)
        
        self.open_btn = tk.Button(
            button_frame,
            text="Открыть",
            command=self.open_qr,
            bg="#1565c0",
            fg="white",
            font=("Arial", 12),
            padx=20,
            pady=10,
            state="disabled"
        )
        self.open_btn.pack(side="left", padx=5)
        
        # Область для отображения QR-кода
        self.qr_label = tk.Label(
            self.root,
            text="QR-код появится здесь",
            bg="white",
            relief="solid",
            bd=1
        )
        self.qr_label.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Статусная строка
        self.status_var = tk.StringVar(value="Готов к работе")
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=self.bg_color,
            font=("Arial", 10)
        )
        status_label.pack(side="bottom", pady=5)
        
    def generate_qr(self):
        """Генерация QR-кода"""
        text = self.text_entry.get("1.0", "end-1c").strip()
        
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст или URL!")
            return
        
        try:
            # Создание QR-кода
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=self.size_var.get(),
                border=4,
            )
            
            qr.add_data(text)
            qr.make(fit=True)
            
            # Создание изображения с пользовательскими цветами
            qr_img = qr.make_image(
                fill_color=self.color_var.get(),
                back_color=self.bg_color_var.get()
            )
            
            # Сохранение временного файла
            self.last_qr_path = "temp_qr.png"
            qr_img.save(self.last_qr_path)
            
            # Отображение в GUI
            self.display_qr(self.last_qr_path)
            
            # Активация кнопок
            self.save_btn.config(state="normal")
            self.open_btn.config(state="normal")
            
            self.status_var.set(f"QR-код создан для: {text[:50]}...")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать QR-код: {str(e)}")
            self.status_var.set("Ошибка при создании QR-кода")
    
    def display_qr(self, image_path):
        """Отображение QR-кода в интерфейсе"""
        try:
            img = Image.open(image_path)
            img.thumbnail((300, 300))
            
            photo = ImageTk.PhotoImage(img)
            self.qr_label.config(image=photo, text="")
            self.qr_label.image = photo
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отобразить QR-код: {str(e)}")
    
    def save_qr(self):
        """Сохранение QR-кода в файл"""
        if not self.last_qr_path:
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG файлы", "*.png"),
                ("JPEG файлы", "*.jpg"),
                ("Все файлы", "*.*")
            ],
            initialfile="qrcode.png"
        )
        
        if file_path:
            try:
                img = Image.open(self.last_qr_path)
                img.save(file_path)
                self.status_var.set(f"QR-код сохранен: {os.path.basename(file_path)}")
                messagebox.showinfo("Успех", "QR-код успешно сохранен!")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
    
    def open_qr(self):
        """Открытие QR-кода в стандартном просмотрщике"""
        if self.last_qr_path and os.path.exists(self.last_qr_path):
            webbrowser.open(f"file://{os.path.abspath(self.last_qr_path)}")
    
    def __del__(self):
        """Очистка временных файлов при закрытии"""
        if self.last_qr_path and os.path.exists(self.last_qr_path):
            try:
                os.remove(self.last_qr_path)
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()