import os
import shutil

from generate_remittance_report import generate_remittance_report

if __name__ == "__main__":
    from sample_data import remittance_report_data

    with open(
        os.path.expanduser("remittance_report.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(
            generate_remittance_report(remittance_report_data), output_file
        )

    print("completed")
