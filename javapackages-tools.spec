%undefine _compress
%undefine _extension
Name:           javapackages-tools
Version:        4.2.0
Release:        1

Summary:        Macros and scripts for Java packaging support

License:        BSD
URL:            https://fedorahosted.org/javapackages/
Source0:        https://fedorahosted.org/released/javapackages/javapackages-%{version}.tar.xz
Source1:        %{name}.macros
Source2:        %{name}.sh

BuildArch:      noarch

BuildRequires:  jpackage-utils
BuildRequires:  asciidoc
BuildRequires:  docbook-style-xsl
BuildRequires:  xmlto
BuildRequires:  python-lxml
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-formencode
%if 0%{?fedora}
BuildRequires:  scl-utils-build
%else
# avoid circular dependency to generate these from _javapakcages_macros
Provides:       mvn(com.sun:tools) = SYSTEM
Provides:       mvn(sun.jdk:jconsole) = SYSTEM
%endif

Requires:       coreutils
%if 0%{?fedora}
Requires:       libxslt
%else
Requires:       xsltproc
%endif
Requires:       lua
Requires:       python
Requires:       python-javapackages = %{version}-%{release}

%if 0%{?fedora}
Provides:       jpackage-utils = %{version}-%{release}
Obsoletes:      jpackage-utils < %{version}-%{release}
%else
%rename jpackage-utils
%rename java-rpmbuild
%endif

%description
This package provides macros and scripts to support Java packaging.

%package -n maven-local
Summary:        Macros and scripts for Maven packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       maven
Requires:       xmvn >= 1.0.0-0.1
# POM files needed by maven itself
Requires:       apache-commons-parent
Requires:       apache-parent
Requires:       geronimo-parent-poms
Requires:       httpcomponents-project
Requires:       jboss-parent
Requires:       jvnet-parent
Requires:       maven-parent
Requires:       maven-plugins-pom
Requires:       mojo-parent
Requires:       objectweb-pom
Requires:       plexus-components-pom
Requires:       plexus-pom
Requires:       plexus-tools-pom
Requires:       sonatype-oss-parent
Requires:       weld-parent
# Common Maven plugins required by almost every build. It wouldn't make
# sense to explicitly require them in every package built with Maven.
Requires:       maven-assembly-plugin
Requires:       maven-compiler-plugin
Requires:       maven-enforcer-plugin
Requires:       maven-jar-plugin
Requires:       maven-javadoc-plugin
Requires:       maven-resources-plugin
Requires:       maven-surefire-plugin
# Tests based on JUnit are very common and JUnit itself is small.
# Include JUnit provider for Surefire just for convenience.
Requires:       maven-surefire-provider-junit
# testng is quite common as well
Requires:       maven-surefire-provider-testng

%description -n maven-local
This package provides macros and scripts to support packaging Maven artifacts.

%package -n python-javapackages
Summary:        Module for handling various files for Java packaging
Requires:       python-lxml

%description -n python-javapackages
Module for handling, querying and manipulating of various files for Java
packaging in Linux distributions

%package -n javapackages-local
Summary:        Non-essential macros and scripts for Java packaging support
Requires:       %{name} = %{version}-%{release}
# We want to use OpenJDK 8 for building packages as it is default
# implementation used in Fedora.  Due to YUM bugs and limitations,
# sometimes Java 7 may be installed alone.  To workaround this
# maven-local explicitly requires version 8 of OpenJDK.  (If needed
# Maven can still work with Java 7, but this needs to be enabled
# explicitly in the spec file.)
Requires:       java-1.8.0-openjdk-devel >= 1:1.8

%description -n javapackages-local
This package provides non-essential macros and scripts to support Java packaging.


%package -n ivy-local
Summary:        Local mode for Apache Ivy
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}

%description -n ivy-local
This package implements local mode fow Apache Ivy, which allows
artifact resolution using XMvn resolver.

%prep
%setup -q -n javapackages-%{version}
%apply_patches

%build
%configure
./build
pushd python
%{__python} setup.py build
popd

%install
./install
sed -e 's/.[17]$/&.xz/' -e 's/.py$/&*/' -i files-*

pushd python
%{__python} setup.py install --skip-build --root %{buildroot}
popd

rm -fr %{buildroot}%{_datadir}/fedora-review/plugins
for f in files-*; do
    sort -u $f > $f.new
    mv $f.new $f
done
sed -i 's|\(.*\).xz$|\1*|g' files-*
install -D -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.d/%{name}.macros
install -D -m755 %{SOURCE2} %{buildroot}%{_prefix}/lib/rpm/%{name}.sh

%check
#./check

%files -f files-common
%doc LICENSE
%{_sysconfdir}/rpm/macros.d/%{name}.macros
%{_prefix}/lib/rpm/%{name}.sh

%files -n javapackages-local -f files-local

%files -n maven-local -f files-maven

%files -n ivy-local -f files-ivy

%files -n python-javapackages
%doc LICENSE
%{python_sitelib}/javapackages*
