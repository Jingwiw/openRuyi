# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Jingwiw <wangjingwei@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global crate_name env_filter
%global full_version 2.0.0
%global pkgname env-filter-2

Name:           rust-env-filter-2
Version:        2.0.0
Release:        %autorelease
Summary:        Rust crate "env_filter"
License:        MIT OR Apache-2.0
URL:            https://github.com/rust-cli/env_logger
#!RemoteAsset:  sha256:900d271a03799a1ee8d1ca9b19893b48ca674a9284fefcfb85f05e74ed314217
Source:         https://static.crates.io/crates/%{crate_name}/%{full_version}/download#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    rustcrates

BuildRequires:  rust-rpm-macros

Requires:       crate(log-0.4/default) >= 0.4.29

Provides:       crate(%{pkgname}) = %{version}

%description
Source code for takopackized Rust crate "env_filter"

%package     -n %{name}+default
Summary:        Filter log events using environment variables - feature "default"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/regex) = %{version}
Requires:       crate(%{pkgname}/std) = %{version}
Provides:       crate(%{pkgname}/default) = %{version}

%description -n %{name}+default
This metapackage enables feature "default" for the Rust env_filter crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+regex
Summary:        Filter log events using environment variables - feature "regex"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(regex-1/perf) >= 1.12.3
Provides:       crate(%{pkgname}/regex) = %{version}

%description -n %{name}+regex
This metapackage enables feature "regex" for the Rust env_filter crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+std
Summary:        Filter log events using environment variables - feature "std"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(log-0.4/std) >= 0.4.29
Requires:       crate(regex-1/perf) >= 1.12.3
Requires:       crate(regex-1/std) >= 1.12.3
Provides:       crate(%{pkgname}/std) = %{version}

%description -n %{name}+std
This metapackage enables feature "std" for the Rust env_filter crate, by pulling in any additional dependencies needed by that feature.

%files
%{_datadir}/cargo/registry/%{crate_name}-%{version}/

%changelog
%autochangelog
