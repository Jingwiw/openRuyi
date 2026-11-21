# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
#
# SPDX-License-Identifier: MulanPSL-2.0

%global crate_name zbus_names
%global full_version 4.3.4
%global pkgname zbus-names-4

Name:           rust-zbus-names-4
Version:        4.3.4
Release:        %autorelease
Summary:        Rust crate "zbus_names"
License:        MIT
URL:            https://github.com/z-galaxy/zbus/
#!RemoteAsset:  sha256:d8bf88b4a3ff53e883001e0e0115b297a9d53c31b9c1edd2bfdd853e3428624e
Source:         https://static.crates.io/crates/%{crate_name}/%{full_version}/download#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    rustcrates

BuildRequires:  rust-rpm-macros

Requires:       crate(serde-1/default) >= 1.0.200
Requires:       crate(serde-1/derive) >= 1.0.200
Requires:       crate(winnow-1/default) >= 1.0.0
Requires:       crate(zvariant-5/default) >= 5.13.1
Requires:       crate(zvariant-5/enumflags2) >= 5.13.1

Provides:       crate(%{pkgname}) = %{version}
Provides:       crate(%{pkgname}/default) = %{version}

%description
Source code for takopackized Rust crate "zbus_names"

%files
%{_datadir}/cargo/registry/%{crate_name}-%{version}/

%changelog
%autochangelog
