# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
#
# SPDX-License-Identifier: MulanPSL-2.0

%global flavor @BUILD_FLAVOR@%{nil}
%global zig_cpu baseline
%global zig_target %{_target_cpu}-linux-gnu
# Upstream resolves lib/ relative to the executable, so install the standard
# library under /usr/lib/zig rather than a multilib-specific libdir.
%global zig_prefix_libdir %{_prefix}/lib
%global zig_cache_dir %{_vpath_builddir}/zig-cache
%global zig_package_dir %{zig_cache_dir}/p

%if %{?flavor}" == "bootstrap"
%bcond bootstrap 1
%else
%bcond bootstrap 0
%end

Name:           zig
Version:        0.15.2
Release:        %autorelease
Summary:        Programming language and toolchain for robust and reusable software
License:        MIT AND NCSA AND LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0 AND GPL-2.0-or-later AND GPL-2.0-or-later WITH GCC-exception-2.0 AND BSD-3-Clause AND Inner-Net-2.0 AND ISC AND LicenseRef-openRuyi-Public-Domain AND GFDL-1.1-or-later AND ZPL-2.1 AND Apache-2.0 WITH LLVM-exception AND Apache-2.0 AND BSD-2-Clause AND Zlib
URL:            https://ziglang.org
VCS:            git:https://codeberg.org/ziglang/zig.git

#!RemoteAsset:  sha256:d9b30c7aa983fcff5eed2084d54ae83eaafe7ff3a84d8fb754d854165a6e521c
Source0:        %{url}/download/%{version}/zig-%{version}.tar.xz
#!RemoteAsset:  sha256:a6845459501df3c3264ebc587b02a7094ad14f4f3f7287c48f04457e784d0d85
Source1:        %{url}/download/%{version}/zig-bootstrap-%{version}.tar.xz
Source2:        macros.zig
BuildSystem:    cmake

BuildOption(conf):  -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo
BuildOption(conf):  -DCMAKE_C_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG -Wno-unused"
BuildOption(conf):  -DCMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG -Wno-unused"
BuildOption(conf):  -DZIG_EXTRA_BUILD_ARGS:STRING="--verbose;--build-id=sha1"
BuildOption(conf):  -DZIG_SHARED_LLVM:BOOL=true
BuildOption(conf):  -DZIG_PIE:BOOL=true
BuildOption(conf):  -DZIG_TARGET_MCPU:STRING=%{zig_cpu}
BuildOption(conf):  -DZIG_TARGET_TRIPLE:STRING=%{zig_target}
BuildOption(conf):  -DZIG_VERSION:STRING="%{version}"

# Drop buildroot-native library paths from the final compiler rpath.
Patch0:         0001-remove-native-lib-directories-from-rpath.patch
# Backport upstream RISC-V unwind support to the 0.15.2 std.debug layout.
Patch1:         0002-std.debug-enable-riscv-linux-unwinding.patch
# Keep generated ELF archive headers acceptable to ld.lld.
Patch2:         0003-link.Elf-initialize-archive-header-fields.patch
# Tolerate GNU-emitted invalid DWARF CFA register definitions.
Patch3:         0004-std.debug-tolerate-invalid-def_cfa_register.patch

ExclusiveArch:  x86_64 riscv64

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.19
BuildRequires:  ninja
%if %{with bootstrap}
BuildRequires:  python3
%else
BuildRequires:  zig
BuildRequires:  clang-devel
BuildRequires:  help2man
BuildRequires:  libxml2-devel
BuildRequires:  lld-devel
BuildRequires:  llvm-devel
BuildRequires:  zlib-devel
%endif

%description
Zig is a general-purpose programming language and toolchain designed for
robustness, optimality, and clarity.


%if %{without bootstrap}
Requires:       %{name}-libs = %{version}-%{release}

%package libs
Summary:        Standard library for %{name}
BuildArch:      noarch

%description libs
This package contains the Zig standard library and runtime support files.

%package rpm-macros
Summary:        RPM macros for building Zig projects
BuildArch:      noarch
Requires:       %{name}
Requires:       rpm

%description rpm-macros
This package contains helper RPM macros for building Zig projects.
%endif

%prep
%if %{with bootstrap}
%autosetup -N -T -D -b 1 -n zig-bootstrap-%{version}
# Keep the embedded stage1 Zig sources aligned with the final source tree fixes.
pushd zig
%autopatch -p1
popd
%else
%autosetup -p1 -n zig-%{version}
%endif

