import os
import matplotlib.pyplot as plt
from collections import defaultdict
from game.auto_game import auto_game


class Simulation:
    @staticmethod
    def generate_uniform_data_winnability(num_records):
        """
        Generates data for all bots and tracks winnability.

        Args:
            num_records (int): Number of simulations to run for each q.

        Returns:
            dict: A dictionary mapping q to a list of tuples (bot, result).
        """
        folder = "winnability-result"
        os.makedirs(folder, exist_ok=True)
        winnability_data = defaultdict(list)

        for q in range(0, 10, 1):
            _q = q / 10
            for _ in range(num_records):
                # Track results for all bots in the same simulation
                results = {}
                for bot in (1, 2, 3, 4):
                    game = auto_game(_q, bot, isUseIpCells=True, isUsePresetPos=True)
                    results[bot] = game.isFireExtinguished

                # Determine if the simulation is winnable
                is_winnable = any(results.values())

                # Write results to files
                for bot, result in results.items():
                    file_path = os.path.join(folder, f"bot{bot}.txt")
                    with open(file_path, "a+") as f:
                        f.write(f"{_q}, {is_winnable}, Bot{bot}\n")

                # Store data for winnability analysis
                winnability_data[_q].append(is_winnable)

        return winnability_data

    @staticmethod
    def getStoredData():
        """Reads previously stored winnability data from files."""
        folder = "winnability-result"
        winnability_data = defaultdict(list)  # {q: [is_winnable]}

        if not os.path.exists(folder):
            print("No stored data found.")
            return winnability_data

        for bot in (1, 2, 3, 4):
            file_path = os.path.join(folder, f"bot{bot}.txt")

            if not os.path.exists(file_path):
                continue  # Skip missing files

            with open(file_path, "r") as f:
                for line in f:
                    q, is_winnable, bot_name = line.strip().split(", ")
                    q = float(q)
                    is_winnable = is_winnable == "True"
                    winnability_data[q].append(is_winnable)

        return winnability_data

    @staticmethod
    def compute_winnability_frequency(winnability_data):
        """
        Computes the frequency of winnable simulations as a function of q.

        Args:
            winnability_data (dict): A dictionary mapping q to a list of is_winnable values.

        Returns:
            dict: A dictionary mapping q to the frequency of winnable simulations.
        """
        winnability_frequency = {}
        for q, is_winnable_list in winnability_data.items():
            winnability_frequency[q] = sum(is_winnable_list) / len(is_winnable_list)
        return winnability_frequency

    @staticmethod
    def plot_winnability_frequency(winnability_frequency):
        """
        Plots the frequency of winnable simulations as a function of q.

        Args:
            winnability_frequency (dict): A dictionary mapping q to the frequency of winnable simulations.
        """
        q_values = sorted(winnability_frequency.keys())
        frequencies = [winnability_frequency[q] for q in q_values]

        plt.figure(figsize=(10, 5))
        plt.plot(q_values, frequencies, marker="o", linestyle="-", label="Winnability Frequency")

        plt.xlabel("Fire Spread Probability (q)")
        plt.ylabel("Frequency of Winnable Simulations")
        plt.title("Frequency of Winnable Simulations as a Function of q")
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
            list: A list of tuples (q, is_winnable, bot).
        """
        data = []
        fullPath = os.path.join(os.getcwd(), "winnability-result", file_path)
        with open(fullPath, "r") as file:
            for line in file:
                q, is_winnable, bot = line.strip().split(", ")
                data.append((float(q), is_winnable == "True", bot))
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
        for q, is_winnable, bot in all_data:
            if is_winnable:  # Only consider winnable simulations
                winnable_counts[q] += 1
                bot_success_rates[bot][q] += 1

        # Normalize by total winnable simulations for each q
        for bot in bot_success_rates:
            for q in bot_success_rates[bot]:
                bot_success_rates[bot][q] /= winnable_counts[q]

        # Debug: Print bot success rates
        print("Bot Success Rates:")
        for bot, success_rates in bot_success_rates.items():
            print(f"{bot}: {success_rates}")

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

        # Check if any data was plotted
        if plt.gca().has_data():
            plt.legend()
        else:
            print("Warning: No data to plot.")

        plt.xlabel("Fire Spread Probability (q)")
        plt.ylabel("Win Rate Among Winnable Simulations")
        plt.title("Bot Performance in Winnable Simulations")
        plt.grid()
        plt.show()