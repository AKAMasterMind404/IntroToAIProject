import os
import random
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
from constants import IS_VARIABLE_GRAPH
from game.auto_game import auto_game
from graph.sample.sample1 import currently_open_1
from helpers.generic import HelperService


class Result:
    @staticmethod
    def write(filename: str, contents: str):
        folderName = 'variable-graph-result' if IS_VARIABLE_GRAPH else 'same-graph-result'
        file_path = f"{os.getcwd()}/{folderName}/{filename}.txt"

        # Writing to the file
        with open(file_path, "a+") as file:
            file.write(f"{contents}\n")

    @staticmethod
    def analyzeBotWinVsQ(bot_types=None):
        if bot_types is None:
            bot_types = [1, 2, 3, 4]
        folderName = 'variable-graph-result' if IS_VARIABLE_GRAPH else 'same-graph-result'
        q_values = [i / 10 for i in range(11)]  # q = 0.0 to 1.0, interval = 0.1

        # Win count and Loss count default values set
        win_counts = {bot: {q: 0 for q in q_values} for bot in bot_types}
        loss_counts = {bot: {q: 0 for q in q_values} for bot in bot_types}

        # Read and process data for each bot
        for bot in bot_types:
            file_path = f"{os.getcwd()}/{folderName}/bot{bot}.txt"

            # Read bot_nth text file
            data = pd.read_csv(file_path, header=None, names=['q', 'win', 'bot_type', 't'])
            data["win"] = data["win"].astype(str).str.strip().str.lower() == "true"

            for _, row in data.iterrows():
                q = row['q']
                win = row['win']
                if q in q_values:
                    win_counts[bot][q] += int(win)
                    loss_counts[bot][q] += int(not win)

        plt.figure(figsize=(10, 6))
        for bot in bot_types:
            wins = [win_counts[bot][q] for q in q_values]
            plt.plot(q_values, wins, marker='o', linestyle='-', label=f'Bot {bot} Wins')

        plt.xlabel("Q (Flammability)", fontsize=12)
        plt.ylabel("Successful Extinguish Count", fontsize=12)
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

        columns = ["q"] + [f"Bot {bot} Extinguish" for bot in bot_types] + [f"Bot {bot} Non-Extinguish" for bot in bot_types]
        table_data_frame = pd.DataFrame(table_data, columns=columns)

        HelperService.printDebug("\nTabular Format:")
        HelperService.printDebug(table_data_frame.to_string(index=False))

    @staticmethod
    def analyzeTimeStepsVsQ(bot_types=None):
        if bot_types is None: bot_types = [1, 2, 3, 4]
        folderName = 'variable-graph-result' if IS_VARIABLE_GRAPH else 'same-graph-result'
        q_values = [i / 10 for i in range(11)]  # q = 0.0 to 1.0, interval = 0.1

        # Initialize data structure to store time steps for each bot and q value
        time_info = {bot: {q: [] for q in q_values} for bot in bot_types}

        # Read and process data for each bot
        for bot in bot_types:
            file_path = f"{os.getcwd()}/{folderName}/bot{bot}.txt"

            # Read CSV
            data = pd.read_csv(file_path, header=None, names=['q', 'win', 'bot_type', 't'])
            data["win"] = data["win"].astype(str).str.strip().str.lower() == "true"

            # Filter winning cases and store time steps
            for _, row in data.iterrows():
                q = row['q']
                win = row['win']
                t = row['t']
                if win and q in q_values:
                    time_info[bot][q].append(t)

        # Plot time steps vs q for each bot
        plt.figure(figsize=(10, 6))
        for bot in bot_types:
            avg_time_steps = [sum(time_info[bot][q]) / len(time_info[bot][q]) if time_info[bot][q] else 0 for q in q_values]
            plt.plot(q_values, avg_time_steps, marker='o', linestyle='-', label=f'Bot {bot}')

        plt.xlabel("Q (Flammability)", fontsize=12)
        plt.ylabel("Average Time Steps (Winning Cases)", fontsize=12)
        plt.title(f"{'Variable' if IS_VARIABLE_GRAPH else 'Constant'} Graph: Time Steps vs Q", fontsize=14)
        plt.xticks(q_values)
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def botWiseAnalysis(botType):
        folderName = 'variable-graph-result' if IS_VARIABLE_GRAPH else 'same-graph-result'
        file_path = f"{os.getcwd()}/{folderName}/bot{botType}.txt"  # File path

        data = pd.read_csv(file_path, header=None, names=['q', 'win', 'bot_type'])

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

        # Debug: HelperService.printDebug computed counts
        HelperService.printDebug("Total Records: " + str(total_records))
        HelperService.printDebug("Wins: " + str(win_counts))
        HelperService.printDebug("Losses: " + str(loss_counts))

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

    # Deprecated
    # @staticmethod
    # def fillRecordsSimple(recordsPerBot):
    #     for qRange in ([0, 0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9, 1]):
    #         for bot in [1,2,3]:
    #             for i in range(recordsPerBot):
    #                 qXRange = random.choice(qRange)
    #                 g = auto_game(q=qXRange, bot_type=bot, isUseIpCells=IS_VARIABLE_GRAPH)
    #                 q, isFireExtinguished, bot_type = g.q, g.isFireExtinguished, g.bot_type
    #                 Result.write(f'bot{bot_type}', f'{q}, {isFireExtinguished}, {bot_type}')
    #             HelperService.printDebug(f"Finished q ranges from {qRange} for bot {bot}")

    @staticmethod
    def get_existing_counts(is_variable_graph):
        folder = "variable-graph-result" if is_variable_graph else "same-graph-result"
        counts = defaultdict(int)

        for bot in range(1, 5):
            file_path = f"{folder}/bot{bot}.txt"
            f = open(file_path, "r")
            for line in f:
                parts = line.strip().split(", ")
                if len(parts) == 3:
                    q = float(parts[0])
                    counts[(bot, q)] += 1

        return counts

    @staticmethod
    def generate_uniform_data(is_variable_graph, num_records):
        ''' Generates data in a uniform manner, or fills in empty records'''
        folder = "variable-graph-result" if is_variable_graph else "same-graph-result"
        existing_counts = Result.get_existing_counts(is_variable_graph)

        q_values = [round(i * 0.1, 1) for i in range(0, 11)]  # 0.1 to 1.0, interval = 0.1
        bots = [1, 2, 3, 4]

        # Determine max count for given bot
        max_count = max(existing_counts.values(), default=0)

        # total count = max_count + count to be normalised
        target_count = max_count + num_records if max_count > 0 else num_records

        for bot in bots:
            f = open(f"{folder}/bot{bot}.txt", "a")
            for q in q_values:
                missing = target_count - existing_counts.get((bot, q), 0)

                for _ in range(missing):
                    isUseIpCells = None if is_variable_graph else currently_open_1
                    g = auto_game(q=q, bot_type=bot, isUseIpCells=isUseIpCells)
                    result = f"{g.q}, {g.isFireExtinguished}, {g.bot_type}, {g.t}\n"
                    f.write(result)
        HelperService.printDebug(f"Data generation complete. Each bot now has {target_count} records per q.")