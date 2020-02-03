import os
import shutil

from bench_trial_demand_spanish import bench_trial_demand_spanish

if __name__ == "__main__":

    with open(
        os.path.expanduser("~/Desktop/bench_trial_demand_spanish.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(
            bench_trial_demand_spanish(),
            output_file,
        )

    print("completed")