/*
 * Empty C++ Application
 */

#include "platform.h"
#include "xil_printf.h"

#include "AxiFifoMM.h"
#include "TimeMeasure.h"

void example();
int values[100] = {106, 118, 151, 147, 149, 145, 155, 129, 166, 156, 141, 153, 130, 150, 160, 137, 150, 133, 105, 106, 131, 101, 112, 108, 83, 100, 102, 72, 70, 105, 78, 91, 108, 83, 93, 87, 89, 97, 114, 126, 136, 114, 146, 140, 138, 127, 127, 146, 135, 138, 148, 148, 137, 125, 161, 133, 123, 117, 116, 135, 132, 124, 90, 97, 88, 99, 105, 90, 106, 76, 90, 105, 108, 99, 102, 105, 99, 91, 116, 105, 115, 115, 117, 146, 156, 163, 135, 153, 140, 145, 138, 148, 134, 131, 131, 136, 126, 144, 127, 0};

int main() {
	init_platform();
	xil_printf("Starting example app\r\n");

	example();

	xil_printf("Closing example app\r\n");
	cleanup_platform();
	return 0;
}

void example() {
	AxiFifoMM fifo(XPAR_AXI_FIFO_0_DEVICE_ID);
	TimeMeasure timer(XPAR_PS7_CORTEXA9_0_CPU_CLK_FREQ_HZ);
	xil_printf("1\r\n");
	constexpr unsigned data_words_num = 100;
	xil_printf("2\r\n");
	std::vector<uint32_t> in_buff;

	for (unsigned i = 0; i < data_words_num; i++) {
		if(i == 1)
			xil_printf("3\r\n");
		in_buff.push_back(values[i]);
	}
	timer.start();
	xil_printf("4\r\n");
	fifo.write(in_buff);
	xil_printf("5\r\n");
	auto DestinationBuffer = fifo.read();
	xil_printf("6\r\n");
	timer.stop();
	for (unsigned i = 0; i < data_words_num-2; i++) {
		xil_printf("Probka nr [%d] = %d\n\r", i, DestinationBuffer[i]);
	}

	uint32_t sum = 0;
	for (auto &val : in_buff) {
		sum += val;
	}
	xil_printf("sum = %d\r\n", sum);
	timer.print_time();

}
