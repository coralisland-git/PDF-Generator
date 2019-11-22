import os
import shutil

from generate_gscca_consolidated_monthly_report import (
    generate_gscca_consolidated_monthly_report,
)

if __name__ == "__main__":
    buff = generate_gscca_consolidated_monthly_report()
    with open(
        os.path.expanduser("~/Desktop/gscca_consolidated_monthly_report.pdf"),
        "wb+",
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
