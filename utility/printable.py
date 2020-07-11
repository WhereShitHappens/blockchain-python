class Printable:
    """A base class which implements printing funcionality."""
    def __repr__(self):
        return str(self.__dict__)