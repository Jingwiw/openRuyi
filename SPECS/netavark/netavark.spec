# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Xuhai Chang <xuhai.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
# SPDX-FileContributor: yyjeqhc <jialin.oerv@isrc.iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           netavark
Version:        2.1.0
Release:        %autorelease
License:        Apache-2.0 AND BSD-3-Clause AND MIT
Summary:        OCI network stack
URL:            https://github.com/containers/netavark
#!RemoteAsset:  sha256:96677048168ddd1abe313e4c2e17f1cace72b60ee1bac8ca12a4bd7dfcadfbbb
Source0:        https://github.com/containers/netavark/archive/v%{version}.tar.gz
BuildSystem:    rust

BuildOption(build):  -- --bin netavark

BuildRequires:  cargo
BuildRequires:  rust >= 1.88
BuildRequires:  rust-rpm-macros
BuildRequires:  crate(anyhow-1/default) >= 1.0.93
BuildRequires:  crate(base16ct-1/default) >= 1.0.0
BuildRequires:  crate(chrono-0.4/clock) >= 0.4.45
BuildRequires:  crate(chrono-0.4/default) >= 0.4.45
BuildRequires:  crate(chrono-0.4/serde) >= 0.4.45
BuildRequires:  crate(clap-4/default) >= 4.6.5
BuildRequires:  crate(clap-4/derive) >= 4.6.5
BuildRequires:  crate(clap-4/env) >= 4.6.5
BuildRequires:  crate(env-logger-0.11/default) >= 0.11.11
BuildRequires:  crate(fs2-0.4/default) >= 0.4.3
BuildRequires:  crate(futures-channel-0.3/default) >= 0.3.33
BuildRequires:  crate(futures-core-0.3/default) >= 0.3.33
BuildRequires:  crate(futures-util-0.3/default) >= 0.3.33
BuildRequires:  crate(hyper-util-0.1/default) >= 0.1.20
BuildRequires:  crate(ipnet-2/default) >= 2.12.1
BuildRequires:  crate(ipnet-2/serde) >= 2.12.1
BuildRequires:  crate(libc-0.2/default) >= 0.2.157
BuildRequires:  crate(log-0.4/default) >= 0.4.30
BuildRequires:  crate(mozim-0.3) >= 0.3.2
BuildRequires:  crate(netlink-packet-core-0.8/default) >= 0.8.2
BuildRequires:  crate(netlink-packet-route-0.31/default) >= 0.31.0
BuildRequires:  crate(netlink-sys-0.8/default) >= 0.8.8
BuildRequires:  crate(nftables-0.6/default) >= 0.6.3
BuildRequires:  crate(nix-0.31/default) >= 0.31.3
BuildRequires:  crate(nix-0.31/net) >= 0.31.3
BuildRequires:  crate(nix-0.31/sched) >= 0.31.3
BuildRequires:  crate(nix-0.31/signal) >= 0.31.3
BuildRequires:  crate(nix-0.31/socket) >= 0.31.3
BuildRequires:  crate(nix-0.31/user) >= 0.31.3
BuildRequires:  crate(once-cell-1/default) >= 1.21.4
BuildRequires:  crate(prost-0.14/default) >= 0.14.4
BuildRequires:  crate(rand-0.10/default) >= 0.10.2
BuildRequires:  crate(regex-1/default) >= 1.13.1
BuildRequires:  crate(serde-1/default) >= 1.0.229
BuildRequires:  crate(serde-1/derive) >= 1.0.229
BuildRequires:  crate(serde-json-1/default) >= 1.0.146
BuildRequires:  crate(serde-with-3/default) >= 3.21.0
BuildRequires:  crate(sha2-0.11/default) >= 0.11.0
BuildRequires:  crate(tempfile-3/default) >= 3.27.0
BuildRequires:  crate(tokio-1/default) >= 1.53.1
BuildRequires:  crate(tokio-1/fs) >= 1.53.1
BuildRequires:  crate(tokio-1/rt) >= 1.53.1
BuildRequires:  crate(tokio-1/rt-multi-thread) >= 1.53.1
BuildRequires:  crate(tokio-1/signal) >= 1.53.1
BuildRequires:  crate(tokio-1/time) >= 1.53.1
BuildRequires:  crate(tokio-stream-0.1/default) >= 0.1.19
BuildRequires:  crate(tokio-stream-0.1/net) >= 0.1.19
BuildRequires:  crate(tonic-0.14/default) >= 0.14.6
BuildRequires:  crate(tonic-prost-0.14/default) >= 0.14.6
BuildRequires:  crate(tonic-prost-build-0.14/default) >= 0.14.6
BuildRequires:  crate(tower-0.5/default) >= 0.5.3
BuildRequires:  crate(tower-0.5/util) >= 0.5.3
BuildRequires:  crate(zbus-5/default) >= 5.18.0
BuildRequires:  make
BuildRequires:  go-md2man
# build.rs needs a protoc binary for generated DHCP proxy bindings.
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  systemd
BuildRequires:  pkgconfig(systemd)

Requires:       nftables
Requires:       aardvark-dns >= 2.0.0

%description
%{summary}

Netavark is a rust based network stack for containers. It is being
designed to work with Podman but is also applicable for other OCI
container management applications.

Netavark is a tool for configuring networking for Linux containers.
Its features include:
* Configuration of container networks via JSON configuration file
* Creation and management of required network interfaces,
    including MACVLAN networks
* All required firewall configuration to perform NAT and port
    forwarding as required for containers
* Support for firewalld and nftables
* Support for rootless containers
* Support for IPv4 and IPv6
* Support for container DNS resolution via aardvark-dns.

%build -p
%ifarch riscv64
export RUST_MIN_STACK=16777216
export CARGO_PROFILE_RELEASE_OPT_LEVEL=2
%endif
export NETAVARK_DEFAULT_FW=nftables
%__make -C docs

%install
mkdir -p bin
install -Dm0755 target/release/netavark bin/netavark

%__make DESTDIR=%{buildroot} PREFIX=%{_prefix} LIBEXECDIR=%{_libexecdir} \
  LIBEXECPODMAN=%{_libexecdir}/podman SYSTEMDDIR=%{_unitdir} install

%check
# Upstream's tests require network namespace setup, bats, and a
# container-oriented environment. Keep the build check minimal here.

%preun
%systemd_preun netavark-dhcp-proxy.service netavark-firewalld-reload.service netavark-nftables-reload.service

%postun
%systemd_postun netavark-dhcp-proxy.service netavark-firewalld-reload.service netavark-nftables-reload.service

%files
%doc README.md
%license LICENSE
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/netavark
%{_mandir}/man1/netavark.1*
%{_mandir}/man7/netavark-firewalld.7*
%{_unitdir}/netavark-dhcp-proxy.service
%{_unitdir}/netavark-dhcp-proxy.socket
%{_unitdir}/netavark-firewalld-reload.service
%{_unitdir}/netavark-nftables-reload.service

%changelog
%autochangelog
