class Team:
    def __init__(self, name=None, pablo=None) -> None:
        if name:
            self.name = name
        else:
            self.name = "team name"
        if pablo:
            self.pablo = int(pablo)
        else:
            self.pablo = 5000