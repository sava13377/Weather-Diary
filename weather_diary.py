import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary - Дневник погоды")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Файл для хранения данных (ОБЯЗАТЕЛЬНОЕ сохранение в JSON)
        self.data_file = "weather_data.json"
        self.entries = []
        
        # Загрузка существующих данных из JSON (если файл есть)
        self.load_from_json_file()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление таблицы
        self.refresh_table()
    
    def create_widgets(self):
        # Рамка для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавление новой записи", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Поля ввода
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=20)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.temp_entry = ttk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Описание погоды:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        self.precip_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Осадки", variable=self.precip_var).grid(row=2, column=0, padx=5, pady=5)
        
        ttk.Button(input_frame, text="➕ Добавить запись", command=self.add_entry).grid(row=2, column=1, padx=5, pady=5)
        
        # Рамка для фильтров
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация записей", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_date = ttk.Entry(filter_frame, width=15)
        self.filter_date.grid(row=0, column=1, padx=5, pady=5)
        self.filter_date.insert(0, "ГГГГ-ММ-ДД")
        
        ttk.Label(filter_frame, text="Температура >").grid(row=0, column=2, padx=5, pady=5)
        self.filter_temp_above = ttk.Entry(filter_frame, width=8)
        self.filter_temp_above.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filter).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(filter_frame, text="🗑 Сбросить фильтр", command=self.reset_filter).grid(row=0, column=5, padx=5, pady=5)
        
        # Рамка для списка записей
        list_frame = ttk.LabelFrame(self.root, text="Записи о погоде", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("Дата", "Температура", "Описание", "Осадки")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.column("Температура", width=100)
        self.tree.column("Осадки", width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Рамка для кнопок управления файлами
        file_frame = ttk.Frame(self.root)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(file_frame, text="💾 Сохранить в JSON", command=self.save_to_json_file).pack(side="left", padx=5)
        ttk.Button(file_frame, text="📂 Загрузить из JSON", command=self.load_from_json_dialog).pack(side="left", padx=5)
        
        # Информационная метка
        info_label = ttk.Label(file_frame, text="✓ Данные автоматически сохраняются в weather_data.json", 
                               foreground="green")
        info_label.pack(side="right", padx=10)
    
    def save_to_json_file(self, filename=None):
        """СОХРАНЕНИЕ В JSON ФАЙЛ (обязательная функция)"""
        if filename is None:
            filename = self.data_file
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=4)
            print(f"✅ Данные сохранены в {filename}")  # Отладка в консоли
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные в JSON: {e}")
            return False
    
    def load_from_json_file(self, filename=None):
        """ЗАГРУЗКА ИЗ JSON ФАЙЛА (обязательная функция)"""
        if filename is None:
            filename = self.data_file
        
        if not os.path.exists(filename):
            print(f"ℹ️ Файл {filename} не найден, создан новый список записей")
            self.entries = []
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.entries = json.load(f)
            print(f"✅ Данные загружены из {filename}, найдено {len(self.entries)} записей")
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные из JSON: {e}")
            self.entries = []
    
    def load_from_json_dialog(self):
        """Загрузка из выбранного JSON файла через диалог"""
        filename = filedialog.askopenfilename(
            title="Выберите JSON файл",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.load_from_json_file(filename)
            self.refresh_table()
    
    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def validate_temperature(self, temp_str):
        try:
            float(temp_str)
            return True
        except ValueError:
            return False
    
    def add_entry(self):
        """Добавление записи с ОБЯЗАТЕЛЬНЫМ сохранением в JSON"""
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        description = self.desc_entry.get().strip()
        precipitation = self.precip_var.get()
        
        # Валидация
        if not date:
            messagebox.showerror("Ошибка", "Дата не может быть пустой!")
            return
        
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return
        
        if not temp:
            messagebox.showerror("Ошибка", "Температура не может быть пустой!")
            return
        
        if not self.validate_temperature(temp):
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
        
        if not description:
            messagebox.showerror("Ошибка", "Описание погоды не может быть пустым!")
            return
        
        # Создание записи
        entry = {
            "date": date,
            "temperature": float(temp),
            "description": description,
            "precipitation": precipitation
        }
        
        self.entries.append(entry)
        
        # ОБЯЗАТЕЛЬНОЕ СОХРАНЕНИЕ В JSON ФАЙЛ
        if self.save_to_json_file():
            self.refresh_table()
            
            # Очистка полей
            self.temp_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.precip_var.set(False)
            
            messagebox.showinfo("Успех", "Запись успешно добавлена и сохранена в JSON!")
        else:
            # Если сохранение не удалось, удаляем добавленную запись
            self.entries.pop()
            messagebox.showerror("Ошибка", "Не удалось сохранить запись в JSON файл!")
    
    def refresh_table(self, filtered_entries=None):
        """Обновление таблицы"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        data = filtered_entries if filtered_entries is not None else self.entries
        data.sort(key=lambda x: x["date"])
        
        for entry in data:
            precip_text = "Да" if entry["precipitation"] else "Нет"
            self.tree.insert("", "end", values=(
                entry["date"],
                f"{entry['temperature']:.1f}°C",
                entry["description"],
                precip_text
            ))
    
    def apply_filter(self):
        filter_date = self.filter_date.get().strip()
        filter_temp_above = self.filter_temp_above.get().strip()
        
        filtered = self.entries.copy()
        
        if filter_date and filter_date != "ГГГГ-ММ-ДД":
            if not self.validate_date(filter_date):
                messagebox.showerror("Ошибка", "Неверный формат даты в фильтре!")
                return
            filtered = [e for e in filtered if e["date"] == filter_date]
        
        if filter_temp_above:
            if not self.validate_temperature(filter_temp_above):
                messagebox.showerror("Ошибка", "Температура в фильтре должна быть числом!")
                return
            temp_threshold = float(filter_temp_above)
            filtered = [e for e in filtered if e["temperature"] > temp_threshold]
        
        self.refresh_table(filtered)
        
        if not filtered:
            messagebox.showinfo("Фильтр", "Нет записей, соответствующих критериям фильтрации")
    
    def reset_filter(self):
        self.filter_date.delete(0, tk.END)
        self.filter_date.insert(0, "ГГГГ-ММ-ДД")
        self.filter_temp_above.delete(0, tk.END)
        self.refresh_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()