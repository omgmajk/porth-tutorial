# Push two numbers to stack and print, simple test case
program = [
    push(35), 
    push(34), 
    plus(), 
    dump(),
    push(420),
    dump(),
    push(10),
    push(9), 
    minus(), # Can't handle negative numbers at the moment, so order here matters
    dump()
]
