# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Jingwiw <wangjingwei@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global crate_name hickory-proto
%global full_version 0.26.1
%global pkgname hickory-proto-0.26

Name:           rust-hickory-proto-0.26
Version:        0.26.1
Release:        %autorelease
Summary:        Rust crate "hickory-proto"
License:        MIT OR Apache-2.0
URL:            https://hickory-dns.org/
#!RemoteAsset:  sha256:0bab31817bfb44672a252e97fe81cd0c18d1b2cf892108922f6818820df8c643
Source:         https://static.crates.io/crates/%{crate_name}/%{full_version}/download#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    rustcrates

BuildRequires:  rust-rpm-macros

Requires:       crate(data-encoding-2/alloc) >= 2.2.0
Requires:       crate(idna-1/alloc) >= 1.0.3
Requires:       crate(idna-1/compiled-data) >= 1.0.3
Requires:       crate(ipnet-2) >= 2.3.0
Requires:       crate(jni-0.22/default) >= 0.22.1
Requires:       crate(once-cell-1/critical-section) >= 1.20.0
Requires:       crate(rand-0.10/alloc) >= 0.10.0
Requires:       crate(rand-0.10/std-rng) >= 0.10.0
Requires:       crate(thiserror-2) >= 2.0.0
Requires:       crate(tinyvec-1/alloc) >= 1.1.1
Requires:       crate(tinyvec-1/default) >= 1.1.1
Requires:       crate(tracing-0.1) >= 0.1.30
Requires:       crate(url-2) >= 2.5.4

Provides:       crate(%{pkgname}) = %{version}
Provides:       crate(%{pkgname}/mdns) = %{version}

%description
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
Source code for takopackized Rust crate "hickory-proto"

%package     -n %{name}+dnssec
Summary:        Safe and secure low-level DNS library - feature "__dnssec"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/std) = %{version}
Requires:       crate(bitflags-2/default) >= 2.4.1
Requires:       crate(rustls-pki-types-1/default) >= 1.10.0
Requires:       crate(time-0.3/default) >= 0.3.0
Provides:       crate(%{pkgname}/dnssec) = %{version}

%description -n %{name}+dnssec
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "__dnssec" for the Rust hickory-proto crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+access-control
Summary:        Safe and secure low-level DNS library - feature "access-control"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/std) = %{version}
Requires:       crate(prefix-trie-0.8/default) >= 0.8.0
Provides:       crate(%{pkgname}/access-control) = %{version}

%description -n %{name}+access-control
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "access-control" for the Rust hickory-proto crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+dnssec-aws-lc-rs
Summary:        Safe and secure low-level DNS library - feature "dnssec-aws-lc-rs"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/dnssec) = %{version}
Requires:       crate(aws-lc-rs-1/aws-lc-sys) >= 1.12.3
Requires:       crate(aws-lc-rs-1/prebuilt-nasm) >= 1.12.3
Requires:       crate(aws-lc-rs-1/ring-io) >= 1.12.3
Provides:       crate(%{pkgname}/dnssec-aws-lc-rs) = %{version}

%description -n %{name}+dnssec-aws-lc-rs
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "dnssec-aws-lc-rs" for the Rust hickory-proto crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+dnssec-ring
Summary:        Safe and secure low-level DNS library - feature "dnssec-ring"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/dnssec) = %{version}
Requires:       crate(ring-0.17/default) >= 0.17.0
Requires:       crate(ring-0.17/std) >= 0.17.0
Provides:       crate(%{pkgname}/dnssec-ring) = %{version}

%description -n %{name}+dnssec-ring
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "dnssec-ring" for the Rust hickory-proto crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+no-std-rand
Summary:        Safe and secure low-level DNS library - feature "no-std-rand"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(critical-section-1/default) >= 1.1.1
Requires:       crate(once-cell-1/critical-section) >= 1.20.0
Provides:       crate(%{pkgname}/no-std-rand) = %{version}

%description -n %{name}+no-std-rand
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "no-std-rand" for the Rust hickory-proto crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+serde
Summary:        Safe and secure low-level DNS library - feature "serde"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/std) = %{version}
Requires:       crate(serde-1/default) >= 1.0.0
Requires:       crate(serde-1/derive) >= 1.0.0
Requires:       crate(url-2/serde) >= 2.5.4
Provides:       crate(%{pkgname}/serde) = %{version}

%description -n %{name}+serde
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "serde" for the Rust hickory-proto crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+std
Summary:        Safe and secure low-level DNS library - feature "std" and 2 more
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(data-encoding-2/alloc) >= 2.2.0
Requires:       crate(data-encoding-2/std) >= 2.2.0
Requires:       crate(ipnet-2/std) >= 2.3.0
Requires:       crate(rand-0.10/alloc) >= 0.10.0
Requires:       crate(rand-0.10/std) >= 0.10.0
Requires:       crate(rand-0.10/std-rng) >= 0.10.0
Requires:       crate(rand-0.10/thread-rng) >= 0.10.0
Requires:       crate(ring-0.17/std) >= 0.17.0
Requires:       crate(thiserror-2/std) >= 2.0.0
Requires:       crate(tracing-0.1/std) >= 0.1.30
Requires:       crate(url-2/std) >= 2.5.4
Provides:       crate(%{pkgname}/default) = %{version}
Provides:       crate(%{pkgname}/std) = %{version}
Provides:       crate(%{pkgname}/testing) = %{version}

%description -n %{name}+std
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "std" for the Rust hickory-proto crate, by pulling in any additional dependencies needed by that feature.

Additionally, this package also provides the "default", and "testing" features.

%package     -n %{name}+wasm-bindgen
Summary:        Safe and secure low-level DNS library - feature "wasm-bindgen"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(js-sys-0.3/default) >= 0.3.44
Requires:       crate(wasm-bindgen-0.2/default) >= 0.2.58
Provides:       crate(%{pkgname}/wasm-bindgen) = %{version}

%description -n %{name}+wasm-bindgen
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "wasm-bindgen" for the Rust hickory-proto crate, by pulling in any additional dependencies needed by that feature.

%files
%{_datadir}/cargo/registry/%{crate_name}-%{version}/

%changelog
%autochangelog
