import os
import matplotlib.pyplot as plt
from collections import defaultdict
from game.auto_game import auto_game


class Simulation:
    @staticmethod
    def generate_uniform_data_winnability(num_records):
        folder = "winnability-result"
        os.makedirs(folder, exist_ok=True)  # Ensure the output folder exists
        winnability_data = defaultdict(list)  # {q: [wins]}

        for bot in (1, 2, 3, 4):
            file_path = os.path.join(folder, f"bot{bot}.txt")
            with open(file_path, "a+") as f:
                for q in range(0, 10, 1):
                    _q = q / 10  # Convert q to decimal (0.0 to 0.9)

                    wins = 0
                    for _ in range(num_records):  # Run multiple trials per q
                        game = auto_game(_q, bot, isUseIpCells=True, isUsePresetPos=True)
                        result = game.isFireExtinguished  # Boolean

                        if result:
                            wins += 1

                        f.write(f"{_q}, {result}, Bot{bot}\n")
                        winnability_data[_q].append(result)

        return winnability_data

    @staticmethod
    def getStoredData():
        """Reads previously stored winnability data from files."""
        folder = "winnability-result"
        winnability_data = defaultdict(list)  # {q: [wins]}

        if not os.path.exists(folder):
            print("No stored data found.")
            return winnability_data

        for bot in (1, 2, 3, 4):
            file_path = os.path.join(folder, f"bot{bot}.txt")

            if not os.path.exists(file_path):
                continue  # Skip missing files

            with open(file_path, "r") as f:
                for line in f:
                    q, win, _ = line.strip().split(", ")
                    q = float(q)
                    win = win == "True"  # Convert string to Boolean
                    winnability_data[q].append(win)

        return winnability_data

    @staticmethod
    def compute_winnability(data):
        """Computes the winnability percentage for each q."""
        q_values = sorted(data.keys())
        winnability = {q: sum(data[q]) / len(data[q]) for q in q_values}  # % of wins
        return q_values, [winnability[q] for q in q_values]

    @staticmethod
    def plot_winnability(winnability_data):
        """Plots winnability as a function of q."""
        q_values, winnability = Simulation.compute_winnability(winnability_data)

        plt.figure(figsize=(10, 5))
        plt.plot(q_values, winnability, marker="o", linestyle="-", label="Winnability")

        plt.xlabel("Fire Spread Probability (q)")
        plt.ylabel("Winnability (%)")
        plt.title("Effect of Fire Spread Rate on Winnability")
        plt.legend()
        plt.grid()
        plt.show()
