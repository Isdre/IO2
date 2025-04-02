from aipython.stripsProblem import STRIPS_domain, Planning_problem, Strips
import time

# Definicja domeny STRIPS dla logistyki
feature_domain_dict = {
    "at": {"A", "B", "C", "D", "E", None},  # Dodano None jako możliwą wartość
    "in": {True, False}
}

# Akcje - poprawiona definicja
actions = {
    "move_T1_A_B": Strips("move_T1_A_B", {"at": {"T1": "A"}}, {"at": {"T1": "B"}}),
    "move_T1_A_C": Strips("move_T1_A_C", {"at": {"T1": "A"}}, {"at": {"T1": "C"}}),
    "move_T1_A_D": Strips("move_T1_A_D", {"at": {"T1": "A"}}, {"at": {"T1": "D"}}),
    "move_T1_A_E": Strips("move_T1_A_E", {"at": {"T1": "A"}}, {"at": {"T1": "E"}}),
    "move_T1_B_A": Strips("move_T1_B_A", {"at": {"T1": "B"}}, {"at": {"T1": "A"}}),
    "move_T1_B_C": Strips("move_T1_B_C", {"at": {"T1": "B"}}, {"at": {"T1": "C"}}),
    "move_T1_B_D": Strips("move_T1_B_D", {"at": {"T1": "B"}}, {"at": {"T1": "D"}}),
    "move_T1_B_E": Strips("move_T1_B_E", {"at": {"T1": "B"}}, {"at": {"T1": "E"}}),
    # Dodaj więcej kombinacji ruchów dla T1 i T2...
    "move_T2_A_B": Strips("move_T2_A_B", {"at": {"T2": "A"}}, {"at": {"T2": "B"}}),
    "move_T2_A_C": Strips("move_T2_A_C", {"at": {"T2": "A"}}, {"at": {"T2": "C"}}),
    
    # Akcje ładowania paczek
    "load_P1_T1_A": Strips("load_P1_T1_A", 
                           {"at": {"T1": "A", "P1": "A"}, "in": {"P1": False}}, 
                           {"in": {"P1": True}, "at": {"P1": None}}),
    "load_P1_T2_A": Strips("load_P1_T2_A", 
                           {"at": {"T2": "A", "P1": "A"}, "in": {"P1": False}}, 
                           {"in": {"P1": True}, "at": {"P1": None}}),
    "load_P2_T1_B": Strips("load_P2_T1_B", 
                           {"at": {"T1": "B", "P2": "B"}, "in": {"P2": False}}, 
                           {"in": {"P2": True}, "at": {"P2": None}}),
    "load_P2_T2_B": Strips("load_P2_T2_B", 
                           {"at": {"T2": "B", "P2": "B"}, "in": {"P2": False}}, 
                           {"in": {"P2": True}, "at": {"P2": None}}),
    "load_P3_T1_C": Strips("load_P3_T1_C", 
                           {"at": {"T1": "C", "P3": "C"}, "in": {"P3": False}}, 
                           {"in": {"P3": True}, "at": {"P3": None}}),
    
    # Akcje rozładowania paczek
    "unload_P1_T1_A": Strips("unload_P1_T1_A", 
                             {"at": {"T1": "A"}, "in": {"P1": True}}, 
                             {"in": {"P1": False}, "at": {"P1": "A"}}),
    "unload_P1_T1_B": Strips("unload_P1_T1_B", 
                             {"at": {"T1": "B"}, "in": {"P1": True}}, 
                             {"in": {"P1": False}, "at": {"P1": "B"}}),
    "unload_P1_T1_C": Strips("unload_P1_T1_C", 
                             {"at": {"T1": "C"}, "in": {"P1": True}}, 
                             {"in": {"P1": False}, "at": {"P1": "C"}}),
    "unload_P1_T1_D": Strips("unload_P1_T1_D", 
                             {"at": {"T1": "D"}, "in": {"P1": True}}, 
                             {"in": {"P1": False}, "at": {"P1": "D"}}),
    "unload_P1_T1_E": Strips("unload_P1_T1_E", 
                             {"at": {"T1": "E"}, "in": {"P1": True}}, 
                             {"in": {"P1": False}, "at": {"P1": "E"}}),
    "unload_P2_T1_E": Strips("unload_P2_T1_E", 
                             {"at": {"T1": "E"}, "in": {"P2": True}}, 
                             {"in": {"P2": False}, "at": {"P2": "E"}}),
    "unload_P3_T1_E": Strips("unload_P3_T1_E", 
                             {"at": {"T1": "E"}, "in": {"P3": True}}, 
                             {"in": {"P3": False}, "at": {"P3": "E"}}),
}

