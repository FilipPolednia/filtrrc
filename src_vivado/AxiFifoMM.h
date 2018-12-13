/*
 * AxiFifoMM.h
 *
 *  Created on: Sep 27, 2018
 *      Author: michal
 */

#ifndef SRC_AXIFIFOMM_H_
#define SRC_AXIFIFOMM_H_

#include "xllfifo.h"

#include <vector>

class AxiFifoMM {
public:
	AxiFifoMM(unsigned DEVICE_ID);
	~AxiFifoMM();

	void write(std::vector<uint32_t> buffer);
	std::vector<uint32_t> read();

private:
	XLlFifo FifoInstance;
	int Status;

	void init(unsigned DEVICE_ID);
};

#endif /* SRC_AXIFIFOMM_H_ */
