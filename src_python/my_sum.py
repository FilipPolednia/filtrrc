from typing import Union

from myhdl import block, always_seq, Signal, intbv, enum, instances
from myhdl._Signal import _DelayedSignal, _Signal


@block
def my_sum(clk, reset, axis_s_raw, axis_m_sum):
    state_t = enum('CALCULATE', 'END', 'START')
    vin = Signal(intbv(0)[32:].signed())
    Vin = Signal(intbv(0)[32:].signed())
    Vout = Signal(intbv(0)[32:].signed())
    d = Signal(intbv(0)[32:].signed())
    state = Signal(state_t.START)

    @always_seq(clk.posedge, reset=reset)
    def sum_proc():
        if state == state_t.START:
            Vout.next = 0
            d.next = 0
            state.next = state_t.CALCULATE

        elif state == state_t.CALCULATE:
            axis_m_sum.tvalid.next = 1
            axis_m_sum.tlast.next = 0
            axis_s_raw.tready.next = 1
            if axis_s_raw.tvalid == 1:  # jeżeli przyszły dane to:
                # vin =       #zapisz gołe dane z IPcore'a
                Vin.next = axis_s_raw.tdata * 256  # dane przesunięte w lewo by uzyskać stały przecinek
                d.next = (Vin - Vout) // 8  # przeliczenie różnicy in-out wraz z przeskalowaniem o arbitralnie ustalony czyn
                Vout.next = Vout + d  # wpisanie stanu wyjścia do akumulatora
                # axis_m_sum.tdata.next: object = Signal(Vout // 256)  # wystawienie danych na zewnątrz z przywróceniem miejsca przecinka
                axis_m_sum.tdata.next = Vout >> 8  # wystawienie danych na zewnątrz z przywróceniem miejsca przecinka
                if axis_s_raw.tlast == 1:
                    state.next = state_t.END
        elif state == state_t.END:
            axis_s_raw.tready.next = 0
            axis_m_sum.tvalid.next = 1
            axis_m_sum.tlast.next = 1
            axis_m_sum.tdata.next = d // 256  # Wypisz na koniec skumulowaną wartość offsetu sygnału
            if axis_m_sum.tready == 1:
                state.next = state_t.START
        else:
            raise ValueError("Undefined state")

    return instances()