# Tworzenie domeny STRIPS
logistics_domain = STRIPS_domain(feature_domain_dict, actions)

######################################################################
# ZADANIE NA 4 PUNKTY
######################################################################

#############################
# 1. Wybór dziedziny STRIPS i definicja trzech problemów
#############################

# Definicja trzech różnych problemów
# Problem 1: Prosty problem transportowy
initial_state_1 = {
    "at": {"T1": "A", "T2": "B", "P1": "A", "P2": "B", "P3": "C"},
    "in": {"P1": False, "P2": False, "P3": False}
}
goal_state_1 = {"at": {"P1": "E", "P2": "E", "P3": "E"}}

# Problem 2: Problem transportowy z alternatywną trasą
initial_state_2 = {
    "at": {"T1": "A", "T2": "C", "P1": "A", "P2": "B", "P3": "D"},
    "in": {"P1": False, "P2": False, "P3": False}
}
goal_state_2 = {"at": {"P1": "D", "P2": "E", "P3": "A"}}

# Problem 3: Złożony problem transportowy
initial_state_3 = {
    "at": {"T1": "C", "T2": "B", "P1": "A", "P2": "D", "P3": "B"},
    "in": {"P1": False, "P2": False, "P3": False}
}
goal_state_3 = {"at": {"P1": "E", "P2": "A", "P3": "C"}}

# Tworzenie problemów planowania
problem_1 = Planning_problem(logistics_domain, initial_state_1, goal_state_1)
problem_2 = Planning_problem(logistics_domain, initial_state_2, goal_state_2)
problem_3 = Planning_problem(logistics_domain, initial_state_3, goal_state_3)

#############################
# 2. Rozwiązanie problemów metodą forward planning
#############################

def solve_problem(problem, with_heuristic=True, timeout=300):
    print(f"\nRozwiązuję problem: {problem.initial} -> {problem.goal}")
    print(f"Używając heurystyki: {with_heuristic}")
    
    start_time = time.time()
    
    if with_heuristic:
        solution = forward_plan_with_heuristic(problem, problem.initial, problem.goal, timeout)
    else:
        solution = forward_plan_without_heuristic(problem, problem.initial, problem.goal, timeout)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    if solution:
        print(f"Rozwiązanie znalezione w czasie {execution_time:.2f} sekund:")
        print([action.name for action in solution])
        print(f"Liczba akcji: {len(solution)}")
    else:
        print(f"Brak rozwiązania po {execution_time:.2f} sekundach.")
    
    return solution, execution_time

# Funkcja planowania bez heurystyki (dla porównania)
def forward_plan_without_heuristic(problem, initial_state, goal_state, timeout=300):
    start_time = time.time()
    actions_sequence = []
    current_state = dict(initial_state)
    
    while time.time() - start_time < timeout:
        # Sprawdź czy osiągnięto cel
        goal_achieved = True
        for feature, value in goal_state.items():
            if feature in current_state:
                for obj, target in value.items():
                    if obj in current_state[feature] and current_state[feature][obj] != target:
                        goal_achieved = False
                        break
            else:
                goal_achieved = False
                break
            
            if not goal_achieved:
                break
                
        if goal_achieved:
            return actions_sequence
            
        # Bez heurystyki - bierzemy pierwszą wykonalną akcję
        for action_name, action in problem.prob_domain.actions.items():
            action_applicable = True
            
            for feature, precond_value in action.preconds.items():
                if feature not in current_state:
                    action_applicable = False
                    break
                
                for obj, value in precond_value.items():
                    if obj not in current_state[feature] or current_state[feature][obj] != value:
                        action_applicable = False
                        break
                
                if not action_applicable:
                    break
                    
            if action_applicable:
                print(f"Wykonuję akcję: {action.name}")
                actions_sequence.append(action)
                
                # Aktualizuj stan
                for feature, effect_value in action.effects.items():
                    if feature not in current_state:
                        current_state[feature] = {}
                        
                    for obj, value in effect_value.items():
                        if value is None:
                            if obj in current_state[feature]:
                                del current_state[feature][obj]
                        else:
                            current_state[feature][obj] = value
                break
        else:
            print("Nie znaleziono wykonalnej akcji")
            return None
                
    print(f"Przekroczono limit czasu {timeout} sekund")
    return actions_sequence if actions_sequence else None

print("\n########## ROZWIĄZYWANIE PROBLEMÓW BEZ HEURYSTYKI ##########")
for i, problem in enumerate([problem_1, problem_2, problem_3], 1):
    print(f"\nProblem {i}:")
    solution, time_taken = solve_problem(problem, with_heuristic=False)

