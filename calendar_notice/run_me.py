import os
import shutil

from generate_calendar_notice import generate_calendar_notice

if __name__ == "__main__":
    buff = generate_calendar_notice()
    with open(
        os.path.expanduser("~/Desktop/calendar_notice.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
