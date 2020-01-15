import os
import shutil

from generate_lvap_state_remittance_form import generate_lvap_state_remittance_form

if __name__ == "__main__":
    from sample_data import lvap_state_remittance_form_data

    with open(
        os.path.expanduser("~/Desktop/lvap_state_remittance_form.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(
            generate_lvap_state_remittance_form(lvap_state_remittance_form_data),
            output_file,
        )

    print("completed")
