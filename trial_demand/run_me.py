import os
import shutil

from generate_trial_demand import generate_bench_trial_demand, generate_non_jury_trial_demand

if __name__ == "__main__":
    bench_trial_demand = generate_bench_trial_demand()
    non_jury_trial_demand = generate_non_jury_trial_demand()

    with open(
        os.path.expanduser("~/Desktop/bench_trial_demand.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(bench_trial_demand, output_file)

    with open(
        os.path.expanduser("~/Desktop/non_jury_trial_demand.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(non_jury_trial_demand, output_file)

    print("completed")
