from generate_fee_bill import generate_fee_bill
import os
import shutil

if __name__ == "__main__":
    from sample_data import fee_bill_data

    buff = generate_fee_bill(fee_bill_data)["document"]

    with open(
            os.path.expanduser("~/Desktop/fee_bill.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
