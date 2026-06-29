from types import MappingProxyType

# all bark constants stored in hertz
# values from Stanford
class BarkIndex:
    _BARK_BAND_EDGES = (0, 100, 200, 300, 400, 510, 630, 770, 920, 1080, 1270, 1480, 1720, 2000, 2320, 2700, 3150, 3700,
                       4400, 5300, 6400, 7700, 9500, 12000, 15500)
    _BARK_BAND_CENTERS = (50, 150, 250, 350, 450, 570, 700, 840, 1000, 1170, 1370, 1600, 1850, 2150, 2500, 2900, 3400,
                         4000, 4800, 5800, 7000, 8500, 10500, 13500)

    def __init__(self):
        pass

    def get_range(self, freq):
        """
        :param freq: in hertz
        :return: tuple with the two edges from the range or null if invalid
        """
        if freq < self._BARK_BAND_EDGES[0] or freq >= self._BARK_BAND_EDGES[-1]:
            return None

        left = 0
        right = len(self._BARK_BAND_EDGES) - 2

        while left <= right:
            mid = (left + right) // 2
            lower_edge = self._BARK_BAND_EDGES[mid]
            upper_edge = self._BARK_BAND_EDGES[mid + 1]

            if lower_edge <= freq < upper_edge:
                return lower_edge, upper_edge

            if freq < lower_edge:
                right = mid - 1
            else:
                left = mid + 1

        return None

    def get_edges(self):
        return self._BARK_BAND_EDGES

    def get_centers(self):
        return self._BARK_BAND_CENTERS