%build
%if %{with bootstrap}
%set_build_flags
export CMAKE_GENERATOR=Ninja
export CMAKE_BUILD_PARALLEL_LEVEL=%{_smp_build_ncpus}
./build %{zig_target} %{zig_cpu}
%else
export CCACHE_DISABLE=1
mkdir -p %{zig_cache_dir} %{zig_package_dir}

%cmake

%cmake_build --target zigcpp
# 0.15.2 has build.zig.zon, but it only references in-tree path dependencies.
# Keep cache and package state inside the build root for hermetic builders.
zig build \
    --verbose \
    --summary all \
    --release=fast \
    -Dtarget=%{zig_target} \
    -Dcpu=%{zig_cpu} \
    --zig-lib-dir lib \
    --build-id=sha1 \
    --system "%{zig_package_dir}" \
    --cache-dir "%{zig_cache_dir}" \
    --global-cache-dir "%{zig_cache_dir}" \
    -Dversion-string="%{version}" \
    -Dstatic-llvm=false \
    -Denable-llvm=true \
    -Dno-langref=true \
    -Dstd-docs=false \
    -Dpie \
    -Dconfig_h="%{__cmake_builddir}/config.h"

help2man --no-discard-stderr --no-info "./zig-out/bin/zig" --version-option=version --output=zig.1
%endif

%check
%if %{with bootstrap}
# Upstream documents that the compiler must find lib/ relative to the binary.
test -x out/zig-%{zig_target}-%{zig_cpu}/bin/zig
out/zig-%{zig_target}-%{zig_cpu}/bin/zig env >/dev/null
%else
test -x zig-out/bin/zig
./zig-out/bin/zig env >/dev/null
%endif

cat > smoke.zig <<'EOF'
test "smoke" {
    try std.testing.expect(true);
}
const std = @import("std");
EOF

%if %{with bootstrap}
out/zig-%{zig_target}-%{zig_cpu}/bin/zig test smoke.zig
%else
./zig-out/bin/zig test smoke.zig
%endif

%install
%if %{with bootstrap}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{zig_prefix_libdir}
install -m 0755 out/zig-%{zig_target}-%{zig_cpu}/bin/zig %{buildroot}%{_bindir}/zig
cp -a out/zig-%{zig_target}-%{zig_cpu}/lib/zig %{buildroot}%{zig_prefix_libdir}/zig
%else
mkdir -p %{zig_cache_dir} %{zig_package_dir}
DESTDIR="%{buildroot}" zig build install \
    --verbose \
    --summary all \
    --release=fast \
    -Dtarget=%{zig_target} \
    -Dcpu=%{zig_cpu} \
    --zig-lib-dir lib \
    --build-id=sha1 \
    --system "%{zig_package_dir}" \
    --cache-dir "%{zig_cache_dir}" \
    --global-cache-dir "%{zig_cache_dir}" \
    -Dversion-string="%{version}" \
    -Dstatic-llvm=false \
    -Denable-llvm=true \
    -Dno-langref=true \
    -Dstd-docs=false \
    -Dpie \
    -Dconfig_h="%{__cmake_builddir}/config.h" \
    --prefix "%{_prefix}" \
    --prefix-lib-dir "%{zig_prefix_libdir}" \
    --prefix-exe-dir "%{_bindir}" \
    --prefix-include-dir "%{_includedir}"
install -D -m 0644 zig.1 %{buildroot}%{_mandir}/man1/zig.1
install -D -m 0644 %{SOURCE2} %{buildroot}%{_rpmmacrodir}/macros.zig
%endif

%files
%if %{with bootstrap}
%license zig/LICENSE
%license llvm/LICENSE.TXT
%license clang/LICENSE.TXT
%license lld/LICENSE.TXT
%license zlib/LICENSE
%license zstd/LICENSE
%doc README.md
%doc zig/README.md
%{_bindir}/zig
%{zig_prefix_libdir}/zig
%else
%license LICENSE
%doc README.md
%{_bindir}/zig
%{_mandir}/man1/zig.1*
%endif

%if %{without bootstrap}
%files libs
%{zig_prefix_libdir}/zig

%files rpm-macros
%{_rpmmacrodir}/macros.zig
%endif

%changelog
%autochangelog
