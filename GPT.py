class WumpusWorldAI:
    def __init__(self, world_size):
        self.world_size = world_size
        self.knowledge_base = []

    def add_knowledge(self, statement):
        self.knowledge_base.append(statement)

    def forward_chaining(self, goal):
        inferred = {}
        count = {}

        for clause in self.knowledge_base:
            for symbol in clause:
                if symbol in inferred:
                    continue
                inferred[symbol] = False
                count[symbol] = 0

        inferred[goal] = False  # Initialize the goal symbol

        agenda = [goal]
        while agenda:
            p = agenda.pop(0)
            if p == goal:
                self.propagate(goal, inferred, count, agenda)
                return inferred[goal]

            for clause in self.knowledge_base:
                if p in clause:
                    count[p] += 1
                    if count[p] == len(clause) - 1 and not inferred[p]:
                        inferred[p] = True
                        agenda.append(p)

    def propagate(self, goal, inferred, count, agenda):
        for clause in self.knowledge_base:
            if goal in clause:
                for symbol in clause:
                    if symbol != goal:
                        count[symbol] += 1
                        if count[symbol] == len(clause) - 1 and not inferred[symbol]:
                            inferred[symbol] = True
                            agenda.append(symbol)

    def backward_chaining(self, goal):
        return self.backward_chaining_helper(goal, {})

    def backward_chaining_helper(self, goal, inferred):
        if goal in inferred:
            return inferred[goal]

        for clause in self.knowledge_base:
            if goal in clause:
                for symbol in clause:
                    if symbol != goal:
                        if not self.backward_chaining_helper(symbol, inferred):
                            return False
        inferred[goal] = True
        return True


# Example usage:
if __name__ == "__main__":
    wumpus_ai = WumpusWorldAI(world_size=(4, 4))
    wumpus_ai.add_knowledge([("Breeze", (1, 1)), ("Breeze", (1, 2))])  # Example knowledge
    print("Forward Chaining Result:", wumpus_ai.forward_chaining(("Pit", (1, 3))))
    print("Backward Chaining Result:", wumpus_ai.backward_chaining(("Pit", (1, 3))))
