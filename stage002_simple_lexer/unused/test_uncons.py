def uncons(xs):
    return (xs[0], xs[1:])

test = [1, 2, 3, 4]
print("Test now holds %s" % test)
(untest, test) = uncons(test)
print("Untest now holds %s" % untest)
print("Test now holds %s" %test)
someother, *test = test
print(f"Someother now holds {someother} and test now holds {test}")
