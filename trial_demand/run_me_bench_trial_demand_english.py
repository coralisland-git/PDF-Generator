import os
import shutil

from bench_trial_demand_english import bench_trial_demand_english

if __name__ == "__main__":

    with open(
        os.path.expanduser("~/Desktop/bench_trial_demand_english.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(
            bench_trial_demand_english(),
            output_file,
        )

    print("completed")