#
# Conditional build:
%bcond_with	nfslock		# nfslock library (requires __libc_open symbol)

Summary:	NFS-safe locking library, includes dotlockfile program
Summary(pl.UTF-8):	Biblioteka blokowania plików uwzględniająca NFS wraz z programem dotlockfile
Name:		liblockfile
Version:	1.14
Release:	1
License:	LGPL v2+ (library), GPL v2+ (dotlockfile)
Group:		Libraries
Source0:	http://ftp.debian.org/debian/pool/main/libl/liblockfile/%{name}_%{version}.orig.tar.gz
# Source0-md5:	420c056ba0cc4d1477e402f70ba2f5eb
BuildRequires:	autoconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Liblockfile is a shared library with NFS-safe locking functions. It
includes the command-line utility ``dotlockfile''.

%description -l pl.UTF-8
liblockfile to biblioteka współdzielona z funkcjami blokowania plików
bezpiecznymi także w przypadku używania NFS-a. Zawiera działający z
linii poleceń program dotlockfile.

%package devel
Summary:	Header files for liblockfile library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki liblockfle
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is a development package for liblockfile. It includes headers and
documentation.

%description devel -l pl.UTF-8
To jest pakiet programistyczny dla liblockfile, zawiera pliki
nagłówkowe i dokumentację.

%package static
Summary:	Static liblockfile library
Summary(pl.UTF-8):	Statyczna biblioteka liblockfile
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static liblockfile library.

%description static -l pl.UTF-8
Statyczna biblioteka liblockfile.

%prep
%setup -q -n %{name}

%{__sed} -i -e 's#-g root##g' Makefile.in

%build
%{__autoconf}
%configure \
	--enable-shared \
	--with-mailgroup \
	%{?with_nfslock:--with-nfslock}

%{__make} all %{?with_nfslock:nfslib}

%install
rm -rf $RPM_BUILD_ROOT

%{makeinstall} \
	DESTDIR=$RPM_BUILD_ROOT \
	MAILGROUP=%(id -gn)

%if %{with nfslock}
%{__make} install_nfslib \
	DESTDIR=$RPM_BUILD_ROOT \
	nfslockdir=$RPM_BUILD_ROOT%{_libdir}
%endif

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT Changelog README
%attr(755,root,root) %{_bindir}/dotlockfile
%attr(755,root,root) %{_libdir}/liblockfile.so.*.*
%attr(755,root,root) %ghost %{_libdir}/liblockfile.so.1
%if %{with nfslock}
%attr(755,root,root) %{_libdir}/nfslock.so.0.1
%endif
%{_mandir}/man1/dotlockfile.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblockfile.so
%{_includedir}/lockfile.h
%{_includedir}/maillock.h
%{_mandir}/man3/lockfile_create.3*
%{_mandir}/man3/maillock.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/liblockfile.a
