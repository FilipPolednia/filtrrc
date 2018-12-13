from myhdl import block, instance, Signal, ResetSignal, StopSimulation, instances, delay
import os

from src.axis import Axis
from src.clk_stim import clk_stim
from src.my_rc import my_rc
from random import *
import math


@block
def testbench(vhdl_output_path=None):

    reset = ResetSignal(0, active=0, async=False)
    clk = Signal(bool(0))

    axis_raw = Axis(32)
    axis_sum = Axis(32)

    clk_gen = clk_stim(clk, period=10)

    @instance
    def reset_gen():
        reset.next = 0
        yield delay(54)
        yield clk.negedge
        reset.next = 1

    @instance
    def write_stim():
        #values = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        values = [106, 118, 151, 147, 149, 145, 155, 129, 166, 156, 141, 153, 130, 150, 160, 137, 150, 133, 105, 106, 131, 101, 112, 108, 83, 100, 102, 72, 70, 105, 78, 91, 108, 83, 93, 87, 89, 97, 114, 126, 136, 114, 146, 140, 138, 127, 127, 146, 135, 138, 148, 148, 137, 125, 161, 133, 123, 117, 116, 135, 132, 124, 90, 97, 88, 99, 105, 90, 106, 76, 90, 105, 108, 99, 102, 105, 99, 91, 116, 105, 115, 115, 117, 146, 156, 163, 135, 153, 140, 145, 138, 148, 134, 131, 131, 136, 126, 144, 127, 0]

        # values = []
        # for i in range(1, 500):
        #     values.append(int(100 + 40*random() + 30 * math.sin(2 * math.pi * 0.005 * i)))
        #
        # values.append(0)
        i = 0
        yield reset.posedge
        while i < len(values):
            yield clk.negedge
            axis_raw.tvalid.next = 1
            axis_raw.tdata.next = values[i]
            if i == len(values) - 1:
                axis_raw.tlast.next = 1
            else:
                axis_raw.tlast.next = 0
            if axis_raw.tready == 1:
                i += 1
        yield clk.negedge
        axis_raw.tvalid.next = 0

    @instance
    def read_stim():
        yield reset.posedge
        yield delay(601)
        yield clk.negedge
        axis_sum.tready.next = 1
        for _ in range(200):
        # while True:
            yield clk.negedge
            if axis_sum.tlast == 1:
                break

        for i in range(10):
            yield clk.negedge
        raise StopSimulation()

    uut = my_rc(clk, reset, axis_raw, axis_sum)

    if vhdl_output_path is not None:
        uut.convert(hdl='VHDL', path=vhdl_output_path)
    return instances()


if __name__ == '__main__':
    trace_save_path = '../out/testbench/'
    vhdl_output_path = '../out/vhdl/'
    os.makedirs(os.path.dirname(trace_save_path), exist_ok=True)
    os.makedirs(os.path.dirname(vhdl_output_path), exist_ok=True)

    tb = testbench(vhdl_output_path)
    #tb = testbench(vhdl_output_path)
    tb.config_sim(trace=True, directory=trace_save_path, name='my_rc_tb')
    tb.run_sim()
