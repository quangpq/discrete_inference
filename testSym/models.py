
class CHANTRI:
    def __init__(self, value):
        self.value = value


class MENHDE:
    def __init__(self, chantri, content):
        self.chantri = chantri
        self.content = content

    def __setattr__(self, name, value):
        if name == 'chantri' and not isinstance(value, CHANTRI):
            raise TypeError('chantri must be an CHANTRI')
        super().__setattr__(name, value)


class BIENMENHDE:
    def __init__(self, symbol, menhde):
        self.symbol = symbol
        self.menhde = menhde


class DANGMENHDE:
    def __init__(self, symbol):
        self.symbol = symbol
        self.pheptinh = None

    @classmethod
    def from_pheptinh(cls, symbol, pheptinh):
        dmd = DANGMENHDE(symbol)
        dmd.pheptinh = pheptinh
        return dmd

class PHEPTINH:
    def __init__(self):
        pass


class PHEPHOI(PHEPTINH):
    def __init__(self, md1, md2):
        super().__init__()
        self.md1 = md1
        self.md2 = md2
