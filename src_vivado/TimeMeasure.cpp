/*
 * TimeMeasure.cpp
 *
 *  Created on: Sep 27, 2018
 *      Author: michal
 */

#include "TimeMeasure.h"

#include "xil_printf.h"

TimeMeasure::TimeMeasure(unsigned cpu_freq) :
		FREQ(cpu_freq), tStart(0), tEnd(0) {
}

TimeMeasure::~TimeMeasure() {
}

void TimeMeasure::start() {
	XTime_GetTime(&tStart);
}

void TimeMeasure::stop() {
	XTime_GetTime(&tEnd);
}

XTime TimeMeasure::elapsed() {
	return tEnd - tStart;
}

void TimeMeasure::print_time() {
	// TODO: some more options for printing (min:sec:ms:us:ns...)
	auto time_passed_ns = (long double) (elapsed() * 2) / ((long double) FREQ / (long double) 1000000000);
	xil_printf("time_passed = %d ns\r\n", uint32_t(time_passed_ns));
}
