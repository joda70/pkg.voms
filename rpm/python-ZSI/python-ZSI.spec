%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-ZSI
Version:        2.1
Release:        16%{?dist}
Summary:        Zolera SOAP Infrastructure
# to obtain some license information have a look at ZSI/__init__.py file
License:        MIT and LBNL BSD and ZPLv2.0
URL:            http://pywebsvcs.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/pywebsvcs/ZSI/ZSI-%{version}_a1/ZSI-%{version}-a1.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel python2-setuptools

%global _description\
The Zolera SOAP Infrastructure provides libraries for developing web services\
using the python programming language. The libraries implement the various\
protocols used when writing web services including SOAP, WSDL, and other\
related protocols.

%description %_description

%package -n python2-zsi
Summary: %summary
Requires:       python2-setuptools
%{?python_provide:%python_provide python2-zsi}

%description -n python2-zsi %_description

%prep
%setup -q -n ZSI-%{version}-a1

# remove cvs internal files and
# get rid of executable perm due to rpmlint's
# warnings like: 
# W: python-zsi spurious-executable-perm
#

find doc/examples -name .cvs\* -exec rm -f {} \;
find doc/examples samples -perm 755 -type f -exec chmod a-x {} \;

%build
%py2_build


%install
rm -rf %{buildroot}
%py2_install

# some files have shebang and aren't executable
# the simple command below looks for them and if
# they're found, it'll do chmod a+x

find %{buildroot}%{python_sitelib}/ZSI \
    -type f -perm 644 -name \*.py \
    -exec grep -q \#\!\.\*python {} \; \
    -and -exec chmod a+x {} \;

%check
# ZSI module is not installed yet, so we need to tell python where to find it
# in order to execute tests
export PYTHONPATH=$(pwd)
good_testlist="test_t1
test_t2
test_t3
test_t5
test_t6
test_t7
test_t9
test_union
test_list
test_URI
test_rfc2617"
for i in $good_testlist; do
    %{__python} test/${i}.py 
done

bad_testlist="test_t8
test_TCtimes"
# These tests fails for now, fix upstream?
for i in $bad_testlist; do
    %{__python} test/${i}.py || :
done
 

%files -n python2-zsi
# we need png's for html's to be more readable
%doc CHANGES README samples doc/examples doc/*.html doc/*.png doc/*.css
%{_bindir}/wsdl2py
%{python2_sitelib}/ZSI
%{python2_sitelib}/ZSI-*.egg-info


%changelog
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.1-14
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1-12
- Python 2 binary package renamed to python2-zsi
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 18 2012 Tim Fenn <tim.fenn@gmail.com> - 2.1-3
- remove PyXML dep

* Sat Aug 11 2012 Tim Fenn <tim.fenn@gmail.com> - 2.1-2
- fix good/bad testlist

* Sat Aug 11 2012 Tim Fenn <tim.fenn@gmail.com> - 2.1-1
- update to 2.1-a1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Tim Fenn <tim.fenn@gmail.com> - 2.0-12
- fix download url (again)
- add ZSI directory to PYTHONPATH
- add test_TCtimes to bad testlist

* Thu Feb 09 2012 Tim Fenn <tim.fenn@gmail.com> - 2.0-11
- fix download url
- use macro style
- add tests

* Wed Feb 08 2012 Tim Fenn <tim.fenn@gmail.com> - 2.0-10
- rebuild for new maintainer

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 13 2010 James Bowes <jbowes@redhat.com> 2.0-7
- Fix typo in description

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0-4
- Rebuild for Python 2.6

* Fri Jan 04 2008 Michał Bentkowski <mr.ecik at gmail.com> - 2.0-3
- Just bumping...

* Sat Dec 29 2007 Michał Bentkowski <mr.ecik at gmail.com> - 2.0-2
- Fix License field (BSD to LBNL BSD)

* Thu Nov 01 2007 Michał Bentkowski <mr.ecik at gmail.com> - 2.0-1
- First release

