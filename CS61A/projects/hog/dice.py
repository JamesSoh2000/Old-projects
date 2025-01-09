def feline_fixes(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    if limit < 0: # Fill in the condition
        # BEGIN
        "*** YOUR CODE HERE ***"
        return 0
        # END

    elif len(start) == 0 or len(goal) == 0:  # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        return len(start) or len(goal)  # Fill in these lines
        # END

    else:
        if start[0] == goal[0]:
            return feline_fixes(start[1:], goal[1:], limit)

        add_diff = feline_fixes(start, goal[1:], limit-1)  # Fill in these lines
        remove_diff = feline_fixes(start[1:], goal, limit-1)
        substitute_diff = feline_fixes(start[1:], goal[1:], limit-1)
        # BEGIN
        "*** YOUR CODE HERE ***"
        return min(add_diff,remove_diff,substitute_diff) + 1
        # END