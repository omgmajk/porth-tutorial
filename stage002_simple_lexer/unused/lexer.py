#   34     35     + .      asdajs
#^
#col

def find_col(line, start, predicate):
    while start < len(line) and not predicate(line[start]):
        start += 1
    return start
    
""" OLD CODE
def strip_col(line, col):
    while col < len(line) and line[col].isspace():
        col += 1

def chop_word(line, col):
    while col < len(line) and !line[col].isspace():
        col += 1
    return col

def lex_line():
    col = strip_col(line, 0) # Stripping before
    while col < len(line):
        col_end = line.find(' ', col)
        if col_end < 0:
            col_end = len(line)
        elif col_end == 0:
            assert False, "unreachable, strip_col must ensure that this never happens"
        yield (col, line[col:col_end]) # Look up usage of yield
        col = strip_col(line, col_end) # Stripping at end of iteration again
"""

def lex_line(line):
    col = find_col(line, 0, lambda x: not x.isspace()) # Advance until no space found
    while col < len(line):
        col_end = find_col(line, col, lambda x: x.isspace()) # Advance until space found
        yield (col, line[col:col_end]) # Partial return, interesting
        col = find_col(line, col_end, lambda x: not x.isspace()) # Keep advancing until next
        

def lex_file(file_path):
    with open(file_path, "r") as f:
        return [(file_path, row, col, token)
                for (row, line) in enumerate(f.readlines())
                for (col, token) in lex_line(line)]


