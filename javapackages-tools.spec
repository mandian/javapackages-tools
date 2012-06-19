Name:           javapackages-tools
Version:        0.3.1
Group:		Development/Java
Release:        1
Summary:        Mandriva macros and scripts for Java packaging support

License:        BSD
URL:            https://fedorahosted.org/javapackages/
Source0:        https://fedorahosted.org/released/javapackages/javapackages-%{version}.tar.xz

BuildArch:           noarch
Requires:            python

Conflicts:           jpackage-utils < 1.7.5-17

%description
Fedora macros and scripts for Java packaging support


%prep
%setup -q -n javapackages-%{version}

%build

%install
install -m0755 -D depgenerators/maven.prov %{buildroot}%{_rpmhome}/maven.prov
install -m0755 -D depgenerators/osgi.prov %{buildroot}%{_rpmhome}/osgi.prov
install -m0755 -D depgenerators/osgi.req %{buildroot}%{_rpmhome}/osgi.req
# Add the maven poms file attribute entry (rpm >= 4.9.0)
install -m0644 -D depgenerators/fileattrs/maven.attr \
                  %{buildroot}%{_rpmhome}/fileattrs/maven.attr
install -m0644 -D depgenerators/fileattrs/osgi.attr \
                  %{buildroot}%{_rpmhome}/fileattrs/osgi.attr

install -pm 644 -D macros.fjava ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm/macros.fjava
install -dm 755 %{buildroot}%{_javadir}-utils/
install -pm 644 scripts/maven_depmap.py %{buildroot}%{_javadir}-utils/


%files
%doc LICENSE
%dir %{_rpmhome}/fileattrs
%{_rpmhome}/fileattrs/*.attr
%{_rpmhome}/*.prov
%{_rpmhome}/*.req
%{_javadir}-utils/maven_depmap.py*
%config(noreplace) %{_sysconfdir}/rpm/macros.fjava

