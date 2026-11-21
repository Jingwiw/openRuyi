# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: yyjeqhc <jialin.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: Li Guan <guanli.oerv@isrc.iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%bcond krun 0
%bcond wasm 0
%bcond criu 0

Name:           crun
Version:        1.31
Release:        %autorelease
Summary:        OCI runtime written in C
License:        GPL-2.0-only
URL:            https://github.com/containers/crun
#!RemoteAsset:  sha256:17d04ba159fada1f1300a36b8afe869afb38bf1bbda28da052e83bb4bee20108
Source0:        https://github.com/containers/crun/releases/download/%{version}/crun-%{version}.tar.gz
BuildSystem:    autotools

BuildOption(conf):  --disable-silent-rules
BuildOption(conf):  --disable-libcrun
BuildOption(conf):  --enable-seccomp
BuildOption(conf):  --enable-systemd
%if %{with krun}
BuildOption(conf):  --with-libkrun
%endif
%if %{with wasm}
BuildOption(conf):  --with-wasmedge
%endif
%if %{with criu}
BuildOption(conf):  --enable-criu
%else
BuildOption(conf):  --disable-criu
%endif

BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(json-c) >= 0.14
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  python3-libmount
BuildRequires:  pkgconfig(python3)
%if %{with krun}
BuildRequires:  pkgconfig(libkrun)
%endif
%if %{with wasm}
BuildRequires:  wasmedge-devel
%endif
%if %{with criu}
BuildRequires:  pkgconfig(criu)
BuildRequires:  pkgconfig(libprotobuf-c)
%endif

Provides:       oci-runtime

%description
crun is a fast and low-memory OCI Container Runtime written in C.

%check
# just skip tests as the env is not support.

%files
%license COPYING
%{_bindir}/crun
%{_mandir}/man1/crun.1*
%if %{with krun}
%{_bindir}/krun
%{_mandir}/man1/krun.1*
%endif
%if %{with wasm}
%{_bindir}/crun-wasm
%endif

%changelog
%autochangelog
