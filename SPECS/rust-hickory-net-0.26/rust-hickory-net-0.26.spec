# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Jingwiw <wangjingwei@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global crate_name hickory-net
%global full_version 0.26.1
%global pkgname hickory-net-0.26

Name:           rust-hickory-net-0.26
Version:        0.26.1
Release:        %autorelease
Summary:        Rust crate "hickory-net"
License:        MIT OR Apache-2.0
URL:            https://hickory-dns.org/
#!RemoteAsset:  sha256:e2295ed2f9c31e471e1428a8f88a3f0e1f4b27c15049592138d1eebe9c35b183
Source:         https://static.crates.io/crates/%{crate_name}/%{full_version}/download#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    rustcrates

BuildRequires:  rust-rpm-macros

Requires:       crate(async-trait-0.1/default) >= 0.1.43
Requires:       crate(cfg-if-1/default) >= 1.0.0
Requires:       crate(data-encoding-2/alloc) >= 2.2.0
Requires:       crate(futures-channel-0.3/alloc) >= 0.3.5
Requires:       crate(futures-channel-0.3/std) >= 0.3.5
Requires:       crate(futures-io-0.3/std) >= 0.3.5
Requires:       crate(futures-util-0.3/alloc) >= 0.3.5
Requires:       crate(futures-util-0.3/async-await-macro) >= 0.3.5
Requires:       crate(futures-util-0.3/std) >= 0.3.5
Requires:       crate(hickory-proto-0.26/std) >= 0.26.0
Requires:       crate(idna-1/alloc) >= 1.0.3
Requires:       crate(idna-1/compiled-data) >= 1.0.3
Requires:       crate(ipnet-2) >= 2.3.0
Requires:       crate(jni-0.22/default) >= 0.22.1
Requires:       crate(rand-0.10/alloc) >= 0.10.0
Requires:       crate(rand-0.10/std-rng) >= 0.10.0
Requires:       crate(thiserror-2) >= 2.0.0
Requires:       crate(tinyvec-1/alloc) >= 1.1.1
Requires:       crate(tinyvec-1/default) >= 1.1.1
Requires:       crate(tracing-0.1) >= 0.1.30
Requires:       crate(url-2) >= 2.5.4

Provides:       crate(%{pkgname}) = %{version}

%description
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
Source code for takopackized Rust crate "hickory-net"

%package     -n %{name}+dnssec
Summary:        Safe and secure low-level DNS library - feature "__dnssec"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(bitflags-2/default) >= 2.4.1
Requires:       crate(lru-cache-0.1/default) >= 0.1.2
Requires:       crate(parking-lot-0.12/default) >= 0.12.0
Requires:       crate(rustls-pki-types-1/default) >= 1.10.0
Requires:       crate(time-0.3/default) >= 0.3.0
Provides:       crate(%{pkgname}/dnssec) = %{version}

%description -n %{name}+dnssec
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "__dnssec" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+h3
Summary:        Safe and secure low-level DNS library - feature "__h3"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(h3-0.0.8/default) >= 0.0.8
Requires:       crate(h3-quinn-0.0.10/default) >= 0.0.10
Requires:       crate(http-1/default) >= 1.1.0
Provides:       crate(%{pkgname}/h3) = %{version}

%description -n %{name}+h3
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "__h3" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+https
Summary:        Safe and secure low-level DNS library - feature "__https"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(bytes-1/default) >= 1.0.0
Requires:       crate(h2-0.4/default) >= 0.4.0
Requires:       crate(h2-0.4/stream) >= 0.4.0
Requires:       crate(http-1/default) >= 1.1.0
Provides:       crate(%{pkgname}/https) = %{version}

%description -n %{name}+https
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "__https" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+quic
Summary:        Safe and secure low-level DNS library - feature "__quic"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(bytes-1/default) >= 1.0.0
Requires:       crate(pin-project-lite-0.2/default) >= 0.2.0
Requires:       crate(quinn-0.11/log) >= 0.11.2
Requires:       crate(quinn-0.11/runtime-tokio) >= 0.11.2
Provides:       crate(%{pkgname}/quic) = %{version}

