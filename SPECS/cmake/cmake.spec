# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Xuhai Chang <xuhai.oerv@isrc.iscas.ac.cn>
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: jchzhou <zhoujiacheng@iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%bcond bootstrap 0
%bcond tests 1
%bcond system_libs 1
%bcond openssl 1

Name:           cmake
Version:        4.3.1
Release:        %autorelease
Summary:        Cross-platform make system
License:        BSD and MIT and zlib
URL:            http://www.cmake.org
VCS:            git:https://gitlab.kitware.com/cmake/cmake
#!RemoteAsset:  sha256:0798f4be7a1a406a419ac32db90c2956936fecbf50db3057d7af47d69a2d7edb
Source0:        https://www.cmake.org/files/v4.3/cmake-%{version}.tar.gz
Source1:        macros.cmake
Source2:        macros.buildsystem.cmake
Source3:        cmake.attr
BuildSystem:    autotools

BuildOption(conf):  --no-system-libs

# qt-gui and emacs-lisp features are removed to make cmake usable ASAP
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc-c++
BuildRequires:  make

%if %{without bootstrap}
BuildRequires:  cmake
BuildRequires:  cmake-data
BuildRequires:  cmake-filesystem
%endif

%if %{with tests}
BuildRequires:  git
%endif

%if %{with system_libs}
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libzstd)
%endif

%if %{with openssl}
BuildRequires:  pkgconfig(openssl)
%endif

Requires:       cmake-data = %{version}-%{release}
Requires:       cmake-rpm-macros = %{version}-%{release}
Requires:       cmake-filesystem = %{version}-%{release}

%description
CMake is used to control the software compilation process using simple
platform and compiler independent configuration files. CMake generates
native makefiles and workspaces that can be used in the compiler
environment of your choice. CMake is quite sophisticated: it is possible
to support complex environments requiring system configuration, preprocessor
generation, code generation, and template instantiation.

%package        data
Summary:        Common data-files for cmake
Requires:       cmake = %{version}-%{release}
Requires:       cmake-rpm-macros = %{version}-%{release}
BuildArch:      noarch

%description    data
This package contains common data-files for cmake.

%package        filesystem
Summary:        Directories used by CMake modules

%description    filesystem
This package owns all directories used by CMake modules.

%package        rpm-macros
Summary:        Common RPM macros for cmake
Requires:       rpm
Conflicts:      cmake-data < 3.10.1-2
BuildArch:      noarch

%description    rpm-macros
This package contains common RPM macros for cmake.

%conf
%if %{with bootstrap}
./bootstrap --prefix=%{_prefix} --datadir=/share/cmake \
             --docdir=/share/doc/cmake --mandir=/share/man \
             --no-system-libs \
             --parallel=$(/usr/bin/getconf _NPROCESSORS_ONLN) \
             --no-system-cppdap \
             --no-system-librhash \
             -- \
             -DCMAKE_USE_OPENSSL=OFF \
             -DBUILD_CursesDialog=OFF \
             -DBUILD_TESTING=OFF
%else
cmake -S . -B build-dir \
      -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DCMAKE_DATA_DIR=share/cmake \
      -DCMAKE_DOC_DIR=share/doc/cmake \
      -DCMAKE_MAN_DIR=share/man \
      -DCMAKE_USE_SYSTEM_LIBRARIES=ON \
      -DCMAKE_USE_SYSTEM_LIBRARY_CPPDAP=OFF \
      -DCMAKE_USE_SYSTEM_LIBRARY_LIBRHASH=OFF \
      -DCMAKE_USE_SYSTEM_LIBRARY_JSONCPP=OFF \
%if %{with openssl}
      -DCMAKE_USE_OPENSSL=ON \
%else
      -DCMAKE_USE_OPENSSL=OFF \
%endif
      -DBUILD_CursesDialog=OFF \
%if %{with tests}
      -DBUILD_TESTING=ON
%else
      -DBUILD_TESTING=OFF
%endif
%endif

%build
%if %{with bootstrap}
make %{?_smp_mflags}
%else
cmake --build build-dir %{?_smp_mflags}
%endif

%install
%if %{with bootstrap}
make DESTDIR=%{buildroot} install
%else
DESTDIR=%{buildroot} cmake --install build-dir
%endif

# Make sure the installed CMake is complete enough to run later.
test -f %{buildroot}%{_datadir}/cmake/Modules/CMake.cmake

