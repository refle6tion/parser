from tokeniser import tokenise
import re


class parser:
    def parser(self, string):
        self.tokens = tokenise(string)
        self.position = 0
        return self.program()

    def current(self):
        return self.tokens[self.position]

    def match(self, token_type):
        token = self.current()
        if token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, got {token.type} at position {token.position}"
            )
        self.position += 1
        return token

    def program(self):
        files = []
        while self.current().type != "EOF":
            files.append(self.file())
        self.match("EOF")
        return {
            "type": "program",
            "files": files,
        }

    def file(self):
        diff = self.match("DIFF")
        index = self.match("INDEX").value if self.current().type == "INDEX" else None
        old_file = self.match("OLD_FILE")
        new_file = self.match("NEW_FILE")
        hunks = []

        while self.current().type == "HUNK":
            hunks.append(self.hunk())

        return {
            "type": "file",
            "diff": diff.value,
            "index": index,
            "old_file": old_file.value,
            "new_file": new_file.value,
            "hunks": hunks,
        }

    def hunk(self):
        header = self.match("HUNK")
        match = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", header.value)
        if not match:
            raise SyntaxError(f"Bad hunk header at position {header.position}: {header.value}")
        old_line = int(match.group(1))
        new_line = int(match.group(3))
        old_count = int(match.group(2) or 1)
        new_count = int(match.group(4) or 1)
        old_file_lines = {}
        new_file_lines = {}

        while self.current().type in {"ADDED", "REMOVED", "CONTEXT"}:
            token = self.current()
            self.position += 1
            if token.type == "ADDED":
                new_file_lines[new_line] = token.value
                new_line += 1
            elif token.type == "REMOVED":
                old_file_lines[old_line] = token.value
                old_line += 1
            else:
                old_line += 1
                new_line += 1

        count_diff = new_count - old_count
        change = {
            "type": "added" if count_diff > 0 else "removed" if count_diff < 0 else "unchanged",
            "lines": abs(count_diff),
        }

        return {
            "type": "hunk",
            "header": header.value,
            "old_start": int(match.group(1)),
            "old_count": old_count,
            "new_start": int(match.group(3)),
            "new_count": new_count,
            "line_change": change,
            "old_file_lines": old_file_lines,
            "new_file_lines": new_file_lines,
        }
