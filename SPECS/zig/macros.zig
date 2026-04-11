%zig_arches x86_64 riscv64
%zig %{_bindir}/zig
%_zig_cache_dir %{_vpath_builddir}/zig-cache
%_zig_package_dir %{_zig_cache_dir}/p
%_zig_cpu baseline
%_zig_target %{_target_cpu}-linux-gnu
# Match upstream runtime lookup for /usr/bin/zig + /usr/lib/zig.
%_zig_prefix_libdir %{_prefix}/lib
%_zig_release_mode safe
%_zig_build_options --verbose --summary all --release=%{_zig_release_mode} --build-id=sha1 -Dtarget=%{_zig_target} -Dcpu=%{_zig_cpu} --system "%{_zig_package_dir}" --cache-dir "%{_zig_cache_dir}" --global-cache-dir "%{_zig_cache_dir}" %{?zig_build_options}
%_zig_install_options --prefix "%{_prefix}" --prefix-lib-dir "%{_zig_prefix_libdir}" --prefix-exe-dir "%{_bindir}" --prefix-include-dir "%{_includedir}" %{?zig_install_options}
%_zig_fetch_options --global-cache-dir "%{_zig_cache_dir}" %{?zig_fetch_options}

# Keep the public macro surface small until there are downstream consumers.
%zig_prep %{shrink: \
    mkdir -p \
        %{_zig_cache_dir} \
        %{_zig_package_dir} \
}
%zig_build %{shrink: \
    %zig \
        build \
        %{?_zig_build_options} \
}
%zig_install %{shrink: \
    DESTDIR="%{buildroot}" \
    %zig \
        build \
        install \
        %{?_zig_build_options} \
        %{?_zig_install_options} \
}
%zig_fetch %{shrink: \
    %zig \
        fetch \
        %{?_zig_fetch_options} \
}
%zig_test %{shrink: \
    %zig \
        build \
        test \
        %{?_zig_build_options} \
        %{?zig_test_options} \
}
