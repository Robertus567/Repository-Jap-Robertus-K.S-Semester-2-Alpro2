import tkinter as tk
from tkinter import ttk, scrolledtext
import random
from PIL import Image, ImageTk
import io

class Karakter:
    def __init__(self, nama):
        self.__nama = nama
        self.__hp = 100
        self.__hp_max = 100
        self.__mana = 50
        self.__mana_max = 50
        self.__attack = 10
        self.__defense = 5
    
    # Getter & Setter Methods (Enkapsulasi)
    def get_nama(self):
        return self.__nama
    
    def get_hp(self):
        return self.__hp
    
    def get_hp_max(self):
        return self.__hp_max
    
    def get_mana(self):
        return self.__mana
    
    def get_mana_max(self):
        return self.__mana_max
    
    def get_attack(self):
        return self.__attack
    
    def get_defense(self):
        return self.__defense
   
    
    # Setter dengan validasi
    def set_hp(self, nilai):
        if nilai < 0:
            self.__hp = 0
        elif nilai > self.__hp_max:
            self.__hp = self.__hp_max
        else:
            self.__hp = nilai
    
    def set_mana(self, nilai):
        if nilai < 0:
            self.__mana = 0
        elif nilai > self.__mana_max:
            self.__mana = self.__mana_max
        else:
            self.__mana = nilai
    
    def set_attack(self, nilai):
        if nilai > 0:
            self.__attack = nilai
    
    def set_defense(self, nilai):
        if nilai > 0:
            self.__defense = nilai
    
    def tampil_status(self):
        return f"""
{self.__nama}
HP: {self.__hp}/{self.__hp_max}
Mana: {self.__mana}/{self.__mana_max}
Attack: {self.__attack}
Defense: {self.__defense}
"""
    
    def serang(self, target):
        damage = max(1, self.__attack - target.get_defense() // 2)
        target.set_hp(target.get_hp() - damage)
        return f"{self.__nama} menyerang {target.get_nama()} dan memberikan {damage} damage!"

    def regenerasi(self):
        hp_regen = int(self.__hp_max * 0.1)
        mana_regen = int(self.__mana_max * 0.1)
        self.set_hp(self.__hp + hp_regen)
        self.set_mana(self.__mana + mana_regen)
        return f"{self.__nama} beristirahat dan memulihkan {hp_regen} HP dan {mana_regen} Mana."


class Warrior(Karakter):
    def __init__(self, nama):
        super().__init__(nama)
        # Tingkatkan atribut warrior - PERTAHANAN TINGGI
        self.set_hp(self.get_hp_max() + 50)  # Warrior punya HP lebih tinggi
        self.set_defense(self.get_defense() + 10)  # Warrior memiliki pertahanan tinggi
        self.__rage = 0  # Atribut khusus Warrior
    
    def get_rage(self):
        return self.__rage
    
    def set_rage(self, nilai):
        if nilai < 0:
            self.__rage = 0
        elif nilai > 100:
            self.__rage = 100
        else:
            self.__rage = nilai
    
    def tampil_status(self):
        status_dasar = super().tampil_status()
        return status_dasar + f"Rage: {self.__rage}/100\n"
    
    def serang(self, target):
        # Warrior memperoleh rage setiap menyerang
        self.set_rage(self.get_rage() + 10)
        damage = max(1, self.get_attack() - target.get_defense() // 2)
        target.set_hp(target.get_hp() - damage)
        return f"{self.get_nama()} menyerang {target.get_nama()} dengan pedang dan memberikan {damage} damage! Rage +10"
    
    def gunakan_skill(self, target):
        if self.get_rage() >= 50:
            self.set_rage(self.get_rage() - 50)
            # Warrior skills focus on high damage
            damage = self.get_attack() * 2
            target.set_hp(target.get_hp() - damage)
            return f"{self.get_nama()} menggunakan HEAVY SLASH dan memberikan {damage} damage! Rage -50"
        else:
            return f"{self.get_nama()} tidak memiliki cukup Rage untuk menggunakan skill!"
    
    # Tambahkan kemampuan defensif khusus Warrior
    def defensive_stance(self):
        bonus_defense = int(self.get_defense() * 0.5)
        self.set_defense(self.get_defense() + bonus_defense)
        return f"{self.get_nama()} menggunakan DEFENSIVE STANCE dan meningkatkan pertahanan sebesar {bonus_defense}!"


class Mage(Karakter):
    def __init__(self, nama):
        super().__init__(nama)
        # Tingkatkan atribut mage
        self.set_mana(self.get_mana_max() + 70)  # Mage punya Mana jauh lebih tinggi
        self.set_attack(self.get_attack() + 5)    # Serangan magic lebih tinggi
        self.__elemen = "Api"  # Atribut khusus Mage
        self.__spells = {
            "Api": {"damage": 1.8, "mana_cost": 30, "effect": "membakar"},
            "Air": {"damage": 1.5, "mana_cost": 25, "effect": "membekukan"},
            "Tanah": {"damage": 1.6, "mana_cost": 28, "effect": "menghancurkan"},
            "Angin": {"damage": 1.4, "mana_cost": 20, "effect": "menyayat"}
        }
    
    def get_elemen(self):
        return self.__elemen
    
    def set_elemen(self, elemen):
        elemen_tersedia = ["Api", "Air", "Tanah", "Angin"]
        if elemen in elemen_tersedia:
            self.__elemen = elemen
            return f"{self.get_nama()} berganti ke elemen {elemen}."
        else:
            return f"Elemen {elemen} tidak tersedia."
    
    def tampil_status(self):
        status_dasar = super().tampil_status()
        spell_info = self.__spells[self.__elemen]
        return status_dasar + f"Elemen: {self.__elemen} (Damage x{spell_info['damage']}, Mana cost: {spell_info['mana_cost']})\n"
    
    def serang(self, target):
        # Mage memiliki serangan dasar yang lemah
        damage = max(1, self.get_attack() // 2 - target.get_defense() // 4)
        target.set_hp(target.get_hp() - damage)
        return f"{self.get_nama()} menyerang {target.get_nama()} dengan tongkat dan memberikan {damage} damage!"
    
    def gunakan_skill(self, target):
        spell = self.__spells[self.__elemen]
        if self.get_mana() >= spell["mana_cost"]:
            self.set_mana(self.get_mana() - spell["mana_cost"])
            damage = int(self.get_attack() * spell["damage"])
            target.set_hp(target.get_hp() - damage)
            return f"{self.get_nama()} meluncurkan {self.__elemen} BALL dan {spell['effect']} {target.get_nama()}, memberikan {damage} damage! Mana -{spell['mana_cost']}"
        else:
            return f"{self.get_nama()} tidak memiliki cukup Mana untuk menggunakan spell!"
    
    # Tambahkan spell khusus untuk Mage
    def arcane_shield(self):
        mana_cost = 15
        if self.get_mana() >= mana_cost:
            self.set_mana(self.get_mana() - mana_cost)
            shield_amount = int(self.get_mana() * 0.5)
            self.set_hp(self.get_hp() + shield_amount)
            return f"{self.get_nama()} menciptakan ARCANE SHIELD dan memulihkan {shield_amount} HP! Mana -{mana_cost}"
        else:
            return f"{self.get_nama()} tidak memiliki cukup Mana untuk menciptakan perisai!"
    
    # Hanya Mage yang bisa menggunakan spell
    def use_special_spell(self, target):
        # Spell spesial yang hanya dimiliki Mage
        mana_cost = 40
        if self.get_mana() >= mana_cost:
            self.set_mana(self.get_mana() - mana_cost)
            damage = int(self.get_attack() * 2.5)
            target.set_hp(target.get_hp() - damage)
            return f"{self.get_nama()} melepaskan ARCANE BURST dan memberikan {damage} damage! Mana -{mana_cost}"
        else:
            return f"{self.get_nama()} tidak memiliki cukup Mana untuk menggunakan spell spesial!"


class Archer(Karakter):
    def __init__(self, nama):
        super().__init__(nama)
        # Tingkatkan atribut archer untuk serangan jarak jauh
        self.set_attack(self.get_attack() + 8)  # Archer memiliki serangan dasar tinggi
        self.__arrow_count = 20  # Atribut khusus Archer
        self.__arrow_types = ["Normal", "Api", "Es", "Racun"]
        self.__current_arrow = "Normal"
        self.__arrow_multipliers = {
            "Normal": 1.0,
            "Api": 1.3,
            "Es": 1.2,
            "Racun": 1.5
        }
    
    def get_arrow_count(self):
        return self.__arrow_count
    
    def set_arrow_count(self, nilai):
        if nilai < 0:
            self.__arrow_count = 0
        else:
            self.__arrow_count = nilai
    
    def get_arrow_type(self):
        return self.__current_arrow
    
    def set_arrow_type(self, arrow_type):
        if arrow_type in self.__arrow_types:
            self.__current_arrow = arrow_type
            return f"{self.get_nama()} mengganti jenis panah menjadi {arrow_type}."
        else:
            return f"Jenis panah {arrow_type} tidak tersedia."
    
    def tampil_status(self):
        status_dasar = super().tampil_status()
        arrow_info = f"Arrow: {self.__arrow_count}\n"
        arrow_info += f"Arrow Type: {self.__current_arrow} (Damage x{self.__arrow_multipliers[self.__current_arrow]})\n"
        return status_dasar + arrow_info
    
    def serang(self, target):
        if self.__arrow_count > 0:
            self.__arrow_count -= 1
            # Archer memiliki kemungkinan critical hit - menggambarkan keahlian jarak jauh
            critical = random.randint(1, 5) == 1  # 20% peluang critical (ditingkatkan dari 10%)
            base_damage = max(1, self.get_attack() - target.get_defense() // 3)
            
            # Apply arrow type multiplier
            damage = int(base_damage * self.__arrow_multipliers[self.__current_arrow])
            
            if critical:
                damage *= 2
                target.set_hp(target.get_hp() - damage)
                return f"{self.get_nama()} menembakkan panah {self.__current_arrow} CRITICAL pada {target.get_nama()} dari jarak jauh dan memberikan {damage} damage! Arrow -1"
            else:
                target.set_hp(target.get_hp() - damage)
                return f"{self.get_nama()} menembakkan panah {self.__current_arrow} pada {target.get_nama()} dari jarak jauh dan memberikan {damage} damage! Arrow -1"
        else:
            return f"{self.get_nama()} kehabisan panah!"
    
    def gunakan_skill(self, target):
        if self.__arrow_count >= 5 and self.get_mana() >= 20:
            self.__arrow_count -= 5
            self.set_mana(self.get_mana() - 20)
            
            # Tingkatkan damage untuk ARROW RAIN
            base_damage = self.get_attack() * 3
            damage = int(base_damage * self.__arrow_multipliers[self.__current_arrow])
            
            target.set_hp(target.get_hp() - damage)
            return f"{self.get_nama()} menggunakan {self.__current_arrow} ARROW RAIN dari jarak jauh dan memberikan {damage} damage! Arrow -5, Mana -20"
        elif self.__arrow_count < 5:
            return f"{self.get_nama()} tidak memiliki cukup panah untuk menggunakan skill!"
        else:
            return f"{self.get_nama()} tidak memiliki cukup Mana untuk menggunakan skill!"
    
    def crafting_arrow(self):
        self.__arrow_count += 10
        return f"{self.get_nama()} membuat 10 panah baru. Total panah: {self.__arrow_count}."
    
    # Tambahkan kemampuan untuk mengubah jenis panah
    def change_arrow_type(self):
        current_index = self.__arrow_types.index(self.__current_arrow)
        next_index = (current_index + 1) % len(self.__arrow_types)
        self.__current_arrow = self.__arrow_types[next_index]
        return f"{self.get_nama()} mengubah jenis panah menjadi {self.__current_arrow}."


# Class baru: Assassin dengan penekanan pada kritik dan serangan diam-diam
class Assassin(Karakter):
    def __init__(self, nama):
        super().__init__(nama)
        # Modifikasi atribut assassin
        self.set_attack(self.get_attack() + 12)  # Serangan sangat tinggi
        self.set_defense(self.get_defense() - 2)  # Tapi defense lebih rendah
        self.__stealth = 100  # Atribut khusus Assassin
        self.__stealth_max = 100
        self.__poison_level = 0  # Tingkat racun pada senjata
        self.__critical_chance = 25  # Persentase kesempatan critical hit (25%)
    
    # Enkapsulasi untuk atribut khusus Assassin
    def get_stealth(self):
        return self.__stealth
    
    def set_stealth(self, nilai):
        if nilai < 0:
            self.__stealth = 0
        elif nilai > self.__stealth_max:
            self.__stealth = self.__stealth_max
        else:
            self.__stealth = nilai
    
    def get_poison_level(self):
        return self.__poison_level
    
    def set_poison_level(self, nilai):
        if nilai < 0:
            self.__poison_level = 0
        elif nilai > 5:  # Maksimal level racun adalah 5
            self.__poison_level = 5
        else:
            self.__poison_level = nilai
    
    def get_critical_chance(self):
        return self.__critical_chance
    
    def tampil_status(self):
        status_dasar = super().tampil_status()
        return status_dasar + f"Stealth: {self.__stealth}/{self.__stealth_max}\nPoison Level: {self.__poison_level}/5\nCritical Chance: {self.__critical_chance}%\n"
    
    def serang(self, target):
        # Peluang critical hit tinggi dan memanfaatkan stealth
        stealth_bonus = 1.0
        if self.__stealth > 50:
            stealth_bonus = 1.5
            self.set_stealth(self.__stealth - 30)
        
        critical = random.randint(1, 100) <= self.__critical_chance
        base_damage = max(1, self.get_attack() - target.get_defense() // 3)
        damage = int(base_damage * stealth_bonus)
        
        if critical:
            damage *= 2.5  # Critical damage lebih tinggi
            target.set_hp(target.get_hp() - damage)
            result = f"{self.get_nama()} menusuk titik lemah {target.get_nama()} dan memberikan {damage} CRITICAL damage!"
        else:
            target.set_hp(target.get_hp() - damage)
            result = f"{self.get_nama()} menyerang {target.get_nama()} dengan belati dan memberikan {damage} damage!"
        
        # Tambahkan efek racun jika ada
        if self.__poison_level > 0:
            poison_damage = self.__poison_level * 3
            target.set_hp(target.get_hp() - poison_damage)
            result += f" Racun memberikan {poison_damage} damage tambahan!"
        
        return result
    
    def gunakan_skill(self, target):
        mana_cost = 25
        if self.get_mana() >= mana_cost:
            self.set_mana(self.get_mana() - mana_cost)
            
            # SHADOW STRIKE: serangan kuat yang meningkatkan peluang critical
            self.__critical_chance += 5
            damage = int(self.get_attack() * 2.2)
            target.set_hp(target.get_hp() - damage)
            
            return f"{self.get_nama()} menggunakan SHADOW STRIKE dan memberikan {damage} damage! Critical Chance +5%! Mana -{mana_cost}"
        else:
            return f"{self.get_nama()} tidak memiliki cukup Mana untuk menggunakan skill!"
    
    def apply_poison(self):
        # Meningkatkan level racun pada senjata
        if self.get_mana() >= 10:
            self.set_mana(self.get_mana() - 10)
            old_level = self.__poison_level
            self.set_poison_level(self.__poison_level + 1)
            return f"{self.get_nama()} melapisi senjata dengan racun mematikan. Level racun: {old_level} → {self.__poison_level}! Mana -10"
        else:
            return f"{self.get_nama()} tidak memiliki cukup Mana untuk meracuni senjata!"
    
    def vanish(self):
        # Kemampuan untuk menghilang dan meningkatkan stealth
        mana_cost = 15
        if self.get_mana() >= mana_cost:
            self.set_mana(self.get_mana() - mana_cost)
            stealth_gain = 50
            self.set_stealth(self.__stealth + stealth_gain)
            return f"{self.get_nama()} menghilang ke dalam bayangan dan memulihkan {stealth_gain} Stealth! Mana -{mana_cost}"
        else:
            return f"{self.get_nama()} tidak memiliki cukup Mana untuk menghilang!"


class RPGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Battle Arena RPG")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")  # Warna latar belakang dark blue slate
        
        # Buat karakter
        self.player = None
        self.enemy = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame pemilihan karakter
        self.character_frame = tk.Frame(self.root, bg="#2c3e50")
        self.character_frame.pack(pady=20)
        
        tk.Label(self.character_frame, text="Pilih Kelas Karaktermu:", font=("Arial", 14, "bold"), bg="#2c3e50", fg="#ecf0f1").pack()
        
        # Tambahkan deskripsi kelas
        warrior_desc = "Warrior: Pertahanan tinggi, HP besar, serangan fisik kuat"
        mage_desc = "Mage: Ahli spell dengan berbagai elemen, satu-satunya yang bisa menggunakan Special Spell"
        archer_desc = "Archer: Serangan jarak jauh dengan berbagai jenis panah, peluang critical tinggi"
        assassin_desc = "Assassin: Serangan sangat kuat, ahli racun, peluang critical tertinggi"
        
        self.class_var = tk.StringVar(value="Warrior")
        tk.Radiobutton(self.character_frame, text=warrior_desc, variable=self.class_var, value="Warrior", bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e", justify=tk.LEFT).pack(anchor=tk.W)
        tk.Radiobutton(self.character_frame, text=mage_desc, variable=self.class_var, value="Mage", bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e", justify=tk.LEFT).pack(anchor=tk.W)
        tk.Radiobutton(self.character_frame, text=archer_desc, variable=self.class_var, value="Archer", bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e", justify=tk.LEFT).pack(anchor=tk.W)
        tk.Radiobutton(self.character_frame, text=assassin_desc, variable=self.class_var, value="Assassin", bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e", justify=tk.LEFT).pack(anchor=tk.W)
        
        tk.Label(self.character_frame, text="Nama Karakter:", bg="#2c3e50", fg="#ecf0f1").pack(pady=(10, 0))
        self.name_entry = tk.Entry(self.character_frame, width=20, bg="#34495e", fg="#ecf0f1", insertbackground="#ecf0f1")
        self.name_entry.pack()
        self.name_entry.insert(0, "Petualang")
        
        tk.Button(self.character_frame, text="Buat Karakter", command=self.create_character, bg="#3498db", fg="#ecf0f1", activebackground="#2980b9").pack(pady=10)
        
        # Frame permainan (akan ditampilkan setelah karakter dibuat)
        self.game_frame = tk.Frame(self.root, bg="#2c3e50")
        
        # Area status karakter
        self.status_frame = tk.Frame(self.game_frame, bg="#2c3e50")
        self.status_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        # Area gambar karakter (placeholder)
        self.char_image_label = tk.Label(self.status_frame, bg="#2c3e50")
        self.char_image_label.pack(pady=10)
        
        # Status karakter
        self.player_status = scrolledtext.ScrolledText(self.status_frame, width=30, height=10, wrap=tk.WORD, bg="#34495e", fg="#ecf0f1")
        self.player_status.pack(pady=5)
        
        # Area musuh
        self.enemy_frame = tk.Frame(self.game_frame, bg="#2c3e50")
        self.enemy_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        
        # Label gambar musuh (placeholder)
        self.enemy_image_label = tk.Label(self.enemy_frame, bg="#2c3e50")
        self.enemy_image_label.pack(pady=10)
        
        # Status musuh
        self.enemy_status = scrolledtext.ScrolledText(self.enemy_frame, width=30, height=10, wrap=tk.WORD, bg="#34495e", fg="#ecf0f1")
        self.enemy_status.pack(pady=5)
        
        # Area log pertarungan
        self.battle_frame = tk.Frame(self.game_frame, bg="#2c3e50")
        self.battle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.battle_log = scrolledtext.ScrolledText(self.battle_frame, width=50, height=10, wrap=tk.WORD, bg="#34495e", fg="#ecf0f1")
        self.battle_log.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Frame tombol aksi
        self.action_frame = tk.Frame(self.game_frame, bg="#2c3e50")
        self.action_frame.pack(pady=10)
        
        self.attack_btn = tk.Button(self.action_frame, text="Serang", command=self.attack, bg="#e74c3c", fg="#ecf0f1", activebackground="#c0392b", width=10)
        self.attack_btn.grid(row=0, column=0, padx=5)
        
        self.skill_btn = tk.Button(self.action_frame, text="Skill", command=self.use_skill, bg="#27ae60", fg="#ecf0f1", activebackground="#2ecc71", width=10)
        self.skill_btn.grid(row=0, column=1, padx=5)
        
        self.special_btn = tk.Button(self.action_frame, text="Special", command=self.use_special, bg="#9b59b6", fg="#ecf0f1", activebackground="#8e44ad", width=10)
        self.special_btn.grid(row=0, column=2, padx=5)
        
        self.class_special_btn = tk.Button(self.action_frame, text="Class Power", command=self.use_class_special, bg="#f1c40f", fg="#34495e", activebackground="#f39c12", width=10)
        self.class_special_btn.grid(row=0, column=3, padx=5)
        
        self.rest_btn = tk.Button(self.action_frame, text="Istirahat", command=self.rest, bg="#f39c12", fg="#ecf0f1", activebackground="#d35400", width=10)
        self.rest_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.new_enemy_btn = tk.Button(self.action_frame, text="Lawan Baru", command=self.create_enemy, bg="#3498db", fg="#ecf0f1", activebackground="#2980b9", width=10)
        self.new_enemy_btn.grid(row=1, column=1, padx=5, pady=5)
        
        self.restart_btn = tk.Button(self.action_frame, text="Mulai Ulang", command=self.restart_game, bg="#95a5a6", fg="#ecf0f1", activebackground="#7f8c8d", width=10)
        self.restart_btn.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
    
    def create_character(self):
        name = self.name_entry.get() if self.name_entry.get() else "Petualang"
        class_choice = self.class_var.get()
        
        if class_choice == "Warrior":
            self.player = Warrior(name)
            self.player_image = self.create_avatar("Warrior", "player")
        elif class_choice == "Mage":
            self.player = Mage(name)
            self.player_image = self.create_avatar("Mage", "player")
        elif class_choice == "Archer":
            self.player = Archer(name)
            self.player_image = self.create_avatar("Archer", "player")
        else:
            self.player = Assassin(name)
            self.player_image = self.create_avatar("Assassin", "player")
        
        # Tambahkan stat bonus untuk karakter player
        self.player.set_attack(self.player.get_attack() + 5)
        self.player.set_defense(self.player.get_defense() + 3)
        
        # Tampilkan gambar karakter
        self.char_image_label.config(image=self.player_image)
        
        # Update status karakter
        self.update_player_status()
        
        # Sembunyikan frame pemilihan karakter
        self.character_frame.pack_forget()
        
        # Tampilkan frame permainan
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        
        # Buat musuh pertama
        self.create_enemy()
        
        # Log pesan selamat datang dan tips sesuai kelas
        self.log_message(f"Selamat datang {name}! Bersiaplah untuk pertarungan!")
        
        if isinstance(self.player, Warrior):
            self.log_message("Tip: Sebagai Warrior, gunakan Defensive Stance untuk meningkatkan pertahanan!")
        elif isinstance(self.player, Mage):
            self.log_message("Tip: Sebagai Mage, coba ganti elemen untuk menggunakan berbagai spell! Hanya Mage yang dapat menggunakan Special Spell.")
        elif isinstance(self.player, Archer):
            self.log_message("Tip: Sebagai Archer, coba ganti jenis panah untuk efek serangan berbeda!")
        else:
            self.log_message("Tip: Sebagai Assassin, gunakan Apply Poison untuk memberikan damage berkelanjutan dan Vanish untuk meningkatkan stealth!")
    
    def create_enemy(self):
        # Buat musuh acak
        enemy_classes = [Warrior, Mage, Archer, Assassin]
        enemy_names = ["Hera", "Aphrodite", "Freya", "Kali", "Artemis", "Gaia", "Athena", "Hestia", "Selene"]
        enemy_class = random.choice(enemy_classes)
        enemy_name = random.choice(enemy_names)
        
        self.enemy = enemy_class(enemy_name)
        
        # Sesuaikan level musuh dengan HP player
        enemy_level = max(1, self.player.get_hp() // 25)
        for _ in range(enemy_level):
            self.enemy.set_attack(self.enemy.get_attack() + random.randint(1, 3))
            self.enemy.set_defense(self.enemy.get_defense() + random.randint(0, 2))
        
        # Buat avatar musuh
        if isinstance(self.enemy, Warrior):
            self.enemy_image = self.create_avatar("Warrior", "enemy")
        elif isinstance(self.enemy, Mage):
            self.enemy_image = self.create_avatar("Mage", "enemy")
        elif isinstance(self.enemy, Archer):
            self.enemy_image = self.create_avatar("Archer", "enemy")
        else:
            self.enemy_image = self.create_avatar("Assassin", "enemy")
        
        # Set gambar musuh (pastikan ini terpanggil)
        self.enemy_image_label.config(image=self.enemy_image)
        
        # Update status musuh
        self.update_enemy_status()
        
        self.log_message(f"{enemy_name} level {enemy_level} muncul! Bersiaplah untuk bertarung!")
    
    
    def create_avatar(self, class_type, character_type):
        """
        Mengambil gambar dari URL untuk avatar
        class_type: jenis kelas (Warrior, Mage, Archer, Assassin)
        character_type: "player" atau "enemy"
        """
        # Dictionary URL gambar untuk berbagai karakter
        avatar_urls = {
            "player": {
                "Warrior": "https://i.pinimg.com/736x/08/21/26/082126c13c6e5feb56800b9ba0425225--warriors-game-pixel-characters.jpg",
                "Mage": "https://imgcdn.stablediffusionweb.com/2024/3/26/335e2680-a0cb-47ba-867b-967dd4a4d506.jpg",
                "Archer": "https://i.redd.it/pixel-art-archer-v0-6wzkaqoknwoc1.jpeg?s=7acc643d5438abb50e436bbf68e755c2725a793d",
                "Assassin": "https://66.media.tumblr.com/tumblr_mb7aulYPzi1rfjowdo1_540.gif"
            },
            "enemy": {
                "Warrior": "https://i.pinimg.com/originals/46/b7/2a/46b72a10de7ca06b7d6f9f90b374a0bc.png",
                "Mage": "https://i.pinimg.com/originals/cf/95/3d/cf953d4cb9ab133d08e7e4b3fd183a51.jpg",
                "Archer": "https://i.pinimg.com/originals/66/9d/0e/669d0ee4256c0a66720800719048355c.gif",
                "Assassin": "https://pics.craiyon.com/2023-12-01/RTFObzUkTKCzOmcf061AVQ.webp"
            }
        }
        
        # Gunakan URL gambar dari dictionary
        try:
            import urllib.request
            import ssl
            
            # Tambahkan context SSL untuk menghindari error SSL Certificate
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            url = avatar_urls[character_type][class_type]
            
            # Tambahkan User-Agent untuk mencegah blokir
            req = urllib.request.Request(
                url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            )
            
            # Gunakan ssl_context yang sudah dibuat
            with urllib.request.urlopen(req, context=ssl_context) as connection:
                raw_data = connection.read()
                
            image = Image.open(io.BytesIO(raw_data))
            image = image.resize((100, 100))  # Resize gambar ke 100x100 pixel
            
            # Tampilkan pesan sukses
            print(f"Berhasil memuat gambar {character_type} {class_type}")
            
            return ImageTk.PhotoImage(image)
            
        except Exception as e:
            # Jika ada error, gunakan avatar standar
            print(f"Gagal memuat gambar {character_type} {class_type}: {e}")
            
            # Buat karakter avatar sederhana sebagai fallback
            color_map = {
                "Warrior": "#e74c3c" if character_type == "player" else "#c0392b",
                "Mage": "#3498db" if character_type == "player" else "#2980b9",
                "Archer": "#2ecc71" if character_type == "player" else "#27ae60", 
                "Assassin": "#9b59b6" if character_type == "player" else "#8e44ad"
            }
            letter_map = {"Warrior": "W", "Mage": "M", "Archer": "A", "Assassin": "S"}
            
            img = Image.new('RGB', (100, 100), color_map[class_type])
            io_obj = io.BytesIO()
            img.save(io_obj, format='PNG')
            io_obj.seek(0)
            
            # Tambahkan label teks ke gambar fallback
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            # Posisikan teks di tengah
            letter = letter_map[class_type]
            # Gunakan font besar
            try:
                font = ImageFont.truetype("arial.ttf", 45)
            except:
                font = ImageFont.load_default()
            # Gambar teks di tengah
            w, h = draw.textsize(letter, font=font) if hasattr(draw, 'textsize') else (40, 40)
            draw.text(((100-w)/2, (100-h)/2), letter, fill="white", font=font)
            
            io_obj = io.BytesIO()
            img.save(io_obj, format='PNG')
            io_obj.seek(0)
            
            return ImageTk.PhotoImage(Image.open(io_obj))
    
    def update_player_status(self):
        self.player_status.delete(1.0, tk.END)
        self.player_status.insert(tk.END, self.player.tampil_status())
    
    def update_enemy_status(self):
        self.enemy_status.delete(1.0, tk.END)
        self.enemy_status.insert(tk.END, self.enemy.tampil_status())
    
    def log_message(self, message):
        self.battle_log.insert(tk.END, message + "\n\n")
        self.battle_log.see(tk.END)
    
    def check_enemy_defeat(self):
        if self.enemy.get_hp() <= 0:
            self.log_message(f"{self.enemy.get_nama()} dikalahkan!")
            
            # Pulihkan sedikit HP dan Mana player setelah menang
            hp_recover = int(self.player.get_hp_max() * 0.2)
            mana_recover = int(self.player.get_mana_max() * 0.3)
            
            self.player.set_hp(self.player.get_hp() + hp_recover)
            self.player.set_mana(self.player.get_mana() + mana_recover)
            
            self.log_message(f"{self.player.get_nama()} memulihkan {hp_recover} HP dan {mana_recover} Mana!")
            
            # Khusus untuk archer, pulihkan panah
            if isinstance(self.player, Archer):
                arrow_recover = 5
                self.player.set_arrow_count(self.player.get_arrow_count() + arrow_recover)
                self.log_message(f"{self.player.get_nama()} menemukan {arrow_recover} panah baru!")
            
            # Khusus untuk assassin, reset stealth
            if isinstance(self.player, Assassin):
                self.player.set_stealth(100)
                self.log_message(f"{self.player.get_nama()} kembali bersembunyi dalam bayangan!")
            
            self.update_player_status()
            return True
        return False
    
    def enemy_turn(self):
        # Musuh selalu memilih aksi terbaik berdasarkan kondisinya
        if self.enemy.get_hp() < self.enemy.get_hp_max() * 0.3:
            # Jika HP rendah, istirahat
            result = self.enemy.regenerasi()
        elif isinstance(self.enemy, Mage) and self.enemy.get_mana() >= 40 and random.random() < 0.7:
            # Mage memiliki kemungkinan menggunakan special spell jika memiliki cukup mana
            result = self.enemy.use_special_spell(self.player)
        elif self.enemy.get_mana() >= 25 and random.random() < 0.6:
            # Gunakan skill jika memiliki cukup mana dan peluang 60%
            result = self.enemy.gunakan_skill(self.player)
        elif isinstance(self.enemy, Assassin) and self.enemy.get_poison_level() < 3 and self.enemy.get_mana() >= 10 and random.random() < 0.4:
            # Assassin menggunakan racun jika levelnya rendah
            result = self.enemy.apply_poison()
        elif isinstance(self.enemy, Archer) and self.enemy.get_arrow_count() < 5:
            # Archer membuat panah baru jika kehabisan
            result = self.enemy.crafting_arrow()
        else:
            # Serangan biasa
            result = self.enemy.serang(self.player)
        
        self.log_message(result)
        self.update_player_status()
        self.update_enemy_status()
        
        # Periksa apakah player dikalahkan
        if self.player.get_hp() <= 0:
            self.log_message(f"{self.player.get_nama()} dikalahkan! Game Over!")
            self.disable_action_buttons()
    
    def attack(self):
        result = self.player.serang(self.enemy)
        self.log_message(result)
        
        self.update_player_status()
        self.update_enemy_status()
        
        if not self.check_enemy_defeat():
            # Jika musuh masih hidup, giliran musuh
            self.root.after(1000, self.enemy_turn)
    
    def use_skill(self):
        result = self.player.gunakan_skill(self.enemy)
        self.log_message(result)
        
        self.update_player_status()
        self.update_enemy_status()
        
        if not self.check_enemy_defeat():
            # Jika musuh masih hidup, giliran musuh
            self.root.after(1000, self.enemy_turn)
    
    def use_special(self):
        # Hanya Mage yang dapat menggunakan kemampuan special spell
        if isinstance(self.player, Mage):
            result = self.player.use_special_spell(self.enemy)
        else:
            result = f"{self.player.get_nama()} tidak dapat menggunakan special spell! Hanya Mage yang memiliki kemampuan ini."
        
        self.log_message(result)
        
        self.update_player_status()
        self.update_enemy_status()
        
        if not self.check_enemy_defeat() and isinstance(self.player, Mage):
            # Jika musuh masih hidup dan special berhasil digunakan, giliran musuh
            self.root.after(1000, self.enemy_turn)
    
    def use_class_special(self):
        # Tombol untuk kemampuan khusus kelas
        if isinstance(self.player, Warrior):
            result = self.player.defensive_stance()
        elif isinstance(self.player, Mage):
            result = self.player.arcane_shield()
        elif isinstance(self.player, Archer):
            result = self.player.change_arrow_type()
        else:  # Assassin
            result = self.player.vanish()
        
        self.log_message(result)
        self.update_player_status()
        
        # Giliran musuh setelah menggunakan kemampuan khusus
        self.root.after(1000, self.enemy_turn)
    
    def rest(self):
        result = self.player.regenerasi()
        self.log_message(result)
        
        self.update_player_status()
        
        # Giliran musuh setelah istirahat
        self.root.after(1000, self.enemy_turn)
    
    def disable_action_buttons(self):
        self.attack_btn.config(state=tk.DISABLED)
        self.skill_btn.config(state=tk.DISABLED)
        self.special_btn.config(state=tk.DISABLED)
        self.class_special_btn.config(state=tk.DISABLED)
        self.rest_btn.config(state=tk.DISABLED)
    
    def restart_game(self):
        # Reset game
        self.game_frame.pack_forget()
        self.character_frame.pack(pady=20)
        
        # Reset tombol
        self.attack_btn.config(state=tk.NORMAL)
        self.skill_btn.config(state=tk.NORMAL)
        self.special_btn.config(state=tk.NORMAL)
        self.class_special_btn.config(state=tk.NORMAL)
        self.rest_btn.config(state=tk.NORMAL)
        
        # Bersihkan log
        self.battle_log.delete(1.0, tk.END)


# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = RPGApp(root)
    root.mainloop()