import os
import shutil

from generate_bkh_bench_warrant import generate_bkh_bench_warrant

if __name__ == "__main__":
    buff = generate_bkh_bench_warrant()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("bkh_bench_warrant")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
