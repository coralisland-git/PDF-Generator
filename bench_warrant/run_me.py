import os
import shutil

from generate_bench_warrant import generate_bench_warrant

if __name__ == "__main__":
    from sample_data import bench_warrant_data

    with open(
        os.path.expanduser("~/Desktop/bench_warrant.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(
            generate_bench_warrant(bench_warrant_data),
            output_file,
        )

    print("completed")