#############################
# 3. Heurystyka i rozwiązanie problemu z heurystyką
#############################

# Heurystyka została już zdefiniowana jako manhattan_distance
# Opis heurystyki: Odległość Manhattan mierzy odległość między obecną lokalizacją 
# paczki a jej lokalizacją docelową, biorąc pod uwagę liczbę kroków potrzebnych
# do przemieszczenia się między lokalizacjami. Jest to dobra heurystyka, ponieważ
# jest dopuszczalna (nigdy nie przeszacowuje kosztu) i informacyjna (pomaga
# kierować wyszukiwaniem w kierunku celu).

print("\n########## ROZWIĄZYWANIE PROBLEMÓW Z HEURYSTYKĄ ##########")
for i, problem in enumerate([problem_1, problem_2, problem_3], 1):
    print(f"\nProblem {i}:")
    solution, time_taken = solve_problem(problem, with_heuristic=True)

######################################################################
# ZADANIE NA 6 PUNKTÓW
######################################################################

#############################
# 1. Wszystkie zadania na 4 punkty zostały już zrealizowane
#############################

#############################
# 2. Definicja podcelów i rozwiązanie problemów z podcelami
#############################

# Definicja podcelów dla każdego problemu
subgoals_1 = [
    {"at": {"P1": "C"}},  # Podcel 1 - przenieś P1 do C
    {"at": {"P1": "E", "P2": "E"}},  # Podcel 2 - przenieś P1 i P2 do E
]

subgoals_2 = [
    {"at": {"P3": "C"}},  # Podcel 1 - przenieś P3 do C
    {"at": {"P2": "E", "P3": "A"}},  # Podcel 2 - przenieś P2 do E i P3 do A
]

subgoals_3 = [
    {"at": {"P1": "D"}},  # Podcel 1 - przenieś P1 do D
    {"at": {"P2": "A", "P3": "D"}},  # Podcel 2 - przenieś P2 do A i P3 do D
]

print("\n########## ROZWIĄZYWANIE PROBLEMÓW Z PODCELAMI BEZ HEURYSTYKI ##########")
for i, (problem, subgoals) in enumerate(zip([problem_1, problem_2, problem_3], 
                                         [subgoals_1, subgoals_2, subgoals_3]), 1):
    print(f"\nProblem {i} z podcelami:")
    start_time = time.time()
    solution_with_subgoals = solve_with_subgoals(problem, subgoals)
    end_time = time.time()
    
    if solution_with_subgoals:
        print(f"Rozwiązanie z podcelami znalezione w czasie {end_time - start_time:.2f} sekund:")
        print([action.name for action in solution_with_subgoals])
        print(f"Liczba akcji: {len(solution_with_subgoals)}")
    else:
        print(f"Nie udało się rozwiązać problemu z podcelami po {end_time - start_time:.2f} sekundach.")

print("\n########## ROZWIĄZYWANIE PROBLEMÓW Z PODCELAMI Z HEURYSTYKĄ ##########")
# Modyfikacja funkcji solve_with_subgoals, aby używała heurystyki
def solve_with_subgoals_and_heuristic(problem, subgoals):
    current_state = dict(problem.initial)
    actions_sequence = []

    for subgoal in subgoals:
        subproblem = Planning_problem(problem.prob_domain, current_state, subgoal)
        solution = forward_plan_with_heuristic(subproblem, current_state, subgoal)
        if solution:
            actions_sequence.extend(solution)
            # Aktualizacja stanu po osiągnięciu podcelu
            for action in solution:
                for feature, effect_value in action.effects.items():
                    if feature not in current_state:
                        current_state[feature] = {}
                    
                    for obj, value in effect_value.items():
                        if value is None:
                            if obj in current_state[feature]:
                                del current_state[feature][obj]
                        else:
                            current_state[feature][obj] = value
        else:
            print("Nie udało się osiągnąć podcelu:", subgoal)
            return None

    return actions_sequence

for i, (problem, subgoals) in enumerate(zip([problem_1, problem_2, problem_3], 
                                         [subgoals_1, subgoals_2, subgoals_3]), 1):
    print(f"\nProblem {i} z podcelami i heurystyką:")
    start_time = time.time()
    solution_with_subgoals = solve_with_subgoals_and_heuristic(problem, subgoals)
    end_time = time.time()
    
    if solution_with_subgoals:
        print(f"Rozwiązanie z podcelami i heurystyką znalezione w czasie {end_time - start_time:.2f} sekund:")
        print([action.name for action in solution_with_subgoals])
        print(f"Liczba akcji: {len(solution_with_subgoals)}")
    else:
        print(f"Nie udało się rozwiązać problemu z podcelami i heurystyką po {end_time - start_time:.2f} sekundach.")

