# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: yyjeqhc <jialin.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           sudo
Version:        1.9.17p2
Release:        %autorelease
Summary:        Allows restricted root access for specified users
License:        ISC
URL:            https://www.sudo.ws
VCS:            git:https://github.com/sudo-project/sudo.git
#!RemoteAsset:  sha256:4a38a1ab3adb1199257edc2a7c4a2bd714665eb605b04368843b06dada2cfcfb
Source0:        https://www.sudo.ws/dist/%{name}-%{version}.tar.gz
Source1:        sudoers.conf
Source2:        sudo.pam
Source3:        sudo-i.pam
BuildSystem:    autotools

BuildOption(conf):  --disable-root-mailer
BuildOption(conf):  --disable-intercept
BuildOption(conf):  --disable-log-server
BuildOption(conf):  --disable-log-client
BuildOption(conf):  --with-logging=syslog
BuildOption(conf):  --with-logfac=authpriv
BuildOption(conf):  --with-pam
BuildOption(conf):  --with-pam-login
BuildOption(conf):  --with-editor=/bin/vi
BuildOption(conf):  --without-ldap
BuildOption(conf):  --with-selinux
BuildOption(conf):  --with-passprompt="[sudo] password for %p: "
BuildOption(conf):  --with-linux-audit
BuildOption(conf):  --with-sssd
BuildOption(install):  install_uid=`id -u` install_gid=`id -g` sudoers_uid=`id -u` sudoers_gid=`id -g`

BuildRequires:  pkgconfig(audit)
BuildRequires:  pkgconfig(pam)
BuildRequires:  groff
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  gettext
BuildRequires:  pkgconfig(zlib)

Recommends:     vim-minimal

Requires:       pam
Requires(post): coreutils

%description
Sudo is a program designed to allow a sysadmin to give limited root privileges
to users and log root activity. The basic philosophy is to give as few
privileges as possible but still allow people to get their work done.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains header files for developing sudo plugins.

%conf -p
export CFLAGS="%{build_cflags} -fpie" LDFLAGS="%{build_ldflags} -pie"

%install -a
# Set correct permissions
chmod 755 %{buildroot}%{_bindir}/* %{buildroot}%{_sbindir}/*
# Create required directories
install -p -d -m 700 %{buildroot}/var/db/sudo/lectured
install -p -d -m 750 %{buildroot}%{_sysconfdir}/sudoers.d
install -p -d -m 755 %{buildroot}%{_sysconfdir}/dnf/protected.d/
# Install sudoers config
install -p -c -m 0440 %{S:1} %{buildroot}/etc/sudoers
# Install dnf protection config
echo sudo > sudo.conf
install -p -c -m 0644 sudo.conf %{buildroot}/etc/dnf/protected.d/
rm -f sudo.conf
# Fix permissions on plugins
chmod +x %{buildroot}%{_libexecdir}/sudo/*.so
# Clean up unwanted files
rm -f %{buildroot}%{_datadir}/examples/sudo
rm -f %{buildroot}%{_sysconfdir}/sudoers.dist
# Add ld.so.conf.d entry for plugins
mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "/usr/libexec/sudo" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf
# Install PAM files
install -D -p -m 0644 %{S:2} %{buildroot}/etc/pam.d/sudo
install -D -p -m 0644 %{S:3} %{buildroot}/etc/pam.d/sudo-i

%find_lang sudo --all-name --generate-subpackages

%post
/bin/chmod 0440 /etc/sudoers || :

%files
%doc %{_docdir}/%{name}
%license LICENSE.md
%attr(0440,root,root) %config(noreplace) /etc/sudoers
%attr(0750,root,root) %dir /etc/sudoers.d/
%config(noreplace) /etc/dnf/protected.d/sudo.conf
%config(noreplace) /etc/sudo.conf
%{_tmpfilesdir}/sudo.conf
%attr(4111,root,root) %{_bindir}/sudo
%attr(0111,root,root) %{_bindir}/sudoreplay
%{_bindir}/sudoedit
%{_bindir}/cvtsudoers
%{_sbindir}/visudo
%{_libexecdir}/sudo/sesh
%{_libexecdir}/sudo/sudo_noexec.so
%{_libexecdir}/sudo/sudoers.so
%{_libexecdir}/sudo/group_file.so
%{_libexecdir}/sudo/system_group.so
%{_libexecdir}/sudo/audit_json.so
%{_libexecdir}/sudo/libsudo_util.so*
%dir /var/db/sudo
%dir /var/db/sudo/lectured
%dir %{_libexecdir}/sudo
%config(noreplace) /etc/pam.d/sudo
%config(noreplace) /etc/pam.d/sudo-i
%config(noreplace) /etc/ld.so.conf.d/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%{_includedir}/sudo_plugin.h

%changelog
%autochangelog
