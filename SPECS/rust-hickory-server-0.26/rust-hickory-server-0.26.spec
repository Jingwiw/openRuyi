# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Jingwiw <wangjingwei@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global crate_name hickory-server
%global full_version 0.26.1
%global pkgname hickory-server-0.26

Name:           rust-hickory-server-0.26
Version:        0.26.1
Release:        %autorelease
Summary:        Rust crate "hickory-server"
License:        MIT OR Apache-2.0
URL:            https://hickory-dns.org/
#!RemoteAsset:  sha256:130236ba6abba90da6a7acf7a87b27d862b592c3145dc74bc47bf86d8ff198ec
Source:         https://static.crates.io/crates/%{crate_name}/%{full_version}/download#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    rustcrates

BuildRequires:  rust-rpm-macros

Requires:       crate(async-trait-0.1/default) >= 0.1.43
Requires:       crate(bytes-1/default) >= 1.0.0
Requires:       crate(cfg-if-1/default) >= 1.0.0
Requires:       crate(data-encoding-2) >= 2.2.0
Requires:       crate(futures-util-0.3/std) >= 0.3.5
Requires:       crate(hickory-net-0.26/tokio) >= 0.26.0
Requires:       crate(hickory-proto-0.26/serde) >= 0.26.0
Requires:       crate(hickory-proto-0.26/std) >= 0.26.0
Requires:       crate(ipnet-2/serde) >= 2.3.0
Requires:       crate(ipnet-2/std) >= 2.3.0
Requires:       crate(prefix-trie-0.8/default) >= 0.8.0
Requires:       crate(serde-1/default) >= 1.0.0
Requires:       crate(serde-1/derive) >= 1.0.0
Requires:       crate(thiserror-2) >= 2.0.0
Requires:       crate(time-0.3/default) >= 0.3.0
Requires:       crate(tokio-1/default) >= 1.21.0
Requires:       crate(tokio-1/macros) >= 1.21.0
Requires:       crate(tokio-1/net) >= 1.21.0
Requires:       crate(tokio-1/sync) >= 1.21.0
Requires:       crate(tokio-util-0.7/default) >= 0.7.9
Requires:       crate(tracing-0.1) >= 0.1.30

Provides:       crate(%{pkgname}) = %{version}
Provides:       crate(%{pkgname}/default) = %{version}
Provides:       crate(%{pkgname}/dnssec) = %{version}
Provides:       crate(%{pkgname}/testing) = %{version}

%description
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
Source code for takopackized Rust crate "hickory-server"

%package     -n %{name}+h3
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "__h3"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/quic) = %{version}
Requires:       crate(h3-0.0.8/default) >= 0.0.8
Requires:       crate(h3-quinn-0.0.10/default) >= 0.0.10
Provides:       crate(%{pkgname}/h3) = %{version}

%description -n %{name}+h3
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "__h3" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+https
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "__https"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/tls) = %{version}
Requires:       crate(h2-0.4/default) >= 0.4.0
Requires:       crate(h2-0.4/stream) >= 0.4.0
Requires:       crate(http-1/default) >= 1.1.0
Provides:       crate(%{pkgname}/https) = %{version}

%description -n %{name}+https
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "__https" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+tls
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "__tls" and 1 more
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(rustls-0.23/logging) >= 0.23.23
Requires:       crate(rustls-0.23/std) >= 0.23.23
Requires:       crate(rustls-0.23/tls12) >= 0.23.23
Requires:       crate(tokio-rustls-0.26) >= 0.26.0
Provides:       crate(%{pkgname}/quic) = %{version}
Provides:       crate(%{pkgname}/tls) = %{version}

%description -n %{name}+tls
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "__tls" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

Additionally, this package also provides the "__quic" feature.

%package     -n %{name}+dnssec-aws-lc-rs
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "dnssec-aws-lc-rs"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/dnssec) = %{version}
Requires:       crate(hickory-proto-0.26/dnssec-aws-lc-rs) >= 0.26.0
Requires:       crate(hickory-proto-0.26/serde) >= 0.26.0
Requires:       crate(hickory-proto-0.26/std) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/dnssec-aws-lc-rs) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Requires:       crate(serde-1/derive) >= 1.0.0
Requires:       crate(serde-1/rc) >= 1.0.0
Provides:       crate(%{pkgname}/dnssec-aws-lc-rs) = %{version}

%description -n %{name}+dnssec-aws-lc-rs
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "dnssec-aws-lc-rs" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+dnssec-ring
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "dnssec-ring"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/dnssec) = %{version}
Requires:       crate(hickory-proto-0.26/dnssec-ring) >= 0.26.0
Requires:       crate(hickory-proto-0.26/serde) >= 0.26.0
Requires:       crate(hickory-proto-0.26/std) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/dnssec-ring) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Requires:       crate(serde-1/derive) >= 1.0.0
Requires:       crate(serde-1/rc) >= 1.0.0
Provides:       crate(%{pkgname}/dnssec-ring) = %{version}

%description -n %{name}+dnssec-ring
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "dnssec-ring" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+h3-aws-lc-rs
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "h3-aws-lc-rs"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/h3) = %{version}
Requires:       crate(%{pkgname}/quic-aws-lc-rs) = %{version}
Requires:       crate(hickory-net-0.26/h3-aws-lc-rs) >= 0.26.0
Requires:       crate(hickory-net-0.26/tokio) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/h3-aws-lc-rs) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Provides:       crate(%{pkgname}/h3-aws-lc-rs) = %{version}