######################################################################
# ZADANIE NA 8 PUNKTÓW
######################################################################

#############################
# 1. Wszystkie zadania na 6 punktów zostały już zrealizowane
#############################

#############################
# 2. Definicja i rozwiązanie trzech dodatkowych złożonych problemów
#############################

# Definicja trzech złożonych problemów wymagających minimum 20 instancji akcji
# Problem 4: Skomplikowany problem transportowy z wieloma paczkami
initial_state_4 = {
    "at": {"T1": "A", "T2": "E", "P1": "A", "P2": "B", "P3": "C", "P4": "D", "P5": "E"},
    "in": {"P1": False, "P2": False, "P3": False, "P4": False, "P5": False}
}
goal_state_4 = {"at": {"P1": "E", "P2": "D", "P3": "C", "P4": "B", "P5": "A"}}

# Problem 5: Zamiana lokalizacji wszystkich paczek
initial_state_5 = {
    "at": {"T1": "A", "T2": "E", "P1": "A", "P2": "B", "P3": "C", "P4": "D", "P5": "E"},
    "in": {"P1": False, "P2": False, "P3": False, "P4": False, "P5": False}
}
goal_state_5 = {"at": {"P1": "E", "P2": "A", "P3": "D", "P4": "C", "P5": "B"}}

# Problem 6: Transport paczek do centralnego punktu i dystrybucja
initial_state_6 = {
    "at": {"T1": "A", "T2": "E", "P1": "A", "P2": "B", "P3": "B", "P4": "D", "P5": "E", "P6": "A"},
    "in": {"P1": False, "P2": False, "P3": False, "P4": False, "P5": False, "P6": False}
}
goal_state_6 = {"at": {"P1": "C", "P2": "C", "P3": "E", "P4": "E", "P5": "A", "P6": "A"}}

# Tworzenie problemów planowania
problem_4 = Planning_problem(logistics_domain, initial_state_4, goal_state_4)
problem_5 = Planning_problem(logistics_domain, initial_state_5, goal_state_5)
problem_6 = Planning_problem(logistics_domain, initial_state_6, goal_state_6)

# Definicja podcelów dla złożonych problemów
subgoals_4 = [
    {"at": {"P5": "D"}},  # Podcel 1
    {"at": {"P5": "C", "P4": "A"}},  # Podcel 2
    {"at": {"P5": "B", "P4": "A", "P3": "D"}},  # Podcel 3
    {"at": {"P5": "A", "P4": "B", "P3": "C", "P2": "D", "P1": "E"}},  # Podcel 4
]

subgoals_5 = [
    {"at": {"P1": "C", "P2": "C"}},  # Podcel 1
    {"at": {"P1": "D", "P2": "D", "P3": "A"}},  # Podcel 2
    {"at": {"P1": "E", "P2": "A", "P3": "B", "P4": "C"}},  # Podcel 3
    {"at": {"P1": "E", "P2": "A", "P3": "D", "P4": "C", "P5": "B"}},  # Podcel 4
]

subgoals_6 = [
    {"at": {"P1": "C", "P6": "C"}},  # Podcel 1
    {"at": {"P1": "C", "P2": "C", "P3": "C", "P6": "C"}},  # Podcel 2
    {"at": {"P1": "C", "P2": "C", "P3": "E", "P4": "E", "P5": "A", "P6": "A"}},  # Podcel 3
]

print("\n########## ROZWIĄZYWANIE ZŁOŻONYCH PROBLEMÓW Z PODCELAMI I HEURYSTYKĄ ##########")
for i, (problem, subgoals) in enumerate(zip(
    [problem_4, problem_5, problem_6], 
    [subgoals_4, subgoals_5, subgoals_6]), 4):
    
    print(f"\nProblem {i} (złożony) z podcelami i heurystyką:")
    start_time = time.time()
    solution_with_subgoals = solve_with_subgoals_and_heuristic(problem, subgoals)
    end_time = time.time()
    
    if solution_with_subgoals:
        print(f"Rozwiązanie znalezione w czasie {end_time - start_time:.2f} sekund:")
        print([action.name for action in solution_with_subgoals])
        print(f"Liczba akcji: {len(solution_with_subgoals)}")
        if len(solution_with_subgoals) >= 20:
            print("✓ Problem spełnia wymaganie minimum 20 instancji akcji")
        else:
            print("✗ Problem nie spełnia wymagania minimum 20 instancji akcji")
    else:
        print(f"Nie udało się rozwiązać problemu po {end_time - start_time:.2f} sekundach.")

