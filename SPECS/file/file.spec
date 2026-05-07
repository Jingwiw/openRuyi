# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%bcond bootstrap 0
%bcond seccomp 1
%bcond compression 1
%bcond autoreconf 1

Name:           file
Version:        5.46
Release:        %autorelease
Summary:        A Tool to Determine File Types
License:        BSD-2-Clause
URL:            http://www.darwinsys.com/file/
VCS:            git:https://github.com/file/file
#!RemoteAsset:  sha256:c9cc77c7c560c543135edc555af609d5619dbef011997e988ce40a3d75d86088
Source0:        https://www.astron.com/pub/file/file-%{version}.tar.gz
Buildsystem:    autotools

BuildOption(conf):  --disable-silent-rules
BuildOption(conf):  --enable-fsect-man5

%if %{with seccomp}
BuildOption(conf):  --enable-libseccomp
%else
BuildOption(conf):  --disable-libseccomp
%endif

%if %{with compression}
BuildOption(conf):  --enable-zlib
BuildOption(conf):  --enable-bzlib
BuildOption(conf):  --enable-xzlib
BuildOption(conf):  --enable-zstdlib
BuildOption(conf):  --disable-lzlib
BuildOption(conf):  --disable-lrziplib
%else
BuildOption(conf):  --disable-zlib
BuildOption(conf):  --disable-bzlib
BuildOption(conf):  --disable-xzlib
BuildOption(conf):  --disable-zstdlib
BuildOption(conf):  --disable-lzlib
BuildOption(conf):  --disable-lrziplib
%endif

BuildRequires:  make
BuildRequires:  gcc

%if %{with autoreconf}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
%endif

%if %{with seccomp}
BuildRequires:  pkgconfig(libseccomp)
%endif

%if %{with compression}
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libzstd)
%endif

%description
With the file command, you can obtain information on the file type of a
specified file. File type recognition is controlled by the file
/etc/magic, which contains the classification criteria. This command is
used by apsfilter to permit automatic printing of different file types.

%package        devel
Summary:        Development files for libmagic, a library to determine file types
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glibc-devel

%description    devel
This package contains all necessary include files and libraries needed
to develop applications that require the magic "file" interface.

%if %{with autoreconf}
%conf -p
autoreconf -fiv
%endif

%install -a
rm -f %{buildroot}%{_libdir}/libmagic.la

%files
%defattr (-,root,root)
%attr(755,root,root) %{_bindir}/file
%{_libdir}/lib*.so.*
%{_datadir}/misc/magic.mgc
%doc %{_mandir}/man1/file.1.gz
%license COPYING
%doc AUTHORS NEWS ChangeLog

%files devel
%defattr (-,root,root)
%{_libdir}/lib*.so
%{_includedir}/magic.h
%{_libdir}/pkgconfig/libmagic.pc
%doc %{_mandir}/man3/libmagic.3.gz
%defattr (-,root,root)
%doc %{_mandir}/man5/magic.5.gz
%license COPYING
%doc README.DEVELOPER AUTHORS NEWS ChangeLog

%changelog
%autochangelog
