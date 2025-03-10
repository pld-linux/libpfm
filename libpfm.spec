#
# Conditional build:
%bcond_without	python	# Python modules (any)
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
#
%if %{without python}
%undefine	with_python2
%undefine	with_python3
%endif
Summary:	Library to encode performance events for use by perf tool
Summary(pl.UTF-8):	Biblioteka do kodowania zdarzeń związanych z wydajnością do użycia przez narzędzie perf
Name:		libpfm
Version:	4.13.0
Release:	
License:	MIT
Group:		Libraries
Source0:	https://downloads.sourceforge.net/perfmon2/%{name}-%{version}.tar.gz
# Source0-md5:	673aaf0613f8fd1d886b4c5867c2fef1
Patch0:		%{name}-build.patch
URL:		https://perfmon2.sourceforge.net/
%{?with_python2:BuildRequires:	python-devel >= 2}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
%{?with_python:BuildRequires:	swig-python >= 2}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libpfm4 is a library to help encode events for use with operating
system kernels performance monitoring interfaces. The current version
provides support for the perf_events interface available in upstream
Linux kernels since v2.6.31.

%description -l pl.UTF-8
libpfm4 to biblioteka pomagająca kodować zdarzenia do wykorzystania
przez interfejsy jądra systemu do monitorowania wydajności. Obecna
wersja zapewnia obsługę interfejsu perf_events dostępnego w jądrach
Linuksa od wersji 2.6.31.

%package devel
Summary:	Header files for libpfm 4 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libpfm 4
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libpfm 4 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libpfm 4.

%package static
Summary:	Static libpfm 4 library
Summary(pl.UTF-8):	Statyczna biblioteka libpfm 4
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libpfm 4 library.

%description static -l pl.UTF-8
Statyczna biblioteka libpfm 4.

%package -n python-perfmon
Summary:	Python 2 bindings for libpfm and perf_event_open system call
Summary(pl.UTF-8):	Wiązania Pythona 2 do libpfm i wywołania systemowego perf_event_open
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-perfmon
Python 2 bindings for libpfm and perf_event_open system call.

%description -n python-perfmon -l pl.UTF-8
Wiązania Pythona 2 do libpfm i wywołania systemowego perf_event_open.

%package -n python3-perfmon
Summary:	Python 3 bindings for libpfm and perf_event_open system call
Summary(pl.UTF-8):	Wiązania Pythona 3 do libpfm i wywołania systemowego perf_event_open
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-perfmon
Python 3 bindings for libpfm and perf_event_open system call.

%description -n python3-perfmon -l pl.UTF-8
Wiązania Pythona 3 do libpfm i wywołania systemowego perf_event_open.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	OPTIM="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	CONFIG_PFMLIB_NOPYTHON=y

cd python
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	CONFIG_PFMLIB_NOPYTHON=y \
	LDCONFIG=/bin/true

cd python
%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_libdir}/libpfm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpfm.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpfm.so
%{_includedir}/perfmon
%{_mandir}/man3/libpfm*.3*
%{_mandir}/man3/pfm_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libpfm.a

%if %{with python2}
%files -n python-perfmon
%defattr(644,root,root,755)
%dir %{py_sitedir}/perfmon
%attr(755,root,root) %{py_sitedir}/perfmon/_perfmon_int.so
%{py_sitedir}/perfmon/*.py[co]
%{py_sitedir}/perfmon-4.0-py*.egg-info
%endif

%if %{with python3}
%files -n python3-perfmon
%defattr(644,root,root,755)
%dir %{py3_sitedir}/perfmon
%attr(755,root,root) %{py3_sitedir}/perfmon/_perfmon_int.cpython-*.so
%{py3_sitedir}/perfmon/*.py
%{py3_sitedir}/perfmon/__pycache__
%{py3_sitedir}/perfmon-4.0-py*.egg-info
%endif
