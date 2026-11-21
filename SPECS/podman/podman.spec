# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
# SPDX-FileContributor: Li Guan <guanli.oerv@isrc.iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global build_tags seccomp systemd libsqlite3 libsubid grpcnotrace

Name:           podman
Version:        6.2.0
Release:        %autorelease
Summary:        Manage containers, images, pods, and their volumes
License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND MIT AND MPL-2.0
URL:            https://podman.io/
VCS:            git:https://github.com/podman-container-tools/podman
#!RemoteAsset:  sha256:cb182273c5c5e3ea079f8f88a9a30a574d247f80e0b9dd9c02df1d2e6f6f3705
Source0:        https://github.com/podman-container-tools/podman/archive/refs/tags/v%{version}.tar.gz
BuildSystem:    autotools

BuildOption(build):  BUILDFLAGS=-trimpath
BuildOption(build):  all docker-docs
BuildOption(build):  GOMD2MAN=go-md2man
BuildOption(build):  BUILDTAGS="%{build_tags}"
BuildOption(build):  GOPROXY=off
BuildOption(build):  PREFIX=%{_prefix}
BuildOption(build):  TMPFILESDIR=%{_tmpfilesdir}
BuildOption(build):  LIBEXECDIR=%{_libexecdir}
BuildOption(install):  BUILDTAGS="%{build_tags}"
BuildOption(install):  install.docker-full
BuildOption(install):  GOPROXY=off
BuildOption(install):  install.completions
BuildOption(install):  PREFIX=%{_prefix}
BuildOption(install):  TMPFILESDIR=%{_tmpfilesdir}
BuildOption(install):  LIBEXECDIR=%{_libexecdir}

BuildRequires:  gcc
BuildRequires:  go >= 1.26.8
BuildRequires:  go-md2man
BuildRequires:  groff
BuildRequires:  make
BuildRequires:  man
BuildRequires:  pkg-config
BuildRequires:  subid-devel
BuildRequires:  envsubst
BuildRequires:  pkgconfig(gpgme)
BuildRequires:  pkgconfig(libbtrfsutil)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(python3)
BuildRequires:  systemd-rpm-macros

Requires:       containers-common
Requires:       conmon
Requires:       crun
Requires:       passt
Requires:       netavark >= 2.0.0
Requires:       catatonit

%package        docker
Summary:        Docker command interface for Podman
Requires:       %{name}%{?_isa} = %{version}-%{release}
Conflicts:      docker-cli

%description    docker
Docker command wrappers and compatibility files for Podman.

%description
Podman (the POD MANager) is a tool for managing containers and images,
volumes mounted into those containers, and pods made from groups of
containers.

%prep -a
# Read the system CA bundle without legacy compatibility links.
sed -i 's|^}$|\t"/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem",\n}|' pkg/machine/certificates/certificates_linux.go

# no configure scripts
%conf

%check
%make_build localunit GOPROXY=off BUILDTAGS="%{build_tags}"

%files
%doc README.md CONTRIBUTING.md install.md transfer.md
%license LICENSE vendor/modules.txt
%{_bindir}/podman
%{_bindir}/podman-remote
%{_bindir}/podmansh
%{_datadir}/bash-completion/completions/podman*
%{_datadir}/fish/vendor_completions.d/podman*.fish
%{_datadir}/zsh/site-functions/_podman*
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/quadlet
%{_libexecdir}/podman/rootlessport
%{_mandir}/man*/podman*
%{_mandir}/man5/quadlet.5.*
%{_systemdgeneratordir}/podman-system-generator
%{_systemdusergeneratordir}/podman-user-generator
%{_tmpfilesdir}/podman.conf
%{_unitdir}/podman*
%{_userunitdir}/podman*

%files docker
%{_bindir}/docker
%{_sysconfdir}/profile.d/podman-docker.*
%{_tmpfilesdir}/podman-docker.conf
%{_datadir}/user-tmpfiles.d/podman-docker.conf
%{_mandir}/man1/docker*
%{_mandir}/man5/docker*

%changelog
%autochangelog
