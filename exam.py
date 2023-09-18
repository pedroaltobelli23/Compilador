import re

def remove_golang_comments(script):
    # Define a regular expression pattern to match both single-line and multi-line comments
    comment_pattern = r'(/\*([^*]|(\*+[^*/]))*\*+/)|(//.*)'

    # Use the re.sub() function to replace matched comments with an empty string
    script_without_comments = re.sub(comment_pattern, '', script, flags=re.MULTILINE)

    return script_without_comments

# Example usage:
golang_script = """
package main

import "fmt"

func main() {
    // This is a single-line comment
    fmt.Println("Hello, World!") // This is another comment
    /* This is a multi-line
       comment */
}
"""

cleaned_script = remove_golang_comments(golang_script)
print(cleaned_script)