import os
import shutil

from generate_remittance_report import generate_local_victim_remittance_report

if __name__ == "__main__":
    from sample_data import local_victim_remmitance_report_data

    with open(
        os.path.expanduser("~/Desktop/local_victim_assistance_remittance_report.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(
            generate_local_victim_remittance_report(local_victim_remmitance_report_data),
            output_file,
        )

    print("completed")
