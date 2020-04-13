import os
import shutil

from generate_ignition_interlock_court_order import (
    generate_ignition_interlock_court_order,
)

from data_mapping import data_mapping

if __name__ == "__main__":
    buff = generate_ignition_interlock_court_order(data_mapping())

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("ignition_interlock_court_order")),
        "wb+",
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
