
Summary: Window Manager Improved 2, a X11 window manager for hackers
Name: wmii
Version: 3.1
License: MIT
Release: %mkrel 1
Group: Graphical desktop/Other
URL: http://www.wmii.de/
Source: http://wmii.de/download/wmii-%{version}.tar.bz2
Source1: http://wmi.modprobe.de/uploads/WMI/wmipaper.pdf.bz2
Patch0: wmii-lib.patch
# Patch1: wmii.wmii.patch.bz2
BuildRoot: %{_tmppath}/root-%{name}-%{version}
BuildRequires: gcc
BuildRequires: freetype2-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: cairo-devel
BuildRequires: pyrex
BuildRequires: X11-devel
BuildRequires: X11-static-devel
Requires: xterm


%description
WMI is a new lightweight window manager for X11, which attempts to
combine the best features of LarsWM, Ion, evilwm and ratpoison into 
one window manager.

window manager improved 2 - is the next generation of the WMI 
project. Due to a complete rewrite it is highly modularized and 
uses a new configuration and inter-process communication interface 
which is oriented on the 9p protocol of the plan9 operating system. 
It achieves following goals: 

reduction of compile time 
reduction of memory usage 
reduction of lines of code 
performance improvements 
improved rendering capabilities (optional cairo) 
improved configuration and IPC interface (libixp) 
modularized components 

wmi was a single binary. Due to the modularization wmii consists of 
following binaries: 

wmii (core window manager) 
wmiinput (input mode) 
wmibar (generic bar, also usable for basic menus) 
wmipager (workspace pager) 
wmir (next generation wmiremote) 
wmirat (the rat - shortcut handler)

%package devel
Summary: Window Manager Improved 2 devel files
Group: Development/C

%description devel
WMI is a new lightweight window manager for X11, which attempts to
combine the best features of LarsWM, Ion, evilwm and ratpoison into
one window manager.


%prep
%setup -n wmii-%{version}
%patch0 -p1
#%patch1 -p0
bunzip2 -c %{SOURCE1} > wmipaper.pdf

%build
%ifarch x86_64
perl -pi -e "s|^X11LIB.*|X11LIB=/usr/X11R6/lib64|" $RPM_BUILD_DIR/%name-%realversion/config.mk
%endif

%make PREFIX=%{_prefix} CONFPREFIX=%{_sysconfdir} MANPREFIX=%{_mandir} \
  INCDIR=%{_includedir} LIBDIR=%{_libdir} LIB=%{_lib}

%install
%{__rm} -rf %{buildroot}

# Note: the makeinstall macro doesn't use DESTDIR correctly.
%{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} CONFPREFIX=%{_sysconfdir} MANPREFIX=%{_mandir} \
  INCDIR=%{_includedir} LIBDIR=%{_libdir}  LIB=%{_lib} install

# install devel files
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
find lib* -name '*.a' -exec cp {} $RPM_BUILD_ROOT%{_libdir} \; -print
find lib* -name '*.h' -exec cp {} $RPM_BUILD_ROOT%{_includedir} \; -print

# Install generated scripts to hook up WMI into gdm, xdm, and Co.
%__mkdir -p $RPM_BUILD_ROOT%_sysconfdir/X11/wmsession.d
%__cat >    $RPM_BUILD_ROOT%_sysconfdir/X11/wmsession.d/19%name << EOF
NAME=%name
EXEC=%{_bindir}/%name
DESC=%summary
SCRIPT:
exec %{_bindir}/%name
EOF

%clean
%{__rm} -rf ${buildroot}

%post
%make_session

%postun
%make_session

%files
%defattr(0644, root, root, 0755)
%attr(0755, root, root) %{_bindir}/*
%{_mandir}/man*/*
%dir %_sysconfdir/wmii-3
%attr(0755, root, root) %config(noreplace) %_sysconfdir/wmii-3/*
%config(noreplace) %_sysconfdir/X11/wmsession.d/19%name
%doc LICENSE README wmipaper.pdf

%files devel
%defattr(0644, root, root, 0755)
%{_libdir}/*.a
%{_includedir}/*
%doc LICENSE README

