# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Li Guan <guanli.oerv@isrc.iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global build_tags seccomp systemd libsqlite3 libsubid

Name:           buildah
Version:        1.46.1
Release:        %autorelease
Summary:        A tool that facilitates building OCI images
License:        Apache-2.0
URL:            https://github.com/podman-container-tools/buildah
#!RemoteAsset:  sha256:23c8436ddc87602ef049b94c35a584037ad80f47c679c85a9fdf53647289d2dd
Source:         https://github.com/podman-container-tools/buildah/archive/v%{version}.tar.gz
BuildSystem:    autotools

BuildOption(build):  BUILDTAGS="%{build_tags}"
BuildOption(build):  GOPROXY=off
BuildOption(install):  GOPROXY=off
BuildOption(build):  PREFIX=%{_prefix}

BuildOption(install):  BUILDTAGS="%{build_tags}"
BuildOption(install):  DESTDIR=%{buildroot}
BuildOption(install):  PREFIX=%{_prefix}

BuildRequires:  go >= 1.26.8
BuildRequires:  subid-devel
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  make
BuildRequires:  fdupes
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libassuan)
BuildRequires:  pkgconfig(gpgme)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  btrfs-progs-devel

Requires:       netavark >= 2.0.0
Requires:       containers-common
Requires:       crun

%description
A tool that facilitates building OCI images.

# No configure.
%conf

%install -a
install -D -m 0644 contrib/completions/bash/buildah %{buildroot}%{bash_completions_dir}/buildah

# No tests.
%check

%files
%license LICENSE
%{_mandir}/man1/buildah*
%{_bindir}/buildah
%{_datadir}/bash-completion/completions/buildah

%changelog
%autochangelog
