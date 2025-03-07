import random
import matplotlib.pyplot as plt
import pandas as pd

from game.auto_game import auto_game


class Result:
    @staticmethod
    def write(filename: str, contents: str):
        file_path = f"result/{filename}.txt"  # Relative path from root/main.py

        # Writing to the file
        with open(file_path, "a+") as file:
            file.write(f"{contents}\n")

    @staticmethod
    def botWiseAnalysis(botType):
        file_path = f"result/bot{botType}.txt"  # File path

        # Read the file
        data = pd.read_csv(file_path, header=None, names=['q', 'win', 'bot_type'])

        # Debug: Print first few rows to check if data is loaded correctly
        print("Raw Data Preview:\n", data.head())

        # Convert 'win' column to boolean
        data["win"] = data["win"].astype(str).str.strip().str.lower() == "true"

        # Define q ranges
        ranges = {
            "0 - 0.3": (0.0, 0.3),
            "0.4 - 0.6": (0.4, 0.6),
            "0.7 - 1": (0.7, 1.0)
        }

        # Initialize counters
        win_counts = {label: 0 for label in ranges}
        total_records = {label: 0 for label in ranges}

        # Count wins and total records per range
        allRecords = list(data.iterrows())
        for _, row in allRecords:
            q, win = row['q'], row['win']
            for label, (low, high) in ranges.items():
                if low <= q <= high:
                    total_records[label] += 1  # Count all records in this range
                    if win:
                        win_counts[label] += 1  # Count only wins
                    break  # Found range, exit loop

        # Compute losses
        loss_counts = {label: total_records[label] - win_counts[label] for label in ranges}

        # Debug: Print computed counts
        print("Total Records:", total_records)
        print("Wins:", win_counts)
        print("Losses:", loss_counts)

        # X-axis labels and values
        labels = list(ranges.keys())
        wins = [win_counts[label] for label in labels]
        losses = [loss_counts[label] for label in labels]

        # Plot stacked bar chart
        plt.figure(figsize=(8, 6))
        plt.bar(labels, wins, color="green", label="Wins")
        plt.bar(labels, losses, bottom=wins, color="red", label="Losses")

        # Labels and title
        plt.xlabel("q Ranges", fontsize=12)
        plt.ylabel("Total Records", fontsize=12)
        plt.title(f"Win/Loss Analysis for Bot {botType}", fontsize=14)
        plt.ylim(0, len(allRecords) // len(ranges))
        plt.legend()

        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()

    @staticmethod
    def fillRecords(recordsPerBot):
        for qRange in ([0, 0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9, 1]):
            for bot in [4]:
                for i in range(recordsPerBot):
                    qXRange = random.choice(qRange)
                    g = auto_game(q=qXRange, bot_type=bot)
                    q, isFireExtinguished, bot_type = g.q, g.isFireExtinguished, g.bot_type
                    Result.write(f'bot{bot_type}', f'{q}, {isFireExtinguished}, {bot_type}')
                print(f"Finished q ranges from {qRange} for bot {bot}")