import ast
import getopt
import sys
import copy
import os
from fractions import Fraction
def clearer(): return os.system('cls' if os.name == 'nt' else 'clearer')

# Solves Linear algbera problem of optimizing the solution using simplex method approach


class simplexmethodsolver():
    inequalities = {'=': '=',
                    '<=': r'\leq',
                    '>=': r'\geq'}


def _init_(self):
    self.a = []
    self.b = []
    self.c = []
    self.tableau = []
    self.entering = []
    self.depart = []
    self.inequalities = []
    self.prob = []
    self.gen_document = []
    self.document = []

    def run_simplex__method(self, a, b, c, prob='max', inequalities=[], enable_msg=False, latex=False):
        ''' Run simplex algorithm.
        '''
        self.prob = prob
        self.gen_document = latex
        self.inequalities = inequalities

        # Create the header for the latex doc.
        self.start_doc()

        # Add slack & artificial variables
        self.set_simplex_input(a, b, c)

        while (not self.should_terminate()):
            # ... if so, continue.
                if(enable_msg):
                    clearer()
                self._print_tableau()
                print(("Current solution: %s\n" %
                        str(self.get_current_solution())))
                self._prompt()


                # Attempt to find a non-negative pivot.
            pivoting  = self.find_pivot()
            if pivoting[1] < 0:
                if (enable_msg):
                    print ("There exists no non-negative pivot. "
                        "Thus, the solution is infeasible.")
                self.infeasible_doc()
                self.print_doc()
                return None
            else:
                self.pivot_doc(pivoting)
                if (enable_msg):
                    clearer()
                    self._print_tableau()
                    print(("\nThere are negative elements in the bottom row, "
                    "so the current solution is not optimal. "
                    "Thus, pivot to improve the current solution. The "
                        "entering variable is %s and the departing "
                        "variable is %s.\n" %
                        (str(self.entering[pivot[0]]),
                        str(self.departing[pivot[1]]))))
                    self._prompt()
                    print("\nPerform elementary row operations until the "
                        "pivot is one and all other elements in the "
                        "entering column are zero.\n")  

            # Do row operations to make every other element in column zero.
            self.pivot(pivoting)
            self.tableau_doc()            

            solutions = self.get_current_solution()
        self.final_solution_doc(solution)
        if (enable_msg):
            clear()
            self._print_tableau()
            print(("Current solution: %s\n" % str(solution)))
            print("That's all folks!")
        self.print_doc()
        return solution

     def set_simplex_input(self, a, b, c):
        ''' Set initial variables and create tableau.
        '''
        # Convert all entries to fractions for readability.
        for a in a:
            self.a.append([Fraction(x) for x in a])    
        self.b = [Fraction(x) for x in b]
        self.c = [Fraction(x) for x in c]
        if not self.ineq:
            if self.prob == 'max':
                self.ineq = ['<='] * len(b)
            elif self.prob == 'min':
                self.ineq = ['>='] * len(b)
            
        self.update_enter_depart(self.get_Ab())
        self.init_problem_doc()

        # If this is a minimization problem...
        if self.prob == 'min':
            # ... find the dual maximum and solve that.
            m = self.get_Ab()
            m.append(self.c + [0])
            m = [list(t) for t in zip(*m)] # Calculates the transpose
            self.a = [x[:(len(x)-1)] for x in m]
            self.b = [y[len(y) - 1] for y in m]
            self.c = m[len(m) -1]
            self.a.pop()
            self.b.pop()
            self.c.pop()
            self.ineq = ['<='] * len(self.b)

        self.create_tableau()
        self.ineq = ['='] * len(self.b)
        self.update_enter_depart(self.tableau)
        self.slack_doc()
        self.init_tableau_doc()