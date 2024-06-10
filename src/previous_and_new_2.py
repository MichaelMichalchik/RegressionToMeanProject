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
        self.previous_population = []  # Store the entire previous population

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
        self.previous_population = [Individual(ind.id, ind.intrinsic_value, ind.extrinsic_value) for ind in self.population]
        for individual in self.population:
            individual.extrinsic_value = np.random.normal(100, 10)
        self.update_phenotypes(self.population, self.weight_genetic)
        self.display_table()
        self.track_changes()
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

    def track_changes(self):
        if self.round > 1:
            # Previous round top and bottom 5 IDs
            previous_top_five_ids = [ind.id for ind in self.previous_population if ind.id in self.top_five_ids]
            previous_bottom_five_ids = [ind.id for ind in self.previous_population if ind.id in self.bottom_five_ids]

            # Current round top and bottom 5 IDs
            sorted_population = sorted(self.population, key=lambda x: x.phenotype, reverse=True)
            new_top_five_ids = [ind.id for ind in sorted_population[:5]]
            new_bottom_five_ids = [ind.id for ind in sorted_population[-5:]]

            # Calculate changes for previous top and bottom
            previous_top_five_changes = [(ind.id, round(ind.phenotype - [pind.phenotype for pind in self.previous_population if pind.id == ind.id][0], 2)) for ind in self.population if ind.id in self.top_five_ids]
            previous_bottom_five_changes = [(ind.id, round(ind.phenotype - [pind.phenotype for pind in self.previous_population if pind.id == ind.id][0], 2)) for ind in self.population if ind.id in self.bottom_five_ids]

            prev_top_changes_str = ", ".join([f"ID {id}: {change:+.2f}" for id, change in previous_top_five_changes])
            prev_bottom_changes_str = ", ".join([f"ID {id}: {change:+.2f}" for id, change in previous_bottom_five_changes])

            # Calculate changes for new top and bottom
            new_top_five_changes = [(ind.id, round(ind.phenotype - [pind.phenotype for pind in self.previous_population if pind.id == ind.id][0], 2)) for ind in self.population if ind.id in new_top_five_ids]
            new_bottom_five_changes = [(ind.id, round(ind.phenotype - [pind.phenotype for pind in self.previous_population if pind.id == ind.id][0], 2)) for ind in self.population if ind.id in new_bottom_five_ids]

            new_top_changes_str = ", ".join([f"ID {id}: {change:+.2f}" for id, change in new_top_five_changes])
            new_bottom_changes_str = ", ".join([f"ID {id}: {change:+.2f}" for id, change in new_bottom_five_changes])

            self.previous_top_changes_label.config(text=f"Change in Previous Top 5: {prev_top_changes_str}")
            self.previous_bottom_changes_label.config(text=f"Change in Previous Bottom 5: {prev_bottom_changes_str}")

            self.new_top_changes_label.config(text=f"Change in New Top 5: {new_top_changes_str}")
            self.new_bottom_changes_label.config(text=f"Change in New Bottom 5: {new_bottom_changes_str}")

            # Update for next round
            self.top_five_ids = new_top_five_ids
            self.bottom_five_ids = new_bottom_five_ids

    def update_statistics(self):
        phenotypes = [ind.phenotype for ind in self.population]
        previous_phenotypes = [ind.phenotype for ind in self.previous_population]
        mean = np.mean(phenotypes)
        std_dev = np.std(phenotypes)
        previous_mean = np.mean(previous_phenotypes)
        previous_std_dev = np.std(previous_phenotypes)
        self.statistics_label.config(text=f"Previous Mean: {previous_mean:.2f}, Std Dev: {previous_std_dev:.2f}\nNew Mean: {mean:.2f}, Std Dev: {std_dev:.2f}")

    def create_widgets(self):
        # Maximize window
        self.root.state('normal')
        self.root.attributes('-zoomed', True)

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create three frames for the three tables
        table_frame_1 = ttk.Frame(main_frame, padding="5")
        table_frame_1.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        table_frame_2 = ttk.Frame(main_frame, padding="5")
        table_frame_2.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        table_frame_3 = ttk.Frame(main_frame, padding="5")
        table_frame_3.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Slider for genetic weight
        self.slider = ttk.Scale(main_frame, from_=0, to=100, orient='horizontal', command=self.slider_changed)
        self.slider.set(self.weight_genetic)
        self.slider.grid(row=1, column=0, columnspan=3, pady=10)

        # Button to reshuffle environment
        self.reshuffle_button = ttk.Button(main_frame, text="Reshuffle Environment", command=self.reshuffle_environment)
        self.reshuffle_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Table to display phenotypes
        columns = ("ID", "Phenotype")
        self.table = ttk.Treeview(table_frame_1, columns=columns, show='headings')
        self.table.heading("ID", text="ID")
        self.table.heading("Phenotype", text="Phenotype")
        self.table.grid(row=0, column=0, pady=10)

        for individual in self.population:
            self.table.insert('', 'end', values=(individual.id, f"{individual.phenotype:.2f}"))

        # New Top Five Table
        self.top_five_label = ttk.Label(table_frame_2, text="New Top Five")
        self.top_five_label.grid(row=0, column=0, pady=5)
        self.top_five_table = ttk.Treeview(table_frame_2, columns=columns, show='headings')
        self.top_five_table.heading("ID", text="ID")
        self.top_five_table.heading("Phenotype", text="Phenotype")
        self.top_five_table.grid(row=1, column=0, pady=10)
        for _ in range(5):
            self.top_five_table.insert('', 'end', values=("", ""))

        # New Bottom Five Table
        self.bottom_five_label = ttk.Label(table_frame_3, text="New Bottom Five")
        self.bottom_five_label.grid(row=0, column=0, pady=5)
        self.bottom_five_table = ttk.Treeview(table_frame_3, columns=columns, show='headings')
        self.bottom_five_table.heading("ID", text="ID")
        self.bottom_five_table.heading("Phenotype", text="Phenotype")
        self.bottom_five_table.grid(row=1, column=0, pady=10)
        for _ in range(5):
            self.bottom_five_table.insert('', 'end', values=("", ""))

        # Labels to display changes
        self.previous_top_changes_label = ttk.Label(main_frame, text="Change in Previous Top 5: ")
        self.previous_top_changes_label.grid(row=3, column=0, pady=5)

        self.previous_bottom_changes_label = ttk.Label(main_frame, text="Change in Previous Bottom 5: ")
        self.previous_bottom_changes_label.grid(row=4, column=0, pady=5)

        self.new_top_changes_label = ttk.Label(main_frame, text="Change in New Top 5: ")
        self.new_top_changes_label.grid(row=3, column=1, pady=5)

        self.new_bottom_changes_label = ttk.Label(main_frame, text="Change in New Bottom 5: ")
        self.new_bottom_changes_label.grid(row=4, column=1, pady=5)

        # Label to display statistics
        self.statistics_label = ttk.Label(main_frame, text="Previous Mean: , Std Dev: \nNew Mean: , Std Dev: ")
        self.statistics_label.grid(row=5, column=0, columnspan=3, pady=5)

    def slider_changed(self, event):
        self.weight_genetic = int(self.slider.get())
        self.update_phenotypes(self.population, self.weight_genetic)
        self.display_table()
        self.update_statistics()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()