%description -n %{name}+quic
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "__quic" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+tls
Summary:        Safe and secure low-level DNS library - feature "__tls"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/tokio) = %{version}
Requires:       crate(bytes-1/default) >= 1.0.0
Requires:       crate(rustls-0.23/logging) >= 0.23.23
Requires:       crate(rustls-0.23/std) >= 0.23.23
Requires:       crate(rustls-0.23/tls12) >= 0.23.23
Requires:       crate(tokio-rustls-0.26/early-data) >= 0.26.0
Provides:       crate(%{pkgname}/tls) = %{version}

%description -n %{name}+tls
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "__tls" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+dnssec-aws-lc-rs
Summary:        Safe and secure low-level DNS library - feature "dnssec-aws-lc-rs"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/dnssec) = %{version}
Requires:       crate(aws-lc-rs-1/aws-lc-sys) >= 1.12.3
Requires:       crate(aws-lc-rs-1/prebuilt-nasm) >= 1.12.3
Requires:       crate(aws-lc-rs-1/ring-io) >= 1.12.3
Requires:       crate(hickory-proto-0.26/dnssec-aws-lc-rs) >= 0.26.0
Requires:       crate(hickory-proto-0.26/std) >= 0.26.0
Provides:       crate(%{pkgname}/dnssec-aws-lc-rs) = %{version}

%description -n %{name}+dnssec-aws-lc-rs
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "dnssec-aws-lc-rs" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+dnssec-ring
Summary:        Safe and secure low-level DNS library - feature "dnssec-ring"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/dnssec) = %{version}
Requires:       crate(hickory-proto-0.26/dnssec-ring) >= 0.26.0
Requires:       crate(hickory-proto-0.26/std) >= 0.26.0
Requires:       crate(ring-0.17/default) >= 0.17.0
Requires:       crate(ring-0.17/std) >= 0.17.0
Provides:       crate(%{pkgname}/dnssec-ring) = %{version}

%description -n %{name}+dnssec-ring
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "dnssec-ring" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+h3-aws-lc-rs
Summary:        Safe and secure low-level DNS library - feature "h3-aws-lc-rs"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/h3) = %{version}
Requires:       crate(%{pkgname}/quic-aws-lc-rs) = %{version}
Provides:       crate(%{pkgname}/h3-aws-lc-rs) = %{version}

%description -n %{name}+h3-aws-lc-rs
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "h3-aws-lc-rs" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+h3-ring
Summary:        Safe and secure low-level DNS library - feature "h3-ring"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/h3) = %{version}
Requires:       crate(%{pkgname}/quic-ring) = %{version}
Provides:       crate(%{pkgname}/h3-ring) = %{version}

%description -n %{name}+h3-ring
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "h3-ring" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+https-aws-lc-rs
Summary:        Safe and secure low-level DNS library - feature "https-aws-lc-rs"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/https) = %{version}
Requires:       crate(%{pkgname}/tls-aws-lc-rs) = %{version}
Provides:       crate(%{pkgname}/https-aws-lc-rs) = %{version}

%description -n %{name}+https-aws-lc-rs
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "https-aws-lc-rs" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+https-ring
Summary:        Safe and secure low-level DNS library - feature "https-ring"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/https) = %{version}
Requires:       crate(%{pkgname}/tls-ring) = %{version}
Provides:       crate(%{pkgname}/https-ring) = %{version}

%description -n %{name}+https-ring
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "https-ring" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+mdns
Summary:        Safe and secure low-level DNS library - feature "mdns"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(socket2-0.6/all) >= 0.6.0
Provides:       crate(%{pkgname}/mdns) = %{version}

%description -n %{name}+mdns
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "mdns" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+quic-aws-lc-rs
Summary:        Safe and secure low-level DNS library - feature "quic-aws-lc-rs"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/quic) = %{version}
Requires:       crate(%{pkgname}/tls-aws-lc-rs) = %{version}
Requires:       crate(quinn-0.11/log) >= 0.11.2
Requires:       crate(quinn-0.11/runtime-tokio) >= 0.11.2
Requires:       crate(quinn-0.11/rustls-aws-lc-rs) >= 0.11.2
Provides:       crate(%{pkgname}/quic-aws-lc-rs) = %{version}

