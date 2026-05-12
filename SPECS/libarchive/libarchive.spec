# SPDX-FileCopyrightText: (C) 2025, 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025, 2026 openRuyi Project Contributors
# SPDX-FileContributor: Jingwiw <wangjingwei@iscas.ac.cn>
# SPDX-FileContributor: Xuhai Chang <xuhai.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%bcond acl 1
%bcond expat 0
%bcond iconv 1
%bcond libb2 0
%bcond lz4 1
%bcond lzo2 0
%bcond mbedtls 0
%bcond nettle 0
%bcond openssl 1
%bcond xattr 1
%bcond xml2 1

Name:           libarchive
Version:        3.8.7
Release:        %autorelease
Summary:        Utility and C library to create and read several streaming archive formats
License:        BSD-2-Clause
URL:            https://www.libarchive.org/
VCS:            git:https://github.com/libarchive/libarchive
#!RemoteAsset:  sha256:d3a8ba457ae25c27c84fd2830a2efdcc5b1d40bf585d4eb0d35f47e99e5d4774
Source0:        https://github.com/libarchive/libarchive/releases/download/v%{version}/libarchive-%{version}.tar.xz
BuildSystem:    autotools

BuildOption(conf):  --disable-static
%if %{without acl}
BuildOption(conf):  --disable-acl
%endif
%if %{without xattr}
BuildOption(conf):  --disable-xattr
%endif
%if %{without expat}
BuildOption(conf):  --without-expat
%endif
%if %{without iconv}
BuildOption(conf):  --without-iconv
%endif
%if %{without libb2}
BuildOption(conf):  --without-libb2
%endif
%if %{without lz4}
BuildOption(conf):  --without-lz4
%endif
%if %{without lzo2}
BuildOption(conf):  --without-lzo2
%endif
%if %{without mbedtls}
BuildOption(conf):  --without-mbedtls
%endif
%if %{without nettle}
BuildOption(conf):  --without-nettle
%endif
%if %{without openssl}
BuildOption(conf):  --without-openssl
%endif
%if %{without xml2}
BuildOption(conf):  --without-xml2
%endif

%if %{with acl}
BuildRequires:  pkgconfig(libacl)
%endif
BuildRequires:  pkgconfig(bzip2)
%if %{with lz4}
BuildRequires:  pkgconfig(liblz4)
%endif
BuildRequires:  libtool
%if %{with xml2}
BuildRequires:  pkgconfig(libxml-2.0)
%endif
%if %{with xattr}
BuildRequires:  pkgconfig(libattr)
%endif
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(zlib)
%if %{with expat}
BuildRequires:  pkgconfig(expat)
%endif
%if %{with libb2}
BuildRequires:  pkgconfig(libb2)
%endif
%if %{with lzo2}
BuildRequires:  pkgconfig(lzo2)
%endif
%if %{with mbedtls}
BuildRequires:  pkgconfig(mbedtls)
%endif
%if %{with nettle}
BuildRequires:  pkgconfig(nettle)
%endif
%if %{with openssl}
BuildRequires:  pkgconfig(openssl)
%endif

%description
Libarchive is a programming library that can create and read several
different streaming archive formats, including most popular tar
variants and several cpio formats. It can also write shar archives and
read ISO-9660 CDROM images. The bsdtar program is an implementation of
tar(1) that is built on top of libarchive. It started as a test
harness, but has grown and is now the standard system tar for FreeBSD 5
and 6.

This package contains the bsdtar cmdline utility.

%package     -n bsdtar
Summary:        Utility to read several different streaming archive formats
Requires:       %{name}%{?_isa} >= %{version}-%{release}

%description -n bsdtar
This package contains the bsdtar cmdline utility.

%package        devel
Summary:        Development files for libarchive
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glibc-devel

%description    devel
Libarchive is a programming library that can create and read several
different streaming archive formats, including most popular tar
variants and several cpio formats. It can also write shar archives and
read ISO-9660 CDROM images. The bsdtar program is an implementation of
tar(1) that is built on top of libarchive. It started as a test
harness, but has grown and is now the standard system tar for FreeBSD 5
and 6.

This package contains the development files.

%install -a
rm "%{buildroot}%{_mandir}/man5/"{tar,cpio,mtree}.5*
sed -i -e '/Libs.private/d' %{buildroot}%{_libdir}/pkgconfig/libarchive.pc

%files -n bsdtar
%license COPYING
%{_bindir}/bsdcat
%{_bindir}/bsdcpio
%{_bindir}/bsdtar
%{_bindir}/bsdunzip
%{_mandir}/man1/*
%{_mandir}/man5/*

%files
%license COPYING
%doc NEWS
%{_libdir}/libarchive.so.*

%files devel
%license COPYING
%doc examples/
%{_mandir}/man3/*
%{_libdir}/libarchive.so
%{_includedir}/archive*
%{_libdir}/pkgconfig/libarchive.pc

%changelog
%autochangelog
