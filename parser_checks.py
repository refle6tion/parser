from parser2 import parser
from tokeniser import tokenise


def run_checks(verbose=False):
    assert tokenise("")[-1].type == "EOF"
    assert len(tokenise(r"\ No newline at end of file")) == 1

    sample = """diff --git a/src/index.js b/src/index.js
index 83a90c3..4f11b2b 100644
--- a/src/index.js
+++ b/src/index.js
@@ -1,7 +1,8 @@
 function greetUser(name) {
-  if (!name) {
-    return "Hello, Guest!";
-  }
-  return "Hello, " + name + "!";
+  if (name === "Admin") {
+    return "Welcome back, Administrator!";
+  }
+  const userName = name || "Guest";
+  return `Hello, ${userName}!`;
 }
"""
    result = parser().parser(sample)
    file = result["files"][0]
    hunk = file["hunks"][0]

    checks = [
        (file["old_file"], "a/src/index.js"),
        (file["new_file"], "b/src/index.js"),
        (hunk["old_start"], 1),
        (hunk["old_count"], 7),
        (hunk["new_start"], 1),
        (hunk["new_count"], 8),
        (hunk["line_change"], {"type": "added", "lines": 1}),
        (hunk["old_file_lines"][2], "  if (!name) {"),
        (hunk["old_file_lines"][5], "  return \"Hello, \" + name + \"!\";"),
        (hunk["new_file_lines"][2], "  if (name === \"Admin\") {"),
        (hunk["new_file_lines"][6], "  return `Hello, ${userName}!`;"),
    ]
    for actual, expected in checks:
        if actual != expected:
            raise AssertionError(f"Expected {expected!r}, got {actual!r}")

    if verbose:
        print("parser checks passed")


if __name__ == "__main__":
    run_checks(verbose=True)
