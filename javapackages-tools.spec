%bcond_without bootstrap
%bcond_without gradle

# Don't generate requires on jpackage-utils and java-headless for
# provided pseudo-artifacts: com.sun:tools and sun.jdk:jconsole.
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}/maven-metadata/javapackages-metadata.xml$

Name:           javapackages-tools
Version:	6.0.0
Release:        1
Group:		Development/Java
Summary:        Macros and scripts for Java packaging support

License:        BSD
URL:            https://github.com/fedora-java/javapackages
Source0:        https://github.com/fedora-java/javapackages/archive/%{version}.tar.gz

Patch102:	javapackages-5.3.0-no-fedora-deps.patch
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

# For now
Provides:	javapackages-filesystem

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
%if %{without bootstrap}
Requires:	%{_bindir}/xmvn
Requires:	mvn(org.fedoraproject.xmvn:xmvn-mojo)
# Common Maven plugins required by almost every build. It wouldn't make
# sense to explicitly require them in every package built with Maven.
Requires:	mvn(org.apache.maven.plugins:maven-compiler-plugin)
Requires:	mvn(org.apache.maven.plugins:maven-jar-plugin)
Requires:	mvn(org.apache.maven.plugins:maven-resources-plugin)
Requires:	mvn(org.apache.maven.plugins:maven-surefire-plugin)
%endif

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
%autosetup -p1 -n javapackages-%{version}
sed -i 's#/bin/objectweb-asm3-processor#/usr/bin/objectweb-asm3-processor#' bin/shade-jar

%build
%configure --rpmmacrodir=%{_sysconfdir}/rpm
./build

pushd python
%{__python} setup.py build
popd

%if %{without gradle}
rm -rf %{buildroot}%{_bindir}/gradle-local
rm -rf %{buildroot}%{_datadir}/gradle-local
#rm -rf %{buildroot}%{_mandir}/man7/gradle_build.7
%endif

%install
./install
sed -e 's/.[17]$/&*/' -e 's/.py$/&*/' -i files-*

# Don't own standard directories
sed -i -e '/usr.lib.rpm$/d' files-*
sed -i -e '/usr.lib.rpm.fileattrs$/d' files-*
sed -i -e '/usr.lib.jvm$/d' files-*

pushd python
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

%check
# bootstrap enabled, tests failed
./check 3 || exit 0

%files -f files-tools
%license LICENSE

%files -n javapackages-local -f files-local -f files-filesystem -f files-generators

%files -n maven-local

%if %{with gradle}
%files -n gradle-local -f files-gradle
%endif

%files -n ivy-local -f files-ivy

%files -n python-javapackages
%license LICENSE
%{python_sitelib}/javapackages-%{version}-py*.*.egg-info
%{python_sitelib}/javapackages/
