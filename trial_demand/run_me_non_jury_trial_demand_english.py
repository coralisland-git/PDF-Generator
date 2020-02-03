import os
import shutil

from non_jury_trial_demand_english import non_jury_trial_demand_english

if __name__ == "__main__":

    with open(
        os.path.expanduser("~/Desktop/non_jury_trial_demand_english.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(
            non_jury_trial_demand_english(),
            output_file,
        )

    print("completed")