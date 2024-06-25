import tkinter as tk
from tkinter import ttk
import numpy as np
from individual import Individual

class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Regression to the Mean Simulation")

        self.n = 100
        self.weight_genetic = 0.5  # Start with 50% genetic weight
        self.round = 1

        # Generate initial population
        self.population = self.generate_population(self.n)
        self.previous_population = []  # Store the entire previous population

        # Store genetic components separately
        self.genetic_components = [ind.intrinsic_value for ind in self.population]

        # Create UI components
        self.create_widgets()

        # Display initial phenotypes
        self.update_phenotypes(self.population)
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

    def update_phenotypes(self, population):
        for individual in population:
            individual.phenotype = individual.calculate_phenotype(self.weight_genetic)

    def reshuffle_environment(self):
        self.previous_population = [Individual(ind.id, ind.intrinsic_value, ind.extrinsic_value) for ind in self.population]
        for i, individual in enumerate(self.population):
            individual.extrinsic_value = np.random.normal(100, 10)  # Only reshuffle the environmental component
            individual.intrinsic_value = self.genetic_components[i]  # Ensure genetic component remains unchanged
        self.update_phenotypes(self.population)
        self.display_table()
        self.track_changes()
        self.update_top_bottom_five()
        self.update_statistics()
        self.round += 1

    def display_table(self):
        for i, individual in enumerate(self.population):
            self.table.item(self.table.get_children()[i], values=(individual.id, f"{individual.phenotype:.2f}", f"{individual.genetic_score:.2f}", f"{individual.environmental_score:.2f}"))

    def update_top_bottom_five(self):
        sorted_population = sorted(self.population, key=lambda x: x.phenotype, reverse=True)
        
        self.top_five_ids = [ind.id for ind in sorted_population[:5]]
        self.bottom_five_ids = [ind.id for ind in sorted_population[-5:]]

        self.previous_top_five = [ind for ind in self.population if ind.id in self.top_five_ids]
        self.previous_bottom_five = [ind for ind in self.population if ind.id in self.bottom_five_ids]

        self.update_top_bottom_tables()

    def update_top_bottom_tables(self):
        for i, individual in enumerate(self.previous_top_five):
            values = (individual.id, f"{individual.phenotype:.2f}", f"{individual.genetic_score:.2f}", f"{individual.environmental_score:.2f}")
            if i < len(self.top_five_table.get_children()):
                self.top_five_table.item(self.top_five_table.get_children()[i], values=values)
            else:
                self.top_five_table.insert('', 'end', values=values)

        for i, individual in enumerate(self.previous_bottom_five):
            values = (individual.id, f"{individual.phenotype:.2f}", f"{individual.genetic_score:.2f}", f"{individual.environmental_score:.2f}")
            if i < len(self.bottom_five_table.get_children()):
                self.bottom_five_table.item(self.bottom_five_table.get_children()[i], values=values)
            else:
                self.bottom_five_table.insert('', 'end', values=values)

    def track_changes(self):
        if self.round > 1:
            # Calculate weighted phenotypes for current and previous populations
            current_phenotypes = {ind.id: ind.calculate_phenotype(self.weight_genetic) for ind in self.population}
            previous_phenotypes = {ind.id: ind.calculate_phenotype(self.weight_genetic) for ind in self.previous_population}

            # Previous round top and bottom 5 IDs
            previous_top_five_ids = [ind.id for ind in self.previous_population if ind.id in self.top_five_ids]
            previous_bottom_five_ids = [ind.id for ind in self.previous_population if ind.id in self.bottom_five_ids]

            # Current round top and bottom 5 IDs
            sorted_population = sorted(self.population, key=lambda x: x.calculate_phenotype(self.weight_genetic), reverse=True)
            new_top_five_ids = [ind.id for ind in sorted_population[:5]]
            new_bottom_five_ids = [ind.id for ind in sorted_population[-5:]]

            # Calculate changes for previous top and bottom
            previous_top_five_changes = [(id, round(current_phenotypes[id] - previous_phenotypes[id], 2)) for id in previous_top_five_ids]
            previous_bottom_five_changes = [(id, round(current_phenotypes[id] - previous_phenotypes[id], 2)) for id in previous_bottom_five_ids]

            prev_top_changes_str = ", ".join([f"ID {id}: {change:+.2f}" for id, change in previous_top_five_changes])
            prev_bottom_changes_str = ", ".join([f"ID {id}: {change:+.2f}" for id, change in previous_bottom_five_changes])

            # Calculate changes for new top and bottom
            new_top_five_changes = [(id, round(current_phenotypes[id] - previous_phenotypes[id], 2)) for id in new_top_five_ids]
            new_bottom_five_changes = [(id, round(current_phenotypes[id] - previous_phenotypes[id], 2)) for id in new_bottom_five_ids]

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
        previous_phenotypes = [ind.phenotype for ind in self.previous_population] if self.previous_population else phenotypes
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
        main_frame.columnconfigure(0, weight=2)  # Give more weight to the main table
        main_frame.columnconfigure(1, weight=1)  # Equal weight for top five
        main_frame.columnconfigure(2, weight=1)  # Equal weight for bottom five

        # Create three frames for the three tables
        table_frame_1 = ttk.Frame(main_frame, padding="5")
        table_frame_1.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 20))

        table_frame_2 = ttk.Frame(main_frame, padding="5")
        table_frame_2.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(20, 20))

        table_frame_3 = ttk.Frame(main_frame, padding="5")
        table_frame_3.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(20, 0))

        # Label to display genetic and environmental percentages
        self.gen_env_label = ttk.Label(main_frame, text=f"Genetic: {self.weight_genetic*100:.1f}%, Environmental: {(1-self.weight_genetic)*100:.1f}%")
        self.gen_env_label.grid(row=1, column=0, columnspan=3, pady=5)

        # Slider for genetic weight
        self.slider = ttk.Scale(main_frame, from_=0, to=100, orient='horizontal', command=self.slider_changed)
        self.slider.set(self.weight_genetic * 100)  # Start with 50% genetic weight
        self.slider.grid(row=2, column=0, columnspan=3, pady=10)

        # Button to reshuffle environment
        self.reshuffle_button = ttk.Button(main_frame, text="Reshuffle Environment", command=self.reshuffle_environment)
        self.reshuffle_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Table to display phenotypes
        columns = ("ID", "Phenotype", "Genetic", "Environmental")
        self.table = ttk.Treeview(table_frame_1, columns=columns, show='headings')
        self.table.heading("ID", text="ID")
        self.table.heading("Phenotype", text="Phenotype")
        self.table.heading("Genetic", text="Genetic")
        self.table.heading("Environmental", text="Environmental")
        self.table.grid(row=0, column=0, pady=10)

        # Adjust the size of the main table
        self.table.column("ID", width=50)
        self.table.column("Phenotype", width=100)
        self.table.column("Genetic", width=100)
        self.table.column("Environmental", width=100)

        for individual in self.population:
            self.table.insert('', 'end', values=(individual.id, f"{individual.phenotype:.2f}", f"{individual.genetic_score:.2f}", f"{individual.environmental_score:.2f}"))

        # New Top Five Table
        self.top_five_label = ttk.Label(table_frame_2, text="New Top Five")
        self.top_five_label.grid(row=0, column=0, pady=5)
        self.top_five_table = ttk.Treeview(table_frame_2, columns=columns, show='headings', height=5)
        for col in columns:
            self.top_five_table.heading(col, text=col)
            self.top_five_table.column(col, width=75)
        self.top_five_table.grid(row=1, column=0, pady=10)

        # New Bottom Five Table
        self.bottom_five_label = ttk.Label(table_frame_3, text="New Bottom Five")
        self.bottom_five_label.grid(row=0, column=0, pady=5)
        self.bottom_five_table = ttk.Treeview(table_frame_3, columns=columns, show='headings', height=5)
        for col in columns:
            self.bottom_five_table.heading(col, text=col)
            self.bottom_five_table.column(col, width=75)
        self.bottom_five_table.grid(row=1, column=0, pady=10)

        # Labels to display changes
        self.previous_top_changes_label = ttk.Label(main_frame, text="Change in Previous Top 5: ")
        self.previous_top_changes_label.grid(row=4, column=0, pady=5)

        self.previous_bottom_changes_label = ttk.Label(main_frame, text="Change in Previous Bottom 5: ")
        self.previous_bottom_changes_label.grid(row=5, column=0, pady=5)

        self.new_top_changes_label = ttk.Label(main_frame, text="Change in New Top 5: ")
        self.new_top_changes_label.grid(row=4, column=2, pady=5)  # Adjusted to column 2

        self.new_bottom_changes_label = ttk.Label(main_frame, text="Change in New Bottom 5: ")
        self.new_bottom_changes_label.grid(row=5, column=2, pady=5)  # Adjusted to column 2

        # Label to display statistics
        self.statistics_label = ttk.Label(main_frame, text="Previous Mean: , Std Dev: \nNew Mean: , Std Dev: ")
        self.statistics_label.grid(row=6, column=0, columnspan=3, pady=5)

    def slider_changed(self, event):
        self.weight_genetic = self.slider.get() / 100.0
        self.gen_env_label.config(text=f"Genetic: {self.weight_genetic*100:.1f}%, Environmental: {(1-self.weight_genetic)*100:.1f}%")
        self.update_phenotypes(self.population)
        self.display_table()
        self.update_statistics()
        self.update_top_bottom_five()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()