def auto_game(graphFunction: ()):
    graph = graphFunction(None)
    graph.initialize_ship_opening()
    if graph.game_over:
        graph = graphFunction(None)
        graph.proceed()
    else:
        graph.canProceed = False
        while graph.step < 5:
            graph.proceed()
        steps = 0
        while graph.step == 5 and not graph.game_over:
            steps += 1
            graph.proceed()
            # Generate report
        print(f"{steps} Steps taken!")
    return graph
