from myhdl import block, delay, instance


@block
def clk_stim(clk, period=10):

    low_time = int(period/2)
    high_time = period - low_time

    @instance
    def drive_clk():
        while True:
            yield delay(low_time)
            clk.next = 1
            yield delay(high_time)
            clk.next = 0

    return drive_clk
