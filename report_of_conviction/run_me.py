import os
import shutil

from report_of_conviction import report_of_conviction

if __name__ == "__main__":

    with open(
        os.path.expanduser("~/Desktop/report_of_conviction.pdf"), "wb+"        
    ) as output_file:
        shutil.copyfileobj(
            report_of_conviction(),
            output_file,
        )

    print("completed")