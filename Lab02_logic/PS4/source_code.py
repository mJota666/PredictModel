import os
import time
import itertools

INPUT_PATH = 'C:/Users/nguye/OneDrive/Desktop/Lab02_logic/PredictModel/Lab02_logic/Input'
OUTPUT_PATH = 'C:/Users/nguye/OneDrive/Desktop/Lab02_logic/PredictModel/Lab02_logic/Output'

class KnowldegeBase:
    def __init__(self, statement, size, clauses):
        self.statement = statement
        self.size = size
        self.negative_statement = self.get_negative_statement()
        self.clauses = clauses
    def get_negative_statement(self):
        negations = []
        for atom in self.statement:
            if atom[0] == '-':
                negations.append(atom[1:])
            else:
                negations.append('-' + atom)
        return negations
    def get_negative_atom(self, atom):
        if atom[0] == '-':
            return atom[1:]
        else:
            return '-' + atom
    def check_complementary(self, clause):
        for atom in clause:
            if self.get_negative_atom(atom) in clause:
                return True
        return False
    def norm_clause(self, clause):
        clause = list(dict.fromkeys(clause))
        tuple_form = []
        for atom in clause:
            if atom[0] == '-':
                tuple_form.append((atom[1], -1))
            else:
                tuple_form.append((atom[0], 1))
        tuple_form.sort()
        res = []
        for tup in tuple_form:
            if tup[1] == -1:
                res.append('-' + tup[0])
            else:
                res.append(tup[0])
        return res
    def check_satisfaction(self, kb, old_clause, new_clause):
        if old_clause == new_clause:
            return False
        elif not new_clause:
            return False      
        else:
            return True
    def resolve(self, new_kb, clause_1, clause_2):
        new_clause = []
        for atom in clause_1:
            neg_atom = self.get_negative_atom(atom)
            if neg_atom in clause_2:
                new_clause_1 = clause_1[:]
                new_clause_2 = clause_2[:]
                new_clause_1.remove(atom)
                new_clause_2.remove(neg_atom)
                if not new_clause_1 and not new_clause_2:
                    new_clause.append('{}')
                else:
                    clause = new_clause_1 + new_clause_2
                    clause = self.norm_clause(clause)
                    if not self.check_complementary(clause) and clause not in new_kb:
                        new_clause = clause
        return new_clause
    def PL_Resolution(self, knowledge_base):
        new_kb = knowledge_base.clauses[:]
        for statement in knowledge_base.negative_statement:
            new_kb.append([statement])
        statement = knowledge_base.statement
        new_clauses = []
        while 1:
            bases = []            
            for clause1 in new_kb:
                for clause2 in new_kb:
                    if clause1 != clause2:
                        resolvent = self.resolve(new_kb, clause1, clause2)
                        if self.check_satisfaction(new_kb, clause1, resolvent):
                            if resolvent not in bases and resolvent not in new_kb:
                                bases += [resolvent]
                                if ['{}'] in bases:
                                    new_clauses += [bases]
                                    return new_clauses, True
            new_kb += bases
            new_clauses += [bases]
            if not bases:
                return new_clauses, False


def extract_or(clause):
    clause = clause.split()
    clause = list(filter(lambda x:x != 'OR', clause))
    clause.sort(key=lambda x: x.lower().lstrip('-'))
    return clause

def read_file(file_path):
    try:
        with open(file_path) as file:
            content = file.read().splitlines()
            statement = content[0]
            statement = extract_or(statement)
            size = content[1]
            clauses = content[2:]
            new_clauses = []
            for clause in clauses:
                new_clauses.append(extract_or(clause))
            return statement, size, new_clauses
    except:
        print("Cannot open", file_path)

def write_file(file_name, new_set, check):
    with open(file_name, 'w') as file:
        for items in new_set:
            file.write(str(len(items))+'\n')
            for item in items:
                for index, i  in enumerate(item):
                    file.write(str(i))
                    if (index != len(item) - 1):
                        file.write(' OR ')
                file.write('\n')
        if check == True:
            file.write("YES")
        else:
            file.write("NO")

def main():
    file_names = os.listdir(INPUT_PATH)
    for index, file_name in enumerate(file_names):
        if file_name.endswith('.txt'):
            statement, size, clauses = read_file(os.path.join(INPUT_PATH, file_name))
            knowledge_base = KnowldegeBase(statement, size, clauses)
            new_set, check = knowledge_base.PL_Resolution(knowledge_base)
            write_file(OUTPUT_PATH + "/output" + str(index + 1).zfill(2) + '.txt', new_set, check)

if __name__ == '__main__':
    main() 