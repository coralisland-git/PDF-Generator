import os
import shutil

from generate_ticket_payment_breakdown import generate_ticket_payment_breakdown

if __name__ == "__main__":
    buff = generate_ticket_payment_breakdown()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("ticket_payment_breakdown")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
