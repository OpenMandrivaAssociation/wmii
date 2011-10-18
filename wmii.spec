%define	changeset	f3d88385ea7c

Summary: Window Manager Improved 2, a X11 window manager for hackers
Name: wmii
Version: 3.10
License: MIT
Release: %mkrel -c b1 1
Group: Graphical desktop/Other
URL: http://wmii.suckless.org/
Source0: hg.suckless.org/wmii/archive/%{changeset}.tar.gz

BuildRequires: freetype2-devel
BuildRequires: cairo-devel
BuildRequires: python-pyrex
BuildRequires: X11-devel
BuildRequires: libixp-devel > 0.5
BuildRequires: python-devel
Requires:	xterm
Requires:	xmessage 
Requires:	dwm-tools


%description
WMii is a dynamic window manager for X11.  It supports classic and tiled 
window management with extended keyboard, mouse, and 9P-based remote control.  
It consists of the wmii window manager and the wmiir the remote access utility.

%package python
Summary: Window Manager Improved 2 python files
Group: Graphical desktop/Other

%description python
Python files for %{name}.

%package devel
Summary: Window Manager Improved 2 devel files
Group: Development/C

%description devel
Development files for %{name}.


%prep
%setup -qn %{name}-%{changeset}

%build
sed -i \
    -e "/^PREFIX/s|=.*|= /usr|" \
    -e "/ETC/s|=.*|= /etc/X11|" \
%ifarch x86_64
	-e "s|/usr/lib|/usr/lib64|g" \
	-e "/ LIBDIR/s|=.*|= /usr/lib64|" \
%endif
    config.mk

%make

%install
%makeinstall_std

# install devel files
mkdir -p %{buildroot}%{_includedir}
find lib* -name '*.a' -exec cp {} %{buildroot}%{_libdir} \; -print
find lib* -name '*.h' -exec cp {} %{buildroot}%{_includedir} \; -print

# Install generated scripts to hook up WMI into gdm, xdm, and Co.
mkdir -p %{buildroot}%_sysconfdir/X11/wmsession.d
cat >    %{buildroot}%_sysconfdir/X11/wmsession.d/19%name << EOF
NAME=%name
EXEC=%{_bindir}/%name
DESC=%summary
SCRIPT:
exec %{_bindir}/%name
EOF


%if %mdkversion < 200900
%post
%make_session

%postun
%make_session
%endif

%files
%defattr(0644, root, root, 0755)
%doc LICENSE README 
%attr(0755, root, root) %{_bindir}/*
%{_mandir}/man1/*
%dir %_sysconfdir/X11/wmii-hg/
%attr(0755, root, root) %config(noreplace) %_sysconfdir/X11/%{name}-hg/*
%config(noreplace) %_sysconfdir/X11/wmsession.d/19%name

%files python
%defattr(0644, root, root, 0755)
%py_puresitedir

%files devel
%defattr(0644, root, root, 0755)
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*

