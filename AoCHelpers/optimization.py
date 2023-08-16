class BranchAndBound(object):
    def __init__(self, starting_state = None, solved_state = None, max_steps = 1000, states_to_keep = None, find_all_solutions = False):
        self.starting_state = starting_state
        self.solved_state = solved_state
        self.solved_state_hash = self.get_state_hash(solved_state)
        self.max_steps = max_steps
        self.states_to_keep = states_to_keep
        self.find_all_solutions = find_all_solutions

    def get_valid_moves(self, state):
        raise NotImplementedError('Subclass should override this method')
    
    def get_state_hash(self, state):
        raise NotImplementedError('Subclass should override this method')
    
    def apply_move(self, state, move):
        raise NotImplementedError('Subclass should override this method')
    
    def is_finished(self, state):
        if self.solved_state == None:
            raise ValueError('Solved state not provided')
        return self.get_state_hash(state) == self.solved_state_hash
    
    def prune_states(self, states):
        if not self.states_to_keep:
            return states
        sorted_states = sorted(states, key = lambda state: self.score_state(state), reverse=True)
        if self.states_to_keep > 1:
            return sorted_states[:self.states_to_keep]
        else:
            return sorted_states[:int(self.states_to_keep * len(states)) + 1]

    def score_state(self, state):
        raise NotImplementedError('Subclass should override this method if using pruning')
    
    def get_minimal_path(self):
        if self.starting_state is None:
            raise NotImplementedError('Subclass should provide starting state')
        
        seen_states = set()
        seen_states.add(self.get_state_hash(self.starting_state))
        current_states = [self.starting_state]
        self.current_step = 0
        self.solutions = []
        try:
            while self.current_step < self.max_steps:
                self.current_step += 1
                new_states = []
                for state in current_states:
                    for move in self.get_valid_moves(state):
                        new_state = self.apply_move(state, move)
                        if self.is_finished(new_state):
                            if self.find_all_solutions:
                                self.solutions.append((self.current_step, new_state))
                            else:
                                return (self.current_step, new_state)
                        new_state_hash = self.get_state_hash(new_state)
                        if new_state_hash not in seen_states:
                            seen_states.add(new_state_hash)
                            new_states.append(new_state)
                if not new_states:
                    if self.find_all_solutions:
                        return self.solutions
                    else:
                        raise ValueError(f'No new states found on step {self.current_step}')
                current_states = self.prune_states(new_states)
        except:
            print(f'Exception at step {self.current_step}')
            raise

        if self.find_all_solutions:
            return self.solutions
        else:
            raise ValueError(f'Could not find solution in {self.max_steps} steps ({len(seen_states)} states evaluated)')
    
class Pathfinder(BranchAndBound):
    def __init__(self, map, starting_location, target_location, allow_wrap = False, **kwargs):
        self.map = map
        self.allow_wrap = allow_wrap
        self.solved_state_hash = self.get_state_hash(target_location)
        super().__init__(starting_state = starting_location, solved_state = target_location, **kwargs)

    def neighbors(self, location):
        raise NotImplementedError
    
    def get_valid_moves(self, location):
        return [move for move in self.neighbors(location) if self.is_valid_location(move)]

    def is_valid_location(self, move):
        return self.map[move]
    
    def apply_move(self, state, move):
        return move
    
    def get_state_hash(self, state):
        return state

def ORTHOGONAL(location):
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        yield (location[0] + dx, location[1] + dy)

def ALL_DIRECT(location):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == dy == 0:
                continue
            yield (location[0] + dx, location[1] + dy)