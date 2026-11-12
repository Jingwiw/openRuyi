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
Source1:        sudo.pam
Source2:        sudo-i.pam
BuildSystem:    autotools

# Stop the mailer when dropping privileges fails; https://github.com/sudo-project/sudo/commit/3e474c2f201484be83d994ae10a4e20e8c81bb69.
Patch0:         1000-mailer-privilege-drop.patch
# Ignore caller time zones during policy evaluation; https://github.com/sudo-project/sudo/commit/db669167ca599f2a94cd8a4c5fae9e473c81a2fd.
Patch1:         1001-policy-time-zone.patch
# Preserve command TZ while clearing the policy environment; https://github.com/sudo-project/sudo/commit/1820a349687522f51023d1ae5925125f59679a8c.
Patch2:         1002-preserve-command-time-zone.patch

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
BuildOption(conf):  --enable-pie
BuildOption(conf):  --enable-zlib=system
BuildOption(conf):  --enable-tmpfiles.d=%{_tmpfilesdir}
BuildOption(conf):  --with-sssd
BuildOption(install):  install_uid=`id -u` install_gid=`id -g` sudoers_uid=`id -u` sudoers_gid=`id -g`

BuildRequires:  pkgconfig(audit)
BuildRequires:  pkgconfig(pam)
BuildRequires:  groff
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

%install -a
# Set correct permissions
chmod 755 %{buildroot}%{_bindir}/* %{buildroot}%{_sbindir}/*
# Create required directories
install -p -d -m 700 %{buildroot}/var/db/sudo/lectured
install -p -d -m 750 %{buildroot}%{_sysconfdir}/sudoers.d
install -p -d -m 755 %{buildroot}%{_sysconfdir}/dnf/protected.d/
# Enable wheel in the upstream configuration; keep local edits on upgrade.
sed -i 's/^# %wheel ALL=(ALL:ALL) ALL$/%wheel ALL=(ALL) ALL/' %{buildroot}%{_sysconfdir}/sudoers
# Install dnf protection config
echo sudo > sudo.conf
install -p -c -m 0644 sudo.conf %{buildroot}/etc/dnf/protected.d/
rm -f sudo.conf
# Enable stripping; declare final plugin permissions below.
chmod +x %{buildroot}%{_libexecdir}/sudo/*.so
# Clean up unwanted files
rm -f %{buildroot}%{_datadir}/examples/sudo
rm -f %{buildroot}%{_sysconfdir}/sudoers.dist
# Add the private library directory to the loader cache.
install -d -m 0755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
printf '%s\n' '%{_libexecdir}/sudo' > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
# Install PAM files
install -D -p -m 0644 %{SOURCE1} %{buildroot}/etc/pam.d/sudo
install -D -p -m 0644 %{SOURCE2} %{buildroot}/etc/pam.d/sudo-i

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
%attr(0644,root,root) %{_libexecdir}/sudo/sudo_noexec.so
%attr(0644,root,root) %{_libexecdir}/sudo/sudoers.so
%attr(0644,root,root) %{_libexecdir}/sudo/group_file.so
%attr(0644,root,root) %{_libexecdir}/sudo/system_group.so
%attr(0644,root,root) %{_libexecdir}/sudo/audit_json.so
%{_libexecdir}/sudo/libsudo_util.so*
%dir /var/db/sudo
%dir /var/db/sudo/lectured
%dir %{_libexecdir}/sudo
%config(noreplace) /etc/pam.d/sudo
%config(noreplace) /etc/pam.d/sudo-i
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%{_includedir}/sudo_plugin.h

%changelog
%autochangelog
