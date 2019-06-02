class Municipality(object):
    def __init__(self):
        self.config_mun = {
            "name": "Sample City Name",
            "long_name": "Village of Sample City Name",
            "county": "Lake",
            "state": "Illinois",
        }

    @property
    def name(self):
        return self.config_mun["name"]

    @property
    def long_name(self):
        return self.config_mun["long_name"]

    @property
    def county(self):
        return self.config_mun["county"]

    @property
    def state(self):
        return self.config_mun["state"]
