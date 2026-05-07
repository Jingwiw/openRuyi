# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: yyjeqhc <jialin.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           samurai
Version:        1.3
Release:        %autorelease
Summary:        ninja-compatible build tool written in C
License:        Apache-2.0
URL:            https://github.com/michaelforney/samurai
#!RemoteAsset:  sha256:44ff119a27b343ec47a797fa8701c19b9e672230bc15f3c6a6cede9641ea6332
Source:         https://github.com/michaelforney/samurai/archive/refs/tags/%{version}.tar.gz
BuildSystem:    autotools

BuildOption(build):  CC=%{__cc}
BuildOption(install):  PREFIX=%{_prefix}
BuildOption(install):  MANDIR=%{_mandir}

BuildRequires:  make

%description
samurai is a ninja-compatible build tool written in C99
with a focus on simplicity, speed, and portability.

# No configure
%conf

# No test suite
%check

%install -a
ln -s samu %{buildroot}%{_bindir}/ninja

%files
%license LICENSE
%doc README.md
%{_bindir}/samu
%{_mandir}/man1/samu.1*


%package        ninja
Summary:        samu as ninja
Provides:       ninja
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description ninja
This package provides ninja command, implemented as a symbolic link to the samu command
of samurai package.

%files ninja
%license LICENSE
%doc README.md
%{_bindir}/ninja


%changelog
%autochangelog
