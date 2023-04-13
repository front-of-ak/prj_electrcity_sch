from charges_class import Charge
from constants import ST_CHARGE


class Capacitor:
    def __init__(self, canvas, coords, side_num=5, charge=ST_CHARGE):
        self.charges_inside = [[Charge() for i in range(side_num)], [Charge() for i in range(side_num)]]

    def change_coords(self):
        pass
