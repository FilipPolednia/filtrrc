from myhdl import block, always_seq, Signal, intbv, enum, instances


@block
def my_sum(clk, reset, axis_s_raw, axis_m_sum):
    state_t = enum('COUNT', 'WRITE_COUNT', 'WRITE_SUM')
    accumulator = Signal(intbv(0)[32:])
    counter = Signal(intbv(0)[32:])
    state = Signal(state_t.COUNT)

    @always_seq(clk.posedge, reset=reset)
    def sum_proc():
        if state == state_t.COUNT:
            axis_m_sum.tvalid.next = 0
            axis_m_sum.tlast.next = 0
            axis_s_raw.tready.next = 1
            if axis_s_raw.tvalid == 1:
                accumulator.next = accumulator + axis_s_raw.tdata
                counter.next = counter + 1
                if axis_s_raw.tlast == 1:
                    state.next = state_t.WRITE_COUNT
        elif state == state_t.WRITE_COUNT:
            axis_s_raw.tready.next = 0
            axis_m_sum.tvalid.next = 1
            axis_m_sum.tlast.next = 0
            axis_m_sum.tdata.next = counter
            if axis_m_sum.tready == 1:
                state.next = state_t.WRITE_SUM
                counter.next = 0
        elif state == state_t.WRITE_SUM:
            axis_s_raw.tready.next = 0
            axis_m_sum.tvalid.next = 1
            axis_m_sum.tlast.next = 1
            axis_m_sum.tdata.next = accumulator
            if axis_m_sum.tready == 1:
                state.next = state_t.COUNT
                accumulator.next = 0
        else:
            raise ValueError("Undefined state")

    return instances()
