Summary: Database-specific drivers for libdbi
Name: libdbi-drivers
Version: 0.8.3
Release: 5.1%{?dist}
Group: Development/Libraries
License: LGPLv2+
URL: http://libdbi-drivers.sourceforge.net/

Source: http://prdownloads.sourceforge.net/libdbi-drivers/%{name}-%{version}.tar.gz
Patch1: libdbi-drivers-cflags.patch
Patch2: libdbi-drivers-error-handler.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: libdbi >= 0.8
BuildRequires: libdbi-devel >= 0.8
BuildRequires: autoconf openjade docbook-style-dsssl

%description
libdbi implements a database-independent abstraction layer in C, similar to the
DBI/DBD layer in Perl. Writing one generic set of code, programmers can
leverage the power of multiple databases and multiple simultaneous database
connections by using this framework.

libdbi-drivers contains the database-specific plugins needed to connect
libdbi to particular database servers.

%package -n libdbi-dbd-mysql
Summary: MySQL plugin for libdbi
Group: Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires: mysql
BuildRequires: mysql-devel, openssl-devel

%description -n libdbi-dbd-mysql
This plugin provides connectivity to MySQL database servers through the
libdbi database independent abstraction layer. Switching a program's plugin
does not require recompilation or rewriting source code.

%package -n libdbi-dbd-pgsql
Summary: PostgreSQL plugin for libdbi
Group: Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires: postgresql-libs
BuildRequires: postgresql-devel, krb5-devel, openssl-devel

%description -n libdbi-dbd-pgsql
This plugin provides connectivity to PostgreSQL database servers through the
libdbi database independent abstraction layer. Switching a program's plugin
does not require recompilation or rewriting source code.

%package -n libdbi-dbd-sqlite
Summary: SQLite plugin for libdbi
Group: Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires: sqlite >= 3
BuildRequires: sqlite-devel

%description -n libdbi-dbd-sqlite
This plugin provides access to an embedded SQL engine using libsqlite3 through
the libdbi database independent abstraction layer. Switching a program's plugin
does not require recompilation or rewriting source code.

%clean 
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1
%patch2 -p1

autoconf

%build
# configure is broken, must pass both --with-*sql-libdir _AND_
# --with-*sql-incdir in order for --with-*sql-libdir to be used
%configure --with-mysql --with-pgsql --with-sqlite3 \
	--with-mysql-libdir=%{_libdir}/mysql \
	--with-mysql-incdir=%{_includedir} \
	--with-pgsql-libdir=%{_libdir} \
	--with-pgsql-incdir=%{_includedir} \
	--with-sqlite3-libdir=%{_libdir} \
	--with-sqlite3-incdir=%{_includedir} \
	--with-dbi-libdir=%{_libdir}

make %{?_smp_mflags}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

rm -f ${RPM_BUILD_ROOT}%{_libdir}/dbd/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/dbd/*.la
# package the docs via %doc directives
rm -rf $RPM_BUILD_ROOT%{_docdir}/libdbi-drivers

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING README
%doc drivers/mysql/dbd_mysql/*.html
%doc drivers/mysql/*.pdf
%doc drivers/pgsql/dbd_pgsql/*.html
%doc drivers/pgsql/*.pdf
%doc drivers/sqlite3/dbd_sqlite3/*.html
%doc drivers/sqlite3/*.pdf
%dir %{_libdir}/dbd

%files -n libdbi-dbd-mysql
%defattr(-,root,root)
%{_libdir}/dbd/libdbdmysql.*

%files -n libdbi-dbd-pgsql
%defattr(-,root,root)
%{_libdir}/dbd/libdbdpgsql.*

%files -n libdbi-dbd-sqlite
%defattr(-,root,root)
%{_libdir}/dbd/libdbdsqlite3.*

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.8.3-5.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Tom Lane <tgl@redhat.com> 0.8.3-3
- Rebuild for mysql 5.1

* Mon Sep  1 2008 Tom Lane <tgl@redhat.com> 0.8.3-2
- Fix mistaken external reference in libdbdsqlite3.so.  (I'm applying this
  as a patch, rather than updating to upstream's 0.8.3-1, because that isn't
  acceptable as an RPM Version tag.)
Resolves: #460734

* Mon Feb 11 2008 Tom Lane <tgl@redhat.com> 0.8.3-1
- Update to version 0.8.3.
- Code is now all licensed LGPLv2+, so adjust License tags.

* Tue Oct 30 2007 Tom Lane <tgl@redhat.com> 0.8.2-1.3
- Fix package's selection of CFLAGS to include RPM_OPT_FLAGS
Resolves: #330691

* Fri Aug  3 2007 Tom Lane <tgl@redhat.com> 0.8.2-1.2
- Correct License tag for sqlite subpackage; it's currently not same license
  as the rest of the code.

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 0.8.2-1.1
- Update to version 0.8.2-1.
- Update License tag to match code.
- Remove static libraries and .la files, per packaging guidelines.
- Fix up packaging of documentation.

* Mon Dec 11 2006 Tom Lane <tgl@redhat.com> 0.8.1a-2
- Enable building of sqlite driver
Resolves: #184568
- Rebuild needed anyway for Postgres library update

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1a-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1a-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1a-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> 0.8.1a-1
- Update to version 0.8.1a.

* Tue Apr 12 2005 Tom Lane <tgl@redhat.com> 0.7.1-3
- Rebuild for Postgres 8.0.2 (new libpq major version).

* Fri Mar 11 2005 Tom Lane <tgl@redhat.com> 0.7.1-2
- Packaging improvements per discussion with sopwith.

* Thu Mar 10 2005 Tom Lane <tgl@redhat.com> 0.7.1-1
- Import new libdbi version, splitting libdbi-drivers into a separate SRPM
  so we can track new upstream packaging.
