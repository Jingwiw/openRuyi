# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Jingwiw <wangjingwei@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           catatonit
Version:        0.2.1
Release:        %autorelease
Summary:        Static init process for containers
License:        GPL-2.0-or-later
URL:            https://github.com/openSUSE/catatonit
VCS:            git:https://github.com/openSUSE/catatonit.git
#!RemoteAsset:  sha256:9950425501af862e12f618bdc930ea755c46db6a16072a1462b4fc93b2bd59bc
Source0:        https://github.com/openSUSE/catatonit/releases/download/v%{version}/catatonit.tar.xz
BuildSystem:    autotools

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  glibc-static
BuildRequires:  make

%description
Catatonit forwards signals and reaps child processes inside containers.
The static executable does not require libraries from the container image.

%conf -p
autoreconf -fiv

%files
%doc README.md CHANGELOG.md
%license COPYING
%{_bindir}/catatonit

%changelog
%autochangelog
