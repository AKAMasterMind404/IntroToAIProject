import os
import matplotlib.pyplot as plt
from collections import defaultdict
from game.auto_game import auto_game
from graph.graph import getGraph


class Winnability:

    @staticmethod
    def generateWinnabilityDataWithFixedPos(simPerQPerBot: int):
        for bot in [1,2,3,4]:
            file = open(f"winnability-result/bot{bot}.txt", 'a+')
            for q in range(0, 10):
                _q = q / 10
                for _ in range(simPerQPerBot):
                    game = auto_game(_q, bot, isUseIpCells=True, isUsePresetPos=False)
                    hasWon = game.isFireExtinguished
                    file.write(f"{_q}, {hasWon}, bot{bot}\n")

    @staticmethod
    def plotWinRateForBots():
        data = []
        for bot in [1, 2, 3, 4]:
            data.append(Winnability._calculateWinsAndLossesForBot(bot))

        q_values = sorted(data[0].keys())  # Extract sorted q values from the first bot's data

        # Determine winnable q values (at least one bot has a win rate > 0)
        winnable_q_values = [
            q for q in q_values if any(data[bot][q]['wins'] > 0 for bot in range(4))
        ]

        plt.figure(figsize=(10, 5))

        bot_labels = ["Bot 1", "Bot 2", "Bot 3", "Bot 4"]
        colors = ["b", "g", "r", "c"]

        for i, bot_data in enumerate(data):
            win_rates = [
                bot_data[q]['wins'] / (bot_data[q]['wins'] + bot_data[q]['losses']) for q in winnable_q_values
            ]
            plt.plot(winnable_q_values, win_rates, marker="o", linestyle="-", color=colors[i], label=bot_labels[i])

        plt.xlabel("Fire Spread Probability (q)")
        plt.ylabel("Win Rate (%)")
        plt.title("Win Rate for Winnable Simulations (Each Bot)")
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def plotWinnability():
        data = []
        for bot in [1, 2, 3, 4]:
            data.append(Winnability._calculateWinsAndLossesForBot(bot))

        q_values = sorted(data[0].keys())

        plt.figure(figsize=(10, 5))

        bot_labels = ["Bot 1", "Bot 2", "Bot 3", "Bot 4"]
        colors = ["b", "g", "r", "c"]

        for i, bot_data in enumerate(data):
            win_rates = [bot_data[q]['wins'] / (bot_data[q]['wins'] + bot_data[q]['losses']) for q in q_values]
            plt.plot(q_values, win_rates, marker="o", linestyle="-", color=colors[i], label=bot_labels[i])

        plt.xlabel("Fire Spread Probability (q)")
        plt.ylabel("Winnability (%)")
        plt.title("Winnability for Each Bot")
        plt.legend()
        plt.grid()
        plt.show()


    @staticmethod
    def _calculateWinsAndLossesForBot(bot: int):
        botData = open(f"winnability-result/bot{bot}.txt", 'r').readlines()
        qDict = dict()
        for data in botData:
            q, res, bot = data.strip().split(",")
            winAndLossForQ = qDict.get(q)
            if not winAndLossForQ:
                qDict[q] = {'wins': 0, 'losses': 0}

            qDict[q]['wins'] += res.strip() == 'True'
            qDict[q]['losses'] += res.strip() != 'True'
        return qDict