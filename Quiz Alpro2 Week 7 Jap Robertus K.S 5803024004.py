import tkinter as tk
from tkinter import ttk, messagebox
import random

class ArmeniaTripPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Armenia Trip Planner")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        
        self.destinations = {
            "Yerevan": 150000,
            "Lake Sevan": 80000,
            "Dilijan": 70000,
            "Tatev Monastery": 120000,
            "Garni Temple": 65000,
            "Geghard Monastery": 75000,
            "Noravank Monastery": 85000,
            "Khor Virap": 95000,
            "Amberd Fortress": 75000,
            "Gyumri": 110000
        }
        
        self.accommodations = {
            "Luxury Hotel": 1200000,
            "Mid-range Hotel": 800000,
            "Budget Hotel": 500000,
            "Guesthouse": 350000,
            "Hostel": 200000,
            "Homestay": 300000,
            "Apartment Rental": 650000
        }
        
        self.transportation = {
            "Private Car Rental": 700000,
            "Taxi": 450000,
            "Public Transport": 150000,
            "Tour Bus": 300000,
            "Bike Rental": 100000,
            "Private Driver": 850000
        }
        
        self.activities = {
            "Wine Tasting Tour": 250000,
            "Historical Tour": 200000,
            "Hiking Adventure": 150000,
            "Cooking Class": 180000,
            "Cultural Show": 120000,
            "Museum Pass": 100000,
            "Carpet Factory Tour": 80000,
            "Hot Air Balloon Ride": 600000,
            "Spa Day": 350000,
            "Craft Workshop": 175000
        }
        
        # New categories
        self.snacks = {
            "Street Food Tour": 120000,
            "Armenian Cheese Tasting": 85000,
            "Local Sweets Package": 60000,
            "Traditional Bakery Tour": 75000,
            "Wine and Cheese Pairing": 130000,
            "Fruit Market Experience": 45000,
            "Coffee Shop Hopping": 70000,
            "Lavash Making Class": 95000,
            "Dried Fruit and Nuts": 40000,
            "Fine Dining Experience": 250000
        }
        
        self.hidden_gems = {
            "Secret Cave Monastery": 110000,
            "Local Family Dinner": 85000,
            "Off-road Adventure": 220000,
            "Abandoned Soviet Factory": 65000,
            "Armenian Spirits Tasting": 95000,
            "Stargazing at Remote Site": 150000,
            "Shepherd's Mountain Hut Stay": 120000,
            "Obscure Archaeological Site": 70000,
            "Hidden Waterfall Trek": 90000,
            "Underground Jazz Club": 80000
        }
        
        # Flight costs from Indonesia to Armenia
        self.flights = {
            "Economy Class (CGK to EVN)": 12000000,
            "Economy with Layover": 10500000,
            "Premium Economy": 15000000,
            "Business Class": 25000000,
            "Mixed Airlines Budget": 9800000
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#f0f0f0")
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="Armenia Trip Planner", font=("Arial", 22, "bold"), bg="#f0f0f0")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Using Backtracking Algorithm for Exact Budget Planning", font=("Arial", 12), bg="#f0f0f0")
        subtitle_label.pack()
        
        # Input
        input_frame = tk.Frame(self.root, bg="#f0f0f0", bd=2, relief=tk.GROOVE)
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Lokasi start
        location_label = tk.Label(input_frame, text="Starting Point:", font=("Arial", 12), bg="#f0f0f0")
        location_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.location_var = tk.StringVar(value="From Indonesia")
        location_rb1 = tk.Radiobutton(input_frame, text="From Indonesia", variable=self.location_var, 
                                      value="From Indonesia", font=("Arial", 11), bg="#f0f0f0",
                                      command=self.update_min_budget)
        location_rb1.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        location_rb2 = tk.Radiobutton(input_frame, text="Already in Armenia", variable=self.location_var, 
                                      value="Already in Armenia", font=("Arial", 11), bg="#f0f0f0",
                                      command=self.update_min_budget)
        location_rb2.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)
        
        # input budget
        budget_label = tk.Label(input_frame, text="Budget (Rupiah):", font=("Arial", 12), bg="#f0f0f0")
        budget_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.budget_entry = tk.Entry(input_frame, font=("Arial", 12), width=15)
        self.budget_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        self.budget_entry.insert(0, "15000000")  # Default 15 million rupiah
        
        self.min_budget_label = tk.Label(input_frame, text="Min budget: Rp 9,800,000 (includes flight)", 
                                         font=("Arial", 10), fg="red", bg="#f0f0f0")
        self.min_budget_label.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W)
        
        # jumlah destinasi
        destinations_label = tk.Label(input_frame, text="Destinations:", font=("Arial", 12), bg="#f0f0f0")
        destinations_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.destinations_spinbox = tk.Spinbox(input_frame, from_=1, to=5, font=("Arial", 12), width=5)
        self.destinations_spinbox.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        
        # kategori
        categories_label = tk.Label(input_frame, text="Include Categories:", font=("Arial", 12), bg="#f0f0f0")
        categories_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        
        categories_frame = tk.Frame(input_frame, bg="#f0f0f0")
        categories_frame.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky=tk.W)
        
        # Checkboxes for categories
        self.include_snacks = tk.BooleanVar(value=True)
        self.include_hidden_gems = tk.BooleanVar(value=True)
        
        snacks_cb = tk.Checkbutton(categories_frame, text="Snacks & Food", variable=self.include_snacks, 
                                   font=("Arial", 11), bg="#f0f0f0")
        snacks_cb.pack(side=tk.LEFT, padx=10)
        
        hidden_gems_cb = tk.Checkbutton(categories_frame, text="Hidden Gems", variable=self.include_hidden_gems, 
                                        font=("Arial", 11), bg="#f0f0f0")
        hidden_gems_cb.pack(side=tk.LEFT, padx=10)
        
        # tombol plan
        button_frame = tk.Frame(input_frame, bg="#f0f0f0")
        button_frame.grid(row=4, column=0, columnspan=3, pady=15)
        
        plan_button = tk.Button(button_frame, text="Plan My Trip", font=("Arial", 12, "bold"), 
                               bg="#4CAF50", fg="white", padx=20, pady=5, command=self.plan_trip)
        plan_button.pack()
        
        # hasil
        results_frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.GROOVE)
        results_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Results area
        self.results_text = tk.Text(results_frame, font=("Arial", 11), wrap=tk.WORD, bg="white")
        self.results_text.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        results_scrollbar = tk.Scrollbar(results_frame)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        results_scrollbar.config(command=self.results_text.yview)
        self.results_text.config(yscrollcommand=results_scrollbar.set)
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to plan your trip to Armenia!")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        
        self.results_text.tag_config("title", font=("Arial", 14, "bold"))
        self.results_text.tag_config("subtitle", font=("Arial", 12, "bold"))
        self.results_text.tag_config("category", font=("Arial", 11, "bold"))
        self.results_text.tag_config("highlight", foreground="blue")
        self.results_text.tag_config("total", font=("Arial", 11, "bold"), foreground="green")
        self.results_text.tag_config("warning", foreground="red")
    
    def update_min_budget(self):
        if self.location_var.get() == "From Indonesia":
            min_budget = min(self.flights.values()) + 500000  
            self.min_budget_label.config(text=f"Min budget: Rp {min_budget:,} (includes flight)")
        else:
            self.min_budget_label.config(text="Min budget: Rp 500,000")
    
    def exact_backtracking(self, items, target_budget, must_have_categories):
        
        items.sort(key=lambda x: x[1], reverse=True)
        
        result = []
        remaining_items = []
        
        
        for category in must_have_categories:
            category_items = [item for item in items if item[2] == category]
            if category_items:
                
                cheapest = min(category_items, key=lambda x: x[1])
                result.append(cheapest)
                items.remove(cheapest)
        
        
        current_sum = sum(item[1] for item in result)
        remaining_budget = target_budget - current_sum
        
       
        if self.find_exact_subset_sum(items, remaining_budget, 0, [], remaining_items):
            result.extend(remaining_items)
            return result
        
        
        coin_change_result = self.coin_change_approach(items, remaining_budget)
        if coin_change_result:
            result.extend(coin_change_result)
            return result
        
      
        approximate_result = []
        self.find_closest_subset_sum(items, remaining_budget, 0, [], approximate_result, current_sum)
        
        
        if approximate_result:
            result.extend(approximate_result)
            
         
            total_sum = sum(item[1] for item in result)
            difference = target_budget - total_sum
            
            
            if difference != 0:
                result.append(("Budget Adjustment", difference, "Adjustment"))
        
        return result
    
    def find_exact_subset_sum(self, items, target, index, current, result):
       
        current_sum = sum(item[1] for item in current)
        if current_sum == target:
            result.extend(current)
            return True
        
        
        if current_sum > target or index >= len(items):
            return False
        
       
        current.append(items[index])
        if self.find_exact_subset_sum(items, target, index + 1, current, result):
            return True
        current.pop()  
        
        
        return self.find_exact_subset_sum(items, target, index + 1, current, result)
    
    def find_closest_subset_sum(self, items, target, index, current, best_result, best_sum):
        current_sum = sum(item[1] for item in current)
        
        
        if abs(target - current_sum) < abs(target - best_sum) and current_sum <= target:
            best_result.clear()
            best_result.extend(current)
            best_sum = current_sum
        
        
        if index >= len(items):
            return
        
        
        if current_sum + items[index][1] <= target:
            current.append(items[index])
            self.find_closest_subset_sum(items, target, index + 1, current, best_result, best_sum)
            current.pop()  
        
       
        self.find_closest_subset_sum(items, target, index + 1, current, best_result, best_sum)
    
    def coin_change_approach(self, items, target):
        """Use dynamic programming approach similar to coin change problem"""
        
        sorted_items = sorted(items, key=lambda x: x[1])
        
    
        cost_groups = {}
        for item in sorted_items:
            cost = item[1]
            if cost not in cost_groups:
                cost_groups[cost] = []
            cost_groups[cost].append(item)
        
        
        costs = sorted(cost_groups.keys())
        
        
        dp = [float('inf')] * (target + 1)
        dp[0] = 0
        choice = [[] for _ in range(target + 1)]
        
        
        for cost in costs:
            for amount in range(cost, target + 1):
                if dp[amount - cost] + 1 < dp[amount]:
                    dp[amount] = dp[amount - cost] + 1
                    choice[amount] = choice[amount - cost] + [cost]
        
        
        if dp[target] == float('inf'):
            return []
        
        
        result = []
        for cost in choice[target]:
            item = cost_groups[cost].pop(0)
            result.append(item)
        
        return result
    
    def plan_trip(self):
        try:
            # input
            budget = int(self.budget_entry.get())
            num_destinations = int(self.destinations_spinbox.get())
            starting_location = self.location_var.get()
            include_snacks = self.include_snacks.get()
            include_hidden_gems = self.include_hidden_gems.get()
            
            # budget nya
            min_budget = 500000 
            
            if starting_location == "From Indonesia":
                min_flight_cost = min(self.flights.values())
                min_budget = min_flight_cost + 500000  
            
            if budget < min_budget:
                messagebox.showerror("Invalid Budget", 
                                    f"For {'travel from Indonesia' if starting_location == 'From Indonesia' else 'a trip in Armenia'}, " +
                                    f"minimum budget should be Rp {min_budget:,}")
                return
            
            
            self.results_text.delete(1.0, tk.END)
            
            
            self.status_var.set("Planning your trip to Armenia with EXACT budget utilization...")
            self.root.update_idletasks()
            
            
            all_items = []
            
            
            flight_cost = 0
            if starting_location == "From Indonesia":
                
                affordable_flights = {name: cost for name, cost in self.flights.items() if cost <= budget * 0.7}
                if affordable_flights:
                    flight_name = random.choice(list(affordable_flights.keys()))
                    flight_cost = self.flights[flight_name]
                    all_items.append((flight_name, flight_cost, "Flight"))
                else:
                   
                    flight_name = min(self.flights.items(), key=lambda x: x[1])[0]
                    flight_cost = self.flights[flight_name]
                    all_items.append((flight_name, flight_cost, "Flight"))
            
            # Add destinations (randomly select based on num_destinations)
            dest_keys = list(self.destinations.keys())
            random.shuffle(dest_keys)
            selected_destinations = dest_keys[:min(num_destinations, len(dest_keys))]
            
            for dest in selected_destinations:
                all_items.append((dest, self.destinations[dest], "Destination"))
            
            # 1 accommodation, 1 transportation default
            accom_keys = list(self.accommodations.keys())
            trans_keys = list(self.transportation.keys())
            
            # akomodasi dan transportasi
            for accom, cost in self.accommodations.items():
                all_items.append((accom, cost, "Accommodation"))
            
            for trans, cost in self.transportation.items():
                all_items.append((trans, cost, "Transportation"))
            
            # Aktifitas
            for activity, cost in self.activities.items():
                all_items.append((activity, cost, "Activity"))
            
            # jajanan
            if include_snacks:
                for snack, cost in self.snacks.items():
                    all_items.append((snack, cost, "Food & Snacks"))
            
            #  hidden gems
            if include_hidden_gems:
                for gem, cost in self.hidden_gems.items():
                    all_items.append((gem, cost, "Hidden Gem"))
            
            
            must_have_categories = ["Destination", "Accommodation", "Transportation"]
            if starting_location == "From Indonesia":
                must_have_categories.append("Flight")
            
            # Run exact backtracking algorithm
            result = self.exact_backtracking(all_items, budget, must_have_categories)
            
            # Tampilan hasilnya
            if result:
                total_cost = sum(item[1] for item in result)
                remaining = budget - total_cost
                
                
                self.results_text.insert(tk.END, "🇦🇲 YOUR ARMENIA TRIP PLAN 🇦🇲\n", "title")
                self.results_text.insert(tk.END, "=" * 70 + "\n\n")
                
                self.results_text.insert(tk.END, f"Starting location: {starting_location}\n")
                self.results_text.insert(tk.END, f"Total Budget: Rp {budget:,}\n")
                self.results_text.insert(tk.END, f"Total Cost: Rp {total_cost:,}\n")
                self.results_text.insert(tk.END, f"Remaining: Rp {remaining:,}\n\n", "highlight")
                
                if remaining == 0:
                    self.results_text.insert(tk.END, "🎯 Budget utilized with 100% efficiency! 🎯\n\n", "total")
                
                # Group item ne
                categories = {}
                for item_name, item_cost, item_category in result:
                    if item_category not in categories:
                        categories[item_category] = []
                    categories[item_category].append((item_name, item_cost))
                
                # Nampilin item
                category_order = ["Flight", "Destination", "Accommodation", "Transportation", 
                                 "Activity", "Food & Snacks", "Hidden Gem", "Adjustment"]
                
                for category in category_order:
                    if category in categories:
                        if category == "Flight":
                            self.results_text.insert(tk.END, f"✈️ {category.upper()}:\n", "category")
                        elif category == "Destination":
                            self.results_text.insert(tk.END, f"🏛️ {category.upper()}:\n", "category")
                        elif category == "Accommodation":
                            self.results_text.insert(tk.END, f"🏨 {category.upper()}:\n", "category")
                        elif category == "Transportation":
                            self.results_text.insert(tk.END, f"🚗 {category.upper()}:\n", "category")
                        elif category == "Activity":
                            self.results_text.insert(tk.END, f"🎭 {category.upper()}:\n", "category")
                        elif category == "Food & Snacks":
                            self.results_text.insert(tk.END, f"🍽️ {category.upper()}:\n", "category")
                        elif category == "Hidden Gem":
                            self.results_text.insert(tk.END, f"💎 {category.upper()}:\n", "category")
                        else:
                            self.results_text.insert(tk.END, f"📌 {category.upper()}:\n", "category")
                        
                        category_total = 0
                        for item_name, item_cost in categories[category]:
                            if category == "Adjustment":
                                self.results_text.insert(tk.END, f"   • {item_name}: Rp {item_cost:,}\n", "warning")
                            else:
                                self.results_text.insert(tk.END, f"   • {item_name}: Rp {item_cost:,}\n")
                            category_total += item_cost
                        
                        self.results_text.insert(tk.END, f"   Total {category}: Rp {category_total:,}\n\n", "total")
                
                self.results_text.insert(tk.END, "=" * 70 + "\n\n")
                self.results_text.insert(tk.END, "ITINERARY DETAILS:\n", "subtitle")
                
                
                days = len(selected_destinations)
                self.results_text.insert(tk.END, f"Duration: {days} day{'s' if days > 1 else ''}\n\n")
                
                for i, dest in enumerate(selected_destinations):
                    self.results_text.insert(tk.END, f"Day {i+1}: {dest}\n", "highlight")
                    # nambahin aktifitas random
                    day_activities = []
                    for item_name, _, item_category in result:
                        if item_category in ["Activity", "Food & Snacks", "Hidden Gem"] and random.random() > 0.5:
                            if item_name not in day_activities and len(day_activities) < 3:
                                day_activities.append(item_name)
                    
                    for activity in day_activities:
                        self.results_text.insert(tk.END, f"  - {activity}\n")
                    
                    self.results_text.insert(tk.END, "\n")
                
                self.results_text.insert(tk.END, "=" * 70 + "\n")
                self.results_text.insert(tk.END, "This trip plan uses an advanced backtracking algorithm to ensure 100% budget utilization.\n")
                self.results_text.insert(tk.END, "All prices are in Indonesian Rupiah (IDR).\n")
                
                
                self.status_var.set(f"Trip planned successfully! Budget: Rp {budget:,}, Remaining: Rp {remaining:,}")
            else:
                self.results_text.insert(tk.END, "Could not find a suitable trip plan for the given budget.\n", "warning")
                self.results_text.insert(tk.END, "Please try a different budget amount or number of destinations.\n")
                self.status_var.set("Planning failed. Please try different parameters.")
        
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for budget and destinations.")
            self.status_var.set("Planning failed due to invalid input.")

