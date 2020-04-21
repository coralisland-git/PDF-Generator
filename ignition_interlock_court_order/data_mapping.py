class interlockCourtOrder:
    def __init__(self):
        self.data_dict = {}

    def convertToStr(list_of_vals):
        ret_str = ""

    def header(self):
        self.data_dict["name"] = "ANSH ROY FROM TEXAS"
        self.data_dict["case_number"] = "E67963"
        self.data_dict["citation_number"] = ["E67963", "F34943"]
        self.data_dict["license_number"] = "GA 060274748"
        self.data_dict["charge"] = [
            "DRIVING WHILE LIC SUSPENDED",
            "DRIVING WHILE INTOXICATED",
        ]

    def body(self):
        self.data_dict["check_box"] = {"1": True, "2": False, "3": False, "4": False}
        self.data_dict[
            "notes"
        ] = """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
            incididunt ut labore et dolore magna aliqua. Egestas diam in arcu cursus euismod 
            quis viverra. Libero id faucibus nisl tincidunt eget nullam. Velit scelerisque in 
            dictum non consectetur a erat. Amet mattis vulputate enim nulla aliquet porttitor 
            lacus. Facilisis mauris sit amet massa vitae tortor condimentum lacinia quis. Ac 
            turpis egestas integer eget aliquet nibh. Orci phasellus egestas tellus rutrum 
            tellus pellentesque eu tincidunt tortor. Morbi tristique senectus et netus et. 
            Malesuada bibendum arcu vitae elementum curabitur vitae nunc sed velit. Pellentesque 
            habitant morbi tristique senectus et netus et. Nulla facilisi morbi tempus iaculis 
            urna id. Egestas purus viverra accumsan in nisl. Pellentesque id nibh tortor id aliquet 
            lectus proin nibh. Vitae elementum curabitur vitae nunc sed velit dignissim sodales ut. 
            Eu feugiat pretium nibh ipsum consequat nisl vel pretium.
            """

    def getDict(self):
        return self.data_dict

    def __str__(self):
        return str(self.data_dict)


def data_mapping():
    generate = interlockCourtOrder()
    generate.header()
    generate.body()
    return generate.getDict()


if __name__ == "__main__":
    hehe = interlockCourtOrder()
    hehe.header()
    hehe.body()
    print(hehe)
