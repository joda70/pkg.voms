## Turn off meaningless jar repackaging
%define __jar_repack 0

%global random_num %(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 8)

%global base_version 3.3.3.2
%global base_release 0

%if 0%{?rhel} == 5
%define jdk_version 1.7.0
%else
%define jdk_version 1.8.0
%endif

%if %{?build_number:1}%{!?build_number:0}
%define release_version 0.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: voms-admin-server
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: The VOMS Administration service

Group:  Applications/Internet
License:    ASL 2.0
URL: http://italiangrid.github.io/voms
Source:  %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)-%{random_num}

BuildArch:      noarch

BuildRequires:  apache-maven
BuildRequires:  jpackage-utils
BuildRequires:  java-%{jdk_version}-openjdk-devel

Requires: java-%{jdk_version}-openjdk-devel
Requires: python(abi) = 2.6
Requires: curl

%description
The Virtual Organization Membership Service (VOMS) is an attribute authority
which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of
their roles and other attributes in order to issue trusted attribute
certificates and SAML assertions used in the Grid environment for
authorization purposes.

The VOMS Admin service is a web application providing tools for administering
the VOMS VO structure. It provides an intuitive web user interface for daily
administration tasks.

%prep
%setup -q

%build
mvn -U -PEMI,prod -DskipTests clean package

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
tar -C $RPM_BUILD_ROOT -xvzf voms-admin-server/target/%{name}.tar.gz

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/voms-admin

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/voms-admin

%clean
rm -rf $RPM_BUILD_ROOT

%pre

## Create VOMS user if needed
getent group voms > /dev/null || groupadd -r voms
getent passwd voms > /dev/null || useradd -r -g voms \
    -d %{_sysconfdir}/voms -s /sbin/nologin -c "VOMS Server Account" voms

if [ -d "/var/lib/voms-admin/lib" ]; then
  rm -rf /var/lib/voms-admin/lib/*.jar
fi

if [ -d "/usr/share/voms-admin/vo.d" ]; then
  rm -rf /usr/share/voms-admin/vo.d
fi

if [ -d "/usr/share/voms-admin/work" ]; then
  rm -rf /usr/share/voms-admin/work
fi

exit 0

%post
/sbin/chkconfig --add voms-admin

if [ $1 -gt 1 ]; then
    if [ -e /etc/voms-admin/voms-siblings.xml ]; then
        rm -f /etc/voms-admin/voms-siblings.xml
    fi
    chown -R voms /etc/voms-admin
    chown -R voms /var/tmp/voms-admin
fi

%preun
if [ $1 = 0 ]; then
    /sbin/service voms-admin stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del voms-admin
fi
exit 0

%postun
if [ $1 -gt 1 ]; then
    /sbin/service voms-admin restart 2>&1 || :
fi

%files

%defattr(-,root,root,-)

%{_initrddir}/voms-admin

%dir %{_sysconfdir}/voms-admin
%config(noreplace) %{_sysconfdir}/sysconfig/voms-admin

%config(noreplace) %{_sysconfdir}/voms-admin/voms-admin-server.logback
%config(noreplace) %{_sysconfdir}/voms-admin/voms-admin-server.properties

%{_sbindir}/*

%{_javadir}/voms-admin.jar
%{_javadir}/voms-container.jar
%{_datadir}/webapps/voms-admin.war

%{_datadir}/doc/voms-admin-server/* 

%dir %{_datadir}/voms-admin/info-providers
%{_datadir}/voms-admin/info-providers/*

%dir %{_datadir}/voms-admin/templates
%{_datadir}/voms-admin/templates/*

%dir %{_datadir}/voms-admin/wsdls
%{_datadir}/voms-admin/wsdls/*

/var/lib/voms-admin/lib/*.jar
/var/lib/voms-admin/tools/*

%dir %{_localstatedir}/lib/voms-admin/vo.d
%attr(-,voms,voms) %dir %{_localstatedir}/lib/voms-admin/work
%attr(-,voms,voms) %dir %{_localstatedir}/log/voms-admin

%changelog
* Fri Apr 21 2017 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 3.3.3.2-0
- Packaging for version 3.3.3.2

* Tue Feb 10 2015 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 3.3.3-1
- Bumped version to 3.3.3.

* Mon Nov 3 2014 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 3.3.2-1
- Bumped version to 3.3.2.

* Mon Nov 3 2014 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 3.3.1-1
- Bumped version to 3.3.1.

* Fri Oct 24 2014 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 3.3.0-1
- Bumped version to 3.3.0 and adapted build to multi-module structure.

* Tue Jun 25 2013 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 3.2.0-1
- Fixes for:
- https://issues.infn.it/jira/browse/VOMS-266
- https://issues.infn.it/jira/browse/VOMS-260
- https://issues.infn.it/jira/browse/VOMS-257

* Tue Mar 19 2013 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 3.1.0-1
- Fixes for the following bugs:
- [VOMS-229] - VOMSES startup script fails in restarting VOMSES web app
- [VOMS-230] - VOMS Admin service incorrectly parses truststore refresh period from configuration
- [VOMS-231] - Standalone VOMS Admin service deployment is not suitable for deployments with large number of VOs (> 10)
- New feature:
- [VOMS-235] - Allow easier search of users with pending Sign AUP requests

* Wed Jul 11 2012 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 3.0.0-1
- VOMS admin now runs as a process in an embedded container

* Fri Dec 16 2011 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 2.7.0-1
- Self-managed packaging
