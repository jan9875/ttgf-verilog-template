SIM ?= verilator
TOPLEVEL_LANG ?= verilog

override VERILOG_SOURCES += Adder.v

COCOTB_TOPLEVEL = Adder

COCOTB_TEST_MODULES = test_adder 

include $(shell cocotb-config --makefiles)/Makefile.sim
