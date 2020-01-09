Name:		cgdcbxd
Version:	1.0.1
Release:	2%{?dist}
Summary:	DCB network priority mangement daemon	
Group:		System Environment/Base
License:	GPLv2
URL:		https://github.com/jrfastab/cgdcbxd
Source0:	jrfastab-%{name}-v%{version}-0-g87bd754.tar.gz
Source1:	%{name}.init
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libcgroup-devel libmnl-devel libtool
Requires:	libcgroup libmnl
Requires(post):         chkconfig
Requires(preun):        chkconfig
Requires(preun):        initscripts
Requires(postun):       initscripts


%description
This is a daemon to manage the priority of network traffic in dcb enabled
environments.  By using the information exchanged over the dcbx protocol on a
LAN, this package will enforce network priority on running applications on your
host using the net_prio cgroup

%prep
%setup -q -n jrfastab-cgdcbxd-87bd754

%build
./bootstrap.sh
%{configure}
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf %{buildroot}%{_sysconfdir}
install -D -m755 %{SOURCE1} %{buildroot}%{_initddir}/cgdcbxd

%clean
rm -rf %{buidroot}

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ]; then
    /sbin/service %{name} condrestart > /dev/null  2>&1 || :
fi

%files
%{_mandir}/man8/*
%{_sbindir}/*
%{_initddir}/%{name}

%changelog
* Wed Oct 17 2012 Neil Horman <nhorman@redhat.com> 1.0.1-2
- Fixed up missing initscript (bz 867540)
 
* Mon Jun 25 2012 Neil Horman <nhorman@tuxdriver.com> 1.0.1-1 
- Initial build
