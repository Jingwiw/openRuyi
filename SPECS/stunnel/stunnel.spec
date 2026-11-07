# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Jingwiw <wangjingwei@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global __provides_exclude_from ^%{_libdir}/stunnel/.*$

Name:           stunnel
Version:        5.82
Release:        %autorelease
Summary:        TLS proxy for network services
License:        GPL-2.0-or-later WITH stunnel-exception AND MIT
URL:            https://www.stunnel.org/
VCS:            git:https://github.com/mtrojnar/stunnel.git
#!RemoteAsset:  sha256:8e7438ccd6b3a2ab05182d0846e112a56a7f557ecdee40de07bf67820008bef7
Source0:        https://www.stunnel.org/downloads/stunnel-%{version}.tar.gz
BuildSystem:    autotools

BuildOption(conf):  --with-ssl=%{_prefix}
BuildOption(conf):  --with-bashcompdir=%{_datadir}/bash-completion/completions
BuildOption(conf):  --enable-ipv6
BuildOption(conf):  --enable-systemd
BuildOption(conf):  --disable-libwrap
BuildOption(conf):  --disable-static

BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(python3)
BuildRequires:  python3dist(cryptography)
BuildRequires:  openssl

%description
Stunnel adds TLS encryption to network services without changing their
source code. It supports client and server connections, certificate
verification and systemd socket activation.

%install -a
rm -f %{buildroot}%{_bindir}/stunnel3
rm -f %{buildroot}%{_libdir}/stunnel/*.la
install -d %{buildroot}%{_mandir}/pl/man8
mv %{buildroot}%{_mandir}/man8/stunnel.pl.8 %{buildroot}%{_mandir}/pl/man8/stunnel.8
mv %{buildroot}%{_sysconfdir}/stunnel/stunnel.conf-sample %{buildroot}%{_docdir}/stunnel/
rm -rf %{buildroot}%{_localstatedir}/lib/stunnel
rm -rf %{buildroot}%{_docdir}/stunnel/examples
install -m 644 tools/stunnel.service %{buildroot}%{_docdir}/stunnel/
rm -f %{buildroot}%{_docdir}/stunnel/COPYING.md %{buildroot}%{_docdir}/stunnel/COPYRIGHT.md %{buildroot}%{_docdir}/stunnel/CREDITS.md

%files
%doc %{_docdir}/stunnel
%license COPYING.md COPYRIGHT.md CREDITS.md
%dir %{_sysconfdir}/stunnel
%{_bindir}/stunnel
%dir %{_libdir}/stunnel
%{_libdir}/stunnel/libstunnel.so
%{_datadir}/bash-completion/completions/stunnel.bash
%{_mandir}/man8/stunnel.8*
%lang(pl) %{_mandir}/pl/man8/stunnel.8*

%changelog
%autochangelog
