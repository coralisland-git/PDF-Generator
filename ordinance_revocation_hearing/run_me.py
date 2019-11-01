import os
import shutil

from generate_ordinance_revocation_hearing import generate_ordinance_revocation_hearing

if __name__ == "__main__":
    from sample_data import ordinance_revocation_hearing_data

    with open(
        os.path.expanduser("ordinance_revocation_hearing.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(
            generate_ordinance_revocation_hearing(ordinance_revocation_hearing_data),
            output_file,
        )

    print("completed")
