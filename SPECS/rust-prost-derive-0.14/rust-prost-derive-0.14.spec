# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
#
# SPDX-License-Identifier: MulanPSL-2.0

%global crate_name prost-derive
%global full_version 0.14.4
%global pkgname prost-derive-0.14

Name:           rust-prost-derive-0.14
Version:        0.14.4
Release:        %autorelease
Summary:        Rust crate "prost-derive"
License:        Apache-2.0
URL:            https://github.com/tokio-rs/prost
#!RemoteAsset:  sha256:b570b25f7617e43d59005d0990ccb79e950a423952cea19671b7a876da390adf
Source:         https://static.crates.io/crates/%{crate_name}/%{full_version}/download#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    rustcrates

BuildRequires:  rust-rpm-macros

Requires:       crate(anyhow-1/default) >= 1.0.1
Requires:       crate(itertools-0.10/default) >= 0.10.1
Requires:       crate(proc-macro2-1/default) >= 1.0.60
Requires:       crate(quote-1/default) >= 1.0.0
Requires:       crate(syn-2/default) >= 2.0.0
Requires:       crate(syn-2/extra-traits) >= 2.0.0

Provides:       crate(%{pkgname}) = %{version}
Provides:       crate(%{pkgname}/default) = %{version}

%description
Source code for takopackized Rust crate "prost-derive"

%files
%{_datadir}/cargo/registry/%{crate_name}-%{version}/

%changelog
%autochangelog
