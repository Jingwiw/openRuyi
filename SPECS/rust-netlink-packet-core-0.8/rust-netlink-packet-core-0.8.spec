# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
#
# SPDX-License-Identifier: MulanPSL-2.0

%global crate_name netlink-packet-core
%global full_version 0.8.2
%global pkgname netlink-packet-core-0.8

Name:           rust-netlink-packet-core-0.8
Version:        0.8.2
Release:        %autorelease
Summary:        Rust crate "netlink-packet-core"
License:        MIT
URL:            https://github.com/rust-netlink/netlink-packet-core
#!RemoteAsset:  sha256:b897d7bd4f0af82e68d40d0344cf37e97f9c97ddf74a098de3e4da05e96ca395
Source:         https://static.crates.io/crates/%{crate_name}/%{full_version}/download#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    rustcrates

BuildRequires:  rust-rpm-macros

Requires:       crate(paste-1/default) >= 1.0.0

Provides:       crate(%{pkgname}) = %{version}
Provides:       crate(%{pkgname}/default) = %{version}

%description
Source code for takopackized Rust crate "netlink-packet-core"

%files
%{_datadir}/cargo/registry/%{crate_name}-%{version}/

%changelog
%autochangelog
