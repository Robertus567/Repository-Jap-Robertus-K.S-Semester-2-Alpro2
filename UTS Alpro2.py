import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import random
import heapq
from PIL import Image, ImageTk, ImageDraw
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Food:
    def __init__(self, name, calories, protein, carbs, fat, is_vegan=True, is_gluten_free=True, contains=None):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.is_vegan = is_vegan
        self.is_gluten_free = is_gluten_free
        self.contains = contains or []

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"

class MealPlanner:
    def __init__(self):
        #data makanan
        self.foods = [
            Food("Nasi Putih", 130, 2.7, 28, 0.3, True, False, []),
            Food("Nasi Merah", 110, 2.5, 23, 0.8, True, False, []),
            Food("Roti Gandum", 80, 4, 15, 1, True, False, ["gluten"]),
            Food("Kentang Rebus", 87, 1.9, 20, 0.1, True, True, []),
            Food("Telur Rebus", 70, 6, 0.6, 5, False, True, ["telur"]),
            Food("Dada Ayam", 165, 31, 0, 3.6, False, True, []),
            Food("Tahu", 80, 8, 2, 5, True, True, ["kacang"]),
            Food("Tempe", 160, 15, 7, 9, True, True, ["kacang"]),
            Food("Daging Sapi", 250, 26, 0, 17, False, True, []),
            Food("Brokoli", 30, 2.5, 6, 0.3, True, True, []),
            Food("Wortel", 25, 0.6, 6, 0.1, True, True, []),
            Food("Bayam", 23, 2.9, 3.6, 0.4, True, True, []),
            Food("Alpukat", 160, 2, 8, 15, True, True, []),
            Food("Pisang", 105, 1.3, 27, 0.4, True, True, []),
            Food("Apel", 95, 0.5, 25, 0.3, True, True, []),
            Food("Susu Sapi", 120, 8, 12, 5, False, True, ["susu"]),
            Food("Susu Almond", 60, 1, 8, 2.5, True, True, ["kacang"]),
            Food("Keju", 110, 7, 1.5, 9, False, True, ["susu"]),
            Food("Yogurt", 100, 5, 12, 3, False, True, ["susu"]),
            Food("Minyak Zaitun", 120, 0, 0, 14, True, True, []),
            Food("Dark Chocolate", 150, 2, 15, 10, True, True, [])
        ]
        
        #Preferensi makanan(suka/ga ada/ga suka)
        self.preferred_foods = []
        self.disliked_foods = []
        # Nge cari unavailable foods
        self.unavailable_foods = []

    def is_food_valid(self, food, restrictions):
        # Cek apakah makanan ada di daftar unavailable foods/ ga ada bahan nya
        if food.name in self.unavailable_foods:
            return False
            
        if restrictions['vegan'] and not food.is_vegan:
            return False
        if restrictions['gluten_free'] and not food.is_gluten_free:
            return False
        if restrictions['keto'] and food.carbs > 5:
            return False
        if food.name in self.disliked_foods:
            return False
        
        for allergen in restrictions['allergies']:
            if allergen in food.contains:
                return False
        return True

    def evaluate_meal(self, meal, target_calories, restrictions):
        """Evaluate meal quality using branch and bound"""
        total_calories = sum(food.calories for food in meal)
        total_protein = sum(food.protein for food in meal)
        total_carbs = sum(food.carbs for food in meal)
        total_fat = sum(food.fat for food in meal)
        
        # Kalori penalti
        if total_calories < target_calories * 0.9:
            calorie_penalty = (target_calories - total_calories) * 2
        else:
            calorie_penalty = abs(target_calories - total_calories)
        
        
        preference_score = 0
        for food in meal:
            if food.name in self.preferred_foods:
                preference_score -= 50  
            if food.name in self.disliked_foods:
                preference_score += 100  
        
        # Saran diet
        if restrictions['keto']:
            if total_carbs > 30:
                return float('inf')  # Bound - terlalu banyak carbs untuk keto
            if total_fat < total_protein:
                return calorie_penalty + 200 + preference_score
            return calorie_penalty + preference_score
        
        # Standard diet saran
        ideal_protein = (target_calories * 0.175) / 4
        protein_diff = abs(ideal_protein - total_protein)
        
        return calorie_penalty + protein_diff * 2 + preference_score

    def backtracking_meal_plan(self, target_calories, restrictions, max_items=5, time_slots=3):
        """Generate meal plan using backtracking with branch and bound"""
        valid_foods = [food for food in self.foods if self.is_food_valid(food, restrictions)]
        preferred_foods = [food for food in self.foods if food.name in self.preferred_foods]

        
        if not valid_foods:
            return []
        
        min_calories_per_meal = target_calories * 0.25 / time_slots
        calories_per_slot = target_calories / time_slots
        
        best_plans = []
        tried_combinations = set()
        
        def backtrack(current_meal, remaining_slots, start_idx, running_total):
            if len(current_meal) == max_items or remaining_slots == 0:
                if running_total < min_calories_per_meal:
                    return
                
                meal_key = tuple(sorted(food.name for food in current_meal))
                if meal_key in tried_combinations:
                    return
                tried_combinations.add(meal_key)
                
                score = self.evaluate_meal(current_meal, calories_per_slot, restrictions)
                if len(best_plans) < time_slots:
                    heapq.heappush(best_plans, (score, current_meal.copy()))
                elif score < best_plans[0][0]:
                    heapq.heappushpop(best_plans, (score, current_meal.copy()))
                return
            
            if running_total > calories_per_slot * 1.3: #BOUND
                return
            
            for i in range(start_idx, len(valid_foods)):
                food = valid_foods[i]
                current_meal.append(food)
                backtrack(current_meal, remaining_slots - 1, i + 1, running_total + food.calories) #Branch
                current_meal.pop()
            for food in preferred_foods:
               if food not in current_meal:
                   current_meal.append(food)
                   running_total += food.calories
        
        # Mulai proses backtracking
        for _ in range(time_slots * 2):
            backtrack([], max_items, 0, 0)
        
        return [meal for _, meal in sorted(best_plans, key=lambda x: x[0])]
    
    def generate_meal_plan(self, target_calories, restrictions, max_items=5, time_slots=3):
        """Generate optimized meal plan"""
        meal_plans = self.backtracking_meal_plan(target_calories, restrictions, max_items, time_slots)
        
        # Cek apakah kalori memenuhi
        total_plan_calories = sum(sum(food.calories for food in meal) for meal in meal_plans)
        
        # kalo dibawah target, bisa coba naikin jumlah minimal kalori atau jumlah item
        if total_plan_calories < target_calories * 0.95:
            min_calories = target_calories / time_slots * 0.6
            meal_plans = self.backtracking_meal_plan(target_calories, restrictions, max_items + 1, time_slots)
        
        return meal_plans

class MealPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nutri Plan - Perencana Makan Cerdas")
        self.root.geometry("900x700")
        self.planner = MealPlanner()
        
        # Variables for storing sizes
        self.current_width = 900
        self.current_height = 700
        
        # Add binding for window resize
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Create a style for the application
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TCheckbutton", font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        self.style.configure("Title.TLabel", font=("Arial", 24, "bold"))
        self.style.configure("Subtitle.TLabel", font=("Arial", 12))
        
        # Menyimpan data rencana makan untuk dicetak
        self.current_meal_plan = None
        self.target_calories = 0
        
        # Buat element UI
        self.create_main_ui()
        
    def on_window_resize(self, event):
        # Only handle window resize events, not widget resize events
        if event.widget == self.root:
            # Update current sizes
            self.current_width = event.width
            self.current_height = event.height
            
            # Could add specific layout adjustments here based on new size
            
    def create_logo(self):
        """Create a simple logo for Nutri Plan"""
        width, height = 100, 100
        
        # Create a simple circular logo
        img = Image.new('RGBA', (width, height), (255, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw outer circle
        draw.ellipse((5, 5, 95, 95), fill="#4CAF50")
        # Draw inner circle
        draw.ellipse((15, 15, 85, 85), fill="#8BC34A")
        # Draw a simple leaf shape
        points = [(30, 35), (50, 20), (70, 35), (85, 50), (70, 65), (50, 80), (30, 65), (15, 50)]
        draw.polygon(points, fill="#FFFFFF")
        # Draw food dots
        draw.ellipse((35, 40, 45, 50), fill="#FF5722")
        draw.ellipse((55, 40, 65, 50), fill="#2196F3")
        draw.ellipse((45, 55, 55, 65), fill="#FFC107")
        
        return ImageTk.PhotoImage(img)
        
    def create_main_ui(self):
        # Create a notebook to hold different screens
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        # Main frame for meal planning
        self.main_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.main_frame, text="Rencana Makan")
        
        # Help frame for user guide
        self.help_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.help_frame, text="Panduan")
        
        # Results frame for generated meal plans
        self.results_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.results_frame, text="Hasil")
        
        # About frame for information about the algorithm
        self.about_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.about_frame, text="Tentang")
        
        # Set up the frames
        self.setup_main_frame()
        self.setup_help_frame()
        self.setup_about_frame()
        
        # Initialize results frame (will be populated later)
        ttk.Label(self.results_frame, text="Silakan generate rencana makan terlebih dahulu", 
                 style="Header.TLabel").pack(pady=20)
        
        # Start on main frame directly instead of guide
        self.notebook.select(self.main_frame)
        
    def setup_main_frame(self):
        # Header frame
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill="x", pady=5)
    
        # Try to create logo
        try:
            logo_img = self.create_logo()
            logo_label = ttk.Label(header_frame, image=logo_img)
            logo_label.image = logo_img 
            logo_label.pack(side="left", padx=10)
        except Exception as e:
            print(f"Error creating logo: {e}")
            logo_label = ttk.Label(header_frame, text="🥗", font=("Arial", 30))
            logo_label.pack(side="left", padx=10)
    
        # Title
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side="left", padx=10)
        ttk.Label(title_frame, text="Nutri Plan", style="Title.TLabel").pack(anchor="w")
        ttk.Label(title_frame, text="Perencana Makan dengan Algoritma Cerdas", 
                 style="Subtitle.TLabel").pack(anchor="w")
        
        # Help button
        help_button = ttk.Button(header_frame, text="?", width=3, 
                                command=lambda: self.notebook.select(self.help_frame))
        help_button.pack(side="right", padx=10)
        
        # Create two column layout for better space usage
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill="both", expand=True, pady=10)
        
        # Left column for basic settings
        settings_frame = ttk.LabelFrame(content_frame, text="Pengaturan Dasar")
        settings_frame.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)
        
        # Setup basic settings
        self.setup_basic_settings(settings_frame)
        
        # Right column for food preferences
        prefs_frame = ttk.LabelFrame(content_frame, text="Preferensi Makanan")
        prefs_frame.pack(side="right", fill="both", expand=True, padx=(5, 0), pady=5)
        
        # Setup food preferences
        self.setup_food_preferences(prefs_frame)
        
        # Buttons at the top for better visibility on small screens
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill="x", pady=10)
        
        # Move buttons to right after the title for better visibility
        content_frame.pack_forget()
        button_frame.pack_forget()
        
        # Now repack in correct order
        button_frame.pack(fill="x", pady=10, after=header_frame)
        content_frame.pack(fill="both", expand=True, pady=10, after=button_frame)
        
        generate_btn = ttk.Button(button_frame, text="Generate Rencana Makan", 
                                  command=self.generate_plan)
        generate_btn.pack(side="left", padx=5)
        
        reset_btn = ttk.Button(button_frame, text="Reset", command=self.reset_form)
        reset_btn.pack(side="left", padx=5)
        
    def setup_basic_settings(self, parent):
        # Target calories
        cal_frame = ttk.Frame(parent)
        cal_frame.pack(fill="x", pady=5)
        ttk.Label(cal_frame, text="Target Kalori:").pack(side="left")
        self.calories_var = tk.StringVar(value="1500")
        ttk.Entry(cal_frame, textvariable=self.calories_var, width=10).pack(side="left", padx=5)
        
        # Number of meals
        meal_frame = ttk.Frame(parent)
        meal_frame.pack(fill="x", pady=5)
        ttk.Label(meal_frame, text="Jumlah Waktu Makan:").pack(side="left")
        self.meals_var = tk.StringVar(value="3")
        ttk.Spinbox(meal_frame, from_=1, to=6, textvariable=self.meals_var, width=5).pack(side="left", padx=5)
        
        # Max items per meal
        item_frame = ttk.Frame(parent)
        item_frame.pack(fill="x", pady=5)
        ttk.Label(item_frame, text="Maks. Item per Waktu Makan:").pack(side="left")
        self.items_var = tk.StringVar(value="4")
        ttk.Spinbox(item_frame, from_=1, to=10, textvariable=self.items_var, width=5).pack(side="left", padx=5)
        
        # Diet restrictions - use a grid for better spacing
        diet_frame = ttk.LabelFrame(parent, text="Diet Khusus")
        diet_frame.pack(fill="x", pady=10)
        
        self.vegan_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(diet_frame, text="Vegan/Vegetarian", variable=self.vegan_var).pack(anchor="w", padx=5)
        
        self.gluten_free_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(diet_frame, text="Gluten-Free", variable=self.gluten_free_var).pack(anchor="w", padx=5)
        
        self.keto_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(diet_frame, text="Keto", variable=self.keto_var).pack(anchor="w", padx=5)
        
        # Allergies
        allergies_frame = ttk.LabelFrame(parent, text="Alergi")
        allergies_frame.pack(fill="x", pady=10)
        
        self.allergy_kacang = tk.BooleanVar(value=False)
        ttk.Checkbutton(allergies_frame, text="Kacang", variable=self.allergy_kacang).pack(anchor="w", padx=5)
        
        self.allergy_susu = tk.BooleanVar(value=False)
        ttk.Checkbutton(allergies_frame, text="Susu", variable=self.allergy_susu).pack(anchor="w", padx=5)
        
        self.allergy_telur = tk.BooleanVar(value=False)
        ttk.Checkbutton(allergies_frame, text="Telur", variable=self.allergy_telur).pack(anchor="w", padx=5)
    
    def setup_food_preferences(self, parent):
        # Get food names
        food_names = [food.name for food in self.planner.foods]
        
        # Create frames for each type
        liked_frame = ttk.LabelFrame(parent, text="Makanan yang Disukai")
        liked_frame.pack(fill="x", pady=5)
        
        disliked_frame = ttk.LabelFrame(parent, text="Makanan yang Tidak Disukai")
        disliked_frame.pack(fill="x", pady=5)
        
        unavailable_frame = ttk.LabelFrame(parent, text="Bahan Tidak Tersedia")
        unavailable_frame.pack(fill="x", pady=5)
        
        # Liked foods
        self.liked_var = tk.StringVar()
        liked_combo_frame = ttk.Frame(liked_frame)
        liked_combo_frame.pack(fill="x", pady=5)
        self.liked_combo = ttk.Combobox(liked_combo_frame, textvariable=self.liked_var, values=food_names, width=20)
        self.liked_combo.pack(side="left", padx=5)
        ttk.Button(liked_combo_frame, text="Tambah", command=self.add_liked_food).pack(side="left")
        
        self.liked_list = tk.Text(liked_frame, height=3, width=30, wrap="word")
        self.liked_list.pack(fill="x", padx=5, pady=5)
        self.liked_list.config(state="disabled")
        
        # Disliked foods
        self.disliked_var = tk.StringVar()
        disliked_combo_frame = ttk.Frame(disliked_frame)
        disliked_combo_frame.pack(fill="x", pady=5)
        self.disliked_combo = ttk.Combobox(disliked_combo_frame, textvariable=self.disliked_var, values=food_names, width=20)
        self.disliked_combo.pack(side="left", padx=5)
        ttk.Button(disliked_combo_frame, text="Tambah", command=self.add_disliked_food).pack(side="left")
        
        self.disliked_list = tk.Text(disliked_frame, height=3, width=30, wrap="word")
        self.disliked_list.pack(fill="x", padx=5, pady=5)
        self.disliked_list.config(state="disabled")
        
        # Unavailable foods
        self.unavailable_var = tk.StringVar()
        unavailable_combo_frame = ttk.Frame(unavailable_frame)
        unavailable_combo_frame.pack(fill="x", pady=5)
        self.unavailable_combo = ttk.Combobox(unavailable_combo_frame, textvariable=self.unavailable_var, values=food_names, width=20)
        self.unavailable_combo.pack(side="left", padx=5)
        ttk.Button(unavailable_combo_frame, text="Tambah", command=self.add_unavailable_food).pack(side="left")
        
        self.unavailable_list = tk.Text(unavailable_frame, height=3, width=30, wrap="word")
        self.unavailable_list.pack(fill="x", padx=5, pady=5)
        self.unavailable_list.config(state="disabled")
    
    def setup_help_frame(self):
        """Set up the help/guide frame with user instructions"""
        # Welcome header
        ttk.Label(self.help_frame, text="Selamat Datang di Nutri Plan!", 
                 style="Title.TLabel").pack(pady=10)
        
        # Create scrollable text area for instructions
        guide_text = scrolledtext.ScrolledText(self.help_frame, wrap=tk.WORD, height=25)
        guide_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # User guide text
        guide_content = """
Panduan Penggunaan Nutri Plan
=============================

Nutri Plan adalah aplikasi perencana makanan cerdas yang menggunakan algoritma Branch and Bound untuk menyusun rencana makanan yang optimal sesuai kebutuhan kalori dan preferensi diet Anda.

MEMULAI
-------
1. Gunakan tab "Rencana Makan" untuk memasukkan semua preferensi dan informasi Anda.
2. Setelah mengklik "Generate Rencana Makan", hasil akan ditampilkan di tab "Hasil".

PENGATURAN DASAR
---------------
• Target Kalori: Masukkan jumlah kalori harian yang Anda inginkan (misal: 1500, 2000)
• Jumlah Waktu Makan: Pilih berapa kali Anda ingin makan dalam sehari (1-6)
• Maks. Item per Waktu Makan: Jumlah maksimal makanan per waktu makan

DIET KHUSUS
-----------
• Vegan/Vegetarian: Aktifkan untuk hanya mendapatkan makanan nabati
• Gluten-Free: Aktifkan untuk menghindari makanan yang mengandung gluten
• Keto: Aktifkan untuk diet rendah karbohidrat dan tinggi lemak

ALERGI
------
Centang kotak untuk setiap bahan yang Anda alergi:
• Kacang: Menghindari makanan berbasis kacang-kacangan
• Susu: Menghindari produk susu
• Telur: Menghindari telur dan produk berbasis telur

PREFERENSI MAKANAN
-----------------
Anda dapat menyesuaikan rencana makanan dengan:

• Makanan yang Disukai: Makanan yang Anda ingin lebih sering muncul dalam rencana
  - Pilih makanan dari dropdown
  - Klik "Tambah" untuk menambahkan ke daftar
  
• Makanan yang Tidak Disukai: Makanan yang Anda kurang suka (masih mungkin muncul)
  - Pilih makanan dari dropdown
  - Klik "Tambah" untuk menambahkan ke daftar
  
• Bahan Tidak Tersedia: Bahan yang tidak tersedia (tidak akan muncul sama sekali)
  - Pilih makanan dari dropdown
  - Klik "Tambah" untuk menambahkan ke daftar

HASIL RENCANA MAKAN
------------------
Setelah mengklik "Generate Rencana Makan", Anda akan melihat:
• Rencana makanan untuk setiap waktu makan
• Daftar bahan makanan per waktu makan
• Informasi kalori dan nutrisi
• Grafik distribusi nutrisi
• Ringkasan total nutrisi harian

CETAK RENCANA MAKAN
-----------------
Anda dapat mencetak rencana makan dengan menekan tombol "Cetak Rencana" pada halaman hasil.
File akan disimpan dalam format .txt yang dapat dibuka dengan aplikasi teks biasa.

TIPS PENGGUNAAN
--------------
• Bila ingin membuat ulang rencana makan dengan preferensi sama, cukup klik "Generate Rencana Makan" lagi
• Gunakan "Reset" untuk mengembalikan semua pengaturan ke nilai default
• Jika hasil tidak muncul, coba kurangi batasan atau tambah lebih banyak makanan yang tersedia
• Untuk diet khusus seperti keto, aplikasi akan memastikan komposisi nutrisi sesuai dengan kebutuhan diet
        """
        
        guide_text.insert(tk.END, guide_content)
        guide_text.config(state=tk.DISABLED)
        
        # Button to return to main screen
        ttk.Button(self.help_frame, text="Kembali ke Rencana Makan", 
                  command=lambda: self.notebook.select(self.main_frame)).pack(pady=10)
    
    def setup_about_frame(self):
        """Add information about the algorithm to the about tab"""
        ttk.Label(self.about_frame, text="Tentang Nutri Plan", 
                 style="Title.TLabel").pack(pady=10)
        
        algorithm_info = """
Penjelasan Penggunaan Algoritma Backtracking dengan Branch and Bound:

1. Algoritma Backtracking:
   - Mencoba berbagai kombinasi makanan untuk membuat rencana makanan
   - Mencabut pilihan yang tidak sesuai (backtrack) dan mencoba pilihan lain
   - Mengeksplorasi semua kemungkinan rencana makanan yang valid

2. Optimasi dengan Branch and Bound:
   - Menghitung batas bawah (lower bound) untuk setiap kombinasi makanan
   - Memotong cabang pencarian jika batas bawah lebih buruk dari solusi terbaik yang ditemukan
   - Menggunakan fungsi evaluasi untuk memilih rencana makanan terbaik
   - Berhenti jika total kalori sudah melebihi batas yang ditentukan (bound)

3. Keunggulan Pendekatan Ini:
   - Lebih efisien daripada brute force karena memangkas cabang yang tidak menjanjikan
   - Menemukan solusi optimal atau mendekati optimal
   - Dapat menangani berbagai batasan diet secara bersamaan
       
4. Fitur yang Ditingkatkan:
   - Memastikan total kalori memenuhi atau melebihi target harian
   - Meningkatkan distribusi kalori antar waktu makan
   - Mempertimbangkan preferensi makanan yang disukai dan tidak disukai
   - Memungkinkan pengaturan item maksimum per waktu makan
   - Mengabaikan bahan makanan yang tidak tersedia
        """
        
        info_text = scrolledtext.ScrolledText(self.about_frame, wrap=tk.WORD, height=20)
        info_text.pack(fill="both", expand=True, padx=10, pady=10)
        info_text.insert(tk.END, algorithm_info)
        info_text.config(state=tk.DISABLED)
        
        # Button to return to main screen
        ttk.Button(self.about_frame, text="Kembali ke Rencana Makan", 
                  command=lambda: self.notebook.select(self.main_frame)).pack(pady=10)
    
    def show_guide(self):
        """Show the guide on first start"""
        self.notebook.select(self.help_frame)
    
    def add_liked_food(self):
        """Add a food to the liked foods list"""
        food = self.liked_var.get()
        if food and food not in self.planner.preferred_foods:
            self.planner.preferred_foods.append(food)
            self.update_preferences_display()
    
    def add_disliked_food(self):
        """Add a food to the disliked foods list"""
        food = self.disliked_var.get()
        if food and food not in self.planner.disliked_foods:
            self.planner.disliked_foods.append(food)
            self.update_preferences_display()
    
    def add_unavailable_food(self):
        """Add a food to the unavailable foods list"""
        food = self.unavailable_var.get()
        if food and food not in self.planner.unavailable_foods:
            self.planner.unavailable_foods.append(food)
            self.update_preferences_display()
    
    def update_preferences_display(self):
        """Update the displayed preferences lists"""
        # Update liked foods display
        self.liked_list.config(state="normal")
        self.liked_list.delete(1.0, tk.END)
        self.liked_list.insert(tk.END, ", ".join(self.planner.preferred_foods))
        self.liked_list.config(state="disabled")
        
        # Update disliked foods display
        self.disliked_list.config(state="normal")
        self.disliked_list.delete(1.0, tk.END)
        self.disliked_list.insert(tk.END, ", ".join(self.planner.disliked_foods))
        self.disliked_list.config(state="disabled")
        
        # Update unavailable foods display
        self.unavailable_list.config(state="normal")
        self.unavailable_list.delete(1.0, tk.END)
        self.unavailable_list.insert(tk.END, ", ".join(self.planner.unavailable_foods))
        self.unavailable_list.config(state="disabled")
    
    def reset_form(self):
        """Reset all form inputs to default values"""
        # Reset basic settings
        self.calories_var.set("1500")
        self.meals_var.set("3")
        self.items_var.set("4")
        
        # Reset diet restrictions
        self.vegan_var.set(False)
        self.gluten_free_var.set(False)
        self.keto_var.set(False)
        
        # Reset allergies
        self.allergy_kacang.set(False)
        self.allergy_susu.set(False)
        self.allergy_telur.set(False)
        
        # Reset food preferences
        self.planner.preferred_foods = []
        self.planner.disliked_foods = []
        self.planner.unavailable_foods = []
        self.update_preferences_display()
        
        # Reset current meal plan
        self.current_meal_plan = None
        
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.results_frame, text="Silakan generate rencana makan terlebih dahulu", 
                 style="Header.TLabel").pack(pady=20)
        
        messagebox.showinfo("Reset", "Semua pengaturan telah direset ke nilai awal")
    
    def get_meal_name(self, index, total_meals):
        """Get the appropriate meal name based on index and total meals"""
        if total_meals <= 3:
            meal_names = ["Sarapan", "Makan Siang", "Makan Malam"]
            return meal_names[index] if index < len(meal_names) else f"Waktu Makan {index+1}"
        else:
            # For more than 3 meals, use standard names plus snacks
            if index == 0:
                return "Sarapan"
            elif index == 1:
                return "Makan Siang"
            elif index == total_meals - 1:
                return "Makan Malam"
            else:
                # Calculate snack number (index 2 becomes Snack 1, etc.)
                snack_num = index - 1
                return f"Snack {snack_num}"
    
    def generate_plan(self):
        """Generate a meal plan based on user inputs"""
        try:
            # Get user inputs
            target_calories = int(self.calories_var.get())
            meals_count = int(self.meals_var.get())
            max_items = int(self.items_var.get())
            
            # Get diet restrictions
            restrictions = {
                'vegan': self.vegan_var.get(),
                'gluten_free': self.gluten_free_var.get(),
                'keto': self.keto_var.get(),
                'allergies': []
            }
            
            # Add allergies
            if self.allergy_kacang.get():
                restrictions['allergies'].append("kacang")
            if self.allergy_susu.get():
                restrictions['allergies'].append("susu")
            if self.allergy_telur.get():
                restrictions['allergies'].append("telur")
            
            # Generate meal plan
            meal_plans = self.planner.generate_meal_plan(
                target_calories, restrictions, max_items, meals_count
            )
            
            # Store current plan for printing
            self.current_meal_plan = meal_plans
            self.target_calories = target_calories
            
            # Show results
            self.display_results(meal_plans, target_calories, meals_count)
            
            # Switch to results tab
            self.notebook.select(self.results_frame)
            
        except ValueError as e:
            messagebox.showerror("Error", "Masukkan nilai numerik yang valid untuk kalori dan jumlah makanan")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    
    def display_results(self, meal_plans, target_calories, meals_count):
        """Display meal plan results in the results frame"""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Check if meal plan was successfully generated
        if not meal_plans:
            ttk.Label(self.results_frame, text="Tidak dapat membuat rencana makan dengan batasan yang diberikan. Coba kurangi batasan.",
                     style="Header.TLabel").pack(pady=20)
            return
        
        # Results header
        header_frame = ttk.Frame(self.results_frame)
        header_frame.pack(fill="x", pady=10)
        
        ttk.Label(header_frame, text=f"Rencana Makan {target_calories} Kalori", 
                 style="Title.TLabel").pack(side="left", pady=5)
        
        # Add print button
        print_btn = ttk.Button(header_frame, text="Cetak Rencana", 
                              command=self.print_meal_plan)
        print_btn.pack(side="right", padx=10)
        
        # Create a notebook for meal times
        meal_notebook = ttk.Notebook(self.results_frame)
        meal_notebook.pack(fill="both", expand=True, pady=10, padx=5)
        
        # Total nutrition
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        # Display each meal
        for i, meal in enumerate(meal_plans):
            if i >= meals_count:  # Only show requested number of meals
                break
                
            meal_name = self.get_meal_name(i, meals_count)
            
            # Create a frame for this meal
            meal_frame = ttk.Frame(meal_notebook, padding=10)
            meal_notebook.add(meal_frame, text=meal_name)
            
            # Meal header
            ttk.Label(meal_frame, text=f"{meal_name}", 
                     style="Header.TLabel").pack(anchor="w", pady=5)
            
            # Meal contents
            meal_calories = sum(food.calories for food in meal)
            meal_protein = sum(food.protein for food in meal)
            meal_carbs = sum(food.carbs for food in meal)
            meal_fat = sum(food.fat for food in meal)
            
            # Update totals
            total_calories += meal_calories
            total_protein += meal_protein
            total_carbs += meal_carbs
            total_fat += meal_fat
            
            # Create two column layout: food list and nutritional info
            meal_content_frame = ttk.Frame(meal_frame)
            meal_content_frame.pack(fill="both", expand=True)
            
            # Left column: Food list
            food_frame = ttk.LabelFrame(meal_content_frame, text="Daftar Makanan")
            food_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
            
            # Food table
            food_columns = ('name', 'calories', 'protein', 'carbs', 'fat')
            food_tree = ttk.Treeview(food_frame, columns=food_columns, show='headings', height=len(meal))
            
            # Configure columns
            food_tree.heading('name', text='Nama Makanan')
            food_tree.heading('calories', text='Kalori')
            food_tree.heading('protein', text='Protein (g)')
            food_tree.heading('carbs', text='Karb (g)')
            food_tree.heading('fat', text='Lemak (g)')
            
            # Set column widths
            food_tree.column('name', width=150)
            food_tree.column('calories', width=70, anchor='center')
            food_tree.column('protein', width=70, anchor='center')
            food_tree.column('carbs', width=70, anchor='center')
            food_tree.column('fat', width=70, anchor='center')
            
            # Add foods to table
            for food in meal:
                food_tree.insert('', 'end', values=(
                    food.name, 
                    f"{food.calories:.0f}", 
                    f"{food.protein:.1f}", 
                    f"{food.carbs:.1f}", 
                    f"{food.fat:.1f}"
                ))
            
            food_tree.pack(fill="both", expand=True, pady=5)
            
            # Right column: Nutritional info
            info_frame = ttk.LabelFrame(meal_content_frame, text="Informasi Nutrisi")
            info_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
            
            # Basic nutritional info
            ttk.Label(info_frame, text=f"Total Kalori: {meal_calories:.0f} kcal").pack(anchor="w", pady=2)
            ttk.Label(info_frame, text=f"Protein: {meal_protein:.1f}g ({meal_protein*4/meal_calories*100:.0f}%)").pack(anchor="w", pady=2)
            ttk.Label(info_frame, text=f"Karbohidrat: {meal_carbs:.1f}g ({meal_carbs*4/meal_calories*100:.0f}%)").pack(anchor="w", pady=2)
            ttk.Label(info_frame, text=f"Lemak: {meal_fat:.1f}g ({meal_fat*9/meal_calories*100:.0f}%)").pack(anchor="w", pady=2)
            
            # Nutrient distribution pie chart
            self.create_meal_chart(info_frame, meal_protein, meal_carbs, meal_fat)
        
        # Summary tab
        summary_frame = ttk.Frame(meal_notebook, padding=10)
        meal_notebook.add(summary_frame, text="Ringkasan")
        
        ttk.Label(summary_frame, text="Ringkasan Nutrisi Harian", 
                 style="Header.TLabel").pack(pady=5)
        
        # Daily totals
        ttk.Label(summary_frame, text=f"Target Kalori: {target_calories} kcal").pack(anchor="w", pady=2)
        ttk.Label(summary_frame, text=f"Total Kalori: {total_calories:.0f} kcal ({total_calories/target_calories*100:.0f}% dari target)").pack(anchor="w", pady=2)
        ttk.Label(summary_frame, text=f"Total Protein: {total_protein:.1f}g ({total_protein*4/total_calories*100:.0f}%)").pack(anchor="w", pady=2)
        ttk.Label(summary_frame, text=f"Total Karbohidrat: {total_carbs:.1f}g ({total_carbs*4/total_calories*100:.0f}%)").pack(anchor="w", pady=2)
        ttk.Label(summary_frame, text=f"Total Lemak: {total_fat:.1f}g ({total_fat*9/total_calories*100:.0f}%)").pack(anchor="w", pady=2)
        
        # Create overall distribution chart
        self.create_meal_chart(summary_frame, total_protein, total_carbs, total_fat, larger=True)
    
    def create_meal_chart(self, parent, protein, carbs, fat, larger=False):
        """Create a pie chart showing macronutrient distribution"""
        # Calculate calories from each macro
        protein_cal = protein * 4
        carbs_cal = carbs * 4
        fat_cal = fat * 9
        total_cal = protein_cal + carbs_cal + fat_cal
        
        # Set size based on larger flag
        size = 3 if larger else 2
        
        # Create figure
        fig = plt.Figure(figsize=(size, size))
        ax = fig.add_subplot(111)
        
        if total_cal > 0:  # Avoid division by zero
            # Calculate percentages
            labels = 'Protein', 'Karbohidrat', 'Lemak'
            sizes = [protein_cal/total_cal*100, carbs_cal/total_cal*100, fat_cal/total_cal*100]
            colors = ['#ff9999','#66b3ff','#99ff99']
            
            # Create pie chart
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
        else:
            ax.text(0.5, 0.5, "Tidak ada data", ha='center', va='center')
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def print_meal_plan(self):
        """Export meal plan to a text file"""
        if not self.current_meal_plan:
            messagebox.showinfo("Info", "Tidak ada rencana makan untuk dicetak. Harap generate terlebih dahulu.")
            return
        
        # Ask user where to save the file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Simpan Rencana Makan"
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            with open(file_path, 'w') as file:
                # Write header
                file.write("===================================\n")
                file.write(f"RENCANA MAKAN {self.target_calories} KALORI\n")
                file.write("===================================\n\n")
                
                # Get meals count
                meals_count = int(self.meals_var.get())
                
                # Total nutrition
                total_calories = 0
                total_protein = 0
                total_carbs = 0
                total_fat = 0
                
                # Write each meal
                for i, meal in enumerate(self.current_meal_plan):
                    if i >= meals_count:  # Only show requested number of meals
                        break
                        
                    meal_name = self.get_meal_name(i, meals_count)
                    
                    # Calculate meal totals
                    meal_calories = sum(food.calories for food in meal)
                    meal_protein = sum(food.protein for food in meal)
                    meal_carbs = sum(food.carbs for food in meal)
                    meal_fat = sum(food.fat for food in meal)
                    
                    # Update overall totals
                    total_calories += meal_calories
                    total_protein += meal_protein
                    total_carbs += meal_carbs
                    total_fat += meal_fat
                    
                    # Write meal header
                    file.write(f"## {meal_name} ##\n")
                    file.write("----------------------------------\n")
                    
                    # Write foods
                    for food in meal:
                        file.write(f"{food.name}: {food.calories:.0f} kcal, Protein: {food.protein:.1f}g, Karb: {food.carbs:.1f}g, Lemak: {food.fat:.1f}g\n")
                    
                    # Write meal totals
                    file.write("----------------------------------\n")
                    file.write(f"Total Kalori: {meal_calories:.0f} kcal\n")
                    file.write(f"Total Protein: {meal_protein:.1f}g ({meal_protein*4/meal_calories*100:.0f}%)\n")
                    file.write(f"Total Karbohidrat: {meal_carbs:.1f}g ({meal_carbs*4/meal_calories*100:.0f}%)\n")
                    file.write(f"Total Lemak: {meal_fat:.1f}g ({meal_fat*9/meal_calories*100:.0f}%)\n\n")
                
                # Write summary
                file.write("===================================\n")
                file.write("RINGKASAN NUTRISI HARIAN\n")
                file.write("===================================\n")
                file.write(f"Target Kalori: {self.target_calories} kcal\n")
                file.write(f"Total Kalori: {total_calories:.0f} kcal ({total_calories/self.target_calories*100:.0f}% dari target)\n")
                file.write(f"Total Protein: {total_protein:.1f}g ({total_protein*4/total_calories*100:.0f}%)\n")
                file.write(f"Total Karbohidrat: {total_carbs:.1f}g ({total_carbs*4/total_calories*100:.0f}%)\n")
                file.write(f"Total Lemak: {total_fat:.1f}g ({total_fat*9/total_calories*100:.0f}%)\n")
                
            messagebox.showinfo("Sukses", f"Rencana makan berhasil disimpan ke {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan file: {str(e)}")

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = MealPlannerApp(root)
    root.mainloop()


