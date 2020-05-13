import os
import shutil

from generate_fpc_evidence_log import generate_fpc_evidence_log

if __name__ == "__main__":
    buff = generate_fpc_evidence_log()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("fpc_evidence_log")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
