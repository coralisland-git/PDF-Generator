import os
import shutil

from generate_directive_to_pull_and_clear_warrant import directive_to_pull_and_clear_warrant


if __name__ == "__main__":
    buff = directive_to_pull_and_clear_warrant()
    with open(
        os.path.expanduser("~/Desktop/directive_to_pull_and_clear_warrant.pdf"),
        "wb+",
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
