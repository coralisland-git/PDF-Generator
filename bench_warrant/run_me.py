import os
import shutil
import json

from generate_bench_warrant import generate_bench_warrant

if __name__ == "__main__":
    from sample_data import bench_warrant_data

    doc_result = generate_bench_warrant(bench_warrant_data)
    with open(os.path.expanduser("~/Desktop/bench_warrant.pdf"), "wb+") as output_file:
        shutil.copyfileobj(doc_result["document"], output_file)
    with open(os.path.expanduser("~/Desktop/bench_warrant.json"), "w+") as output_file:
        output_file.write(json.dumps(doc_result["metadata"], indent=4))

    print("completed")
