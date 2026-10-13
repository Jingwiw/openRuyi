# SPDX-FileCopyrightText: (C) 2025, 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025, 2026 openRuyi Project Contributors
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: yyjeqhc <jialin.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
# SPDX-FileContributor: Suyun <ziyu.oerv@isrc.iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

# default without systemd
%bcond systemd 0

Name:           krb5
Version:        1.22.2
Release:        %autorelease
Summary:        The Kerberos 5 network authentication system
License:        MIT
URL:            https://web.mit.edu/kerberos/
VCS:            git:https://github.com/krb5/krb5
#!RemoteAsset:  sha256:3243ffbc8ea4d4ac22ddc7dd2a1dc54c57874c40648b60ff97009763554eaf13
Source:         https://kerberos.org/dist/krb5/1.22/%{name}-%{version}.tar.gz
Source1:        kadmind.service
Source2:        kpropd.service
BuildSystem:    autotools

# Fix C23 strchr const handling: https://github.com/krb5/krb5/commit/ad4dcf1856dadc4b352b5c8ff08e51c7290fb41f
Patch0:         1000-fix-strchr-conformance-to-c23.patch
# Initialize PKINIT test data: https://github.com/krb5/krb5/commit/34d661676b1db04d870be3d7ad26616aa69d1f3d
Patch1:         1001-initialize-pkinit-test-data.patch

BuildOption(conf):  --without-ldap
BuildOption(conf):  --disable-static
BuildOption(conf):  --enable-dns-for-realm
BuildOption(conf):  --disable-rpath
BuildOption(conf):  --enable-pkinit
BuildOption(conf):  --with-crypto-impl=openssl
BuildOption(conf):  --with-system-et
BuildOption(conf):  --with-system-ss
BuildOption(conf):  --with-system-verto
BuildOption(conf):  --with-lmdb
BuildOption(conf):  --localstatedir=%{_localstatedir}
BuildOption(build):  -C src
BuildOption(install):  -C src
# Run tests serially because test realms share listener ports.
BuildOption(check):  -C src -j1

BuildRequires:  autoconf
BuildRequires:  bison
BuildRequires:  make
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(cmocka)
BuildRequires:  pkgconfig(libkeyutils)
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(com_err)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  libverto-libev
BuildRequires:  pkgconfig(libverto)
BuildRequires:  pkgconfig(lmdb)
BuildRequires:  pkgconfig(ss)

%if %{with systemd}
BuildRequires:  systemd-rpm-macros
%endif

%if %{with systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

Requires:       libverto-libev%{?_isa}

%description
Kerberos is a network authentication system. This package contains all the
core libraries, clients, servers, and plugins.

%package        devel
Summary:        Development files for MIT Kerberos 5
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig(libkeyutils)
Requires:       pkgconfig(com_err)
Requires:       pkgconfig(libverto)
Requires:       pkgconfig(ss)

%description    devel
This package contains the libraries, header files, and documentation needed
for developing applications that use Kerberos 5.

%conf -p
cd src
export DEFCCNAME=DIR:/run/user/%%{uid}/krb5cc
autoreconf -fi

%install -a
install -D -m 644 src/util/ac_check_krb5.m4 %{buildroot}%{_datadir}/aclocal/ac_check_krb5.m4
install -d -m 755 %{buildroot}%{_sysconfdir}/krb5.conf.d

install -d -m 700 %{buildroot}%{_localstatedir}/kerberos/krb5kdc

%if %{with systemd}
install -d -m 755 %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/kadmind.service
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/kpropd.service
%endif

install -m 644 src/config-files/krb5.conf %{buildroot}%{_sysconfdir}/krb5.conf
install -m 644 src/config-files/kdc.conf %{buildroot}%{_sysconfdir}/kdc.conf

%if %{with systemd}
%post
%systemd_post kadmind.service kpropd.service
%preun
%systemd_preun kadmind.service kpropd.service
%postun
%systemd_postun_with_restart kadmind.service kpropd.service
%endif

%files
%license doc/notice.rst
%doc doc/
%config(noreplace) %{_sysconfdir}/kdc.conf
%config(noreplace) %{_sysconfdir}/krb5.conf
%dir %{_sysconfdir}/krb5.conf.d
%dir %attr(0700,root,root) %{_localstatedir}/kerberos
%dir %attr(0700,root,root) %{_localstatedir}/kerberos/krb5kdc
%if %{with systemd}
%{_unitdir}/kadmind.service
%{_unitdir}/kpropd.service
%endif
%{_libdir}/lib*.so.*
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%{_libdir}/krb5/plugins/*/*.so
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%exclude %{_mandir}/man1/krb5-config.1*
%exclude %{_mandir}/man5/.k5identity.5.gz
%exclude %{_mandir}/man5/.k5login.5.gz
%{_datadir}/locale/*/LC_MESSAGES/mit-krb5.mo
%dir %{_datadir}/examples
%dir %{_datadir}/examples/krb5
%{_datadir}/examples/krb5/*

%files devel
%{_includedir}/gssapi/
%{_includedir}/gssrpc/
%{_includedir}/kadm5/
%{_includedir}/kdb.h
%{_includedir}/krad.h
%{_includedir}/krb5.h
%{_includedir}/krb5/*
%{_includedir}/gssapi.h
%{_includedir}/profile.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/gssrpc.pc
%{_libdir}/pkgconfig/kadm-client.pc
%{_libdir}/pkgconfig/kadm-server.pc
%{_libdir}/pkgconfig/kdb.pc
%{_libdir}/pkgconfig/krb5-gssapi.pc
%{_libdir}/pkgconfig/krb5.pc
%{_libdir}/pkgconfig/mit-krb5-gssapi.pc
%{_libdir}/pkgconfig/mit-krb5.pc
%{_bindir}/krb5-config
%{_datadir}/aclocal/ac_check_krb5.m4
%{_mandir}/man1/krb5-config.1*
%{_mandir}/man5/.k5identity.5.gz
%{_mandir}/man5/.k5login.5.gz

%changelog
%autochangelog
