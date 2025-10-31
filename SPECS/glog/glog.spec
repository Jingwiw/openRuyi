# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Xuhai Chang <xuhai.oerv@isrc.iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           glog
Version:        0.7.1
Release:        %autorelease
Summary:        A C++ application logging library
License:        BSD
URL:            https://github.com/google/glog
#!RemoteAsset
Source0:        https://github.com/google/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  gcc
BuildRequires:  gflags-devel
BuildRequires:  cmake make
BuildSystem:    cmake
BuildOption(conf): -DBUILD_SHARED_LIBS=ON

%description
Google glog is a library that implements application-level
logging. This library provides logging APIs based on C++-style
streams and various helper macros.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files
%doc ChangeLog COPYING README.rst
%{_libdir}/libglog.so.*
%{_libdir}/libglog.so

%files devel
%{_libdir}/cmake/glog/
%dir %{_includedir}/glog
%{_includedir}/glog/*

%changelog
%{?autochangelog}
