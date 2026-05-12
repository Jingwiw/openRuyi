# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Jingwiw <wangjingwei@iscas.ac.cn>
# SPDX-FileContributor: Suyun114 <ziyu.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           libgcrypt
Version:        1.11.2
Release:        %autorelease
Summary:        The GNU Crypto Library
License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND GPL-3.0-or-later
URL:            https://gnupg.org/software/libgcrypt
VCS:            git:https://git.gnupg.org/libgcrypt.git
#!RemoteAsset:  sha256:6ba59dd192270e8c1d22ddb41a07d95dcdbc1f0fb02d03c4b54b235814330aac
Source:         https://gnupg.org/ftp/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2
BuildSystem:    autotools

BuildRequires:  pkgconfig(gpg-error)

%description
Libgcrypt is a general purpose library of cryptographic building
blocks.  It is originally based on code used by GnuPG.  It does not
provide any implementation of OpenPGP or other protocols.  Thorough
understanding of applied cryptography is required to use Libgcrypt.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Libgcrypt is a general purpose library of cryptographic building
blocks.  It is originally based on code used by GnuPG.  It does not
provide any implementation of OpenPGP or other protocols.  Thorough
understanding of applied cryptography is required to use Libgcrypt.

This package contains needed files to compile and link against the
library.

%files
%license COPYING COPYING.LIB LICENSES
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_libdir}/libgcrypt.so.*

%files devel
%license COPYING COPYING.LIB LICENSES
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_bindir}/mpicalc
%{_libdir}/libgcrypt.so
%{_libdir}/pkgconfig/libgcrypt.pc
%{_datadir}/aclocal/libgcrypt.m4
%{_includedir}/gcrypt*.h
%{_infodir}/gcrypt.info*
%{_mandir}/man1/*

%changelog
%autochangelog
