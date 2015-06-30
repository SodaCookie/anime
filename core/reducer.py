def top_level_reducer(owner, child):
    return owner

def bot_level_reducer(owner, child):
    return child

def addition_reducer(owner, child):
    return owner + child

def mult_reducer(owner, child):
    return owner * child
