# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
#
# SPDX-License-Identifier: MulanPSL-2.0

%global crate_name inotify-sys
%global full_version 0.1.8
%global pkgname inotify-sys-0.1

Name:           rust-inotify-sys-0.1
Version:        0.1.8
Release:        %autorelease
Summary:        Rust crate "inotify-sys"
License:        ISC
URL:            https://github.com/hannobraun/inotify-sys
#!RemoteAsset:  sha256:c033f80b2c113cdf91ab7a33faa9cbc014726dcad99880c8609af2a370edf37d
Source:         https://static.crates.io/crates/%{crate_name}/%{full_version}/download#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    rustcrates

BuildRequires:  rust-rpm-macros

Requires:       crate(libc-0.2/default) >= 0.2.0

Provides:       crate(%{pkgname}) = %{version}
Provides:       crate(%{pkgname}/default) = %{version}
Provides:       crate(%{pkgname}/freebsd-native) = %{version}

%description
Source code for takopackized Rust crate "inotify-sys"

%files
%{_datadir}/cargo/registry/%{crate_name}-%{version}/

%changelog
%autochangelog
