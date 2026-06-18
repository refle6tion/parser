class Token:
    def __init__(self, type_, value=None, position=0):
        self.type = type_
        self.value = value
        self.position = position

    def __repr__(self):
        if self.value is None:
            return f"Token({self.type!r}, position={self.position})"
        return f"Token({self.type!r}, {self.value!r}, position={self.position})"


def tokenise(string):
    tokens = []
    position = 0

    for position, line in enumerate(string.splitlines(), start=1):
        if line.startswith("diff --git "):
            tokens.append(Token("DIFF", line, position))
        elif line.startswith("index "):
            tokens.append(Token("INDEX", line, position))
        elif line.startswith("--- "):
            tokens.append(Token("OLD_FILE", line[4:], position))
        elif line.startswith("+++ "):
            tokens.append(Token("NEW_FILE", line[4:], position))
        elif line.startswith("@@ "):
            tokens.append(Token("HUNK", line, position))
        elif line.startswith("+"):
            tokens.append(Token("ADDED", line[1:], position))
        elif line.startswith("-"):
            tokens.append(Token("REMOVED", line[1:], position))
        elif line.startswith(" ") or line == "":
            tokens.append(Token("CONTEXT", line[1:] if line else "", position))
        elif line == r"\ No newline at end of file":
            pass
        else:
            raise SyntaxError(f"Unexpected line at {position}: {line!r}")

    tokens.append(Token("EOF", position=position + 1))
    return tokens
