# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Li Guan <guanli.oerv@isrc.iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global commit cba357068dc586e7540971eb40bb56c5e62c4de1

Name:           passt
Version:        0+git20261002.cba3570
Release:        %autorelease
Summary:        Plug A Simple Socket Transport
License:        GPL-2.0-or-later AND BSD-3-Clause
URL:            https://passt.top/passt
#!RemoteAsset:  sha256:2bd6f52562a201e8960c17d6ae459a10bb18dc7ef2e7fa617ec82a872db9e403
Source:         https://passt.top/passt/snapshot/passt-%{commit}.tar.xz
BuildSystem:    autotools

BuildOption(prep):  -p1 -n %{name}-%{commit}
BuildOption(build):  VERSION=%{version}
BuildOption(install):  DESTDIR=%{buildroot}
BuildOption(install):  prefix=%{_prefix}

BuildRequires:  make

%description
Plug A Simple Socket Transport.

# No configure.
%conf

# No tests.
%check

%files
%doc README.md doc/demo.sh
%license LICENSES/GPL-2.0-or-later.txt
%license LICENSES/BSD-3-Clause.txt
%{_mandir}/man1/passt*
%{_mandir}/man1/pasta*
%{_bindir}/passt*
%{_bindir}/pasta*
%{_bindir}/pesto
%{_mandir}/man1/pesto.1*

%changelog
%autochangelog
