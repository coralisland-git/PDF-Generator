import os
import shutil

from generate_retirement_fund_remittance_form import (
    generate_retirement_fund_remittance_form,
)

if __name__ == "__main__":
    from sample_data import retirement_fund_remittance_form_data

    with open(
        os.path.expanduser("~/Desktop/retirement_fund_remittance_form.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(
            generate_retirement_fund_remittance_form(
                retirement_fund_remittance_form_data
            ),
            output_file,
        )

    print("completed")
