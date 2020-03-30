import os
import shutil

from generate_ignition_interlock_exemption import generate_ignition_interlock_exemption

if __name__ == "__main__":
    buff = generate_ignition_interlock_exemption()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("ignition_interlock_exemption")),
        "wb+",
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
