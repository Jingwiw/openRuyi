# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: yyjeqhc <jialin.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           nghttp2
Version:        1.69.0
Release:        %autorelease
Summary:        Implementation of Hypertext Transfer Protocol version 2 in C
License:        MIT
URL:            https://nghttp2.org/
VCS:            git:https://github.com/nghttp2/nghttp2
#!RemoteAsset:  sha256:1fb324b6ec2c56f6bde0658f4139ffd8209fa9e77ce98fd7a5f63af8d0e508ad
Source0:        https://github.com/nghttp2/nghttp2/releases/download/v%{version}/nghttp2-%{version}.tar.xz
BuildSystem:    autotools

BuildOption(conf):  --disable-static
BuildOption(conf):  --disable-silent-rules
BuildOption(conf):  --enable-app
BuildOption(conf):  --enable-http3
BuildOption(conf):  --disable-examples
BuildOption(conf):  --disable-hpack-tools
BuildOption(conf):  --with-libxml2

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  python3-rpm-macros
BuildRequires:  tzdata
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(openssl) >= 3.5.0
BuildRequires:  pkgconfig(libev) >= 4.11
BuildRequires:  pkgconfig(libcares) >= 1.16.0
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libngtcp2) >= 1.16.0
BuildRequires:  pkgconfig(libngtcp2_crypto_ossl) >= 1.16.0
BuildRequires:  pkgconfig(libnghttp3) >= 1.12.0

%description
This is an implementation of Hypertext Transfer Protocol version 2.

The framing layer of HTTP/2 is implemented as a form of reusable C library.
On top of that, we have implemented HTTP/2 client, server and proxy. We
have also developed load test and benchmarking tool for HTTP/2.

HPACK encoder and decoder are available as public API.

%package        devel
Summary:        Development files for nghttp2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for usage with libnghttp2, which implements
Hypertext Transfer Protocol version 2.

%package        tools
Summary:        HTTP/2 and HTTP/3 clients, servers and load testing tools
Requires:       tzdata
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
This package provides nghttp, nghttpd, nghttpx and h2load for HTTP
requests, serving, proxying and load testing.

%prep
%autosetup -p1 -n nghttp2-%{version}

%install -a
rm -f %{buildroot}%{_datadir}/nghttp2/fetch-ocsp-response
rm -f %{buildroot}%{_docdir}/nghttp2/README.rst

%files
%license COPYING
# The main package now only contains the library
%{_libdir}/libnghttp2.so.14
%{_libdir}/libnghttp2.so.14.*

%files devel
%dir %{_includedir}/%{name}/
%{_includedir}/%{name}/%{name}*.h
%{_libdir}/libnghttp2.so
%{_libdir}/pkgconfig/libnghttp2.pc

%files tools
%{_bindir}/nghttp
%{_bindir}/nghttpd
%{_bindir}/nghttpx
%{_bindir}/h2load
%{_mandir}/man1/nghttp.1*
%{_mandir}/man1/nghttpd.1*
%{_mandir}/man1/nghttpx.1*
%{_mandir}/man1/h2load.1*

%changelog
%autochangelog