# install cmake rpm macros
install -p -m0644 -D %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.cmake
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|4|" %{buildroot}%{_rpmmacrodir}/macros.cmake
install -p -m0644 -D %{SOURCE2} %{buildroot}%{_rpmmacrodir}/macros.buildsystem.cmake

install -p -m0644 -D %{SOURCE3} %{buildroot}%{_fileattrsdir}/cmake.attr

# update cmake rpm macro file timestamp
touch -r %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.cmake
touch -r %{SOURCE2} %{buildroot}%{_rpmmacrodir}/macros.buildsystem.cmake

# install Copyright and dependencies' Copyright
install -d %{buildroot}%{_libdir}/cmake
cp -p Source/kwsys/Copyright.txt ./Copyright_kwsys
cp -p Utilities/KWIML/Copyright.txt ./Copyright_KWIML
cp -p Utilities/cmlibarchive/COPYING ./COPYING_cmlibarchive
cp -p Utilities/cmliblzma/COPYING ./COPYING_cmliblzma
cp -p Utilities/cmcurl/COPYING ./COPYING_cmcurl
cp -p Utilities/cmlibrhash/COPYING ./COPYING_cmlibrhash
cp -p Utilities/cmzlib/Copyright.txt ./Copyright_cmzlib
cp -p Utilities/cmexpat/COPYING ./COPYING_cmexpat
cp -p Utilities/cmcppdap/LICENSE LICENSE.cppdap
cp -p Utilities/cmcppdap/NOTICE NOTICE.cppdap
cp -p Utilities/cmjsoncpp/LICENSE ./LICENSE.cmjsoncpp

# install help files
install -d %{buildroot}%{_docdir}/cmake
cp -pr %{buildroot}%{_datadir}/cmake/Help %{buildroot}%{_docdir}/cmake

# temporary files used to create cmake-filesystem package
find %{buildroot}%{_datadir}/cmake -type d | sed -e 's!^%{buildroot}!%%dir "!g' -e 's!$!"!g' > data_dirs.mf
find %{buildroot}%{_libdir}/cmake -type d | sed -e 's!^%{buildroot}!%%dir "!g' -e 's!$!"!g' > lib_dirs.mf

# remove unnecessary emacs lisp files
rm -rf %{buildroot}%{_datadir}/emacs

%if %{with tests}
%check
# Requires network access to run some tests, so exclude them
NO_TEST="CTestTestUpload"
# Exclude CPack component tests
NO_TEST="$NO_TEST|CPackComponentsForAll-RPM-default"
NO_TEST="$NO_TEST|CPackComponentsForAll-RPM-OnePackPerGroup"
NO_TEST="$NO_TEST|CPackComponentsForAll-RPM-AllInOne"
# curl test may fail
NO_TEST="$NO_TEST|curl"

%ifarch riscv64
# timeout for riscv64
NO_TEST="$NO_TEST|Qt5Autogen.ManySources|Qt5Autogen.MocInclude|Qt5Autogen.MocIncludeSymlink|Qt6Autogen.MocIncludeSymlink"
%endif

%if %{with bootstrap}
bin/ctest %{?_smp_mflags} -V -E "$NO_TEST" --output-on-failure
%else
build-dir/bin/ctest %{?_smp_mflags} -V -E "$NO_TEST" --output-on-failure
%endif
%endif

%files
%doc %dir %{_docdir}/cmake
%license Copyright_* COPYING* LICENSE.rst CONTRIBUTORS.rst
%license LICENSE.cppdap NOTICE.cppdap LICENSE.cmjsoncpp
%{_bindir}/cmake
%{_bindir}/cpack
%{_bindir}/ctest
%{_libdir}/cmake
%doc %{_docdir}/cmake/*

%files filesystem -f data_dirs.mf -f lib_dirs.mf

%files data
%{_datadir}/cmake
%{_datadir}/aclocal/cmake.m4
%{_datadir}/bash-completion
%{_datadir}/vim/vimfiles/indent/%{name}.vim
%{_datadir}/vim/vimfiles/syntax/%{name}.vim
%exclude %{_datadir}/cmake/Templates/Windows/Windows_TemporaryKey.pfx

%files rpm-macros
%{_fileattrsdir}/cmake.attr
%{_rpmmacrodir}/macros.cmake
%{_rpmmacrodir}/macros.buildsystem.cmake

%changelog
%autochangelog
