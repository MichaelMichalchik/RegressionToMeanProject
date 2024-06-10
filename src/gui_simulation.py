import tkinter as tk
from tkinter import ttk
import numpy as np
from individual import Individual

class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Regression to the Mean Simulation")

        self.n = 100
        self.weight_genetic = 50
        self.round = 1

        # Generate initial population
        self.population = self.generate_population(self.n)
        self.previous_top_five = []
        self.previous_bottom_five = []
        self.top_five_ids = []
        self.bottom_five_ids = []

        # Create UI components
        self.create_widgets()

        # Display initial phenotypes
        self.update_phenotypes(self.population, self.weight_genetic)
        self.display_table()
        self.update_top_bottom_five()
        self.update_statistics()

    def generate_population(self, n):
        population = []
        for i in range(1, n + 1):
            intrinsic_value = np.random.normal(100, 10)
            extrinsic_value = np.random.normal(100, 10)
            population.append(Individual(i, intrinsic_value, extrinsic_value))
        return population

    def update_phenotypes(self, population, weight_genetic):
        for individual in population:
            individual.phenotype = individual.calculate_phenotype(weight_genetic)

    def reshuffle_environment(self):
        previous_population = [Individual(ind.id, ind.intrinsic_value, ind.extrinsic_value) for ind in self.population]
        for individual in self.population:
            individual.extrinsic_value = np.random.normal(100, 10)
        self.update_phenotypes(self.population, self.weight_genetic)
        self.display_table()
        self.track_changes(previous_population)
        self.update_top_bottom_five()
        self.update_statistics()
        self.round += 1

    def display_table(self):
        for i, individual in enumerate(self.population):
            self.table.item(self.table.get_children()[i], values=(individual.id, f"{individual.phenotype:.2f}"))

    def update_top_bottom_five(self):
        sorted_population = sorted(self.population, key=lambda x: x.phenotype, reverse=True)
        
        self.top_five_ids = [ind.id for ind in sorted_population[:5]]
        self.bottom_five_ids = [ind.id for ind in sorted_population[-5:]]

        self.previous_top_five = [ind for ind in self.population if ind.id in self.top_five_ids]
        self.previous_bottom_five = [ind for ind in self.population if ind.id in self.bottom_five_ids]

        self.update_top_bottom_tables()

    def update_top_bottom_tables(self):
        for i, individual in enumerate(self.previous_top_five):
            self.top_five_table.item(self.top_five_table.get_children()[i], values=(individual.id, f"{individual.phenotype:.2f}"))
        for i, individual in enumerate(self.previous_bottom_five):
            self.bottom_five_table.item(self.bottom_five_table.get_children()[i], values=(individual.id, f"{individual.phenotype:.2f}"))

    def track_changes(self, previous_population):
        if self.round > 1:
            previous_top_five_dict = {ind.id: ind.phenotype for ind in previous_population if ind.id in self.top_five_ids}
            previous_bottom_five_dict = {ind.id: ind.phenotype for ind in previous_population if ind.id in self.bottom_five_ids}

            top_five_changes = [(ind.id, round(ind.phenotype - previous_top_five_dict.get(ind.id, ind.phenotype), 2)) for ind in self.population if ind.id in self.top_five_ids]
            bottom_five_changes = [(ind.id, round(ind.phenotype - previous_bottom_five_dict.get(ind.id, ind.phenotype), 2)) for ind in self.population if ind.id in self.bottom_five_ids]

            new_top_five_changes = [(ind.id, round(ind.phenotype - previous_top_five_dict.get(ind.id, ind.phenotype), 2)) for ind in self.population if ind.id in self.top_five_ids]
            new_bottom_five_changes = [(ind.id, round(ind.phenotype - previous_bottom_five_dict.get(ind.id, ind.phenotype), 2)) for ind in self.population if ind.id in self.bottom_five_ids]

            prev_top_increases_str = ", ".join([f"ID {id}: {change:+.2f}" for id, change in top_five_changes])
            prev_bottom_decreases_str = ", ".join([f"ID {id}: {change:+.2f}" for id, change in bottom_five_changes])

            new_top_increases_str = ", ".join([f"ID {id}: {change:+.2f}" for id, change in new_top_five_changes])
            new_bottom_decreases_str = ", ".join([f"ID {id}: {change:+.2f}" for id, change in new_bottom_five_changes])

            self.top_increases_label.config(text=f"Previous Top 5 changes: {prev_top_increases_str}")
            self.top_decreases_label.config(text=f"Previous Bottom 5 changes: {prev_bottom_decreases_str}")

            self.new_top_increases_label.config(text=f"New Top 5 changes: {new_top_increases_str}")
            self.new_bottom_decreases_label.config(text=f"New Bottom 5 changes: {new_bottom_decreases_str}")

    def update_statistics(self):
        phenotypes = [ind.phenotype for ind in self.population]
        mean = np.mean(phenotypes)
        std_dev = np.std(phenotypes)
        self.statistics_label.config(text=f"Mean: {mean:.2f}, Std Dev: {std_dev:.2f}")

    def create_widgets(self):
        # Slider for genetic weight
        self.slider = ttk.Scale(self.root, from_=0, to=100, orient='horizontal', command=self.slider_changed)
        self.slider.set(self.weight_genetic)
        self.slider.pack(pady=10)

        # Button to reshuffle environment
        self.reshuffle_button = ttk.Button(self.root, text="Reshuffle Environment", command=self.reshuffle_environment)
        self.reshuffle_button.pack(pady=10)

        # Table to display phenotypes
        columns = ("ID", "Phenotype")
        self.table = ttk.Treeview(self.root, columns=columns, show='headings')
        self.table.heading("ID", text="ID")
        self.table.heading("Phenotype", text="Phenotype")
        self.table.pack(pady=10)

        for individual in self.population:
            self.table.insert('', 'end', values=(individual.id, f"{individual.phenotype:.2f}"))

        # New Top Five Table
        self.top_five_label = ttk.Label(self.root, text="New Top Five")
        self.top_five_label.pack(pady=5)
        self.top_five_table = ttk.Treeview(self.root, columns=columns, show='headings')
        self.top_five_table.heading("ID", text="ID")
        self.top_five_table.heading("Phenotype", text="Phenotype")
        self.top_five_table.pack(pady=10)
        for _ in range(5):
            self.top_five_table.insert('', 'end', values=("", ""))

        # New Bottom Five Table
        self.bottom_five_label = ttk.Label(self.root, text="New Bottom Five")
        self.bottom_five_label.pack(pady=5)
        self.bottom_five_table = ttk.Treeview(self.root, columns=columns, show='headings')
        self.bottom_five_table.heading("ID", text="ID")
        self.bottom_five_table.heading("Phenotype", text="Phenotype")
        self.bottom_five_table.pack(pady=10)
        for _ in range(5):
            self.bottom_five_table.insert('', 'end', values=("", ""))

        # Labels to display changes
        self.top_increases_label = ttk.Label(self.root, text="Previous Top 5 changes: ")
        self.top_increases_label.pack(pady=5)

        self.top_decreases_label = ttk.Label(self.root, text="Previous Bottom 5 changes: ")
        self.top_decreases_label.pack(pady=5)

        self.new_top_increases_label = ttk.Label(self.root, text="New Top 5 changes: ")
        self.new_top_increases_label.pack(pady=5)

        self.new_bottom_decreases_label = ttk.Label(self.root, text="New Bottom 5 changes: ")
        self.new_bottom_decreases_label.pack(pady=5)

        # Label to display statistics
        self.statistics_label = ttk.Label(self.root, text="Mean: , Std Dev: ")
        self.statistics_label.pack(pady=5)

    def slider_changed(self, event):
        self.weight_genetic = int(self.slider.get())
        self.update_phenotypes(self.population, self.weight_genetic)
        self.display_table()
        self.update_statistics()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()
