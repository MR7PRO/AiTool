import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import string
import os
import csv
from datetime import datetime


class ModernMultiToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Multi-Tool App")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)

        # Initialize transactions list for expense tracker
        self.transactions = []

        # تحسين المظهر العام
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        # إطار رئيسي
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # إنشاء تبويبات للأدوات
        self.tab_control = ttk.Notebook(self.main_frame)

        # إنشاء التبويبات
        self.tabs = {
            'calculator': ttk.Frame(self.tab_control),
            'todo': ttk.Frame(self.tab_control),
            'notepad': ttk.Frame(self.tab_control),
            'password': ttk.Frame(self.tab_control),
            'currency': ttk.Frame(self.tab_control),
            'xogame': ttk.Frame(self.tab_control),
            'expense': ttk.Frame(self.tab_control),
            'timer': ttk.Frame(self.tab_control),
            'converter': ttk.Frame(self.tab_control),
            'flashcards': ttk.Frame(self.tab_control)
        }

        # إضافة التبويبات
        for name, text in [
            ('calculator', 'Calculator'),
            ('todo', 'To-Do List'),
            ('notepad', 'Notepad'),
            ('password', 'Password Generator'),
            ('currency', 'Currency Converter'),
            ('xogame', 'XO Game'),
            ('expense', 'Expense Tracker'),
            ('timer', 'Timer'),
            ('converter', 'Unit Converter'),
            ('flashcards', 'Flashcards')
        ]:
            self.tab_control.add(self.tabs[name], text=text)

        self.tab_control.pack(expand=1, fill="both")

        # شريط الحالة
        self.status_bar = ttk.Label(root, text="Ready", relief='sunken')
        self.status_bar.pack(fill='x', padx=10, pady=(0, 10))

        # تهيئة الأدوات
        self.setup_calculator()
        self.setup_todo_list()
        self.setup_notepad()
        self.setup_password_generator()
        self.setup_currency_converter()
        self.setup_xo_game()
        self.setup_expense_tracker()
        self.setup_timer()
        self.setup_unit_converter()
        self.setup_flashcards()

    def configure_styles(self):
        """تكوين أنماط الواجهة"""
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Tahoma', 10))
        self.style.configure('TButton', font=('Tahoma', 10), padding=5)
        self.style.configure('TEntry', font=('Tahoma', 11), padding=5)
        self.style.configure('TNotebook.Tab', font=('Tahoma', 10, 'bold'), padding=[10, 5])
        self.style.configure('Header.TLabel', font=('Tahoma', 12, 'bold'))
        self.style.configure('Large.TButton', font=('Tahoma', 12), padding=8)
        self.style.configure('Accent.TButton', background='#4CAF50', foreground='white')
        self.style.map('Accent.TButton',
                       background=[('active', '#45a049'), ('pressed', '#3d8b40')])

        # ألوان خاصة
        self.style.configure('Calculator.TButton', font=('Tahoma', 14), width=5, padding=10)
        self.style.configure('Game.TButton', font=('Tahoma', 24), width=3, height=2)

    def update_status(self, message):
        """تحديث شريط الحالة"""
        self.status_bar.config(text=message)
        self.root.after(3000, lambda: self.status_bar.config(text="جاهز"))

    # ====================== 1. آلة حاسبة ======================
    def setup_calculator(self):
        frame = ttk.Frame(self.tabs['calculator'])
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        # شاشة الآلة الحاسبة
        self.calc_var = tk.StringVar()
        calc_display = ttk.Entry(frame, textvariable=self.calc_var, font=('Tahoma', 20),
                                 justify='right', state='readonly')
        calc_display.grid(row=0, column=0, columnspan=4, sticky='nsew', pady=(0, 10), ipady=10)

        # أزرار الآلة الحاسبة
        buttons = [
            ('7', '8', '9', '/'),
            ('4', '5', '6', '*'),
            ('1', '2', '3', '-'),
            ('0', '.', '=', '+'),
            ('C', '⌫', '(', ')')
        ]

        for row_idx, row in enumerate(buttons, start=1):
            for col_idx, btn_text in enumerate(row):
                if btn_text == '=':
                    btn = ttk.Button(frame, text=btn_text, style='Accent.TButton',
                                     command=self.calculate)
                elif btn_text == 'C':
                    btn = ttk.Button(frame, text=btn_text,
                                     command=self.clear_calc)
                elif btn_text == '⌫':
                    btn = ttk.Button(frame, text=btn_text,
                                     command=self.backspace_calc)
                else:
                    btn = ttk.Button(frame, text=btn_text,
                                     command=lambda b=btn_text: self.add_to_calc(b))

                btn.grid(row=row_idx, column=col_idx, sticky='nsew', padx=2, pady=2)

        # جعل الأزرار تتمدد مع تغير حجم النافذة
        for i in range(6):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)

    def add_to_calc(self, char):
        current = self.calc_var.get()
        self.calc_var.set(current + char)

    def clear_calc(self):
        self.calc_var.set('')

    def backspace_calc(self):
        current = self.calc_var.get()
        self.calc_var.set(current[:-1])

    def calculate(self):
        try:
            expression = self.calc_var.get()
            result = eval(expression)
            self.calc_var.set(str(result))
            self.update_status("تمت العملية الحسابية بنجاح")
        except Exception as e:
            messagebox.showerror("خطأ", "تعبير غير صالح")
            self.calc_var.set('')

    # ====================== 2. قائمة مهام ======================
    def setup_todo_list(self):
        main_frame = ttk.Frame(self.tabs['todo'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # شريط الأدوات
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill='x', pady=(0, 10))

        self.todo_entry = ttk.Entry(toolbar, font=('Tahoma', 12))
        self.todo_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))

        ttk.Button(toolbar, text="إضافة", style='Accent.TButton',
                   command=self.add_todo).pack(side='left', padx=2)

        # قائمة المهام
        self.todo_listbox = tk.Listbox(main_frame, font=('Tahoma', 12),
                                       selectbackground='#4CAF50', selectforeground='white')
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical',
                                  command=self.todo_listbox.yview)
        self.todo_listbox.config(yscrollcommand=scrollbar.set)

        self.todo_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # شريط الأدوات السفلي
        bottom_toolbar = ttk.Frame(main_frame)
        bottom_toolbar.pack(fill='x', pady=(10, 0))

        ttk.Button(bottom_toolbar, text="حذف",
                   command=self.delete_todo).pack(side='left', padx=2)
        ttk.Button(bottom_toolbar, text="حفظ",
                   command=self.save_todos).pack(side='right', padx=2)
        ttk.Button(bottom_toolbar, text="تحميل",
                   command=self.load_todos).pack(side='right', padx=2)

        # تحميل المهام عند البدء
        self.load_todos()

    def add_todo(self):
        task = self.todo_entry.get()
        if task:
            self.todo_listbox.insert(tk.END, task)
            self.todo_entry.delete(0, tk.END)
            self.update_status(f"تمت إضافة المهمة: {task}")

    def delete_todo(self):
        try:
            selected = self.todo_listbox.curselection()[0]
            task = self.todo_listbox.get(selected)
            self.todo_listbox.delete(selected)
            self.update_status(f"تم حذف المهمة: {task}")
        except IndexError:
            messagebox.showwarning("تحذير", "لم يتم اختيار أي مهمة")

    def save_todos(self):
        tasks = self.todo_listbox.get(0, tk.END)
        try:
            with open('todos.txt', 'w', encoding='utf-8') as f:
                for task in tasks:
                    f.write(task + '\n')
            self.update_status("تم حفظ المهام بنجاح")
        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن حفظ المهام: {e}")

    def load_todos(self):
        try:
            if os.path.exists('todos.txt'):
                with open('todos.txt', 'r', encoding='utf-8') as f:
                    tasks = f.read().splitlines()
                self.todo_listbox.delete(0, tk.END)
                for task in tasks:
                    self.todo_listbox.insert(tk.END, task)
                self.update_status("تم تحميل المهام بنجاح")
        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن تحميل المهام: {e}")

    # ====================== 3. مفكرة ======================
    def setup_notepad(self):
        main_frame = ttk.Frame(self.tabs['notepad'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # شريط الأدوات
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill='x', pady=(0, 10))

        ttk.Button(toolbar, text="جديد", command=self.new_file).pack(side='left', padx=2)
        ttk.Button(toolbar, text="فتح", command=self.open_file).pack(side='left', padx=2)
        ttk.Button(toolbar, text="حفظ", command=self.save_file).pack(side='left', padx=2)
        ttk.Button(toolbar, text="حفظ باسم", command=self.save_file_as).pack(side='left', padx=2)

        # منطقة النص
        self.notepad_text = tk.Text(main_frame, font=('Tahoma', 12), wrap='word',
                                    padx=10, pady=10, undo=True)
        scrollbar = ttk.Scrollbar(main_frame, command=self.notepad_text.yview)
        self.notepad_text.config(yscrollcommand=scrollbar.set)

        self.notepad_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # معلومات الملف
        self.file_info = ttk.Label(main_frame, text="ملف غير محفوظ", relief='sunken')
        self.file_info.pack(fill='x', pady=(10, 0))

        self.current_file = None

    def new_file(self):
        self.notepad_text.delete(1.0, tk.END)
        self.current_file = None
        self.file_info.config(text="ملف جديد غير محفوظ")
        self.update_status("تم إنشاء ملف جديد")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("ملفات نصية", "*.txt"), ("كل الملفات", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.notepad_text.delete(1.0, tk.END)
                self.notepad_text.insert(1.0, content)
                self.current_file = file_path
                self.file_info.config(text=f"الملف: {os.path.basename(file_path)}")
                self.update_status(f"تم فتح الملف: {file_path}")
            except Exception as e:
                messagebox.showerror("خطأ", f"لا يمكن فتح الملف: {e}")

    def save_file(self):
        if self.current_file:
            try:
                content = self.notepad_text.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.file_info.config(text=f"الملف: {os.path.basename(self.current_file)}")
                self.update_status(f"تم حفظ الملف: {self.current_file}")
            except Exception as e:
                messagebox.showerror("خطأ", f"لا يمكن حفظ الملف: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("ملفات نصية", "*.txt"), ("كل الملفات", "*.*")])
        if file_path:
            try:
                content = self.notepad_text.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.current_file = file_path
                self.file_info.config(text=f"الملف: {os.path.basename(file_path)}")
                self.update_status(f"تم حفظ الملف: {file_path}")
            except Exception as e:
                messagebox.showerror("خطأ", f"لا يمكن حفظ الملف: {e}")

    # ====================== 4. مولد كلمات سر ======================
    def setup_password_generator(self):
        main_frame = ttk.Frame(self.tabs['password'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # إعدادات كلمة السر
        settings_frame = ttk.LabelFrame(main_frame, text="إعدادات كلمة السر")
        settings_frame.pack(fill='x', pady=(0, 20))

        ttk.Label(settings_frame, text="طول كلمة السر:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.pwd_length = tk.IntVar(value=12)
        ttk.Entry(settings_frame, textvariable=self.pwd_length, width=5).grid(row=0, column=1, padx=5, pady=5,
                                                                              sticky='w')

        # خيارات الأحرف
        options_frame = ttk.Frame(settings_frame)
        options_frame.grid(row=1, column=0, columnspan=2, pady=5)

        self.include_upper = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="أحرف كبيرة", variable=self.include_upper).pack(side='left', padx=5)

        self.include_lower = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="أحرف صغيرة", variable=self.include_lower).pack(side='left', padx=5)

        self.include_digits = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="أرقام", variable=self.include_digits).pack(side='left', padx=5)

        self.include_symbols = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="رموز", variable=self.include_symbols).pack(side='left', padx=5)

        # زر الإنشاء
        ttk.Button(main_frame, text="إنشاء كلمة سر", style='Accent.TButton',
                   command=self.generate_password).pack(pady=(0, 20))

        # عرض كلمة السر
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill='x')

        self.password_var = tk.StringVar()
        ttk.Entry(password_frame, textvariable=self.password_var, font=('Tahoma', 14),
                  state='readonly').pack(side='left', fill='x', expand=True, padx=(0, 5))

        ttk.Button(password_frame, text="نسخ", command=self.copy_to_clipboard).pack(side='right')

        # قوة كلمة السر
        self.strength_var = tk.StringVar(value="قوة كلمة السر: -")
        ttk.Label(main_frame, textvariable=self.strength_var, font=('Tahoma', 10)).pack(pady=(10, 0))

    def generate_password(self):
        length = self.pwd_length.get()
        if length < 4:
            messagebox.showwarning("تحذير", "الطول يجب أن يكون 4 على الأقل")
            return

        characters = ''
        if self.include_upper.get():
            characters += string.ascii_uppercase
        if self.include_lower.get():
            characters += string.ascii_lowercase
        if self.include_digits.get():
            characters += string.digits
        if self.include_symbols.get():
            characters += string.punctuation

        if not characters:
            messagebox.showwarning("تحذير", "يجب اختيار نوع واحد على الأقل من الأحرف")
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_var.set(password)
        self.update_password_strength(password)
        self.update_status("تم إنشاء كلمة سر جديدة")

    def update_password_strength(self, password):
        """تقييم قوة كلمة السر"""
        strength = 0
        length = len(password)

        # نقاط للطول
        if length >= 12:
            strength += 3
        elif length >= 8:
            strength += 2
        elif length >= 6:
            strength += 1

        # نقاط لأنواع الأحرف
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in string.punctuation for c in password)

        char_types = sum([has_upper, has_lower, has_digit, has_symbol])
        strength += char_types - 1

        # تقييم القوة
        if strength >= 5:
            strength_text = "قوية جدًا"
            color = "green"
        elif strength >= 3:
            strength_text = "قوية"
            color = "#4CAF50"
        elif strength >= 2:
            strength_text = "متوسطة"
            color = "orange"
        else:
            strength_text = "ضعيفة"
            color = "red"

        self.strength_var.set(f"قوة كلمة السر: {strength_text}")
        self.strength_var.set(f"قوة كلمة السر: {strength_text}")

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.update_status("تم نسخ كلمة السر إلى الحافظة")

    # ====================== 5. محول عملات ======================
    def setup_currency_converter(self):
        main_frame = ttk.Frame(self.tabs['currency'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # أسعار ثابتة (ليست من API)
        self.rates = {
            'USD': 1.0,
            'SAR': 3.75,  # ريال سعودي
            'EUR': 0.85,  # يورو
            'GBP': 0.73,  # جنيه إسترليني
            'JPY': 110.0,  # ين ياباني
            'AED': 3.67  # درهم إماراتي
        }

        # إطار الإدخال
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill='x', pady=(0, 20))

        ttk.Label(input_frame, text="من:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.from_currency = tk.StringVar(value='USD')
        ttk.OptionMenu(input_frame, self.from_currency, *self.rates.keys()).grid(row=0, column=1, padx=5, pady=5,
                                                                                 sticky='ew')

        ttk.Label(input_frame, text="إلى:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.to_currency = tk.StringVar(value='SAR')
        ttk.OptionMenu(input_frame, self.to_currency, *self.rates.keys()).grid(row=1, column=1, padx=5, pady=5,
                                                                               sticky='ew')

        ttk.Label(input_frame, text="المبلغ:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.amount = tk.DoubleVar(value=1.0)
        ttk.Entry(input_frame, textvariable=self.amount).grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        # زر التحويل
        ttk.Button(main_frame, text="تحويل", style='Accent.TButton',
                   command=self.convert_currency).pack(pady=(0, 20))

        # نتيجة التحويل
        self.result_var = tk.StringVar(value="النتيجة: -")
        result_label = ttk.Label(main_frame, textvariable=self.result_var,
                                 font=('Tahoma', 12, 'bold'))
        result_label.pack()

        # تاريخ التحديث
        update_label = ttk.Label(main_frame, text="آخر تحديث للأسعار: غير متصل",
                                 font=('Tahoma', 8), foreground='gray')
        update_label.pack(pady=(20, 0))

    def convert_currency(self):
        try:
            amount = self.amount.get()
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            # التحويل إلى الدولار أولاً ثم إلى العملة المطلوبة
            amount_in_usd = amount / self.rates[from_curr]
            result = amount_in_usd * self.rates[to_curr]

            self.result_var.set(f"{amount:.2f} {from_curr} = {result:.2f} {to_curr}")
            self.update_status(f"تم تحويل {amount:.2f} {from_curr} إلى {to_curr}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في التحويل: {e}")

    # ====================== 6. لعبة XO ======================
    def setup_xo_game(self):
        main_frame = ttk.Frame(self.tabs['xogame'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # معلومات اللعبة
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='x', pady=(0, 10))

        self.status_var = tk.StringVar(value="دور اللاعب: X")
        ttk.Label(info_frame, textvariable=self.status_var,
                  font=('Tahoma', 12, 'bold')).pack(side='left')

        ttk.Button(info_frame, text="إعادة تشغيل",
                   command=self.reset_game).pack(side='right')

        # لوحة اللعبة
        game_frame = ttk.Frame(main_frame)
        game_frame.pack(expand=True)

        self.current_player = 'X'
        self.board = [' ' for _ in range(9)]
        self.game_buttons = []

        for i in range(3):
            game_frame.grid_rowconfigure(i, weight=1)
            for j in range(3):
                game_frame.grid_columnconfigure(j, weight=1)
                btn = ttk.Button(game_frame, text=' ', style='Game.TButton',
                                 command=lambda row=i, col=j: self.make_move(row, col))
                btn.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')
                self.game_buttons.append(btn)

    def make_move(self, row, col):
        index = row * 3 + col
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.game_buttons[index].config(text=self.current_player)

            if self.check_winner():
                messagebox.showinfo("فوز", f"اللاعب {self.current_player} فاز!")
                self.reset_game()
            elif ' ' not in self.board:
                messagebox.showinfo("تعادل", "اللعبة انتهت بالتعادل!")
                self.reset_game()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.status_var.set(f"دور اللاعب: {self.current_player}")

    def check_winner(self):
        # تحقق من الصفوف
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i + 1] == self.board[i + 2] != ' ':
                return True

        # تحقق من الأعمدة
        for i in range(3):
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != ' ':
                return True

        # تحقق من القطرين
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            return True
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            return True

        return False

    def reset_game(self):
        self.current_player = 'X'
        self.board = [' ' for _ in range(9)]
        for btn in self.game_buttons:
            btn.config(text=' ')
        self.status_var.set(f"دور اللاعب: {self.current_player}")
        self.update_status("تم إعادة تشغيل اللعبة")

    # ====================== 7. إدارة المصاريف ======================
    def setup_expense_tracker(self):
        main_frame = ttk.Frame(self.tabs['expense'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # إطار الإدخال
        input_frame = ttk.LabelFrame(main_frame, text="إضافة معاملة")
        input_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(input_frame, text="النوع:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.trans_type = tk.StringVar(value='مصروف')
        ttk.OptionMenu(input_frame, self.trans_type, 'مصروف', 'دخل').grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(input_frame, text="المبلغ:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.amount = tk.DoubleVar()
        ttk.Entry(input_frame, textvariable=self.amount).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(input_frame, text="الوصف:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.description = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.description).grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        ttk.Button(input_frame, text="إضافة", style='Accent.TButton',
                   command=self.add_transaction).grid(row=3, column=0, columnspan=2, pady=5)

        # عرض المعاملات
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True)

        self.transaction_tree = ttk.Treeview(tree_frame, columns=('type', 'amount', 'description', 'date'),
                                             show='headings')
        self.transaction_tree.heading('type', text='النوع')
        self.transaction_tree.heading('amount', text='المبلغ')
        self.transaction_tree.heading('description', text='الوصف')
        self.transaction_tree.heading('date', text='التاريخ')

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.transaction_tree.yview)
        self.transaction_tree.config(yscrollcommand=scrollbar.set)

        self.transaction_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # شريط الملخص
        summary_frame = ttk.Frame(main_frame)
        summary_frame.pack(fill='x', pady=(10, 0))

        self.balance_var = tk.StringVar(value="الرصيد: 0.00")
        ttk.Label(summary_frame, textvariable=self.balance_var,
                  font=('Tahoma', 12, 'bold')).pack(side='left')

        ttk.Button(summary_frame, text="حفظ", command=self.save_transactions).pack(side='right', padx=5)
        ttk.Button(summary_frame, text="تحميل", command=self.load_transactions).pack(side='right', padx=5)

        # تحميل البيانات عند البدء
        self.load_transactions()

    def add_transaction(self):
        try:
            trans_type = self.trans_type.get()
            amount = self.amount.get()
            description = self.description.get()

            if amount <= 0:
                messagebox.showwarning("تحذير", "المبلغ يجب أن يكون موجبًا")
                return

            if trans_type == 'مصروف':
                amount = -amount

            transaction = {
                'type': 'مصروف' if amount < 0 else 'دخل',
                'amount': abs(amount),
                'description': description,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'signed_amount': amount
            }

            self.transactions.append(transaction)
            self.update_transaction_display()
            self.clear_transaction_input()
            self.update_status(f"تمت إضافة معاملة: {description}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {e}")

    def clear_transaction_input(self):
        self.amount.set(0)
        self.description.set('')

    def update_transaction_display(self):
        # مسح العرض الحالي
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

        # إضافة المعاملات الجديدة
        for trans in self.transactions:
            self.transaction_tree.insert('', 'end', values=(
                trans['type'],
                f"{trans['amount']:.2f}",
                trans['description'],
                trans['date']
            ))

        # حساب الرصيد
        balance = sum(trans['signed_amount'] for trans in self.transactions)
        self.balance_var.set(f"الرصيد: {balance:.2f}")

        # تلوين الرصيد
        if balance < 0:
            self.balance_var.set(f"الرصيد: {balance:.2f} (مدين)")

    def save_transactions(self):
        try:
            with open('transactions.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['type', 'amount', 'description', 'date', 'signed_amount'])
                writer.writeheader()
                writer.writerows(self.transactions)
            self.update_status("تم حفظ المعاملات بنجاح")
        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن حفظ المعاملات: {e}")

    def load_transactions(self):
        try:
            if os.path.exists('transactions.csv'):
                with open('transactions.csv', 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.transactions = []
                    for row in reader:
                        row['amount'] = float(row['amount'])
                        row['signed_amount'] = float(row['signed_amount'])
                        self.transactions.append(row)
                self.update_transaction_display()
                self.update_status("تم تحميل المعاملات بنجاح")
        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن تحميل المعاملات: {e}")

    # ====================== 8. مؤقت عد تنازلي ======================
    def setup_timer(self):
        main_frame = ttk.Frame(self.tabs['timer'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # إعدادات المؤقت
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(pady=(0, 20))

        ttk.Label(settings_frame, text="عدد الدقائق:").grid(row=0, column=0, padx=5, pady=5)
        self.minutes = tk.IntVar(value=1)
        ttk.Entry(settings_frame, textvariable=self.minutes, width=5).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="عدد الثواني:").grid(row=0, column=2, padx=5, pady=5)
        self.seconds = tk.IntVar(value=0)
        ttk.Entry(settings_frame, textvariable=self.seconds, width=5).grid(row=0, column=3, padx=5, pady=5)

        # عرض المؤقت
        self.time_left = tk.StringVar(value="01:00")
        time_label = ttk.Label(main_frame, textvariable=self.time_left,
                               font=('Tahoma', 48, 'bold'))
        time_label.pack(pady=20)

        # أزرار التحكم
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(0, 20))

        ttk.Button(button_frame, text="بدء", style='Accent.TButton',
                   command=self.start_timer).pack(side='left', padx=5)
        ttk.Button(button_frame, text="إيقاف",
                   command=self.stop_timer).pack(side='left', padx=5)
        ttk.Button(button_frame, text="إعادة تعيين",
                   command=self.reset_timer).pack(side='left', padx=5)

        self.timer_running = False
        self.remaining_seconds = 60
        self.update_timer_display()

    def start_timer(self):
        if not self.timer_running:
            minutes = self.minutes.get()
            seconds = self.seconds.get()
            self.remaining_seconds = minutes * 60 + seconds

            if self.remaining_seconds <= 0:
                messagebox.showwarning("تحذير", "الوقت يجب أن يكون أكبر من الصفر")
                return

            self.timer_running = True
            self.update_timer_display()
            self.run_timer()
            self.update_status("تم بدء المؤقت")

    def run_timer(self):
        if self.timer_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_display()
            self.root.after(1000, self.run_timer)
        elif self.timer_running and self.remaining_seconds == 0:
            self.timer_running = False
            messagebox.showinfo("انتهى الوقت", "انتهى الوقت المحدد!")
            self.update_status("انتهى الوقت المحدد")

    def stop_timer(self):
        self.timer_running = False
        self.update_status("تم إيقاف المؤقت")

    def reset_timer(self):
        self.timer_running = False
        minutes = self.minutes.get()
        seconds = self.seconds.get()
        self.remaining_seconds = minutes * 60 + seconds
        self.update_timer_display()
        self.update_status("تم إعادة تعيين المؤقت")

    def update_timer_display(self):
        mins, secs = divmod(self.remaining_seconds, 60)
        self.time_left.set(f"{mins:02d}:{secs:02d}")

        # تغيير اللون عند انخفاض الوقت
        if self.remaining_seconds <= 10 and self.timer_running:
            self.time_left.set(f"{mins:02d}:{secs:02d}")  # يمكن إضافة تلوين هنا

    # ====================== 9. محول وحدات ======================
    def setup_unit_converter(self):
        main_frame = ttk.Frame(self.tabs['converter'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        self.conversion_types = {
            'طول': {
                'متر': 1.0,
                'سنتيمتر': 100.0,
                'ميلليمتر': 1000.0,
                'كيلومتر': 0.001,
                'إنش': 39.3701,
                'قدم': 3.28084,
                'ياردة': 1.09361,
                'ميل': 0.000621371
            },
            'وزن': {
                'كيلوجرام': 1.0,
                'جرام': 1000.0,
                'مليجرام': 1000000.0,
                'طن': 0.001,
                'أوقية': 35.274,
                'رطل': 2.20462,
                'حجر': 0.157473
            },
            'حجم': {
                'لتر': 1.0,
                'مليلتر': 1000.0,
                'جالون': 0.264172,
                'كوارت': 1.05669,
                'باينت': 2.11338,
                'كوب': 4.22675,
                'أونصة سائلة': 33.814
            },
            'درجة حرارة': {
                'مئوية (C°)': 'celsius',
                'فهرنهايت (F°)': 'fahrenheit',
                'كلفن (K)': 'kelvin'
            }
        }

        # اختيار نوع التحويل
        type_frame = ttk.Frame(main_frame)
        type_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(type_frame, text="نوع التحويل:").pack(side='left', padx=5)
        self.conversion_type = tk.StringVar(value='طول')
        type_menu = ttk.OptionMenu(type_frame, self.conversion_type, *self.conversion_types.keys(),
                                   command=self.update_units)
        type_menu.pack(side='left', fill='x', expand=True, padx=5)

        # وحدات التحويل
        units_frame = ttk.Frame(main_frame)
        units_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(units_frame, text="من:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.from_unit = tk.StringVar()
        self.from_menu = ttk.OptionMenu(units_frame, self.from_unit, '')
        self.from_menu.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(units_frame, text="إلى:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.to_unit = tk.StringVar()
        self.to_menu = ttk.OptionMenu(units_frame, self.to_unit, '')
        self.to_menu.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # قيمة الإدخال
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill='x', pady=(0, 20))

        ttk.Label(input_frame, text="القيمة:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.input_value = tk.DoubleVar(value=1.0)
        ttk.Entry(input_frame, textvariable=self.input_value).grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # نتيجة التحويل
        ttk.Button(main_frame, text="تحويل", style='Accent.TButton',
                   command=self.perform_conversion).pack(pady=(0, 20))

        self.result_var = tk.StringVar(value="النتيجة: -")
        ttk.Label(main_frame, textvariable=self.result_var,
                  font=('Tahoma', 12, 'bold')).pack()

        # تهيئة الوحدات
        self.update_units()

    def update_units(self, *args):
        conv_type = self.conversion_type.get()
        units = list(self.conversion_types[conv_type].keys())

        # تحديث قائمة الوحدات
        self.from_menu['menu'].delete(0, 'end')
        self.to_menu['menu'].delete(0, 'end')

        for unit in units:
            self.from_menu['menu'].add_command(label=unit, command=tk._setit(self.from_unit, unit))
            self.to_menu['menu'].add_command(label=unit, command=tk._setit(self.to_unit, unit))

        # تعيين القيم الافتراضية
        self.from_unit.set(units[0])
        self.to_unit.set(units[1] if len(units) > 1 else units[0])

    def perform_conversion(self):
        try:
            conv_type = self.conversion_type.get()
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            value = self.input_value.get()

            if conv_type == 'درجة حرارة':
                result = self.convert_temperature(value, from_unit, to_unit)
            else:
                if from_unit not in self.conversion_types[conv_type] or to_unit not in self.conversion_types[conv_type]:
                    messagebox.showwarning("تحذير", "الوحدات المحددة غير صالحة")
                    return

                # التحويل إلى الوحدة الأساسية أولاً ثم إلى الوحدة المطلوبة
                base_value = value / self.conversion_types[conv_type][from_unit]
                result = base_value * self.conversion_types[conv_type][to_unit]

            self.result_var.set(f"{value} {from_unit} = {result:.4f} {to_unit}")
            self.update_status(f"تم تحويل {value} {from_unit} إلى {to_unit}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في التحويل: {e}")

    def convert_temperature(self, value, from_unit, to_unit):
        """تحويل درجات الحرارة"""
        from_type = self.conversion_types['درجة حرارة'][from_unit]
        to_type = self.conversion_types['درجة حرارة'][to_unit]

        # التحويل إلى مئوية أولاً
        if from_type == 'celsius':
            celsius = value
        elif from_type == 'fahrenheit':
            celsius = (value - 32) * 5 / 9
        elif from_type == 'kelvin':
            celsius = value - 273.15

        # التحويل من مئوية إلى الوحدة المطلوبة
        if to_type == 'celsius':
            return celsius
        elif to_type == 'fahrenheit':
            return celsius * 9 / 5 + 32
        elif to_type == 'kelvin':
            return celsius + 273.15

    # ====================== 10. بطاقات تعليمية ======================
    def setup_flashcards(self):
        main_frame = ttk.Frame(self.tabs['flashcards'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # شريط الأدوات
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill='x', pady=(0, 20))

        ttk.Button(toolbar, text="تحميل بطاقات",
                   command=self.load_flashcards).pack(side='left', padx=2)
        ttk.Button(toolbar, text="حفظ بطاقات",
                   command=self.save_flashcards).pack(side='left', padx=2)

        # عرض البطاقة
        card_frame = ttk.LabelFrame(main_frame, text="البطاقة التعليمية")
        card_frame.pack(fill='both', expand=True, pady=(0, 20))

        self.card_text = tk.StringVar(value="قم بتحميل مجموعة بطاقات لتبدأ")
        self.card_label = ttk.Label(card_frame, textvariable=self.card_text,
                                    font=('Tahoma', 16), wraplength=400,
                                    justify='center')
        self.card_label.pack(fill='both', expand=True, padx=20, pady=20)

        # إدخال الإجابة
        answer_frame = ttk.Frame(main_frame)
        answer_frame.pack(fill='x', pady=(0, 20))

        ttk.Label(answer_frame, text="الإجابة:").pack(side='left', padx=5)
        self.answer_var = tk.StringVar()
        ttk.Entry(answer_frame, textvariable=self.answer_var,
                  font=('Tahoma', 12)).pack(side='left', fill='x', expand=True, padx=5)

        # أزرار التحكم
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill='x')

        ttk.Button(control_frame, text="تحقق", style='Accent.TButton',
                   command=self.check_answer).pack(side='left', padx=5)
        ttk.Button(control_frame, text="التالي",
                   command=self.next_card).pack(side='left', padx=5)
        ttk.Button(control_frame, text="إظهار الإجابة",
                   command=self.show_answer).pack(side='right', padx=5)

        # معلومات المجموعة
        self.deck_info = ttk.Label(main_frame, text="0/0 بطاقات", relief='sunken')
        self.deck_info.pack(fill='x', pady=(10, 0))

        self.flashcards = []
        self.current_card = 0

    def show_current_card(self):
        if self.flashcards:
            card = self.flashcards[self.current_card]
            self.card_text.set(card['word'])
            self.answer_var.set("")
            self.deck_info.config(text=f"{self.current_card + 1}/{len(self.flashcards)} بطاقات")
        else:
            self.card_text.set("لا توجد بطاقات متاحة. قم بتحميل مجموعة بطاقات.")
            self.deck_info.config(text="0/0 بطاقات")

    def check_answer(self):
        if not self.flashcards:
            return

        user_answer = self.answer_var.get().strip()
        correct_answer = self.flashcards[self.current_card]['translation']

        if user_answer.lower() == correct_answer.lower():
            messagebox.showinfo("صحيح", "إجابة صحيحة!")
            self.next_card()
        else:
            messagebox.showwarning("خطأ", f"إجابة خاطئة. حاول مرة أخرى.")

    def next_card(self):
        if not self.flashcards:
            return

        self.current_card = (self.current_card + 1) % len(self.flashcards)
        self.show_current_card()
        self.update_status(f"البطاقة {self.current_card + 1} من {len(self.flashcards)}")

    def show_answer(self):
        if not self.flashcards:
            return

        correct_answer = self.flashcards[self.current_card]['translation']
        messagebox.showinfo("الإجابة", f"الترجمة الصحيحة هي: {correct_answer}")

    def load_flashcards(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("ملفات CSV", "*.csv"), ("كل الملفات", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.flashcards = []
                    for row in reader:
                        if 'word' in row and 'translation' in row:
                            self.flashcards.append({
                                'word': row['word'],
                                'translation': row['translation']
                            })

                if self.flashcards:
                    self.current_card = 0
                    self.show_current_card()
                    self.update_status(f"تم تحميل {len(self.flashcards)} بطاقة من {file_path}")
                else:
                    messagebox.showwarning("تحذير", "الملف لا يحتوي على بطاقات صالحة")
            except Exception as e:
                messagebox.showerror("خطأ", f"لا يمكن تحميل البطاقات: {e}")

    def save_flashcards(self):
        if not self.flashcards:
            messagebox.showwarning("تحذير", "لا توجد بطاقات لحفظها")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("ملفات CSV", "*.csv"), ("كل الملفات", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['word', 'translation'])
                    writer.writeheader()
                    writer.writerows(self.flashcards)
                self.update_status(f"تم حفظ {len(self.flashcards)} بطاقة في {file_path}")
            except Exception as e:
                messagebox.showerror("خطأ", f"لا يمكن حفظ البطاقات: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernMultiToolApp(root)
    root.mainloop()


    def main():
        root = tk.Tk()
        app = ModernMultiToolApp(root)
        root.mainloop()


    if __name__ == "__main__":
        main()
