Summary:	NFS-safe locking library, includes dotlockfile program
Name:		liblockfile
Version:	1.06.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.debian.org/debian/pool/main/libl/liblockfile/%{name}_%{version}.tar.gz
# Source0-md5:	a6ab675558e50ea8d99648f707a121a0
BuildRequires:	autoconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Liblockfile is a shared library with NFS-safe locking functions. It
includes the command-line utility ``dotlockfile''.

%package devel
Summary:	Development library for liblockfile
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is a development library for liblockfile. It includes headers and
documentation.

%prep
%setup -q

%build
%{__autoconf}
%configure \
	--enable-shared \
	--with-mailgroup

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_includedir},%{_mandir}/man{1,3}}

%{__make} install \
	MAILGROUP=%(id -gn) \
	ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/dotlockfile
%attr(755,root,root) %{_libdir}/liblockfile.so.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/liblockfile.so
%{_includedir}/lockfile.h
%{_includedir}/maillock.h
%{_mandir}/man1/dotlockfile.1*
%{_mandir}/man3/lockfile_create.3*
%{_mandir}/man3/maillock.3*
