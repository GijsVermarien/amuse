AC_CONFIG_MACRO_DIRS([m4])

AC_INIT([amuse],[m4_esyscmd_s(python support/version.py)])
AC_CONFIG_SRCDIR([src/amuse/__init__.py])

AC_CONFIG_FILES([config.mk])
AC_CONFIG_FILES([bin/amusifier:bin/amusifier.in],[chmod +x bin/amusifier])
AC_CONFIG_FILES([Makefile])

CODE_GENERATOR=amusifier

AC_SUBST(CODE_GENERATOR)

AC_PROG_CC()
AC_PROG_CXX()
AC_PROG_FC([],95)
AS_IF([test "x$FC" = "x"], [AC_MSG_ERROR([No fortran compiler found, please set the FC flag])])
AX_FC_WORKS()
AX_FC_ISO_C_BINDING()
AC_ARG_VAR([PYTHON], [Python interpreter])

AC_SUBST(FC_ISO_C_BINDINGS)

AM_PATH_PYTHON([3.5])

AC_PATH_PROG([PYTHON], [$PYTHON], [])
AC_ARG_VAR([NVCC], [CUDA compiler command])
AC_ARG_VAR([NVCC_FLAGS], [Extra flags for the CUDA nvcc compiler])

AC_CHECK_PYTHON_DEV()

AC_ARG_VAR([JAVA_HOME], [Java sdk directory])

R_JAVA()

AC_SUBST(JAVA)
AC_SUBST(JAVA_LIBS)

AC_ARG_VAR([MPIEXEC], [mpiexec or mpirun location])
AC_PATH_PROGS(MPIEXEC, $MPIEXEC mpiexec mpirun)
AC_SUBST(MPIEXEC)

AC_ARG_ENABLE(mpi,
    [AS_HELP_STRING([--enable-mpi],[Enable MPI support for communicating with codes, by default enabled])],
    [WITH_MPI=no
    AS_IF([test "x$enable_mpi" != "xno"], [
	    AX_MPI([WITH_MPI=yes], [AC_MSG_ERROR([MPI enabled, but no MPI found])] )
    ])
    ],
    [AX_MPI([WITH_MPI=yes],[WITH_MPI=no])]
)

AC_SUBST(WITH_MPI)

AS_IF([test x"$WITH_MPI" != xno],[
    AC_LANG(C++)
    AX_MPI()
    AC_LANG(C)
    AX_MPI()
    AC_LANG(Fortran)
    AX_MPI()
], [
    MPICC="$CC"
    MPICXX="$CXX"
    MPIFC="$FC"
    
    CFLAGS="$CFLAGS -DNOMPI"
    CXXFLAGS="$CXXFLAGS -DNOMPI"
    FCFLAGS="$FCFLAGS -DNOMPI"
    
    AC_SUBST(MPICC)
    AC_SUBST(MPICXX)
    AC_SUBST(MPIFC)
]    
)

AC_LANG(C)

AC_ARG_ENABLE(openmp,
    [AS_HELP_STRING([--enable-openmp], [Turn off OpenMP support, even if it is available in the compilers])],
    [
        HAVE_OPENMP="no"
        OPENMP_CFLAGS=""
        OPENMP_FCFLAGS=""
        AS_IF([test "x$enable_openmp" != "xno"], [
            AX_OPENMP(
                 [HAVE_OPENMP="yes"]
                ,[HAVE_OPENMP="no"]
            )
            AC_LANG(Fortran)
            AX_OPENMP()
            AC_LANG(C)
        ])
    ],
    [
        AX_OPENMP(
             [HAVE_OPENMP="yes"]
            ,[HAVE_OPENMP="no"]
        )
        AC_LANG(Fortran)
        AX_OPENMP()
        AC_LANG(C)
    ]
)

AC_LANG(Fortran)
AX_GFORTRAN_VERSION()
AX_IFORT_VERSION()
    
