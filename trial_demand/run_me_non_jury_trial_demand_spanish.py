import os
import shutil

from non_jury_trial_demand_spanish import non_jury_trial_demand_spanish

if __name__ == "__main__":

    with open(
        os.path.expanduser("~/Desktop/non_jury_trial_demand_spanish.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(
            non_jury_trial_demand_spanish(),
            output_file,
        )

    print("completed")