Name:		cgdcbxd
Version:	1.0.2
Release:	1%{?dist}
Summary:	DCB network priority management daemon	
Group:		System Environment/Base
License:	GPLv2
URL:		https://github.com/jrfastab/cgdcbxd

# The source for this package was pullled from upstreams vcs.  Specifically it
# was pulled from the projects github site using the following dynamic tarball
# generating url:
# https://github.com/jrfastab/cgdcbxd/zipball/v1.0.1
Source0:	%{name}-%{version}.tar.gz

# The service file was created locally for the fedora project, but will be sent
# upstream shortly
Source1:	%{name}.service
BuildRequires:	libcgroup-devel libmnl-devel libtool systemd-units
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This is a daemon to manage the priority of network traffic in dcb enabled
environments.  By using the information exchanged over the dcbx protocol on a
LAN, this package will enforce network priority on running applications on your
host using the net_prio cgroup

%prep
%setup -q 

%build
./bootstrap.sh
%{configure}
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}
install -D -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/cgdcbxd.service

%files
%doc COPYING
%{_unitdir}/cgdcbxd.service
%{_mandir}/man8/*
%{_sbindir}/*

%post
%systemd_post cgdcbxd.service

%preun
%systemd_preun cgdcbxd.service

%postun
%systemd_postun_with_restart cgdcbxd.service

%changelog
* Tue Jul 23 2013 Neil Horman <nhorman@redhat.com> - 1.0.2-1
- Update to latest upstream

* Tue May 28 2013 Neil Horman <nhorman@redhat.com> - 1.0.1-3
- Fix the spec file to match new systemd install scripts (bz967588)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jun 25 2012 Neil Horman <nhorman@tuxdriver.com> 1.0.1-1 
- Initial build
