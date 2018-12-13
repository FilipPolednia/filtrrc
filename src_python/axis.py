from myhdl import Signal, modbv


class Axis:
    def __init__(self, data_width):
        self.tdata = Signal(modbv(0)[data_width:])
        self.tready = Signal(bool(0))
        self.tvalid = Signal(bool(0))
        self.tlast = Signal(bool(0))
