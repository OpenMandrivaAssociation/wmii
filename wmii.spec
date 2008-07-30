
Summary: Window Manager Improved 2, a X11 window manager for hackers
Name: wmii
Version: 3.6
License: MIT
Release: %mkrel 4
Group: Graphical desktop/Other
URL: http://wmii.cat-v.org/
Source: http://wmii.cat-v.org/download/wmii-%{version}.tar.bz2
Source1: http://wmii.cat-v.org/uploads/WMI/wmipaper.pdf.bz2
Patch1: 02-cflags.dpatch
Patch2: 03-font.dpatch
BuildRoot: %{_tmppath}/root-%{name}-%{version}
BuildRequires: gcc
BuildRequires: freetype2-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: cairo-devel
BuildRequires: python-pyrex
BuildRequires: X11-devel
BuildRequires: X11-static-devel
BuildRequires: libixp-devel
Requires: xterm xmessage dwm-tools


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
%setup -q -n wmii-%{version}
bunzip2 -c %{SOURCE1} > wmipaper.pdf

%patch1 -p1
%patch2 -p1

%build
%ifarch x86_64
sed -i -e "/^LIBDIR/s|=.*|= /usr/lib64|" config.mk
%endif

sed -i \
    -e "/^PREFIX/s|=.*|= /usr|" \
    -e "/^ETC/s|=.*|= /etc/X11|" \
    config.mk

make PREFIX=%{_prefix} CONFPREFIX=%{_sysconfdir}/X11 MANPREFIX=%{_mandir} LIBIXP=/usr/lib/libixp.a STATIC=""

%install
%{__rm} -rf %{buildroot}

make install PREFIX=%{buildroot}/usr ETC=%{buildroot}/etc/X11 LIBIXP=/usr/lib/libixp.a

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

#%clean
#%{__rm} -rf ${buildroot}

%post
%make_session

%postun
%make_session

%files
%defattr(0644, root, root, 0755)
%attr(0755, root, root) %{_bindir}/*
%{_mandir}/man*/*
%dir %_sysconfdir/X11/wmii-3.5
%attr(0755, root, root) %config(noreplace) %_sysconfdir/X11/wmii-3.5/*
%config(noreplace) %_sysconfdir/X11/wmsession.d/19%name
%doc LICENSE README wmipaper.pdf

%files devel
%defattr(0644, root, root, 0755)
%{_libdir}/*.a
%{_includedir}/*
%doc LICENSE README
