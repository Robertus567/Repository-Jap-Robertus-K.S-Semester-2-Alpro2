import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime, timedelta

class ArmeniaTripPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Armenia Trip Planner")
        self.root.geometry("950x750")
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
        
        # Destination properties - includes weather risk and seasonal factors
        self.destination_properties = {
            "Yerevan": {"weather_risk": "Low", "best_season": "Spring/Fall", "elevation": "Low", "crowd_level": "High"},
            "Lake Sevan": {"weather_risk": "Medium", "best_season": "Summer", "elevation": "High", "crowd_level": "Medium"},
            "Dilijan": {"weather_risk": "Medium", "best_season": "Summer/Fall", "elevation": "Medium", "crowd_level": "Low"},
            "Tatev Monastery": {"weather_risk": "High", "best_season": "Spring/Summer", "elevation": "High", "crowd_level": "Medium"},
            "Garni Temple": {"weather_risk": "Low", "best_season": "Any", "elevation": "Medium", "crowd_level": "Medium"},
            "Geghard Monastery": {"weather_risk": "Low", "best_season": "Any", "elevation": "Medium", "crowd_level": "Medium"},
            "Noravank Monastery": {"weather_risk": "Medium", "best_season": "Spring/Fall", "elevation": "Medium", "crowd_level": "Low"},
            "Khor Virap": {"weather_risk": "Low", "best_season": "Clear days", "elevation": "Low", "crowd_level": "Medium"},
            "Amberd Fortress": {"weather_risk": "High", "best_season": "Summer", "elevation": "High", "crowd_level": "Low"},
            "Gyumri": {"weather_risk": "Medium", "best_season": "Spring/Summer", "elevation": "Medium", "crowd_level": "Low"}
        }
        
        # Weather conditions by season
        self.weather_conditions = {
            "Winter": {
                "description": "Cold with snow, especially in highlands",
                "temperature": "-10°C to 5°C",
                "precipitation": "High",
                "notes": "Mountain roads may be closed"
            },
            "Spring": {
                "description": "Mild with rain showers",
                "temperature": "5°C to 20°C",
                "precipitation": "Medium",
                "notes": "Wildflowers bloom in late spring"
            },
            "Summer": {
                "description": "Hot and dry in lowlands, pleasant in highlands",
                "temperature": "20°C to 35°C",
                "precipitation": "Low",
                "notes": "Lake Sevan is best visited in summer"
            },
            "Fall": {
                "description": "Cool with changing colors",
                "temperature": "8°C to 22°C",
                "precipitation": "Low",
                "notes": "Great for hiking and photography"
            }
        }
        
        # Contingency plans for weather disruptions
        self.contingency_plans = {
            "Rain": ["Visit museums in Yerevan", "Indoor markets exploration", "Try local coffee shops"],
            "Snow": ["Book a spa day", "Traditional tavern experience", "Visit Matenadaran (manuscript museum)"],
            "Extreme Heat": ["Visit high-elevation sites", "Schedule activities for early morning", "Lake Sevan swimming"],
            "Fog": ["Reschedule monastery visits", "City walking tours", "Cultural performances"]
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
        
        # Contingency budget options
        self.contingency_options = {
            "Weather Contingency Fund": 200000,
            "Medical Emergency Fund": 500000,
            "Transport Disruption Fund": 150000,
            "Activity Cancellation Insurance": 100000,
            "Flexible Booking Option": 80000
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
        
        # Travel season
        season_label = tk.Label(input_frame, text="Travel Season:", font=("Arial", 12), bg="#f0f0f0")
        season_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.season_var = tk.StringVar(value="Summer")
        seasons = ["Winter", "Spring", "Summer", "Fall"]
        season_combobox = ttk.Combobox(input_frame, textvariable=self.season_var, values=seasons, 
                                      font=("Arial", 11), width=10, state="readonly")
        season_combobox.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        season_combobox.bind("<<ComboboxSelected>>", self.update_weather_info)
        
        # Weather info label
        self.weather_info = tk.StringVar()
        self.weather_info.set("Summer: Hot and dry in lowlands, pleasant in highlands")
        weather_label = tk.Label(input_frame, textvariable=self.weather_info, font=("Arial", 10), fg="blue", bg="#f0f0f0")
        weather_label.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W)
        
        # input budget
        budget_label = tk.Label(input_frame, text="Budget (Rupiah):", font=("Arial", 12), bg="#f0f0f0")
        budget_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.budget_entry = tk.Entry(input_frame, font=("Arial", 12), width=15)
        self.budget_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        self.budget_entry.insert(0, "15000000")  # Default 15 million rupiah
        
        self.min_budget_label = tk.Label(input_frame, text="Min budget: Rp 9,800,000 (includes flight)", 
                                         font=("Arial", 10), fg="red", bg="#f0f0f0")
        self.min_budget_label.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
        
        # jumlah destinasi
        destinations_label = tk.Label(input_frame, text="Destinations:", font=("Arial", 12), bg="#f0f0f0")
        destinations_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.destinations_spinbox = tk.Spinbox(input_frame, from_=1, to=5, font=("Arial", 12), width=5)
        self.destinations_spinbox.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        
        # Contingency planning
        contingency_label = tk.Label(input_frame, text="Contingency Planning:", font=("Arial", 12), bg="#f0f0f0")
        contingency_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.include_contingency = tk.BooleanVar(value=True)
        contingency_cb = tk.Checkbutton(input_frame, text="Include Weather Contingency Plan", 
                                       variable=self.include_contingency, font=("Arial", 11), bg="#f0f0f0")
        contingency_cb.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky=tk.W)
        
        # kategori
        categories_label = tk.Label(input_frame, text="Include Categories:", font=("Arial", 12), bg="#f0f0f0")
        categories_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        
        categories_frame = tk.Frame(input_frame, bg="#f0f0f0")
        categories_frame.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky=tk.W)
        
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
        button_frame.grid(row=6, column=0, columnspan=3, pady=15)
        
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
        
        # Text tags
        self.results_text.tag_config("title", font=("Arial", 14, "bold"))
        self.results_text.tag_config("subtitle", font=("Arial", 12, "bold"))
        self.results_text.tag_config("category", font=("Arial", 11, "bold"))
        self.results_text.tag_config("highlight", foreground="blue")
        self.results_text.tag_config("total", font=("Arial", 11, "bold"), foreground="green")
        self.results_text.tag_config("warning", foreground="red")
        self.results_text.tag_config("weather", foreground="purple")
        
        # Update weather info initially
        self.update_weather_info(None)
    
    def update_weather_info(self, event):
        season = self.season_var.get()
        weather = self.weather_conditions[season]
        self.weather_info.set(f"{season}: {weather['description']} ({weather['temperature']})")
    
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
        
        # Ensure each must-have category is represented
        for category in must_have_categories:
            category_items = [item for item in items if item[2] == category]
            if category_items:
                # Pick the cheapest item from this category
                cheapest = min(category_items, key=lambda x: x[1])
                result.append(cheapest)
                items.remove(cheapest)
        
        # Calculate remaining budget
        current_sum = sum(item[1] for item in result)
        remaining_budget = target_budget - current_sum
        
        # Try to find exact subset sum
        if self.find_exact_subset_sum(items, remaining_budget, 0, [], remaining_items):
            result.extend(remaining_items)
            return result
        
        # If exact subset sum fails, try coin change approach
        coin_change_result = self.coin_change_approach(items, remaining_budget)
        if coin_change_result:
            result.extend(coin_change_result)
            return result
        
        # If all else fails, find closest subset sum
        approximate_result = []
        self.find_closest_subset_sum(items, remaining_budget, 0, [], approximate_result, current_sum)
        
        # Add approximate result to our final result
        if approximate_result:
            result.extend(approximate_result)
            
            # Add adjustment item to make budget exact
            total_sum = sum(item[1] for item in result)
            difference = target_budget - total_sum
            
            # Only add non-zero adjustments
            if difference != 0:
                result.append(("Budget Adjustment", difference, "Adjustment"))
        
        return result
    
    def find_exact_subset_sum(self, items, target, index, current, result):
        # Base case: current sum equals target
        current_sum = sum(item[1] for item in current)
        if current_sum == target:
            result.extend(current)
            return True
        
        # Base case: exceed target or no more items
        if current_sum > target or index >= len(items):
            return False
        
        # Try including current item
        current.append(items[index])
        if self.find_exact_subset_sum(items, target, index + 1, current, result):
            return True
        current.pop()  # Backtrack
        
        # Try excluding current item
        return self.find_exact_subset_sum(items, target, index + 1, current, result)
    
    def find_closest_subset_sum(self, items, target, index, current, best_result, best_sum):
        current_sum = sum(item[1] for item in current)
        
        # Update best result if current is better
        if abs(target - current_sum) < abs(target - best_sum) and current_sum <= target:
            best_result.clear()
            best_result.extend(current)
            best_sum = current_sum
        
        # Base case: no more items
        if index >= len(items):
            return
        
        # Try including current item if it doesn't exceed target
        if current_sum + items[index][1] <= target:
            current.append(items[index])
            self.find_closest_subset_sum(items, target, index + 1, current, best_result, best_sum)
            current.pop()  # Backtrack
        
        # Try excluding current item
        self.find_closest_subset_sum(items, target, index + 1, current, best_result, best_sum)
    
    def coin_change_approach(self, items, target):
        """Use dynamic programming approach similar to coin change problem"""
        
        sorted_items = sorted(items, key=lambda x: x[1])
        
        # Group items by cost
        cost_groups = {}
        for item in sorted_items:
            cost = item[1]
            if cost not in cost_groups:
                cost_groups[cost] = []
            cost_groups[cost].append(item)
        
        # Get unique costs
        costs = sorted(cost_groups.keys())
        
        # Initialize dp table
        dp = [float('inf')] * (target + 1)
        dp[0] = 0
        choice = [[] for _ in range(target + 1)]
        
        # Fill dp table
        for cost in costs:
            for amount in range(cost, target + 1):
                if dp[amount - cost] + 1 < dp[amount]:
                    dp[amount] = dp[amount - cost] + 1
                    choice[amount] = choice[amount - cost] + [cost]
        
        # No solution found
        if dp[target] == float('inf'):
            return []
        
        # Reconstruct solution
        result = []
        for cost in choice[target]:
            item = cost_groups[cost].pop(0)
            result.append(item)
        
        return result
    
    def generate_random_weather_events(self, days, season):
        """Generate random weather events based on season"""
        events = []
        season_weather_prob = {
            "Winter": {"Snow": 0.4, "Clear": 0.3, "Rain": 0.2, "Fog": 0.1},
            "Spring": {"Rain": 0.4, "Clear": 0.4, "Fog": 0.1, "Snow": 0.1},
            "Summer": {"Clear": 0.7, "Rain": 0.2, "Extreme Heat": 0.1},
            "Fall": {"Clear": 0.5, "Rain": 0.3, "Fog": 0.2}
        }
        
        probs = season_weather_prob[season]
        weather_types = list(probs.keys())
        weather_weights = list(probs.values())
        
        for i in range(days):
            weather = random.choices(weather_types, weights=weather_weights)[0]
            events.append(weather)
        
        return events
    
    def plan_trip(self):
        try:
            # input
            budget = int(self.budget_entry.get())
            num_destinations = int(self.destinations_spinbox.get())
            starting_location = self.location_var.get()
            include_snacks = self.include_snacks.get()
            include_hidden_gems = self.include_hidden_gems.get()
            include_contingency = self.include_contingency.get()
            season = self.season_var.get()
            
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
            
            # Clear previous results
            self.results_text.delete(1.0, tk.END)
            
            # Update status
            self.status_var.set("Planning your trip to Armenia with EXACT budget utilization...")
            self.root.update_idletasks()
            
            # Initialize items list
            all_items = []
            
            # Start with flight if traveling from Indonesia
            flight_cost = 0
            if starting_location == "From Indonesia":
                # Choose a flight that costs at most 70% of the budget
                affordable_flights = {name: cost for name, cost in self.flights.items() if cost <= budget * 0.7}
                if affordable_flights:
                    flight_name = random.choice(list(affordable_flights.keys()))
                    flight_cost = self.flights[flight_name]
                    all_items.append((flight_name, flight_cost, "Flight"))
                else:
                    # If no affordable flight, choose the cheapest
                    flight_name = min(self.flights.items(), key=lambda x: x[1])[0]
                    flight_cost = self.flights[flight_name]
                    all_items.append((flight_name, flight_cost, "Flight"))
            
            # Add contingency funds if selected
            if include_contingency:
                contingency_name = "Weather Contingency Fund"
                contingency_cost = self.contingency_options[contingency_name]
                all_items.append((contingency_name, contingency_cost, "Contingency"))
            
            # Filter destinations based on season and weather risk
            suitable_destinations = {}
            for dest, cost in self.destinations.items():
                dest_props = self.destination_properties[dest]
                # Check if current season is in best season
                if season in dest_props["best_season"] or dest_props["best_season"] == "Any":
                    # If high weather risk in winter, exclude high-elevation destinations
                    if season == "Winter" and dest_props["weather_risk"] == "High" and dest_props["elevation"] == "High":
                        continue
                    suitable_destinations[dest] = cost
            
            if not suitable_destinations:
                suitable_destinations = self.destinations  # Fallback to all destinations if none are suitable
            
            # Add destinations (randomly select based on num_destinations)
            dest_keys = list(suitable_destinations.keys())
            random.shuffle(dest_keys)
            selected_destinations = dest_keys[:min(num_destinations, len(dest_keys))]
            
            for dest in selected_destinations:
                all_items.append((dest, self.destinations[dest], "Destination"))
            
            # Add accommodations and transportation
            for accom, cost in self.accommodations.items():
                all_items.append((accom, cost, "Accommodation"))
            
            for trans, cost in self.transportation.items():
                all_items.append((trans, cost, "Transportation"))
            
            # Add activities
            for activity, cost in self.activities.items():
                all_items.append((activity, cost, "Activity"))
            
            # Add snacks if selected
            if include_snacks:
                for snack, cost in self.snacks.items():
                    all_items.append((snack, cost, "Food & Snacks"))
            
            # Add hidden gems if selected
            if include_hidden_gems:
                for gem, cost in self.hidden_gems.items():
                    all_items.append((gem, cost, "Hidden Gem"))
            
            # Define must-have categories
            must_have_categories = ["Destination", "Accommodation", "Transportation"]
            if starting_location == "From Indonesia":
                must_have_categories.append("Flight")
            if include_contingency:
                must_have_categories.append("Contingency")
            
            # Run exact backtracking algorithm
            result = self.exact_backtracking(all_items, budget, must_have_categories)
            
            # Process and display results
            if result:
                total_cost = sum(item[1] for item in result)
                remaining = budget - total_cost
                
                # Display results
                self.results_text.insert(tk.END, "🇦🇲 YOUR ARMENIA TRIP PLAN 🇦🇲\n", "title")
                self.results_text.insert(tk.END, "=" * 70 + "\n\n")
                
                self.results_text.insert(tk.END, f"Starting location: {starting_location}\n")
                self.results_text.insert(tk.END, f"Travel season: {season}\n")
                self.results_text.insert(tk.END, f"Total Budget: Rp {budget:,}\n")
                self.results_text.insert(tk.END, f"Total Cost: Rp {total_cost:,}\n")
                self.results_text.insert(tk.END, f"Remaining: Rp {remaining:,}\n\n", "highlight")
                
                if remaining == 0:
                    self.results_text.insert(tk.END, "🎯 Budget utilized with 100% efficiency! 🎯\n\n", "total")
                
                # Weather information
                self.results_text.insert(tk.END, "⛅ WEATHER CONSIDERATIONS ⛅\n", "category")
                weather_info = self.weather_conditions[season]
                self.results_text.insert(tk.END, f"Season: {season}\n")
                self.results_text.insert(tk.END, f"Typical conditions: {weather_info['description']}\n")
                self.results_text.insert(tk.END, f"Temperature range: {weather_info['temperature']}\n")
                self.results_text.insert(tk.END, f"Precipitation: {weather_info['precipitation']}\n")
                self.results_text.insert(tk.END, f"Note: {weather_info['notes']}\n\n")
                
                # Group items by category
                categories = {}
                for item_name, item_cost, item_category in result:
                    if item_category not in categories:
                        categories[item_category] = []
                    categories[item_category].append((item_name, item_cost))
                
                # Display items by category
                category_order = ["Flight", "Destination", "Accommodation", "Transportation", 
                                 "Activity", "Food & Snacks", "Hidden Gem", "Contingency", "Adjustment"]
                
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
                        elif category == "Contingency":
                            self.results_text.insert(tk.END, f"🛡️ {category.upper()}:\n", "category")
                        elif category == "Adjustment":
                            self.results_text.insert(tk.END, f"⚖️ {category.upper()}:\n", "category")
                        
                        for item_name, item_cost in categories[category]:
                            self.results_text.insert(tk.END, f"• {item_name}: Rp {item_cost:,}\n")
                        
                        # Calculate subtotal for category
                        category_total = sum(item[1] for item in categories[category])
                        self.results_text.insert(tk.END, f"  Subtotal: Rp {category_total:,}\n\n")
                
                # Weather simulation
                self.results_text.insert(tk.END, "🌦️ WEATHER SIMULATION 🌦️\n", "category")
                
                # Determine trip duration based on destinations
                trip_days = max(len(selected_destinations) * 2, 5)  # At least 5 days
                
                # Generate simulated weather events
                weather_events = self.generate_random_weather_events(trip_days, season)
                
                # Create a simulated itinerary
                start_date = datetime.now() + timedelta(days=30)  # Assume travel in 30 days
                
                self.results_text.insert(tk.END, f"Simulated {trip_days}-day itinerary with possible weather conditions:\n\n")
                
                for day in range(trip_days):
                    current_date = start_date + timedelta(days=day)
                    weather = weather_events[day]
                    
                    self.results_text.insert(tk.END, f"Day {day+1} ({current_date.strftime('%d %b')}): ", "subtitle")
                    self.results_text.insert(tk.END, f"{weather} conditions\n", "weather")
                    
                    # If bad weather, suggest contingency plans
                    if weather != "Clear" and include_contingency:
                        self.results_text.insert(tk.END, "  Contingency options:\n")
                        contingency_activities = self.contingency_plans.get(weather, 
                                                                          self.contingency_plans["Rain"])
                        for activity in contingency_activities:
                            self.results_text.insert(tk.END, f"  • {activity}\n")
                    
                    self.results_text.insert(tk.END, "\n")
                
                # Recommendations
                self.results_text.insert(tk.END, "🔍 RECOMMENDATIONS 🔍\n", "category")
                
                # Destination specific recommendations
                for dest in selected_destinations:
                    dest_props = self.destination_properties[dest]
                    self.results_text.insert(tk.END, f"{dest}:\n", "subtitle")
                    self.results_text.insert(tk.END, f"• Weather risk: {dest_props['weather_risk']}\n")
                    self.results_text.insert(tk.END, f"• Best season: {dest_props['best_season']}\n")
                    self.results_text.insert(tk.END, f"• Elevation: {dest_props['elevation']}\n")
                    self.results_text.insert(tk.END, f"• Crowd level: {dest_props['crowd_level']}\n\n")
                
                # Season specific recommendations
                self.results_text.insert(tk.END, f"{season} travel tips:\n", "subtitle")
                if season == "Winter":
                    self.results_text.insert(tk.END, "• Pack warm clothes and waterproof boots\n")
                    self.results_text.insert(tk.END, "• Check road conditions before traveling to highlands\n")
                    self.results_text.insert(tk.END, "• Enjoy skiing at Tsaghkadzor resort\n")
                elif season == "Spring":
                    self.results_text.insert(tk.END, "• Bring layers for variable weather\n")
                    self.results_text.insert(tk.END, "• Visit Dilijan National Park for wildflowers\n")
                    self.results_text.insert(tk.END, "• Enjoy outdoor cafes in Yerevan\n")
                elif season == "Summer":
                    self.results_text.insert(tk.END, "• Bring sun protection and light clothing\n")
                    self.results_text.insert(tk.END, "• Enjoy swimming at Lake Sevan\n")
                    self.results_text.insert(tk.END, "• Start sightseeing early to avoid midday heat\n")
                elif season == "Fall":
                    self.results_text.insert(tk.END, "• Pack layers for changing temperatures\n")
                    self.results_text.insert(tk.END, "• Enjoy harvest festivals in wine regions\n")
                    self.results_text.insert(tk.END, "• Visit forests for autumn colors\n")
                
                self.results_text.insert(tk.END, "\n")
                
                # Algorithm explanation
                self.results_text.insert(tk.END, "🔢 ALGORITHM EXPLANATION 🔢\n", "category")
                self.results_text.insert(tk.END, "This trip was planned using a modified backtracking algorithm with the following steps:\n\n")
                self.results_text.insert(tk.END, "1. Must-have categories (flight, destination, accommodation, transportation) were prioritized\n")
                self.results_text.insert(tk.END, "2. Exact backtracking was used to find items that sum to exactly your budget\n")
                self.results_text.insert(tk.END, "3. If exact sum not possible, a dynamic programming approach similar to the coin change problem was applied\n")
                self.results_text.insert(tk.END, "4. In case of remaining budget, a budget adjustment was added\n")
                self.results_text.insert(tk.END, "5. Weather simulation was conducted based on seasonal probability distributions\n\n")
                
                # Final note
                self.results_text.insert(tk.END, "Thank you for using the Armenia Trip Planner! ".upper(), "title")
                self.results_text.insert(tk.END, "Enjoy your journey to the land of ancient monasteries and breathtaking landscapes!\n", "highlight")
                
                # Update status
                self.status_var.set("Trip plan complete! 100% budget efficiency achieved.")
            else:
                self.results_text.insert(tk.END, "Could not find a suitable trip plan with the given budget.\n", "warning")
                self.results_text.insert(tk.END, "Please try increasing your budget or reducing the number of destinations.\n")
                self.status_var.set("Trip planning failed. Please adjust your parameters.")
        
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numbers for budget and destinations.")
            self.status_var.set("Planning failed due to invalid input.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("An unexpected error occurred during planning.")
            
            
       
    
    # CARA KERJA ALGORITMA:
    # 1. Pertama, algoritma mengurutkan item berdasarkan biaya (menurun) untuk memprioritaskan item dengan biaya lebih tinggi
    # 2. Menyertakan satu item dari setiap kategori wajib (penerbangan, akomodasi, dll.)
    # 3. Kemudian menggunakan backtracking untuk mencari kombinasi item lainnya yang persis sesuai dengan anggaran
    # 4. Jika tidak mungkin menemukan kecocokan yang tepat, beralih ke pendekatan coin change atau closest subset
    
    # KELEBIHAN BACKTRACKING UNTUK MASALAH INI:
    # - Menjamin menemukan kecocokan anggaran yang tepat jika ada
    # - Dapat menangani batasan (kategori wajib) secara alami
    # - Solusi optimal (penggunaan anggaran paling efisien)
    # - Dapat dikombinasikan dengan pendekatan lain untuk kebutuhan yang berbeda
    # - Menyediakan pemahaman yang lebih baik tentang bagaimana anggaran dialokasikan
    
    # KEKURANGAN BACKTRACKING UNTUK MASALAH INI:
    # - Kompleksitas waktu eksponensial dalam kasus terburuk (2^n, dimana n adalah jumlah item)
    # - Dapat menjadi sangat lambat untuk dataset besar
    # - Tidak menjamin menemukan solusi jika tidak ada kombinasi yang tepat
    # - Membutuhkan pendekatan tambahan (seperti coin change) untuk menangani kasus di mana kecocokan tepat tidak ada
    # - Sensitif terhadap urutan item, yang dapat memengaruhi kinerja
            
            

if __name__ == "__main__":
    root = tk.Tk()
    app = ArmeniaTripPlanner(root)
    root.mainloop()