AC_SUBST(GFORTRAN_VERSION)
AC_SUBST(IFORT_VERSION)
AC_SUBST(HAVE_OPENMP)
AC_SUBST(OPENMP_CFLAGS)
AC_SUBST(OPENMP_FCFLAGS)

AC_LANG(C)

AX_CUDA()

AC_PROG_SED()
      
AX_CHECK_CL()

#
# Sapporo 
#

AC_ARG_WITH([sapporo],
    [AS_HELP_STRING([--with-sapporo],[Use sapporo library in given directory])],
    [WITH_SAPPORO=yes],
    [WITH_SAPPORO=no]
)

AC_ARG_ENABLE(sapporo2,
    [AS_HELP_STRING([--enable-sapporo2],[Use the provided sapporo library version 2, instead of sapporo_light])],
    [SAPPORO_VERSION="light"
    SAPPORO_LIBS="-L\${AMUSE_DIR}/lib/sapporo_$SAPPORO_VERSION -lsapporo"
    AS_IF([test "x$enable_sapporo2" != "xno"], [
	SAPPORO_VERSION="2"
    AS_IF([test x$WITH_CUDA  =="xno"], [
      SAPPORO_LIBS="${CL_LIBS} ${OPENMP_CFLAGS} -L\${AMUSE_DIR}/lib/sapporo_$SAPPORO_VERSION -lsapporo"
    ], [
      SAPPORO_LIBS="${OPENMP_CFLAGS} -L\${AMUSE_DIR}/lib/sapporo_$SAPPORO_VERSION -lsapporo"
    ])
    
    ])
    ],
    [SAPPORO_VERSION="light"
    SAPPORO_LIBS="-L\${AMUSE_DIR}/lib/sapporo_$SAPPORO_VERSION -lsapporo]"
)

AC_SUBST(WITH_SAPPORO)
AC_SUBST(SAPPORO_VERSION)
AC_SUBST(SAPPORO_LIBS)

#Fortran-Sockets (FS) Libs

AS_IF([test x"$FC_ISO_C_BINDINGS" != xno],[
	FS_FLAGS="-I\$(AMUSE_DIR)/lib/forsockets"
	FS_LIBS="-L\$(AMUSE_DIR)/lib/forsockets -lforsockets"
], [
	FS_FLAGS=""
	FS_LIBS=""
]
)

AC_SUBST(FS_FLAGS)
AC_SUBST(FS_LIBS)

#Stopcond

SC_FLAGS="-I\$(AMUSE_DIR)/lib/stopcond"

SC_CLIBS="-L\$(AMUSE_DIR)/lib/stopcond -lstopcond"
SC_FCLIBS="-L\$(AMUSE_DIR)/lib/stopcond -lstopcond"
SC_MPI_CLIBS="-L\$(AMUSE_DIR)/lib/stopcond -lstopcondmpi"
SC_MPI_FCLIBS="-L\$(AMUSE_DIR)/lib/stopcond -lstopcondmpi"

AC_SUBST(SC_FLAGS)

AC_SUBST(SC_CLIBS)
AC_SUBST(SC_FCLIBS)
AC_SUBST(SC_MPI_CLIBS)
AC_SUBST(SC_MPI_FCLIBS)

AX_LAPACK([AC_MSG_NOTICE([LAPACK and BLAS found ])], 
          [AC_MSG_ERROR([LAPACK and/or BLAS not found])] )

AX_FFTW()
AX_GMP()
AX_MPFR()
AC_LANG(C++)
save_CFLAGS="$CFLAGS"
save_CPPFLAGS="$CPPFLAGS"
CFLAGS="$MPFR_FLAGS $save_CFLAGS"
CPPFLAGS="$MPFR_FLAGS $save_CPPFLAGS"
cache_var=AS_TR_SH([ac_cv_header_mpfr.h])
#AC_CHECK_HEADER(
#    [mpreal.h],
#    [],
#    [AC_MSG_WARN([Cannot find header (mpreal.h) of the library MPFR with MPFR_FLAGS $MPFR_FLAGS.])]
#)
$as_unset $cache_var
CFLAGS="$save_CFLAGS"
CPPFLAGS="$save_CPPFLAGS"
AC_LANG(C)
    
AX_LIB_HDF5()

AX_LIB_NETCDF4()

DETECT_PIC_FLAGS()
CFLAGS="$CFLAGS $PIC_FLAGS"
CXXFLAGS="$CXXFLAGS $PIC_FLAGS"
FCFLAGS="$FCFLAGS $PIC_FLAGS"

AX_PATH_GSL(1.0, [FOUND_GSL=yes], [
	FOUND_GSL=no
	AC_MSG_WARN([gsl not found, please specify --with-gsl])
])

AC_SUBST(FOUND_GSL)

AC_CHECK_PYTHON_MODULE(numpy, __version__)
AS_IF([test x"$PYTHON_numpy" != x1],
    [AC_MSG_ERROR([numpy not found, please install numpy first])]
)
AS_VERSION_COMPARE([$PYTHON_numpy_VERSION], [1.2.1],
        [AC_MSG_ERROR([numpy version $PYTHON_numpy_VERSION found, but at least 1.3.0 needed])]
)


AS_IF([test x"$WITH_MPI" != xno],[
    AC_CHECK_PYTHON_MODULE(mpi4py, __version__)
    AS_IF([test x"$PYTHON_mpi4py" != x1],
        [AC_MSG_WARN([mpi4py not found, please install mpi4py first])]
    )
    AS_IF([test x"$PYTHON_mpi4py" == x1],
        [AS_VERSION_COMPARE([$PYTHON_mpi4py_VERSION], [1.1],
            [AC_MSG_ERROR([mpi4py version $PYTHON_mpi4py_VERSION found, but at least 1.1.0 needed])]
        )]
    )
])


AC_CHECK_PYTHON_MODULE(h5py, version.version)
AS_VERSION_COMPARE([$PYTHON_h5py_VERSION], [1.1.0],
        [AC_MSG_WARN([h5py version $PYTHON_h5py_VERSION found, but at least 1.1.0 needed])]
)
AC_CHECK_PYTHON_MODULE(pytest, __version__)
AS_VERSION_COMPARE([$PYTHON_pytest_VERSION], [2.999],
        [AC_MSG_WARN([pytest version $PYTHON_pytest_VERSION found, but at least 3.0 needed])]
)
AC_CHECK_PYTHON_MODULE(docutils, __version__)
AS_VERSION_COMPARE([$PYTHON_docutils_VERSION], [0.5],
        [AC_MSG_ERROR([docutils version $PYTHON_docutils_VERSION found, but at least 0.6 needed])]
)
AC_CHECK_PYTHON_MODULE(zlib, __version__)
AS_IF([test x"$PYTHON_zlib" != x1],
    [AC_MSG_ERROR([zlib not found, please recompile python check that development libraries for zlib ar installed first])]
)
$PYTHON -c "import zlib; exit(zlib.crc32('amuse')&0xffffffff == 0xc0cc9367)" 2>/dev/null
AS_IF([test x"$?" != x1],
    [AC_MSG_ERROR([crc32 function of zlib not found, please recompile python])]
)
AS_VERSION_COMPARE([$PYTHON_zlib_VERSION], [1.0],
        [AC_MSG_ERROR([numpy version $PYTHON_zlib_VERSION found, but at least 1.0 needed])]
)
AC_CHECK_PYTHON_MODULE(matplotlib)

#AC_CHECK_PYTHON_MODULE(Cython, __version__)
#AS_VERSION_COMPARE([$PYTHON_Cython_VERSION], [0.13],
#        [AC_MSG_WARN([Cython version $PYTHON_Cython_VERSION found, but at least 0.13 needed])]
#)
AC_OUTPUT

 AC_MSG_NOTICE( Configuration done. Configuration written to config.mk )
