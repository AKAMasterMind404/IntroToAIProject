import random
from game.ui_game import ui_game
from game.auto_game import auto_game
from result.analysis import Result

if __name__ == "__main__":
    isAnalyze = False

    if isAnalyze:
        Result.analysis(3)
    else:
        for bot in [1, 2, 3]:
            for i in range(1000):
                q1Range = random.choice([0, 0.1, 0.2, 0.3])
                g = auto_game(q=q1Range, bot_type=bot)
                q, isFireExtinguished, bot_type = g.q, g.isFireExtinguished, g.bot_type
                Result.write(f'bot{bot_type}', f'{q}, {isFireExtinguished}, {bot_type}')
            print(f"Finished q ranges from 0.1-0.3 for bot {bot}")
            for i in range(100):
                q2Range = random.choice([0.4, 0.5, 0.6])
                g = auto_game(q=q2Range, bot_type=bot)
                q, isFireExtinguished, bot_type = g.q, g.isFireExtinguished, g.bot_type
                Result.write(f'bot{bot_type}', f'{q}, {isFireExtinguished}, {bot_type}')
            print(f"Finished q ranges from 0.1-0.3 for bot {bot}")
            for i in range(100):
                q3Range = random.choice([0.7, 0.8, 0.9, 1])
                g = auto_game(q=q3Range, bot_type=bot)
                q, isFireExtinguished, bot_type = g.q, g.isFireExtinguished, g.bot_type
                Result.write(f'bot{bot_type}', f'{q}, {isFireExtinguished}, {bot_type}')
            print(f"Finished q ranges from 0.1-0.3 for bot {bot}")
