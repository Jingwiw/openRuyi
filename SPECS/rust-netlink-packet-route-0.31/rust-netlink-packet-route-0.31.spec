# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Jingwiw <wangjingwei@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global crate_name netlink-packet-route
%global full_version 0.31.0
%global pkgname netlink-packet-route-0.31

Name:           rust-netlink-packet-route-0.31
Version:        0.31.0
Release:        %autorelease
Summary:        Rust crate "netlink-packet-route"
License:        MIT
URL:            https://github.com/rust-netlink/netlink-packet-route
#!RemoteAsset:  sha256:e2288fcb784eb3defd5fb16f4c4160d5f477de192eac730f43e1d11c24d9a007
Source:         https://static.crates.io/crates/%{crate_name}/%{full_version}/download#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    rustcrates

BuildRequires:  rust-rpm-macros

Requires:       crate(bitflags-2/default) >= 2.0.0
Requires:       crate(libc-0.2/default) >= 0.2.66
Requires:       crate(log-0.4/default) >= 0.4.20
Requires:       crate(log-0.4/std) >= 0.4.20
Requires:       crate(netlink-packet-core-0.8/default) >= 0.8.0

Provides:       crate(%{pkgname}) = %{version}
Provides:       crate(%{pkgname}/default) = %{version}

%description
Source code for takopackized Rust crate "netlink-packet-route"

%files
%{_datadir}/cargo/registry/%{crate_name}-%{version}/

%changelog
%autochangelog
