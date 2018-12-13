/*
 * AxiFifoMM.cpp
 *
 *  Created on: Sep 27, 2018
 *      Author: michal
 */

#include "AxiFifoMM.h"
#include "xstatus.h"

AxiFifoMM::AxiFifoMM(unsigned DEVICE_ID) :
		FifoInstance( { }), Status(XST_SUCCESS) {
	init(DEVICE_ID);
}

AxiFifoMM::~AxiFifoMM() {
	// TODO Auto-generated destructor stub
}

void AxiFifoMM::init(unsigned DEVICE_ID) {
	XLlFifo_Config *Config;
	Status = XST_SUCCESS;

	/* Initialize the Device Configuration Interface driver */
	Config = XLlFfio_LookupConfig(DEVICE_ID);
	if (!Config) {
		xil_printf("No config found for %d\r\n", DEVICE_ID);
		Status = XST_FAILURE;
		return;
	}

	Status = XLlFifo_CfgInitialize(&FifoInstance, Config, Config->BaseAddress);
	if (Status != XST_SUCCESS) {
		xil_printf("Initialization failed\n\r");
		Status = Status;
		return;
	}

	/* Check for the Reset value */
	Status = XLlFifo_Status(&FifoInstance);
	XLlFifo_IntClear(&FifoInstance, 0xffffffff);
	Status = XLlFifo_Status(&FifoInstance);
	if (Status != 0x0) {
		xil_printf("\n ERROR : Reset value of ISR0 : 0x%x\tExpected : 0x0\n\r", XLlFifo_Status(&FifoInstance));
		Status = XST_FAILURE;
		return;
	}

	Status = XST_SUCCESS;
}

void AxiFifoMM::write(std::vector<uint32_t> buffer) {
	//TODO: different functions for blocking/non blocking write?
	for (auto &val : buffer) {
		XLlFifo_TxPutWord(&FifoInstance, val);
	}
	XLlFifo_iTxSetLen(&FifoInstance, (sizeof(uint32_t) * buffer.size()));

	while (!(XLlFifo_IsTxDone(&FifoInstance))) {
	}
}

std::vector<uint32_t> AxiFifoMM::read() {
	//TODO: add size request
	std::vector<uint32_t> tmp;
	auto ReceiveLength = (XLlFifo_iRxGetLen(&FifoInstance)) / sizeof(uint32_t);

	for (unsigned i = 0; i < ReceiveLength; i++) {
		tmp.push_back(XLlFifo_RxGetWord(&FifoInstance));
	}
	return tmp;
}
