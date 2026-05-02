import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DATA_FILE = 'data.json'

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
        self.load_data()
        self.create_widgets()

    def load_data(self):
        try:
            with open(DATA_FILE, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    def create_widgets(self):
        # Поля ввода
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill='x')

        ttk.Label(frame, text="Сумма:").grid(row=0, column=0, sticky='w')
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=0, column=1, sticky='ew', padx=5)

        ttk.Label(frame, text="Категория:").grid(row=1, column=0, sticky='w')
        self.category_entry = ttk.Entry(frame)
        self.category_entry.grid(row=1, column=1, sticky='ew', padx=5)

        ttk.Label(frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky='w')
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=2, column=1, sticky='ew', padx=5)

        ttk.Button(frame, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        # Фильтры и сумма
        filter_frame = ttk.Frame(self.root, padding="10")
        filter_frame.pack(fill='x')

        self.filter_category = tk.StringVar()
        self.filter_date_start = tk.StringVar()
        self.filter_date_end = tk.StringVar()

        ttk.Label(filter_frame, text="Фильтр по категории:").grid(row=0, column=0)
        ttk.Entry(filter_frame, textvariable=self.filter_category).grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Дата начала:").grid(row=1, column=0)
        ttk.Entry(filter_frame, textvariable=self.filter_date_start).grid(row=1, column=1, padx=5)

        ttk.Label(filter_frame, text="Дата окончания:").grid(row=1, column=2)
        ttk.Entry(filter_frame, textvariable=self.filter_date_end).grid(row=1, column=3, padx=5)

        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=2, column=0, columnspan=4)

        self.sum_label = ttk.Label(filter_frame, text="Сумма за период: 0.00 ₽")
        self.sum_label.grid(row=3, column=0, columnspan=4)

        # Таблица расходов
        columns = ("Сумма", "Категория", "Дата")
        self.# Expense Tracker: пошаговая инструкция по созданию

Это подробное руководство по созданию приложения для учёта личных расходов с графическим интерфейсом, фильтрацией, подсчётом суммы за период, сохранением данных в *JSON* и использованием *Git* для контроля версий.

## 1. Выбор инструментов

Для реализации подойдёт язык *Python* и библиотека *Tkinter* (встроенная), а для работы с *JSON* — стандартный модуль. Для контроля версий — *Git*.

## 2. Структура проекта
