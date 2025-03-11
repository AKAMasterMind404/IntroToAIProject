import os
import matplotlib.pyplot as plt
from collections import defaultdict
from game.auto_game import auto_game


class Simulation:
    @staticmethod
    def generate_uniform_data_winnability(num_records):
        folder = "winnability-result"
        os.makedirs(folder, exist_ok=True)
        winnability_data = defaultdict(list)

        for bot in (1, 2, 3, 4):
            file_path = os.path.join(folder, f"bot{bot}.txt")
            f = open(file_path, "a+")
            for q in range(0, 10, 1):
                _q = q / 10
                wins = 0
                for _ in range(num_records):
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

    @staticmethod
    def read_bot_data(file_path):
        """
        Reads bot data from a file.

        Args:
            file_path (str): Path to the bot data file.

        Returns:
            list: A list of tuples (q, winnable, bot).
        """
        data = []
        fullPath = os.path.join(os.getcwd(), "winnability-result", file_path)
        file = open(fullPath, "r")
        for line in file:
            q, winnable, bot = line.strip().split(", ")
            data.append((float(q), winnable == "True", bot))
        return data

    @staticmethod
    def compute_winnability_per_bot(bot_files):
        """
        Computes per-bot win frequency, considering only winnable simulations.

        Args:
            bot_files (list): List of file paths for bot data.

        Returns:
            dict: A dictionary mapping bot IDs to their success rates per q.
        """
        winnable_counts = defaultdict(int)  # {q: total winnable cases}
        bot_success_rates = defaultdict(lambda: defaultdict(float))  # {bot: {q: success rate}}

        # Read data from all files
        all_data = []
        for file_path in bot_files:
            all_data.extend(Simulation.read_bot_data(file_path))

        # Process data
        for q, winnable, bot in all_data:
            if winnable:  # Only consider winnable simulations
                winnable_counts[q] += 1
                bot_success_rates[bot][q] += 1

        # Normalize by total winnable simulations for each q
        for bot in bot_success_rates:
            for q in bot_success_rates[bot]:
                bot_success_rates[bot][q] /= winnable_counts[q]

        return bot_success_rates

    @staticmethod
    def plot_bot_success_rates(bot_success_rates):
        """
        Plots each bot's success rate in winnable simulations.

        Args:
            bot_success_rates (dict): A dictionary mapping bot IDs to their success rates per q.
        """
        plt.figure(figsize=(10, 5))

        for bot, success_rates in bot_success_rates.items():
            q_values = sorted(success_rates.keys())
            rates = [success_rates[q] for q in q_values]

            if rates:  # Only plot if data exists
                plt.plot(q_values, rates, marker="o", linestyle="-", label=f"{bot}")

        plt.xlabel("Fire Spread Probability (q)")
        plt.ylabel("Win Rate Among Winnable Simulations")
        plt.title("Bot Performance in Winnable Simulations")
        plt.legend()
        plt.grid()
        plt.show()
