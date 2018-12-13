/*
 * TimeMeasure.h
 *
 *  Created on: Sep 27, 2018
 *      Author: michal
 */

#ifndef SRC_TIMEMEASURE_H_
#define SRC_TIMEMEASURE_H_

#include "xtime_l.h"

class TimeMeasure {
public:
	TimeMeasure(unsigned cpu_freq);
	~TimeMeasure();
	void start();
	void stop();
	XTime elapsed();
	void print_time();

private:
	unsigned FREQ;
	XTime tStart, tEnd;
};

#endif /* SRC_TIMEMEASURE_H_ */
