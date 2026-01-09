# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%define _name           ollama
%define go_import_path  github.com/ollama/ollama

Name:           ollama
Version:        0.13.5
Release:        %autorelease
Summary:        Get up and running with OpenAI gpt-oss, DeepSeek-R1, Gemma 3 and other models.
License:        MIT
URL:            https://github.com/ollama/ollama
#!RemoteAsset
Source0:        https://github.com/ollama/ollama/archive/v%{version}.tar.gz#/%{_name}-%{version}.tar.gz
BuildSystem:    golang

BuildOption(prep):  -n %{_name}-%{version}

BuildRequires:  go
BuildRequires:  go-rpm-macros
BuildRequires:  go(github.com/agnivade/levenshtein)
BuildRequires:  go(github.com/containerd/console)
BuildRequires:  go(github.com/d4l3k/go-bfloat16)
BuildRequires:  go(github.com/dlclark/regexp2)
BuildRequires:  go(github.com/emirpasic/gods/v2)
BuildRequires:  go(github.com/gin-contrib/cors)
BuildRequires:  go(github.com/gin-gonic/gin)
BuildRequires:  go(github.com/google/go-cmp)
BuildRequires:  go(github.com/google/uuid)
BuildRequires:  go(github.com/mattn/go-runewidth)
BuildRequires:  go(github.com/nlpodyssey/gopickle)
BuildRequires:  go(github.com/olekukonko/tablewriter) < 1.0.0
BuildRequires:  go(github.com/pdevine/tensor)
BuildRequires:  go(github.com/spf13/cobra)
BuildRequires:  go(github.com/stretchr/testify)
BuildRequires:  go(github.com/x448/float16)
BuildRequires:  go(golang.org/x/crypto)
BuildRequires:  go(golang.org/x/image)
BuildRequires:  go(golang.org/x/mod)
BuildRequires:  go(golang.org/x/sync)
BuildRequires:  go(golang.org/x/term)
BuildRequires:  go(golang.org/x/text)
BuildRequires:  go(golang.org/x/tools)
BuildRequires:  go(gonum.org/v1/gonum)
BuildRequires:  go(google.golang.org/protobuf)

%description
Ollama is an open-source platform designed to run large language models locally.
It allows users to generate text, assist with coding, and create content privately
and securely on their own devices.

%prep -a
# Remove bundled dependencies
rm -rf llama/llama.cpp/vendor

%files
%license LICENSE*
%doc README*
%{_bindir}/%{_name}

%changelog
%{?autochangelog}
