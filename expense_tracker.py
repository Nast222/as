import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# --- 1. ГЛОБАЛЬНЫЕ КОНСТАНТЫ ---
DATA_FILE = 'data.json'
DATE_FORMAT = "%Y-%m-%d"  # Формат даты: ГГГГ-ММ-ДД

# --- 2. КЛАСС ДЛЯ УПРАВЛЕНИЯ ДАННЫМИ (МОДЕЛЬ) ---
class ExpenseManager:
    """Класс отвечает за загрузку, сохранение и фильтрацию данных."""
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        """Загружает данные из JSON файла. Если файла нет, создает пустой список."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self):
        """Сохраняет текущий список расходов в JSON файл."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_expense(self, amount, category, date):
        """Добавляет новую запись в список и сохраняет файл."""
        self.data.append({
            "amount": float(amount),
            "category": category,
            "date": date
        })
        self.save_data()

    def filter_expenses(self, category_filter="", start_date=None, end_date=None):
        """
        Фильтрует расходы по категории и/или датам.
        Возвращает отфильтрованный список.
        """
        filtered = self.data.copy()
        
        # Фильтр по категории (без учета регистра)
        if category_filter:
            filtered = [e for e in filtered if category_filter.lower() in e['category'].lower()]
        
        # Фильтр по датам
        if start_date and end_date:
            try:
                start_dt = datetime.strptime(start_date, DATE_FORMAT)
                end_dt = datetime.strptime(end_date, DATE_FORMAT)
                filtered = [
                    e for e in filtered 
                    if start_dt <= datetime.strptime(e['date'], DATE_FORMAT) <= end_dt
                ]
            except ValueError:
                # Если даты указаны неверно, возвращаем пустой список или исходный?
                # Здесь вернем пустой, чтобы показать ошибку в GUI.
                filtered = []
        
        return filtered

# --- 3. КЛАСС ГРАФИЧЕСКОГО ИНТЕРФЕЙСА (ВИД) ---
class ExpenseTrackerApp(tk.Tk):
    """Основной класс приложения Tkinter."""
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("900x650")
        
        # Инициализация менеджера данных
        self.manager = ExpenseManager(DATA_FILE)
        
        # --- СОЗДАНИЕ ВИДЖЕТОВ ---
        self.create_input_frame()
        self.create_filter_frame()
        self.create_treeview()
        
    def create_input_frame(self):
        """Создает поля для ввода нового расхода."""
        frame = ttk.LabelFrame(self, text="Добавить новый расход", padding="10")
        frame.pack(fill='x', padx=10, pady=5)

        # Сумма
        ttk.Label(frame, text="Сумма:").grid(row=0, column=0, sticky='w')
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=0, column=1, sticky='ew', padx=5)

        # Категория
        ttk.Label(frame, text="Категория:").grid(row=1, column=0, sticky='w')
        self.category_entry = ttk.Entry(frame)
        self.category_entry.grid(row=1, column=1, sticky='ew', padx=5)

        # Дата
        ttk.Label(frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky='w')
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=2, column=1, sticky='ew', padx=5)
        
        # Кнопка действия
        ttk.Button(frame, text="Добавить расход", command=self.add_expense).grid(
            row=3, column=0, columnspan=2, pady=10)
            
    def create_filter_frame(self):
        """Создает поля для фильтрации и отображения суммы."""
        frame = ttk.LabelFrame(self, text="Фильтрация и отчет", padding="10")
        frame.pack(fill='x', padx=10, pady=5)

        # Фильтр по категории
        ttk.Label(frame, text="Категория:").grid(row=0, column=0)
        self.filter_category_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.filter_category_var).grid(row=0, column=1, padx=5)

         # Фильтр по датам
         ttk.Label(frame, text="Период:").grid(row=1, column=0)
         ttk.Label(frame, text="С").grid(row=1, column=1)
         self.filter_start_var = tk.StringVar()
         ttk.Entry(frame, textvariable=self.filter_start_var).grid(row=1, column=2)
         
         ttk.Label(frame, text="По").grid(row=1, column=3)
         self.filter_end_var = tk.StringVar()
         ttk.Entry(frame, textvariable=self.filter_end_var).grid(row=1, column=4)
         
         # Кнопка применения фильтра и метка суммы
         ttk.Button(frame, text="Применить фильтр", command=self.apply_filter).grid(
             row=2, column=0, columnspan=5)
             
         self.sum_label = ttk.Label(frame, text="Сумма: 0.00 ₽", font=('Arial', 12))
         self.sum_label.grid(row=3, column=0, columnspan=5)
         
    def create_treeview(self):
        """Создает таблицу для отображения расходов."""
       style = ttk.Style()
       style.configure("Treeview", rowheight=25) 
       
       columns = ("amount", "category", "date")
       self.tree = ttk.Treeview(self, columns=columns, show="headings")
       
       for col in columns:
           self.tree.heading(col, text={"amount": "Сумма", "category": "Категория", "date": "Дата"}[col])
           self.tree.column(col, minwidth=0, width=200)
           
       self.tree.pack(fill='both', expand=True)
       
    # --- 4. ЛОГИКА ОБРАБОТКИ СОБЫТИЙ (КОНТРОЛЛЕР) ---
    def add_expense(self):
       """Обрабатывает добавление нового расхода с валидацией."""
       amount = self.amount_entry.get()
       category = self.category_entry.get()
       date = self.date_entry.get()
       
       # Валидация суммы
       try:
           amount_val = float(amount)
           if amount_val <= 0:
               raise ValueError("Сумма должна быть больше нуля.")
       except ValueError as e:
           messagebox.showerror("Ошибка ввода", str(e))
           return

       # Валидация категории
       if not category.strip():
           messagebox.showerror("Ошибка ввода", "Поле 'Категория' не может быть пустым.")
           return

       # Валидация даты
       try:
           datetime.strptime(date.strip(), DATE_FORMAT)
       except ValueError:
           messagebox.showerror("Ошибка ввода", f"Дата должна быть в формате {DATE_FORMAT}.")
           return

       # Если все проверки пройдены - добавляем запись
       self.manager.add_expense(amount_val, category.strip(), date.strip())
       
       # Очистка полей ввода
       self.amount_entry.delete(0, 'end')
       self.category_entry.delete(0, 'end')
       self.date_entry.delete(0, 'end')
       
       messagebox.showinfo("Успех", "Расход успешно добавлен!")
       
    def apply_filter(self):
       """Обрабатывает нажатие кнопки фильтрации."""
       cat_filter = self.filter_category_var.get()
       start_date = self.filter_start_var.get()
       end_date = self.filter_end_var.get()
       
       # Очищаем таблицу перед обновлением
       for i in self.tree.get_children():
           self.tree.delete(i)
           
      filtered_data = self.manager.filter_expenses(cat_filter.strip(), start_date.strip(), end_date.strip())
      
      total_sum = sum(item['amount'] for item in filtered_data)
      self.sum_label.config(text=f"Сумма: {total_sum:.2f} ₽")
      
      for item in filtered_data:
          # Вставляем строку в таблицу. values должны быть кортежем.
          self.tree.insert("", "end", values=(item['amount'], item['category'], item['date']))
          
# --- 5. ЗАПУСК ПРИЛОЖЕНИЯ ---
if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
