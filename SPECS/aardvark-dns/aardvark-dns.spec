# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Xuhai Chang <xuhai.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: corestudy <2760018909@qq.com>
# SPDX-FileContributor: yyjeqhc <jialin.oerv@isrc.iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           aardvark-dns
Version:        2.1.0
Release:        %autorelease
License:        Apache-2.0 AND MIT AND Zlib
Summary:        Authoritative DNS server for A/AAAA container records
URL:            https://github.com/containers/aardvark-dns
#!RemoteAsset:  sha256:daf871488603e659b0501224cf0731ac317809b1d1701fc061cb4f6ae39a894f
Source0:        https://github.com/containers/aardvark-dns/archive/v%{version}.tar.gz
BuildSystem:    rust

BuildOption(build):  -- --bin aardvark-dns

BuildRequires:  cargo
BuildRequires:  rust >= 1.88
BuildRequires:  rust-rpm-macros
BuildRequires:  crate(arc-swap-1/default) >= 1.9.2
BuildRequires:  crate(chrono-0.4/default) >= 0.4.45
BuildRequires:  crate(clap-4/default) >= 4.6.5
BuildRequires:  crate(clap-4/derive) >= 4.6.5
BuildRequires:  crate(flume-0.12/default) >= 0.12.0
BuildRequires:  crate(futures-0.3/default) >= 0.3.33
BuildRequires:  crate(futures-util-0.3) >= 0.3.33
BuildRequires:  crate(hickory-net-0.26/default) >= 0.26.1
BuildRequires:  crate(hickory-net-0.26/tokio) >= 0.26.1
BuildRequires:  crate(hickory-proto-0.26/default) >= 0.26.1
BuildRequires:  crate(hickory-server-0.26/default) >= 0.26.1
BuildRequires:  crate(inotify-0.11/default) >= 0.11.4
BuildRequires:  crate(libc-0.2/default) >= 0.2.189
BuildRequires:  crate(log-0.4/default) >= 0.4.33
BuildRequires:  crate(nix-0.31/default) >= 0.31.3
BuildRequires:  crate(nix-0.31/fs) >= 0.31.3
BuildRequires:  crate(nix-0.31/net) >= 0.31.3
BuildRequires:  crate(nix-0.31/signal) >= 0.31.3
BuildRequires:  crate(syslog-7/default) >= 7.0.0
BuildRequires:  crate(tokio-1/default) >= 1.53.1
BuildRequires:  crate(tokio-1/macros) >= 1.53.1
BuildRequires:  crate(tokio-1/net) >= 1.53.1
BuildRequires:  crate(tokio-1/rt-multi-thread) >= 1.53.1
BuildRequires:  crate(tokio-1/signal) >= 1.53.1

%description
%{summary}

Forwards other requests to configured resolvers.
Read more about configuration in `src/backend/mod.rs`.

%build -p
%ifarch riscv64
export RUST_MIN_STACK=16777216
export CARGO_PROFILE_RELEASE_OPT_LEVEL=2
%endif

%install
install -Dm0755 target/release/aardvark-dns %{buildroot}%{_libexecdir}/podman/aardvark-dns

%check
# Upstream's integration tests require network namespace setup, bats, and a
# container-oriented environment. Keep the build check minimal here.

%files
%doc README.md
%license LICENSE
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/aardvark-dns

%changelog
%autochangelog
