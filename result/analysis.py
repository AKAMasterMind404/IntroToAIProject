import matplotlib.pyplot as plt
import pandas as pd

class Result:
    @staticmethod
    def write(filename: str, contents: str):
        file_path = f"result/{filename}.txt"  # Relative path from root/main.py

        # Writing to the file
        with open(file_path, "a+") as file:
            file.write(f"{contents}\n")

    @staticmethod
    def analysis(botType):
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
        for _, row in data.iterrows():
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
        plt.ylim(0, 100)  # Set max y-axis to 100
        plt.legend()

        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()

    # Example call
    # analysis("bot1")

