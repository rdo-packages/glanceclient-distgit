%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname glanceclient

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
This is a client for the OpenStack Glance API. There's a Python API (the \
glanceclient module), and a command-line script (glance). Each implements \
100% of the OpenStack Glance API.

Name:             python-glanceclient
Epoch:            1
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Glance

License:          ASL 2.0
URL:              https://launchpad.net/python-glanceclient
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch

BuildRequires:    git

%description
%{common_desc}

%package -n python2-%{sname}
Summary:          Python API and CLI for OpenStack Glance
%{?python_provide:%python_provide python2-glanceclient}

BuildRequires:    python2-devel
BuildRequires:    python2-setuptools
BuildRequires:    python2-pbr

Requires:         python2-keystoneauth1 >= 3.3.0
Requires:         python2-oslo-i18n >= 3.15.3
Requires:         python2-oslo-utils >= 3.33.0
Requires:         python2-pbr
Requires:         python2-prettytable
Requires:         python2-pyOpenSSL >= 16.2.0
Requires:         python2-requests
Requires:         python2-six >= 1.10.0
Requires:         python2-warlock
Requires:         python2-wrapt

%description -n python2-%{sname}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Glance
%{?python_provide:%python_provide python3-glanceclient}

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr

Requires:         python3-keystoneauth1 >= 3.3.0
Requires:         python3-oslo-i18n >= 3.15.3
Requires:         python3-oslo-utils >= 3.33.0
Requires:         python3-pbr
Requires:         python3-prettytable
Requires:         python3-pyOpenSSL >= 16.2.0
Requires:         python3-requests
Requires:         python3-six >= 1.10.0
Requires:         python3-warlock
Requires:         python3-wrapt

%description -n python3-%{sname}
%{common_desc}
%endif

%package doc
Summary:          Documentation for OpenStack Glance API Client

BuildRequires:    python2-sphinx
BuildRequires:    python2-openstackdocstheme
BuildRequires:    python2-keystoneauth1
BuildRequires:    python2-oslo-utils
BuildRequires:    python2-prettytable
BuildRequires:    python2-warlock
BuildRequires:    python2-pyOpenSSL >= 16.2.0
BuildRequires:    openstack-macros

%description      doc
%{common_desc}

This package contains auto-generated documentation.

%prep
%autosetup -n %{name}-%{upstream_version} -S git

%py_req_cleanup

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

# generate html docs
%{__python2} setup.py build_sphinx -b html
# generate man page
%{__python2} setup.py build_sphinx -b man
install -p -D -m 644 doc/build/man/glance.1 %{buildroot}%{_mandir}/man1/glance.1

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
%doc doc/build/html
%license LICENSE

%changelog
