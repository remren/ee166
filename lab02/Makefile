RTL_DIR = RTL
run:
	@echo "\n******** Makefile: Running both Python then RTL ********"
	make run_py run_rtl

run_py:
	@echo "\n******** Makefile: Running Python ********"
	python graphing_verify_RTL.py

run_rtl:
	@echo "\n******** Makefile: Running RTL ********"
	@iverilog '-Wall' '-g2012' $(RTL_DIR)/FIR_63TAP.sv $(RTL_DIR)/tb.sv  && ./a.out