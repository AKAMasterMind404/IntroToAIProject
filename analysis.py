import os
import random
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
from constants import IS_VARIABLE_GRAPH
from game.auto_game import auto_game
from graph.sample.sample1 import currently_open_1


class Result:
    @staticmethod
    def write(filename: str, contents: str):
        folderName = 'variable-graph-result' if IS_VARIABLE_GRAPH else 'same-graph-result'
        file_path = f"{os.getcwd()}/{folderName}/{filename}.txt"  # Relative path from root/main.py

        # Writing to the file
        with open(file_path, "a+") as file:
            file.write(f"{contents}\n")

    @staticmethod
    def analyze_all_bots(bot_types=None):
        if bot_types is None:
            bot_types = [1, 2, 3, 4]
        folderName = 'variable-graph-result' if IS_VARIABLE_GRAPH else 'same-graph-result'
        q_values = [i / 10 for i in range(11)]  # q values from 0.0 to 1.0

        # Initialize data structures
        win_counts = {bot: {q: 0 for q in q_values} for bot in bot_types}
        loss_counts = {bot: {q: 0 for q in q_values} for bot in bot_types}

        # Read and process data for each bot
        for bot in bot_types:
            file_path = f"{os.getcwd()}/{folderName}/bot{bot}.txt"
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue

            # Read CSV
            data = pd.read_csv(file_path, header=None, names=['q', 'win', 'bot_type'])
            data["win"] = data["win"].astype(str).str.strip().str.lower() == "true"

            for _, row in data.iterrows():
                q = row['q']
                win = row['win']
                if q in q_values:
                    win_counts[bot][q] += int(win)
                    loss_counts[bot][q] += int(not win)

        # Visualization 1: Line Graph
        plt.figure(figsize=(10, 6))
        for bot in bot_types:
            wins = [win_counts[bot][q] for q in q_values]
            plt.plot(q_values, wins, marker='o', linestyle='-', label=f'Bot {bot} Wins')

        plt.xlabel("q Values", fontsize=12)
        plt.ylabel("Win Count", fontsize=12)
        plt.title(f"{'Variable' if IS_VARIABLE_GRAPH else 'Constant'} Graph Comparison", fontsize=14)
        plt.xticks(q_values)
        plt.legend()
        plt.grid(True)
        plt.show()

        # Visualization 2: Win/Loss Table
        table_data = []
        for q in q_values:
            row = [q]
            for bot in bot_types:
                row.append(win_counts[bot][q])
                row.append(loss_counts[bot][q])
            table_data.append(row)

        columns = ["q"] + [f"Bot {bot} Wins" for bot in bot_types] + [f"Bot {bot} Losses" for bot in bot_types]
        table_df = pd.DataFrame(table_data, columns=columns)

        print("\nWin/Loss Counts Table:")
        print(table_df.to_string(index=False))

    @staticmethod
    def botWiseAnalysis(botType):
        folderName = 'variable-graph-result' if IS_VARIABLE_GRAPH else 'same-graph-result'
        file_path = f"{os.getcwd()}/{folderName}/bot{botType}.txt"  # File path

        # Read the file
        data = pd.read_csv(file_path, header=None, names=['q', 'win', 'bot_type'])

        # Debug: Print first few rows to check if data is loaded correctly
        print("Raw Data Preview:\n", data.head())

        # Convert 'win' column to boolean
        data["win"] = data["win"].astype(str).str.strip().str.lower() == "true"

        # Define q ranges
        # ranges = {
        #     "0 - 0.3": (0.0, 0.3),
        #     "0.4 - 0.6": (0.4, 0.6),
        #     "0.7 - 1": (0.7, 1.0)
        # }
        ranges = { str(i/10): i/10 for i in range(0, 10, 1)}

        # Initialize counters
        win_counts = {label: 0 for label in ranges}
        total_records = {label: 0 for label in ranges}

        # Count wins and total records per range
        allRecords = list(data.iterrows())
        for _, row in allRecords:
            q, win = row['q'], row['win']
            for label, val in ranges.items():
                if val == q:
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
    def fillRecordsSimple(recordsPerBot):
        for qRange in ([0, 0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9, 1]):
            for bot in [1,2,3]:
                for i in range(recordsPerBot):
                    qXRange = random.choice(qRange)
                    g = auto_game(q=qXRange, bot_type=bot, isUseIPCells=IS_VARIABLE_GRAPH)
                    q, isFireExtinguished, bot_type = g.q, g.isFireExtinguished, g.bot_type
                    Result.write(f'bot{bot_type}', f'{q}, {isFireExtinguished}, {bot_type}')
                print(f"Finished q ranges from {qRange} for bot {bot}")

    @staticmethod
    def get_existing_counts(is_variable_graph):
        """ Reads existing data files and counts records for each (bot, q) pair. """
        folder = "variable-graph-result" if is_variable_graph else "same-graph-result"
        counts = defaultdict(int)

        for bot in range(1, 5):
            file_path = f"{folder}/bot{bot}.txt"
            try:
                with open(file_path, "r") as f:
                    for line in f:
                        parts = line.strip().split(", ")
                        if len(parts) == 3:
                            q = float(parts[0])
                            counts[(bot, q)] += 1
            except FileNotFoundError:
                pass  # If file doesn't exist, treat as zero records

        return counts

    @staticmethod
    def generate_uniform_data(is_variable_graph, num_records):
        """ Ensures uniform distribution of data across all bots and q values. """
        folder = "variable-graph-result" if is_variable_graph else "same-graph-result"
        existing_counts = Result.get_existing_counts(is_variable_graph)

        q_values = [round(i * 0.1, 1) for i in range(1, 11)]  # 0.1 to 1.0
        bots = [1, 2, 3, 4]

        # Determine max existing count for any (bot, q) pair
        max_count = max(existing_counts.values(), default=0)

        # If already uniform, generate 'num_records' for each bot, q
        target_count = max_count + num_records if max_count > 0 else num_records

        for bot in bots:
            for q in q_values:
                missing = target_count - existing_counts.get((bot, q), 0)

                for _ in range(missing):
                    isUseIpCells = None if is_variable_graph else currently_open_1
                    g = auto_game(q=q, bot_type=bot, isUseIPCells=isUseIpCells)
                    result = f"{g.q}, {g.isFireExtinguished}, {g.bot_type}\n"

                    # Append to file
                    with open(f"{folder}/bot{bot}.txt", "a") as f:
                        f.write(result)

        print(f"Data generation complete. Each bot now has {target_count} records per q.")
