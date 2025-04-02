from aipython.stripsProblem import STRIPS_domain, Planning_problem, Strips

# Definicja domeny STRIPS dla logistyki
feature_domain_dict = {
    "at": {"A", "B", "C", "D", "E"},
    "in": {True, False}
}

# Akcje (modyfikacja wcześniej zdefiniowanych)
actions = {
    "move": Strips("move", {"at": "from"}, {"at": "to"}),
    "load": Strips("load", {"at": "L", "in": False}, {"in": True, "at": None}),
    "unload": Strips("unload", {"in": True, "at": "L"}, {"in": False, "at": "L"})
}

# Tworzenie domeny STRIPS
logistics_domain = STRIPS_domain(feature_domain_dict, actions)

# Stany początkowe
initial_state = {
    "at": {"T1": "A", "T2": "B", "P1": "A", "P2": "B", "P3": "C"},
    "in": {"P1": False, "P2": False, "P3": False}
}

# Cele
goal_state = {"at": {"P1": "E", "P2": "E", "P3": "E"}}


# Heurystyka - odległość Manhattan (liczymy liczbę ruchów dla każdej paczki)
def manhattan_distance(state, goal_state, item):
    start_location = state["at"][item]
    goal_location = goal_state["at"][item]

    locations = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}

    return abs(locations[start_location] - locations[goal_location])


# Funkcja rozwiązywania problemu za pomocą forward planning i heurystyki
def forward_plan_with_heuristic(problem, initial_state, goal_state, timeout=300):
    # Tworzymy listę akcji
    actions_sequence = []
    current_state = initial_state
    while current_state != goal_state:
        best_action = None
        best_heuristic_value = float('inf')

        # Wybieramy najlepszą akcję opartą na heurystyce
        for action in problem.prob_domain.actions:
            # Sprawdzamy, jakie akcje pasują do aktualnego stanu
            if all(current_state.get(precond[0], None) == precond[1] for precond in action.preconds.items()):
                new_state = current_state.copy()
                # Zastosuj efekty akcji
                for effect, value in action.effects.items():
                    new_state[effect] = value

                # Obliczamy wartość heurystyki
                heuristic_value = sum(manhattan_distance(new_state, goal_state, item) for item in ["P1", "P2", "P3"])

                if heuristic_value < best_heuristic_value:
                    best_heuristic_value = heuristic_value
                    best_action = action

        # Jeśli nie znaleziono akcji, wyjdź z pętli (brak rozwiązania)
        if not best_action:
            print("Nie znaleziono rozwiązania.")
            break

        # Zastosuj najlepszą akcję
        actions_sequence.append(best_action)
        # Zaktualizuj stan
        for effect, value in best_action.effects.items():
            current_state[effect] = value

    return actions_sequence


# Tworzymy problem planowania
logistics_problem = Planning_problem(logistics_domain, initial_state, goal_state)

# Rozwiązywanie problemu z użyciem forward planning i heurystyki
solution = forward_plan_with_heuristic(logistics_problem, initial_state, goal_state, timeout=300)

# Wydrukowanie rozwiązania
if solution:
    print("Rozwiązanie:", [action.name for action in solution])
else:
    print("Brak rozwiązania.")
