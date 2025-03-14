import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import random
from datetime import datetime, timedelta
import copy
import threading

# Fungsi untuk menghasilkan data pengujian
def generate_test_data(num_people, num_rooms, days):
    """Menghasilkan data acak untuk orang, ruangan, dan ketersediaan"""
    people = []
    rooms = []
    
    # Buat daftar orang
    for i in range(1, num_people + 1):
        person = {
            "id": i,
            "name": f"Orang_{i}",
            # Setiap orang memiliki ketersediaan waktu acak di setiap hari
            "availability": {
                day: [random.choice([True, False]) for _ in range(9, 17)]  # 9 AM - 4 PM
                for day in days
            }
        }
        people.append(person)
    
    # Buat daftar ruangan
    for i in range(1, num_rooms + 1):
        room = {
            "id": i,
            "name": f"Ruangan_{i}",
            "capacity": random.randint(5, 20),
            # Setiap ruangan memiliki ketersediaan waktu acak di setiap hari
            "availability": {
                day: [random.choice([True, False]) for _ in range(9, 17)]  # 9 AM - 4 PM
                for day in days
            }
        }
        rooms.append(room)
    
    # Buat daftar pertemuan yang perlu dijadwalkan
    meetings = []
    for i in range(1, num_people // 2):  # Jumlah pertemuan sekitar setengah jumlah orang
        attendees = random.sample(range(1, num_people + 1), random.randint(3, min(10, num_people)))
        duration = random.choice([1, 2])  # Durasi 1 atau 2 jam
        
        meeting = {
            "id": i,
            "title": f"Pertemuan_{i}",
            "attendees": attendees,
            "duration": duration,
            "priority": random.randint(1, 5)  # 1 adalah prioritas tertinggi
        }
        meetings.append(meeting)
    
    return people, rooms, meetings

# Algoritma tidak efisien - O(n³)
def schedule_meetings_inefficient(people, rooms, meetings, days):
    """
    Algoritma tidak efisien untuk menjadwalkan pertemuan
    Kompleksitas Waktu: O(n³) di mana n adalah jumlah orang/ruangan/slot waktu
    """
    scheduled_meetings = []
    unscheduled_meetings = []
    
    # Urutkan pertemuan berdasarkan prioritas (prioritas rendah = angka rendah)
    sorted_meetings = sorted(meetings, key=lambda x: x["priority"])
    
    for meeting in sorted_meetings:
        scheduled = False
        meeting_attendees = meeting["attendees"]
        meeting_duration = meeting["duration"]
        
        # Coba tiap kombinasi hari, jam, dan ruangan (pendekatan brute force)
        for day in days:
            for hour in range(9, 17 - meeting_duration + 1):  # Mastiin pertemuan selesai sebelum jam 5 sore
                for room in rooms:
                    can_schedule = True
                    room_capacity = room["capacity"]
                    
                    # Periksa kapasitas ruangan
                    if len(meeting_attendees) > room_capacity:
                        continue
                    
                    # Periksa ketersediaan ruangan buat durasi penuh
                    for h in range(hour, hour + meeting_duration):
                        if h - 9 >= len(room["availability"][day]) or not room["availability"][day][h - 9]:
                            can_schedule = False
                            break
                    
                    if not can_schedule:
                        continue
                    
                    # Periksa ketersediaan semua peserta buat durasi penuh (cara ga efisien)
                    for person_id in meeting_attendees:
                        # Cari orang dari daftar (ga efisien - O(n) lookup)
                        person = None
                        for p in people:
                            if p["id"] == person_id:
                                person = p
                                break
                        
                        if not person:
                            can_schedule = False
                            break
                        
                        for h in range(hour, hour + meeting_duration):
                            if h - 9 >= len(person["availability"][day]) or not person["availability"][day][h - 9]:
                                can_schedule = False
                                break
                        
                        if not can_schedule:
                            break
                    
                    if can_schedule:
                        # Jadwalin pertemuan
                        scheduled_meeting = {
                            "meeting_id": meeting["id"],
                            "title": meeting["title"],
                            "day": day,
                            "start_time": hour,
                            "end_time": hour + meeting_duration,
                            "room": room["id"],
                            "attendees": meeting_attendees
                        }
                        scheduled_meetings.append(scheduled_meeting)
                        
                        # Perbarui ketersediaan ruangan
                        for h in range(hour, hour + meeting_duration):
                            room["availability"][day][h - 9] = False
                        
                        # Perbarui ketersediaan orang (cara ga efisien)
                        for person_id in meeting_attendees:
                            for p in people:
                                if p["id"] == person_id:
                                    for h in range(hour, hour + meeting_duration):
                                        p["availability"][day][h - 9] = False
                                    break
                        
                        scheduled = True
                        break
                
                if scheduled:
                    break
            
            if scheduled:
                break
        
        if not scheduled:
            unscheduled_meetings.append(meeting)
    
    return scheduled_meetings, unscheduled_meetings

# Algoritma efisien - O(n log n)
def schedule_meetings_efficient(people, rooms, meetings, days):
    """
    Algoritma efisien untuk menjadwalkan pertemuan
    Kompleksitas Waktu: O(n log n) menggunakan indeks dan pemilihan ruangan yang cerdas
    """
    scheduled_meetings = []
    unscheduled_meetings = []
    
    # Buat indeks akses cepat
    people_dict = {person["id"]: person for person in people}
    rooms_dict = {room["id"]: room for room in rooms}
    
    # Indeks slot waktu tersedia buat tiap orang
    person_availability = {}
    for person in people:
        person_availability[person["id"]] = {}
        for day in days:
            person_availability[person["id"]][day] = set()
            for hour_idx, available in enumerate(person["availability"][day]):
                if available:
                    person_availability[person["id"]][day].add(hour_idx + 9)
    
    # Indeks slot waktu tersedia tiap ruangan
    room_availability = {}
    for room in rooms:
        room_availability[room["id"]] = {}
        for day in days:
            room_availability[room["id"]][day] = set()
            for hour_idx, available in enumerate(room["availability"][day]):
                if available:
                    room_availability[room["id"]][day].add(hour_idx + 9)
    
    # Urutin ruangan berdasarkan kapasitas (pemilihan efisien)
    sorted_rooms = sorted(rooms, key=lambda x: x["capacity"])
    
    # Urutin pertemuan berdasarkan prioritas dan kesulitan penjadwalan (lebih banyak peserta = lebih sulit)
    sorted_meetings = sorted(meetings, key=lambda x: (x["priority"], -len(x["attendees"])))
    
    for meeting in sorted_meetings:
        scheduled = False
        meeting_attendees = meeting["attendees"]
        meeting_duration = meeting["duration"]
        
        # Cari ruangan yang memenuhi kapasitas (mulai dari yang terkecil)
        suitable_rooms = [room for room in sorted_rooms if room["capacity"] >= len(meeting_attendees)]
        
        for day in days:
            if scheduled:
                break
            
            # Temuin slot waktu yang tersedia untuk semua peserta
            common_slots = set(range(9, 17))
            
            for attendee_id in meeting_attendees:
                # Akses langsung pake indeks
                attendee_slots = person_availability[attendee_id][day]
                common_slots &= set(attendee_slots)
            
            # Cari slot berurutan dgn durasi yang cukup
            valid_start_times = []
            for start_time in range(9, 17 - meeting_duration + 1):
                if all(start_time + offset in common_slots for offset in range(meeting_duration)):
                    valid_start_times.append(start_time)
            
            for start_time in valid_start_times:
                if scheduled:
                    break
                
                for room in suitable_rooms:
                    room_id = room["id"]
                    room_slots = room_availability[room_id][day]
                    
                    # Periksa apakah ruangan tersedia buat durasi yang dibutuhkan
                    if all(start_time + offset in room_slots for offset in range(meeting_duration)):
                        # Jadwalin pertemuan
                        scheduled_meeting = {
                            "meeting_id": meeting["id"],
                            "title": meeting["title"],
                            "day": day,
                            "start_time": start_time,
                            "end_time": start_time + meeting_duration,
                            "room": room_id,
                            "attendees": meeting_attendees
                        }
                        scheduled_meetings.append(scheduled_meeting)
                        
                        # Perbarui ketersediaan ruangan
                        for offset in range(meeting_duration):
                            if start_time + offset in room_availability[room_id][day]:
                                room_availability[room_id][day].remove(start_time + offset)
                        
                        # Perbarui ketersediaan tiap orang
                        for attendee_id in meeting_attendees:
                            for offset in range(meeting_duration):
                                if start_time + offset in person_availability[attendee_id][day]:
                                    person_availability[attendee_id][day].remove(start_time + offset)
                        
                        scheduled = True
                        break
        
        if not scheduled:
            unscheduled_meetings.append(meeting)
    
    return scheduled_meetings, unscheduled_meetings

# Format jadwal yg ditampilin di GUI
def format_schedule(scheduled_meetings, algorithm_name, people_dict=None):
    """Menyiapkan jadwal pertemuan dalam format string untuk ditampilkan"""
    if not scheduled_meetings:
        return f"Tidak ada pertemuan yang berhasil dijadwalkan menggunakan {algorithm_name}."
    
    # Urutin berdasarkan hari dan waktu mulai
    sorted_meetings = sorted(scheduled_meetings, key=lambda x: (x["day"], x["start_time"]))
    
    result = f"JADWAL PERTEMUAN ({algorithm_name}):\n"
    result += "=" * (len(result) - 1) + "\n\n"
    
    current_day = None
    for meeting in sorted_meetings:
        # Tampilin hari baru
        if meeting["day"] != current_day:
            current_day = meeting["day"]
            result += f"\n{current_day}:\n"
        
        # Format waktu
        start_time = f"{meeting['start_time']}:00"
        end_time = f"{meeting['end_time']}:00"
        
        # Tampilin informasi pertemuan
        result += f"  {start_time} - {end_time}: {meeting['title']} (Ruangan {meeting['room']})\n"
        
        # Tampilin peserta jika people_dict tersedia
        if people_dict:
            attendees = [people_dict[attendee_id]["name"] for attendee_id in meeting["attendees"]]
            result += f"    Peserta: {', '.join(attendees)}\n"
    
    return result

# Kelas utama aplikasi GUI
class MeetingSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Penjadwalan Pertemuan")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Variabel data
        self.days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
        self.people = []
        self.rooms = []
        self.meetings = []
        self.scheduled_inefficient = []
        self.unscheduled_inefficient = []
        self.scheduled_efficient = []
        self.unscheduled_efficient = []
        self.inefficient_time = 0
        self.efficient_time = 0
        
        # Variabel ukuran dataset
        self.dataset_size = tk.StringVar(value="1")
        
        # komponen GUI
        self.create_widgets()
    
    def create_widgets(self):
        # Frame judul
        title_frame = tk.Frame(self.root, bg="#4a7abc", pady=10)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame, 
            text="SISTEM PENJADWALAN PERTEMUAN", 
            font=("Arial", 16, "bold"), 
            fg="white", 
            bg="#4a7abc"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame, 
            text="Perbandingan Algoritma O(n³) vs O(n log n)", 
            font=("Arial", 10), 
            fg="white", 
            bg="#4a7abc"
        )
        subtitle_label.pack()
        
        # Frame input
        input_frame = tk.Frame(self.root, bg="#f0f0f0", pady=15)
        input_frame.pack(fill=tk.X, padx=20)
        
        # Label ama opsi ukuran dataset
        size_label = tk.Label(
            input_frame, 
            text="Pilih ukuran dataset:", 
            font=("Arial", 10, "bold"), 
            bg="#f0f0f0"
        )
        size_label.grid(row=0, column=0, sticky="w", pady=5)
        
        sizes = [
            ("Kecil (50 orang, 10 ruangan)", "1"),
            ("Sedang (200 orang, 20 ruangan)", "2"),
            ("Besar (500 orang, 30 ruangan)", "3")
        ]
        
        size_frame = tk.Frame(input_frame, bg="#f0f0f0")
        size_frame.grid(row=1, column=0, sticky="w", padx=20)
        
        for i, (text, value) in enumerate(sizes):
            rb = tk.Radiobutton(
                size_frame, 
                text=text, 
                variable=self.dataset_size, 
                value=value, 
                bg="#f0f0f0"
            )
            rb.grid(row=0, column=i, padx=10)
        
        # Tombol mulai penjadwalan
        button_frame = tk.Frame(input_frame, bg="#f0f0f0", pady=10)
        button_frame.grid(row=2, column=0)
        
        schedule_button = tk.Button(
            button_frame, 
            text="Mulai Penjadwalan", 
            command=self.start_scheduling,
            bg="#4a7abc",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        )
        schedule_button.pack()
        
        # Notebook hasil
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Tab hasil perbandingan
        comparison_tab = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(comparison_tab, text="Perbandingan Kinerja")
        
        # Frame hasil waktu eksekusi
        self.performance_frame = tk.LabelFrame(
            comparison_tab, 
            text="Hasil Waktu Eksekusi", 
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        self.performance_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Frame hasil penjadwalan
        self.scheduling_result_frame = tk.LabelFrame(
            comparison_tab, 
            text="Hasil Penjadwalan", 
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        self.scheduling_result_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Tab jadwal algoritma efisien
        efficient_tab = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(efficient_tab, text="Jadwal O(n log n)")
        
        # Area teks nampilke jadwal efisien
        efficient_frame = tk.Frame(efficient_tab, bg="#f0f0f0")
        efficient_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.efficient_text = scrolledtext.ScrolledText(
            efficient_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=20,
            font=("Courier", 10)
        )
        self.efficient_text.pack(fill=tk.BOTH, expand=True)
        
        # Tab jadwal algoritma tidak efisien
        inefficient_tab = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(inefficient_tab, text="Jadwal O(n³)")
        
        # Area teks nampilin jadwal tidak efisien
        inefficient_frame = tk.Frame(inefficient_tab, bg="#f0f0f0")
        inefficient_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.inefficient_text = scrolledtext.ScrolledText(
            inefficient_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=20,
            font=("Courier", 10)
        )
        self.inefficient_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Siap. Pilih ukuran dataset dan klik 'Mulai Penjadwalan'")
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def clear_performance_frame(self):
        for widget in self.performance_frame.winfo_children():
            widget.destroy()
        
        for widget in self.scheduling_result_frame.winfo_children():
            widget.destroy()
    
    def update_performance_results(self):
        # Waktu eksekusi
        inefficient_time_label = tk.Label(
            self.performance_frame, 
            text=f"Algoritma Tidak Efisien: {self.inefficient_time:.4f} detik", 
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        inefficient_time_label.pack(anchor="w", pady=2)
        
        efficient_time_label = tk.Label(
            self.performance_frame, 
            text=f"Algoritma Efisien: {self.efficient_time:.4f} detik", 
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        efficient_time_label.pack(anchor="w", pady=2)
        
        speedup = self.inefficient_time / self.efficient_time if self.efficient_time > 0 else 0
        speedup_label = tk.Label(
            self.performance_frame, 
            text=f"Peningkatan Kecepatan: {speedup:.2f}x lebih cepat", 
            bg="#f0f0f0",
            font=("Arial", 10, "bold"),
            fg="#4a7abc"
        )
        speedup_label.pack(anchor="w", pady=2)
        
        # Hasil penjadwalan
        inefficient_result_label = tk.Label(
            self.scheduling_result_frame, 
            text="Algoritma Tidak Efisien:", 
            bg="#f0f0f0",
            font=("Arial", 10, "bold")
        )
        inefficient_result_label.pack(anchor="w", pady=2)
        
        inefficient_scheduled_label = tk.Label(
            self.scheduling_result_frame, 
            text=f"  Pertemuan terjadwal: {len(self.scheduled_inefficient)}", 
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        inefficient_scheduled_label.pack(anchor="w", pady=1)
        
        inefficient_unscheduled_label = tk.Label(
            self.scheduling_result_frame, 
            text=f"  Pertemuan tidak terjadwal: {len(self.unscheduled_inefficient)}", 
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        inefficient_unscheduled_label.pack(anchor="w", pady=1)
        
        efficient_result_label = tk.Label(
            self.scheduling_result_frame, 
            text="Algoritma Efisien:", 
            bg="#f0f0f0",
            font=("Arial", 10, "bold")
        )
        efficient_result_label.pack(anchor="w", pady=(10, 2))
        
        efficient_scheduled_label = tk.Label(
            self.scheduling_result_frame, 
            text=f"  Pertemuan terjadwal: {len(self.scheduled_efficient)}", 
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        efficient_scheduled_label.pack(anchor="w", pady=1)
        
        efficient_unscheduled_label = tk.Label(
            self.scheduling_result_frame, 
            text=f"  Pertemuan tidak terjadwal: {len(self.unscheduled_efficient)}", 
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        efficient_unscheduled_label.pack(anchor="w", pady=1)
    
    def update_schedule_display(self):
        # Buat dictionary person referensi cepat
        people_dict = {person["id"]: person for person in self.people}
        
        # Tampilin jadwal algoritma efisien
        self.efficient_text.delete(1.0, tk.END)
        efficient_schedule = format_schedule(self.scheduled_efficient, "Algoritma Efisien - O(n log n)", people_dict)
        self.efficient_text.insert(tk.END, efficient_schedule)
        
        # Tampilin jadwal algoritma tidak efisien
        self.inefficient_text.delete(1.0, tk.END)
        inefficient_schedule = format_schedule(self.scheduled_inefficient, "Algoritma Tidak Efisien - O(n³)", people_dict)
        self.inefficient_text.insert(tk.END, inefficient_schedule)
    
    def run_scheduling(self):
        self.update_status("Menghasilkan dataset...")
        
        # Hasilin dataset
        choice = self.dataset_size.get()
        sizes = {
            "1": {"people": 50, "rooms": 10, "name": "Kecil"},
            "2": {"people": 200, "rooms": 20, "name": "Sedang"},
            "3": {"people": 500, "rooms": 30, "name": "Besar"}
        }
        
        num_people = sizes[choice]['people']
        num_rooms = sizes[choice]['rooms']
        
        self.people, self.rooms, self.meetings = generate_test_data(num_people, num_rooms, self.days)
        
        self.update_status(f"Dataset dihasilkan dengan {num_people} orang, {num_rooms} ruangan, dan {len(self.meetings)} pertemuan")
        
        # Salin data jalanke kedua algoritma
        people_inefficient = copy.deepcopy(self.people)
        rooms_inefficient = copy.deepcopy(self.rooms)
        meetings_inefficient = copy.deepcopy(self.meetings)
        
        people_efficient = copy.deepcopy(self.people)
        rooms_efficient = copy.deepcopy(self.rooms)
        meetings_efficient = copy.deepcopy(self.meetings)
        
        # Jalankan algoritma ga efisien
        self.update_status("Menjalankan Algoritma Tidak Efisien (O(n³))...")
        start_time = time.time()
        self.scheduled_inefficient, self.unscheduled_inefficient = schedule_meetings_inefficient(
            people_inefficient, rooms_inefficient, meetings_inefficient, self.days
        )
        self.inefficient_time = time.time() - start_time
        
        # Jalanin algoritma efisien
        self.update_status("Menjalankan Algoritma Efisien (O(n log n))...")
        start_time = time.time()
        self.scheduled_efficient, self.unscheduled_efficient = schedule_meetings_efficient(
            people_efficient, rooms_efficient, meetings_efficient, self.days
        )
        self.efficient_time = time.time() - start_time
        
        # Perbarui GUI dgn hasil
        self.root.after(0, self.update_performance_results)
        self.root.after(0, self.update_schedule_display)
        self.update_status("Penjadwalan selesai!")
        
        # Pilih tab hasil
        self.notebook.select(0)  # Pilih tab perbandingan kinerja
    
    def start_scheduling(self):
        # Ngosongin hasil sebelumnya
        self.clear_performance_frame()
        self.efficient_text.delete(1.0, tk.END)
        self.inefficient_text.delete(1.0, tk.END)
        
        # Jalanin penjadwalan di thread kepisah buat cegah GUI hang
        threading.Thread(target=self.run_scheduling, daemon=True).start()

# Fungsi main
def main():
    root = tk.Tk()
    app = MeetingSchedulerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()