%description -n %{name}+h3-aws-lc-rs
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "h3-aws-lc-rs" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+h3-ring
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "h3-ring"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/h3) = %{version}
Requires:       crate(%{pkgname}/quic-ring) = %{version}
Requires:       crate(hickory-net-0.26/h3-ring) >= 0.26.0
Requires:       crate(hickory-net-0.26/tokio) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/h3-ring) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Provides:       crate(%{pkgname}/h3-ring) = %{version}

%description -n %{name}+h3-ring
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "h3-ring" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+https-aws-lc-rs
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "https-aws-lc-rs"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/https) = %{version}
Requires:       crate(%{pkgname}/tls-aws-lc-rs) = %{version}
Requires:       crate(hickory-net-0.26/https-aws-lc-rs) >= 0.26.0
Requires:       crate(hickory-net-0.26/tokio) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/https-aws-lc-rs) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Provides:       crate(%{pkgname}/https-aws-lc-rs) = %{version}

%description -n %{name}+https-aws-lc-rs
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "https-aws-lc-rs" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+https-ring
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "https-ring"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/https) = %{version}
Requires:       crate(%{pkgname}/tls-ring) = %{version}
Requires:       crate(hickory-net-0.26/https-ring) >= 0.26.0
Requires:       crate(hickory-net-0.26/tokio) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/https-ring) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Provides:       crate(%{pkgname}/https-ring) = %{version}

%description -n %{name}+https-ring
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "https-ring" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+metrics
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "metrics"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(hickory-resolver-0.26/metrics) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Requires:       crate(metrics-0.24/default) >= 0.24.1
Provides:       crate(%{pkgname}/metrics) = %{version}

%description -n %{name}+metrics
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "metrics" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+quic-aws-lc-rs
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "quic-aws-lc-rs"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/quic) = %{version}
Requires:       crate(%{pkgname}/tls-aws-lc-rs) = %{version}
Requires:       crate(hickory-net-0.26/quic-aws-lc-rs) >= 0.26.0
Requires:       crate(hickory-net-0.26/tokio) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/quic-aws-lc-rs) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Provides:       crate(%{pkgname}/quic-aws-lc-rs) = %{version}

%description -n %{name}+quic-aws-lc-rs
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "quic-aws-lc-rs" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+quic-ring
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "quic-ring"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/quic) = %{version}
Requires:       crate(%{pkgname}/tls-ring) = %{version}
Requires:       crate(hickory-net-0.26/quic-ring) >= 0.26.0
Requires:       crate(hickory-net-0.26/tokio) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/quic-ring) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Provides:       crate(%{pkgname}/quic-ring) = %{version}

%description -n %{name}+quic-ring
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "quic-ring" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+recursor
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "recursor"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(hickory-resolver-0.26/recursor) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Provides:       crate(%{pkgname}/recursor) = %{version}

%description -n %{name}+recursor
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "recursor" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+resolver
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "resolver" and 1 more
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Provides:       crate(%{pkgname}/blocklist) = %{version}
Provides:       crate(%{pkgname}/resolver) = %{version}

%description -n %{name}+resolver
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "resolver" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

Additionally, this package also provides the "blocklist" feature.

%package     -n %{name}+rustls-platform-verifier
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "rustls-platform-verifier"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(hickory-resolver-0.26/rustls-platform-verifier) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Provides:       crate(%{pkgname}/rustls-platform-verifier) = %{version}

%description -n %{name}+rustls-platform-verifier
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "rustls-platform-verifier" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+sqlite
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "sqlite"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(rusqlite-0.39/bundled) >= 0.39.0
Requires:       crate(rusqlite-0.39/default) >= 0.39.0
Requires:       crate(rusqlite-0.39/time) >= 0.39.0
Provides:       crate(%{pkgname}/sqlite) = %{version}

%description -n %{name}+sqlite
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "sqlite" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+tls-aws-lc-rs
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "tls-aws-lc-rs"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/tls) = %{version}
Requires:       crate(hickory-net-0.26/tls-aws-lc-rs) >= 0.26.0
Requires:       crate(hickory-net-0.26/tokio) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tls-aws-lc-rs) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Provides:       crate(%{pkgname}/tls-aws-lc-rs) = %{version}

%description -n %{name}+tls-aws-lc-rs
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "tls-aws-lc-rs" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+tls-ring
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "tls-ring"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(%{pkgname}/tls) = %{version}
Requires:       crate(hickory-net-0.26/tls-ring) >= 0.26.0
Requires:       crate(hickory-net-0.26/tokio) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tls-ring) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Provides:       crate(%{pkgname}/tls-ring) = %{version}

%description -n %{name}+tls-ring
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "tls-ring" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+toml
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "toml"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/toml) >= 0.26.0
Requires:       crate(toml-1/default) >= 1.0.1
Provides:       crate(%{pkgname}/toml) = %{version}

%description -n %{name}+toml
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "toml" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+webpki-roots
Summary:        Integrating safe and secure DNS servers into an async Tokio application - feature "webpki-roots"
Requires:       crate(%{pkgname}) = %{version}
Requires:       crate(hickory-resolver-0.26/serde) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/system-config) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/tokio) >= 0.26.0
Requires:       crate(hickory-resolver-0.26/webpki-roots) >= 0.26.0
Provides:       crate(%{pkgname}/webpki-roots) = %{version}

%description -n %{name}+webpki-roots
It supports a variety of protocol features (DNSSEC, TSIG, SIG(0), DoT, DoQ, DoH). Servers can be operated in an authoritative role, or as a forwarding resolver, stub resolver, or a recursive resolver (experimental).
This metapackage enables feature "webpki-roots" for the Rust hickory-server crate, by pulling in any additional dependencies needed by that feature.

%files
%{_datadir}/cargo/registry/%{crate_name}-%{version}/

%changelog
%autochangelog
