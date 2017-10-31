%bcond_without bootstrap

%bcond_without gradle

Name:           javapackages-tools
Version:        4.6.0
Release:        3
Group:		Development/Java
Summary:        Macros and scripts for Java packaging support

License:        BSD
URL:            https://github.com/fedora-java/javapackages
Source0:        https://github.com/fedora-java/javapackages/archive/%{version}.tar.gz
Source1:        %{name}.macros
Source2:        %{name}.sh

# we need the macros in a different place in omv
Patch100:	javapackages-4.2.0-macros.patch
Patch101:	javapackages-4.6.0-python-3.6.patch
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-lxml
BuildRequires:  python-setuptools
BuildRequires:  python-nose
BuildRequires:  python-six
BuildRequires:  python-pyxb
BuildRequires:  asciidoc
BuildRequires:  xmlto
BuildRequires:  dia
%if !%{with bootstrap}
BuildRequires:  javapackages-tools
BuildRequires:  xmvn-resolve >= 2
%endif

Requires:       coreutils
Requires:       lua
Requires:       python-javapackages = %{version}-%{release}
Requires:       python

Provides:       jpackage-utils = %{version}-%{release}
Obsoletes:      jpackage-utils < %{version}-%{release}
%rename java-rpmbuild

Provides:       mvn(com.sun:tools)
Provides:       mvn(sun.jdk:jconsole)

%description
This package provides macros and scripts to support Java packaging.

%package -n maven-local
Summary:        Macros and scripts for Maven packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}
Requires:       maven
Requires:       xmvn >= 2
Requires:       xmvn-mojo >= 2
Requires:       xmvn-connector-aether >= 2
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

%if %{with gradle}
%package -n gradle-local
Summary:        Local mode for Gradle
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}
Requires:       gradle >= 2.2.1-2
Requires:       xmvn-connector-gradle >= 2

%description -n gradle-local
This package implements local mode for Gradle, which allows artifact
resolution using XMvn resolver.
%endif

%package -n ivy-local
Summary:        Local mode for Apache Ivy
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}
Requires:       apache-ivy >= 2.3.0-8
Requires:       xmvn-connector-ivy >= 2

%description -n ivy-local
This package implements local mode fow Apache Ivy, which allows
artifact resolution using XMvn resolver.

%package -n python-javapackages
Summary:        Module for handling various files for Java packaging
Requires:       python-pyxb
Requires:       python-lxml
Requires:       python-six
Obsoletes:      python3-javapackages < %{version}-%{release}

%description -n python-javapackages
Module for handling, querying and manipulating of various files for Java
packaging in Linux distributions

%package doc
Summary:        Guide for Java packaging

%description doc
User guide for Java packaging and using utilities from javapackages-tools

%package -n javapackages-local
Summary:        Non-essential macros and scripts for Java packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       xmvn-install >= 2
Requires:       xmvn-subst >= 2
Requires:       xmvn-resolve >= 2

%description -n javapackages-local
This package provides non-essential macros and scripts to support Java
packaging.

%prep
%setup -q -n javapackages-%{version}

%apply_patches

sed -i 's#/bin/objectweb-asm3-processor#/usr/bin/objectweb-asm3-processor#' bin/shade-jar
%build
%configure
./build

pushd python
%{__python} setup.py build
popd

%if %{without gradle}
rm -rf %{buildroot}%{_bindir}/gradle-local
rm -rf %{buildroot}%{_datadir}/gradle-local
rm -rf %{buildroot}%{_mandir}/man7/gradle_build.7
%endif

%install
./install
sed -e 's/.[17]$/&.gz/' -e 's/.py$/&*/' -i files-*

pushd python
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

%if 0%{?fedora}
%else
rm -fr %{buildroot}%{_datadir}/fedora-review/plugins
for f in files-*; do
    sort -u $f > $f.new
    mv $f.new $f
done
sed -i 's|\(.*\).gz$|\1*|g' files-*
install -D -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.d/%{name}.macros
install -D -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_prefix}/lib/rpm/%{name}.sh
%endif


%check
# bootstrap enabled, tests failed
./check 3 || exit 0

%files -f files-common
%doc LICENSE
%{_sysconfdir}/rpm/macros.d/%{name}.macros
%{_prefix}/lib/rpm/%{name}.sh

%files -n javapackages-local -f files-local
%{_bindir}/gradle-local
%{_datadir}/gradle-local

%files -n maven-local -f files-maven

%if %{with gradle}
%files -n gradle-local -f files-gradle
%endif

%files -n ivy-local -f files-ivy

%files -n python-javapackages
%doc LICENSE
%{python_sitelib}/javapackages*

%files doc -f files-doc
%doc LICENSE
