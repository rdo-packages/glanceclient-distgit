%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname glanceclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:             python-glanceclient
Epoch:            1
Version:          2.5.0
Release:          1%{?dist}
Summary:          Python API and CLI for OpenStack Glance

License:          ASL 2.0
URL:              https://launchpad.net/python-glanceclient
Source0:          https://pypi.io/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch

%description
This is a client for the OpenStack Glance API. There's a Python API (the
glanceclient module), and a command-line script (glance). Each implements
100% of the OpenStack Glance API.

%package -n python2-%{sname}
Summary:          Python API and CLI for OpenStack Glance
%{?python_provide:%python_provide python2-glanceclient}

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr

Requires:         python-babel >= 1.3
Requires:         python-keystoneclient
Requires:         python-oslo-i18n
Requires:         python-oslo-utils
Requires:         python-pbr
Requires:         python-prettytable
Requires:         python-requests
Requires:         python-setuptools
Requires:         python-six >= 1.9.0
Requires:         python-warlock

%description -n python2-%{sname}
This is a client for the OpenStack Glance API. There's a Python API (the
glanceclient module), and a command-line script (glance). Each implements
100% of the OpenStack Glance API.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Glance
%{?python_provide:%python_provide python3-glanceclient}

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr

Requires:         python3-babel >= 1.3
Requires:         python3-keystoneclient
Requires:         python3-oslo-i18n
Requires:         python3-oslo-utils
Requires:         python3-pbr
Requires:         python3-prettytable
Requires:         python3-requests
Requires:         python3-setuptools
Requires:         python3-six >= 1.9.0
Requires:         python3-warlock

%description -n python3-%{sname}
This is a client for the OpenStack Glance API. There's a Python API (the
glanceclient module), and a command-line script (glance). Each implements
100% of the OpenStack Glance API.
%endif

%package doc
Summary:          Documentation for OpenStack Glance API Client

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx

%description      doc
This is a client for the OpenStack Glance API. There's a Python API (the
glanceclient module), and a command-line script (glance). Each implements
100% of the OpenStack Glance API.

This package contains auto-generated documentation.

%prep
%setup -q -n %{name}-%{upstream_version}

rm -rf {,test-}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/glance %{buildroot}%{_bindir}/glance-%{python3_version}
ln -s ./glance-%{python3_version} %{buildroot}%{_bindir}/glance-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/glanceclient/tests
%endif

%py2_install
mv %{buildroot}%{_bindir}/glance %{buildroot}%{_bindir}/glance-%{python2_version}
ln -s ./glance-%{python2_version} %{buildroot}%{_bindir}/glance-2

ln -s ./glance-2 %{buildroot}%{_bindir}/glance

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/glance.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/glance

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/glanceclient/tests


export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# generate man page
sphinx-build -b man doc/source man
install -p -D -m 644 man/glance.1 %{buildroot}%{_mandir}/man1/glance.1

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/glanceclient
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/glance.1.gz
%{_bindir}/glance
%{_bindir}/glance-2
%{_bindir}/glance-%{python2_version}

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/glance.1.gz
%{_bindir}/glance-3
%{_bindir}/glance-%{python3_version}
%endif

%files doc
%doc html
%license LICENSE

%changelog
* Sat Sep 10 2016 Haikel Guemar <hguemar@fedoraproject.org> 1:2.5.0-1
- Update to 2.5.0

