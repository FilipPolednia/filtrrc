from myhdl import block, instance, Signal, ResetSignal, StopSimulation, instances, delay
import os

from axi.axis import Axis
from myhdl_sim.clk_stim import clk_stim
from my_sum import my_sum


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
        values = list(range(50, 100))
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
        while True:
            yield clk.negedge
            if axis_sum.tlast == 1:
                break

        for i in range(10):
            yield clk.negedge
        raise StopSimulation()

    uut = my_sum(clk, reset, axis_raw, axis_sum)

    if vhdl_output_path is not None:
        uut.convert(hdl='VHDL', path=vhdl_output_path)
    return instances()


if __name__ == '__main__':
    trace_save_path = '../out/testbench/'
    vhdl_output_path = '../out/vhdl/'
    os.makedirs(os.path.dirname(trace_save_path), exist_ok=True)
    os.makedirs(os.path.dirname(vhdl_output_path), exist_ok=True)

    tb = testbench(vhdl_output_path)
    tb.config_sim(trace=True, directory=trace_save_path, name='my_sum_tb')
    tb.run_sim()
