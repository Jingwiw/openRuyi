# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: yyjeqhc <jialin.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           authselect
Version:        1.6.1
Release:        %autorelease
Summary:        A tool to select system authentication and identity sources
License:        GPL-3.0-or-later
URL:            https://github.com/authselect/authselect
#!RemoteAsset
Source:         https://github.com/authselect/authselect/archive/%{version}/authselect-%{version}.tar.gz
BuildSystem:    autotools

BuildOption(conf):  --disable-rpath
BuildOption(conf):  --disable-static
BuildOption(conf):  --with-completion-dir=%{bash_completions_dir}
BuildOption(conf):  --with-pythonbin=%{__python3}
BuildOption(conf):  --disable-nls

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(popt)
BuildRequires:  pkgconfig(cmocka)
BuildRequires:  m4
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  chrpath

Requires:       grep
Requires:       sed
Requires:       systemd
Requires:       gawk
Requires:       coreutils
Requires:       findutils
Requires:       pam
Requires:       libpwquality

%description
Authselect is a tool to configure system authentication and identity sources
from a list of supported profiles. It replaces the legacy authconfig tool.

%package        devel
Summary:        Development files for the authselect library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains the development library files and headers for the
authselect tool, used for developing front-ends.

%conf -p
autoreconf -ivf

%install -a
# fix error  0001: file '/usr/bin/authselect' contains a standard runpath '/usr/lib64' in [/usr/lib64]
chrpath -d %{buildroot}%{_bindir}/authselect

rm -fr %{buildroot}%{_datadir}/doc/%{name}

%preun
# This script must be executed before any files are removed.
if [ $1 == 0 ] ; then
    # Remove authselect symbolic links so all authselect files can be
    # deleted safely. If this fail, the uninstallation must fail to avoid
    # breaking the system by removing PAM files. However, the command can
    # only fail if it can not write to the file system.
    %{_bindir}/authselect opt-out || exit 1
fi

%posttrans
# Respect existing local PAM state. Only refresh systems that are already
# explicitly managed by authselect.
if [ -s %{_sysconfdir}/authselect/authselect.conf ] && \
   %{_bindir}/authselect check &> /dev/null ; then
    %{_bindir}/authselect apply-changes &> /dev/null || :
fi
exit 0

%files
%license COPYING
%doc README.md
%dir %{_sysconfdir}/authselect
%dir %{_sysconfdir}/authselect/custom
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/authselect.conf
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/dconf-db
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/dconf-locks
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/fingerprint-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/nsswitch.conf
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/password-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/postlogin
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/smartcard-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/system-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/nsswitch.conf
%ghost %attr(0644,root,root) %{_sysconfdir}/pam.d/fingerprint-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/pam.d/password-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/pam.d/postlogin
%ghost %attr(0644,root,root) %{_sysconfdir}/pam.d/smartcard-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/pam.d/system-auth
%dir %{_localstatedir}/lib/authselect
%ghost %attr(0755,root,root) %{_localstatedir}/lib/authselect/backups/
%dir %{_datadir}/authselect
%dir %{_datadir}/authselect/vendor
%dir %{_datadir}/authselect/default
%{_datadir}/authselect/default/*
%{_bindir}/authselect
%{_libdir}/libauthselect.so.*

%files devel
%{_includedir}/authselect.h
%{_libdir}/libauthselect.so
%{_libdir}/pkgconfig/authselect.pc

%changelog
%{?autochangelog}
