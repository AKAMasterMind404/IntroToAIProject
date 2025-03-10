import os
import random
import matplotlib.pyplot as plt
import pandas as pd
from constants import IS_VARIABLE_GRAPH
from game.auto_game import auto_game
from graph.sample.sample1 import sample_ip_1


class Result:
    @staticmethod
    def write(filename: str, contents: str):
        folderName = 'variable-graph-result' if IS_VARIABLE_GRAPH else 'same-graph-result'
        file_path = f"{os.getcwd()}/{folderName}/{filename}.txt"  # Relative path from root/main.py

        # Writing to the file
        with open(file_path, "a+") as file:
            file.write(f"{contents}\n")

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
                    ipCells: set = None if IS_VARIABLE_GRAPH else sample_ip_1
                    g = auto_game(q=qXRange, bot_type=bot, ipCells=ipCells)
                    q, isFireExtinguished, bot_type = g.q, g.isFireExtinguished, g.bot_type
                    Result.write(f'bot{bot_type}', f'{q}, {isFireExtinguished}, {bot_type}')
                print(f"Finished q ranges from {qRange} for bot {bot}")

    @staticmethod
    def fillRecords(recordsToFill, dataMap: dict):
        qRange1 = [0, 0.1, 0.2, 0.3]
        qRange2 = [0.4, 0.5, 0.6]
        qRange3 = [0.7, 0.8, 0.9, 1]

        maxKey = list(dataMap.keys())[-1]
        maxVal = dataMap[maxKey]

        for bQ in dataMap.keys():
            bVal, qVal = bQ.split("_")
            bVal = int(bVal[1])
            qVal = int(qVal[1])

            qxRange = qRange1
            if qVal == 1:
                qxRange = qRange1
            elif qVal == 2:
                qxRange = qRange2
            elif qVal == 3:
                qxRange = qRange3

            curr = dataMap.get(f"b{bVal}_q{qVal}")
            recBehind = max(maxVal - curr, 0)
            toDo = max(recBehind, recordsToFill//4)
            done = 0

            while toDo > 0 and done <= recordsToFill:
                g = auto_game(q=random.choice(qxRange), bot_type=bVal)
                q_res, isFireExtinguished, bot_type_res = g.q, g.isFireExtinguished, g.bot_type
                Result.write(f'bot{bot_type_res}', f'{q_res}, {isFireExtinguished}, {bot_type_res}')

                toDo -= 1
                done += 1

    @staticmethod
    def getFillRecordQuantity():
        folderName = 'variable-graph-result' if IS_VARIABLE_GRAPH else 'same-graph-result'
        qRange1 = [0, 0.1, 0.2, 0.3]
        qRange2 = [0.4, 0.5, 0.6]
        qRange3 = [0.7, 0.8, 0.9, 1]

        bot1Records, bot2Records, bot3Records, bot4Records = list(), list(), list(), list()
        try:
            bot1Records = open(f"{folderName}/bot1.txt", 'r').readlines()
            bot2Records = open(f"{folderName}/bot2.txt", 'r').readlines()
            bot3Records = open(f"{folderName}/bot3.txt", 'r').readlines()
            bot4Records = open(f"{folderName}/bot4.txt", 'r').readlines()
        except FileNotFoundError:
            pass

        numDict = dict()
        for bot in [1, 2, 3, 4]:
            records = None
            if bot == 1:
                records = bot1Records
            elif bot == 2:
                records = bot2Records
            elif bot == 3:
                records = bot3Records
            elif bot == 4:
                records = bot4Records

            q1Rec, q2Rec, q3Rec = 0, 0, 0
            for rec in records:
                if rec.strip("\n "):
                    q, res, _ = rec.split(",")
                    q = float(q)
                    if q in qRange1:
                        q1Rec += 1
                    elif q in qRange2:
                        q2Rec += 1
                    elif q in qRange3:
                        q3Rec += 1

            for qR in [1, 2, 3]:
                data = None
                if qR == 1: data = q1Rec
                if qR == 2: data = q2Rec
                if qR == 3: data = q3Rec
                numDict[f'b{bot}_q{qR}'] = data
                pass

        result = dict(sorted(numDict.items(), key=lambda item: item[1]))
        return result