%description -n %{name}+quic-aws-lc-rs
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "quic-aws-lc-rs" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+quic-ring
Summary:        Safe and secure low-level DNS library - feature "quic-ring"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/quic) = %{version}
Requires:       crate(%{pkgname}/tls-ring) = %{version}
Requires:       crate(quinn-0.11/log) >= 0.11.2
Requires:       crate(quinn-0.11/runtime-tokio) >= 0.11.2
Requires:       crate(quinn-0.11/rustls-ring) >= 0.11.2
Provides:       crate(%{pkgname}/quic-ring) = %{version}

%description -n %{name}+quic-ring
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "quic-ring" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+rustls-platform-verifier
Summary:        Safe and secure low-level DNS library - feature "rustls-platform-verifier"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(rustls-platform-verifier-0.7/default) >= 0.7.0
Provides:       crate(%{pkgname}/rustls-platform-verifier) = %{version}

%description -n %{name}+rustls-platform-verifier
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "rustls-platform-verifier" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+serde
Summary:        Safe and secure low-level DNS library - feature "serde"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(serde-1/default) >= 1.0.0
Requires:       crate(serde-1/derive) >= 1.0.0
Requires:       crate(url-2/serde) >= 2.5.4
Provides:       crate(%{pkgname}/serde) = %{version}

%description -n %{name}+serde
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "serde" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+socket2
Summary:        Safe and secure low-level DNS library - feature "socket2"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(socket2-0.6/default) >= 0.6.0
Provides:       crate(%{pkgname}/socket2) = %{version}

%description -n %{name}+socket2
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "socket2" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+tls-aws-lc-rs
Summary:        Safe and secure low-level DNS library - feature "tls-aws-lc-rs"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/tls) = %{version}
Requires:       crate(tokio-rustls-0.26/aws-lc-rs) >= 0.26.0
Requires:       crate(tokio-rustls-0.26/early-data) >= 0.26.0
Provides:       crate(%{pkgname}/tls-aws-lc-rs) = %{version}

%description -n %{name}+tls-aws-lc-rs
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "tls-aws-lc-rs" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+tls-ring
Summary:        Safe and secure low-level DNS library - feature "tls-ring"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/tls) = %{version}
Requires:       crate(tokio-rustls-0.26/early-data) >= 0.26.0
Requires:       crate(tokio-rustls-0.26/ring) >= 0.26.0
Provides:       crate(%{pkgname}/tls-ring) = %{version}

%description -n %{name}+tls-ring
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "tls-ring" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+tokio
Summary:        Safe and secure low-level DNS library - feature "tokio" and 1 more
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(tokio-1/default) >= 1.21.0
Requires:       crate(tokio-1/io-util) >= 1.21.0
Requires:       crate(tokio-1/macros) >= 1.21.0
Requires:       crate(tokio-1/net) >= 1.21.0
Requires:       crate(tokio-1/rt) >= 1.21.0
Requires:       crate(tokio-1/rt-multi-thread) >= 1.21.0
Requires:       crate(tokio-1/time) >= 1.21.0
Provides:       crate(%{pkgname}/default) = %{version}
Provides:       crate(%{pkgname}/tokio) = %{version}

%description -n %{name}+tokio
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "tokio" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

Additionally, this package also provides the "default" feature.

%package     -n %{name}+webpki-roots
Summary:        Safe and secure low-level DNS library - feature "webpki-roots"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(webpki-roots-1/default) >= 1.0.0
Provides:       crate(%{pkgname}/webpki-roots) = %{version}

%description -n %{name}+webpki-roots
This is the foundational DNS protocol library used by the other higher-level Hickory DNS crates.
This metapackage enables feature "webpki-roots" for the Rust hickory-net crate, by pulling in any additional dependencies needed by that feature.

%files
%{_datadir}/cargo/registry/%{crate_name}-%{version}/

%changelog
%autochangelog
