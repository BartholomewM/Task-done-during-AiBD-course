import numpy as np


class Sample(object):
    def __init__(self, lst: list):
        self.data = np.array(lst, dtype=float)

    def __repr__(self):
        return f"{self.data}"

    def avarage_mean(self):
        return self.data.sum() / len(self.data)

    # def variance(self):
    #     m = self.avarage_mean()
    #     ss = 0
    #
    #     for it in np.nditer(self.data):
    #         x= (it - m)**2
    #         ss += x
    #
    #     v = ss/len(self.data)
    #
    #     return round(v, 5)

    def variance(self):
        n = len(self.data)

        s1 = np.sum(np.power(self.data, 2))
        s2 = np.power(np.sum(self.data), 2)/n

        out = (s1 - s2)/n

        return round(out, 5)

    def standard_deviation(self):
        return round(np.sqrt(self.variance()), 5)
