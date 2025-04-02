from aipython.stripsProblem import STRIPS_domain, Planning_problem, Strips
import time

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
# z aktualnej lokalizacji do celu
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

# Problem 1: Transport paczek z różnych lokalizacji do celu
initial_state_1 = {
    "at": {"T1": "A", "T2": "B", "P1": "A", "P2": "B", "P3": "C"},
    "in": {"P1": False, "P2": False, "P3": False}
}

goal_state_1 = {"at": {"P1": "E", "P2": "E", "P3": "E"}}

# Podcele dla problemu 1
subgoals_1 = [
    {"at": {"P1": "C", "P2": "D"}},  # Podcel 1
    {"at": {"P1": "E", "P2": "E"}}   # Podcel 2
]

# Problem 2: Transport paczek z większą liczbą lokalizacji
initial_state_2 = {
    "at": {"T1": "A", "T2": "B", "T3": "C", "P1": "A", "P2": "B", "P3": "C", "P4": "D"},
    "in": {"P1": False, "P2": False, "P3": False, "P4": False}
}

goal_state_2 = {"at": {"P1": "E", "P2": "E", "P3": "E", "P4": "E"}}

# Problem 3: Transport paczek z podzielonymi celami
initial_state_3 = {
    "at": {"T1": "A", "T2": "B", "P1": "A", "P2": "B", "P3": "C", "P4": "D"},
    "in": {"P1": False, "P2": False, "P3": False, "P4": False}
}

goal_state_3 = {"at": {"P1": "E", "P2": "D", "P3": "C", "P4": "B"}}

# Problem 4: Większa liczba paczek i lokalizacji
initial_state_4 = {
    "at": {"T1": "A", "T2": "B", "T3": "C", "P1": "A", "P2": "B", "P3": "C", "P4": "D", "P5": "E"},
    "in": {"P1": False, "P2": False, "P3": False, "P4": False, "P5": False}
}

goal_state_4 = {"at": {"P1": "E", "P2": "D", "P3": "C", "P4": "B", "P5": "A"}}

subgoals_4 = [
    {"at": {"P1": "C", "P2": "D", "P3": "B"}},  # Podcel 1
    {"at": {"P1": "E", "P2": "D", "P3": "C", "P4": "B", "P5": "A"}}  # Podcel 2
]

# Funkcja rozwiązywania z podcelami
def solve_with_subgoals(problem, subgoals):
    current_state = problem.initial
    actions_sequence = []

    for subgoal in subgoals:
        subproblem = Planning_problem(problem.prob_domain, current_state, subgoal)
        solution = forward_plan_with_heuristic(subproblem, current_state, subgoal)
        if solution:
            actions_sequence.extend(solution)
            # Aktualizacja stanu
            for action in solution:
                for effect, value in action.effects.items():
                    current_state[effect] = value
        else:
            print("Nie udało się osiągnąć podcelu:", subgoal)
            return None

    return actions_sequence

# Tworzenie problemów planowania
problem_1 = Planning_problem(logistics_domain, initial_state_1, goal_state_1)
problem_2 = Planning_problem(logistics_domain, initial_state_2, goal_state_2)
problem_3 = Planning_problem(logistics_domain, initial_state_3, goal_state_3)
problem_4 = Planning_problem(logistics_domain, initial_state_4, goal_state_4)

# Rozwiązywanie problemów
for i, problem in enumerate([problem_1, problem_2, problem_3, problem_4], start=1):
    start_time = time.time()
    solution = forward_plan_with_heuristic(problem, problem.initial, problem.goal, timeout=300)
    end_time = time.time()

    if solution:
        print(f"Problem {i} rozwiązany w czasie {end_time - start_time:.2f} sekund.")
        print("Rozwiązanie:", [action.name for action in solution])
    else:
        print(f"Problem {i} nie został rozwiązany w czasie 5 minut.")

# Rozwiązywanie problemu 1 z podcelami
solution_with_subgoals = solve_with_subgoals(problem_1, subgoals_1)

if solution_with_subgoals:
    print("Rozwiązanie z podcelami:", [action.name for action in solution_with_subgoals])
else:
    print("Nie udało się rozwiązać problemu z podcelami.")

# Rozwiązywanie problemu 4 z podcelami
solution_with_subgoals_4 = solve_with_subgoals(problem_4, subgoals_4)

if solution_with_subgoals_4:
    print("Rozwiązanie problemu 4 z podcelami:", [action.name for action in solution_with_subgoals_4])
else:
    print("Nie udało się rozwiązać problemu 4 z podcelami.")

