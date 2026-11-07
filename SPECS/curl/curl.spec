# SPDX-FileCopyrightText: (C) 2025, 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025, 2026 openRuyi Project Contributors
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: yyjeqhc <jialin.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

# Ignore results for tests marked flaky or timing-dependent.
%global _test_target test-nonflaky

%bcond openssl 0

Name:           curl
Version:        8.23.0
Release:        %autorelease
Summary:        A Tool for Transferring Data from URLs
License:        curl
URL:            https://curl.se
VCS:            git:https://github.com/curl/curl
#!RemoteAsset:  sha256:8dadd7d2536a314f982ad05a651b713f426bf7d02cc2c76cffb9796f2218e6c5
Source0:        https://curl.se/download/curl-%{version}.tar.xz
BuildSystem:    autotools

BuildOption(conf):  --enable-hsts
BuildOption(conf):  --enable-ipv6
BuildOption(conf):  --enable-ldap
BuildOption(conf):  --enable-ldaps
BuildOption(conf):  --with-libidn2
BuildOption(conf):  --with-nghttp2
BuildOption(conf):  --with-nghttp3
BuildOption(conf):  --with-ngtcp2
BuildOption(conf):  --enable-docs
BuildOption(conf):  --with-gssapi
BuildOption(conf):  --with-brotli
BuildOption(conf):  --with-libssh
BuildOption(conf):  --enable-symbol-hiding
BuildOption(conf):  --disable-static
BuildOption(conf):  --enable-threaded-resolver
BuildOption(conf):  --with-ca-bundle=%{_sysconfdir}/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
%if %{with openssl}
BuildOption(conf):  --with-openssl
%else
BuildOption(conf):  --with-gnutls
%endif

BuildOption(check):  TFLAGS="-j%{_smp_build_ncpus}"

BuildRequires:  groff
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libidn2)
BuildRequires:  pkgconfig(libnghttp2)
BuildRequires:  pkgconfig(libnghttp3)
BuildRequires:  pkgconfig(libngtcp2)
BuildRequires:  pkgconfig(libpsl)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(ldap)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(libbrotlidec)
BuildRequires:  pkgconfig(libssh)
%if %{with openssl}
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(libngtcp2_crypto_ossl)
%else
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(libngtcp2_crypto_gnutls)
%endif
# Test requires
BuildRequires:  nghttp2-tools
BuildRequires:  openssh-clients
BuildRequires:  openssh-server
BuildRequires:  perl
BuildRequires:  stunnel
BuildRequires:  pkgconfig(python3)
Requires:       ca-certificates

%description
Curl is a client to get documents and files from or send documents to a
server using any of the supported protocols (HTTP, HTTPS, FTP, FTPS,
TFTP, DICT, TELNET, LDAP, or FILE). The command is designed to work
without user interaction or any kind of interactivity.

%package        devel
Summary:        Development files for the curl library
Requires:       glibc-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Curl is a client to get documents and files from or send documents to a
server using any of the supported protocols (HTTP, HTTPS, FTP, GOPHER,
DICT, TELNET, LDAP, or FILE). The command is designed to work without
user interaction or any kind of interactivity.

%install -a
rm -f %{buildroot}%{_libdir}/libcurl.la

%files
%doc README RELEASE-NOTES CHANGES.md
%doc docs/{BUGS.md,FAQ,FEATURES.md,TODO,TheArtOfHttpScripting.md}
%license COPYING
%{_bindir}/curl
%{_bindir}/wcurl
%{_mandir}/man1/curl.*
%{_mandir}/man1/wcurl.*
%{_libdir}/libcurl.so.4*

%files devel
%{_bindir}/curl-config
%{_includedir}/curl
%dir %{_datadir}/aclocal/
%{_datadir}/aclocal/libcurl.m4
%{_libdir}/libcurl.so
%{_libdir}/pkgconfig/libcurl.pc
%{_mandir}/man1/curl-config.*
%{_mandir}/man3/*
%doc docs/libcurl/symbols-in-versions
%license COPYING

%changelog
%autochangelog
