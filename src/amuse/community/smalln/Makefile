# standard amuse configuration include
# config.mk will be made after ./configure has run
ifeq ($(origin AMUSE_DIR), undefined)
  AMUSE_DIR := $(shell amusifier --get-amuse-dir)
endif
-include ${AMUSE_DIR}/config.mk

# Makefile to build the worker code.  First draft was auto-generated;
# subsequent versions are hand-coded, so save a copy.  Note that
# all compiles must use MPICXX, not CXX.

ALL	 = smallN_worker
OPT	  = -I$(AMUSE_DIR)/lib/stopcond

MPICXX   ?= mpicxx
SC_FLAGS ?= -I$(AMUSE_DIR)/lib/stopcond
SC_CLIBS  ?=  -L$(AMUSE_DIR)/lib/stopcond -lstopcondmpi 

CFLAGS   += -Wall -g $(OPT) -Isrc
CXXFLAGS += $(CFLAGS) $(SC_FLAGS)
LDFLAGS  += $(SC_CLIBS) -lm $(MUSE_LD_FLAGS)

OBJS = interface.o

AM_LIBS = -L$(AMUSE_DIR)/lib/amuse_mpi -lamuse_mpi
AM_CFLAGS = -I$(AMUSE_DIR)/lib/amuse_mpi

CODELIB = src/libsmallN.a


all: $(ALL)

$(CODELIB):
	make -C src all CXX='$(MPICXX)'

worker_code.cc: interface.py
	$(CODE_GENERATOR) --type=c interface.py SmallNInterface -o $@

interface.h: interface.py
	$(CODE_GENERATOR) --type=h interface.py -i amuse.community.interface.stopping_conditions.StoppingConditionInterface  SmallNInterface -o $@

smallN_worker: worker_code.cc interface.h $(CODELIB) $(OBJS)
	$(MPICXX) $(CXXFLAGS) $(LDFLAGS) worker_code.cc $(OBJS) $(CODELIB) -o $@ $(LDFLAGS) $(LIBS)

%.o: %.cc
	$(MPICXX) $(CXXFLAGS) -c -o $@ $< 

clean:
	$(RM) -r -f *.so *.dSYM *.o *.pyc worker_code.cc interface.h 
	$(RM) -f *~ smallN_worker worker_code.cc
	make -C src clean

distclean: clean