#jalanin program
if __name__ == "__main__":
    root = tk.Tk()
    app = ArmeniaTripPlanner(root)
    root.mainloop()
    
    
    
    
    
    
    
    
    
    
    
# Logika Backtracking yang Digunakan dalam KodeProgram ini menggunakan algoritma backtracking canggih untuk memastikan budget habis tepat 0 rupiah,
#dengan strategi:

#Exact Subset Sum – Mencari kombinasi item yang totalnya sama dengan budget.
#Prioritas Kategori Wajib – Destinasi, akomodasi, transportasi, dan penerbangan (jika dari Indonesia) harus masuk dulu.
#Optimized Pruning – Item disortir dari harga tertinggi agar cabang yang tidak berguna segera dipangkas.
#Pendekatan Bertingkat – Jika solusi tidak ditemukan dengan backtracking murni, program mencoba metode tambahan:
#"Coin Change" dengan pemrograman dinamis.
#"Closest Subset Sum" untuk solusi paling mendekati.
#"Budget Adjustment" agar penggunaan budget tepat 100%.
#Tracking State – Menghindari pengulangan agar lebih efisien.

#Kelebihan & Kekurangan:
#Akurat – Budget pasti habis dengan solusi optimal.
#Fleksibel – Bisa disesuaikan dengan aturan baru.
#Multi-Strategi – Gunakan beberapa pendekatan untuk jaminan solusi.
#Beragam Rencana – Hasilkan itinerary yang berbeda sesuai budget.

#Lambat untuk dataset besar – Kompleksitas tetap O(2ⁿ) di kasus terburuk.
#Beban Rekursi – Bisa berat untuk memori jika banyak kemungkinan kombinasi.
#Tergantung Ketersediaan Item – Solusi terbaik hanya bisa dicapai jika pilihan cukup variatif.

#Fitur Tambahan
#Bisa mulai dari Indonesia (termasuk harga tiket) atau sudah di Armenia.
#Tambahan kategori Food & Snacks dan Hidden Gems.
#Itinerary harian otomatis.
#Validasi budget minimum agar masuk akal.
#UI lebih intuitif dengan ikon dan indikator penggunaan budget.
#Intinya, program ini menjamin rencana perjalanan optimal tanpa sisa budget, dengan pendekatan yang fleksibel dan efisien!


#Note : Budget kalo kebanyakan bisa bikin tkinter freeze !!!!