# Ben Lehrburger
# COSC 076 PA5
# SAT Problem Solver

import random, copy, time
import numpy as np

# Wrap an SAT solver object
class SAT:

    def __init__(self, fileName):

        # Store the file name
        self.file = fileName
        # Open the CNF file associated with the inputted file name
        self.cells = open(fileName, "r")
        # Index = variable, value = variable
        self.indices = {}
        # Index = index, value = boolean
        self.model = {}
        # Store the CNF clauses
        self.clauses = set()
        # Choose a threshold for random choice
        self.threshold = 0.7

        # Associate an index with each variable
        index = 1

        # For each clause in the CNF file
        for clause in self.cells:

            # Format and store each individual clause
            map_clause = clause.split()
            map_clause = map(int, map_clause)
            self.clauses.add(tuple(map_clause))
            clause = clause.strip()
            clause = clause.split(' ')

            # For each variable in the clause
            for variable in clause:
                variable = abs(int(variable))

                # If the variable has not been assigned an index
                if variable not in self.indices.keys():
                    # Add it to the indexing dictionary
                    self.indices[variable] = index
                    # Add it to the model dictionary with a random boolean
                    self.model[index] = bool(random.getrandbits(1))
                    index += 1

    # Implementation of the GSAT algorithm
    def gsat(self):

        # Get the clauses satisfied by the current model
        satisfied_clauses = self.get_satisfied(self.model)

        # If the model satisfies all clauses
        while not self.is_satisfied(satisfied_clauses):

            # Choose a random value between one and zero
            random_value = random.uniform(0, 1)

            # If the random value is greater than the threshold
            if random_value > self.threshold:

                # Randomly choose a variable
                variable = np.random.choice(list(self.model.keys()))
                # Retrieve and flip that variable's truth value
                self.model[variable] = not self.model[variable]
                # Update the set of satisfied clauses
                satisfied_clauses = self.get_satisfied(self.model)

            # If the random value is not greater than the threshold
            else:

                # Store each variable's hypothetical satisfaction score
                new_satisfactions = {}

                # For each variable and its assigned truth value in the model
                for variable, bool in self.model.items():
                    # Make a mutable copy of the model
                    new_model = self.model.copy()
                    # Flip that variable's truth value
                    new_model[variable] = not bool
                    # Store the new model's satisfaction score
                    new_satisfactions[variable] = len(self.get_satisfied(new_model))

                # Get the variable whose truth value-switch satisfies the most clauses
                max_satisfied = max(list(new_satisfactions.values()))
                # Store the most satisfying variables if there is a tie
                most_satisfying_variables = []

                # Retrieve the most satisfying variables by index
                for variable, num_satisfied in new_satisfactions.items():
                    if num_satisfied == max_satisfied:
                        most_satisfying_variables.append(variable)

                # Randomly choose one of the most satisfying variables
                a_satisfying_variable = np.random.choice(most_satisfying_variables)
                # Retrieve and flip that variable's truth value
                self.model[a_satisfying_variable] = not self.model[a_satisfying_variable]
                # Update the set of satisfied clauses
                satisfied_clauses = self.get_satisfied(self.model)

        # Return the solution
        print('Heres the satisfied model:')
        return self.model

    # Implementation of the walkSAT algorithm
    def walksat(self):

        # Get the clauses satisfied by the current model
        satisfied_clauses = self.get_satisfied(self.model)

        # If the model satisfies all clauses
        while not self.is_satisfied(satisfied_clauses):

            # Recalculate the satisfied clauses
            print('There are now ' + str(len(satisfied_clauses)) + ' satisfied clauses out of ' + str(
                len(self.clauses)) + ' total clauses')

            # Get the clauses unsatisfied by the current model
            unsatisfied = self.get_unsatisfied(satisfied_clauses)
            # Randomly choose an unsatisfied clause
            an_unsatisfied_clause = random.choice(list(unsatisfied))

            # Choose a random value between one and zero
            random_value = random.uniform(0, 1)

            # If the random value is greater than the threshold
            if random_value > self.threshold:

                # Randomly choose a variable
                variable = np.random.choice(an_unsatisfied_clause)
                # Retrieve and flip that variable's truth value
                index = self.indices[abs(variable)]
                self.model[index] = not self.model[index]
                # Update the set of satisfied clauses
                satisfied_clauses = self.get_satisfied(self.model)

            # If the random value is not greater than the threshold
            else:

                # Store each variable's hypothetical satisfaction score
                new_satisfactions = {}

                # For each variable in that unsatisfied clause
                for variable in an_unsatisfied_clause:

                    # Make a mutable copy of the model
                    new_model = copy.deepcopy(self.model)
                    # Retrieve the variable's index
                    index = self.indices[abs(variable)]
                    # Retrieve and flip the variable's truth value
                    new_model[index] = not new_model[index]
                    # Store the new model's satisfaction score
                    new_satisfactions[index] = len(self.get_satisfied(new_model))

                # Get the variable whose truth value-switch satisfies the most clauses
                max_satisfied = max(list(new_satisfactions.values()))
                # Store the most satisfying variables if there is a tie
                most_satisfying_variables = []

                # Retrieve the most satisfying variables by index
                for variable, num_satisfied in new_satisfactions.items():
                    if num_satisfied == max_satisfied:
                        most_satisfying_variables.append(variable)

                # Randomly choose one of the most satisfying variables
                a_satisfying_variable = np.random.choice(most_satisfying_variables)
                # Retrieve and flip that variable's truth value
                self.model[a_satisfying_variable] = not self.model[a_satisfying_variable]
                # Update the set of satisfied clauses
                satisfied_clauses = self.get_satisfied(self.model)

        # Return the solution
        return self.model

    # ** HELPER METHODS **

    # Get the satisfied clauses in the model
    def get_satisfied(self, model):

        # Store the satisfied clauses
        satisfied = set()

        # For each clause
        for clause in self.clauses:
            # For each variable in that clause
            for variable in clause:

                # If the clause is not already satisfied
                if clause not in satisfied:
                    # Retrieve that variable's truth value
                    bool = model[self.indices[abs(variable)]]

                    # If the clause needs a false value and the current variable is false
                    if variable < 0 and bool is False:
                        # The clause is satisfied
                        satisfied.add(clause)

                    # If the clause is needs a true value and the current variable is true
                    elif variable > 0 and bool is True:
                        # The clause is satisfied
                        satisfied.add(clause)

        # Return the satisfied clauses
        return satisfied

    # Check to see if the current model satisfies all clauses
    def is_satisfied(self, satisfied):

        # For each clause
        for clause in self.clauses:
            # If the clause not satisfied
            if clause not in satisfied:
                # The model is not satisfied
                return False

        # The model is satisfied
        print('All ' + str(len(satisfied)) + ' clauses are satisfied!')
        return True

    # Retrieve the unsatisfied clauses
    def get_unsatisfied(self, satisfied):

        # Store each unsatisfied clause
        unsatisfied = set()

        # For each clause
        for clause in self.clauses:
            # If the clause not satisfied
            if clause not in satisfied:
                # Store the unsatisfied clause
                unsatisfied.add(clause)

        # Return the unsatisfied clauses
        return unsatisfied

    # Write the puzzle's solution in CNF to a new file
    def write_solution(self, file_name):

        solution = open(file_name, 'x')
        solution = open(file_name, 'w')

        keys = list(self.indices.keys())
        values = list(self.indices.values())

        for index, bool in self.model.items():
            position = values.index(index)
            variable = keys[position]
            if bool is True:
                solution.write(str(variable) + '\n')
            if bool is False:
                solution.write('-' + str(variable) + '\n')
