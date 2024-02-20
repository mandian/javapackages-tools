%bcond_without xmvn_generator
%bcond_without ivy

%global default_jdk %{_prefix}/lib/jvm/java-21-openjdk
%global default_jre %{_prefix}/lib/jvm/jre-21-openjdk

%global maven_home %{_usr}/share/xmvn

Name:           javapackages-tools
Version:        6.2.0
Release:        2
Summary:        Macros and scripts for Java packaging support
License:        BSD-3-Clause
URL:            https://github.com/fedora-java/javapackages
BuildArch:      noarch

Source0:        https://github.com/fedora-java/javapackages/archive/%{version}.tar.gz
Source3:        javapackages-config.json

Source8:        toolchains-openjdk8.xml
Source11:       toolchains-openjdk11.xml
Source17:       toolchains-openjdk17.xml
Source21:       toolchains-openjdk21.xml

Patch0:         0001-coverage-use-usercustomize.patch
Patch1:		javapackages-no-dupes.patch

BuildRequires:  coreutils
BuildRequires:  which
BuildRequires:  make
BuildRequires:  asciidoc
BuildRequires:  xmlto
BuildRequires:  python-devel
BuildRequires:  python-lxml
BuildRequires:  python-setuptools
BuildRequires:  python-pytest

Requires:       javapackages-filesystem = %{version}-%{release}
Requires:       coreutils
Requires:       findutils
Requires:       which
# default JRE
Requires:       jdk-current

Provides:       jpackage-utils = %{version}-%{release}

%description
This package provides macros and scripts to support Java packaging.

%package -n javapackages-filesystem
Summary:        Java packages filesystem layout
Provides:       eclipse-filesystem = %{version}-%{release}

%description -n javapackages-filesystem
This package provides some basic directories into which Java packages
install their content.

%package -n maven-local
Summary:        Macros and scripts for Maven packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}
Requires:       xmvn-minimal
Requires:       mvn(org.fedoraproject.xmvn:xmvn-mojo)
# Common Maven plugins required by almost every build. It wouldn't make
# sense to explicitly require them in every package built with Maven.
Requires:       mvn(org.apache.maven.plugins:maven-compiler-plugin)
Requires:       mvn(org.apache.maven.plugins:maven-jar-plugin)
Requires:       mvn(org.apache.maven.plugins:maven-resources-plugin)
Requires:       mvn(org.apache.maven.plugins:maven-surefire-plugin)

%description -n maven-local
This package provides macros and scripts to support packaging Maven artifacts.

%if %{with ivy}
%package -n ivy-local
Summary:        Local mode for Apache Ivy
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}
Requires:       apache-ivy >= 2.3.0-8
Requires:       xmvn-connector-ivy

%description -n ivy-local
This package implements local mode for Apache Ivy, which allows
artifact resolution using XMvn resolver.
%endif

%package -n python-javapackages
Summary:        Module for handling various files for Java packaging
Requires:       python-lxml

%description -n python-javapackages
Module for handling, querying and manipulating of various files for Java
packaging in Linux distributions

%package -n javapackages-local
Summary:        Non-essential macros and scripts for Java packaging support
Requires:       javapackages-common = %{version}-%{release}
# Java build systems don't have hard requirement on java-devel, so it should be there
Requires:       jdk-current
Requires:       xmvn-tools
%if %{with xmvn_generator}
Requires:       xmvn-generator
%endif

%description -n javapackages-local
This package provides non-essential macros and scripts to support Java packaging.

%package -n javapackages-generators
Summary:        RPM dependency generators for Java packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       python-javapackages = %{version}-%{release}
Requires:       python

%description -n javapackages-generators
RPM dependency generators to support Java packaging.

%package -n javapackages-common
Summary:        Non-essential macros and scripts for Java packaging support
Requires:       javapackages-generators = %{version}-%{release}

%description -n javapackages-common
This package provides non-essential, but commonly used macros and
scripts to support Java packaging.

%package -n javapackages-compat
Summary:        Previously deprecated macros and scripts for Java packaging support
Requires:       javapackages-local = %{version}-%{release}

%description -n javapackages-compat
This package provides previously deprecated macros and scripts to
support Java packaging as well as some additions to them.

%package -n maven-local-openjdk8
Summary:        OpenJDK 8 toolchain for XMvn
RemovePathPostfixes: -openjdk8
Requires:       maven-local
Requires:       java-1.8.0-openjdk-devel

%description -n maven-local-openjdk8
OpenJDK 8 toolchain for XMvn

%package -n maven-local-openjdk11
Summary:        OpenJDK 11 toolchain for XMvn
RemovePathPostfixes: -openjdk11
Requires:       maven-local
Requires:       java-11-openjdk-devel

%description -n maven-local-openjdk11
OpenJDK 11 toolchain for XMvn

%package -n maven-local-openjdk17
Summary:        OpenJDK 17 toolchain for XMvn
RemovePathPostfixes: -openjdk17
Requires:       maven-local
Requires:       java-17-openjdk-devel

%description -n maven-local-openjdk17
OpenJDK 17 toolchain for XMvn

%package -n maven-local-openjdk21
Summary:        OpenJDK 21 toolchain for XMvn
RemovePathPostfixes: -openjdk21
Requires:       maven-local
Requires:       java-21-openjdk-devel

%description -n maven-local-openjdk21
OpenJDK 21 toolchain for XMvn

%prep
%autosetup -p1 -n javapackages-%{version}

%build
%configure --pyinterpreter=%{_bindir}/python \
    --default_jdk=%{default_jdk} --default_jre=%{default_jre} \
    --rpmmacrodir=%{_rpmmacrodir}
./build

%install
./install

sed -e 's/.[17]$/&*/' -i files-*

rm -rf %{buildroot}%{_bindir}/gradle-local
rm -rf %{buildroot}%{_datadir}/gradle-local
rm -rf %{buildroot}%{_mandir}/man7/gradle_build.7
%if %{without ivy}
rm -rf %{buildroot}%{_sysconfdir}/ivy
rm -rf %{buildroot}%{_sysconfdir}/ant.d
%endif

mkdir -p %{buildroot}%{maven_home}/conf/
cp -p %{SOURCE8} %{buildroot}%{maven_home}/conf/toolchains.xml-openjdk8
cp -p %{SOURCE11} %{buildroot}%{maven_home}/conf/toolchains.xml-openjdk11
cp -p %{SOURCE17} %{buildroot}%{maven_home}/conf/toolchains.xml-openjdk17
cp -p %{SOURCE21} %{buildroot}%{maven_home}/conf/toolchains.xml-openjdk21

install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/java/javapackages-config.json

# Don't own standard directories
sed -i -e '/fileattrs$/d' files-generators

%if 0%{?flatpak}
# make both /app (runtime deps) and /usr (build-only deps) builds discoverable
sed -e '/^JAVA_LIBDIR=/s|$|:/usr/share/java|' \
    -e '/^JNI_LIBDIR=/s|$|:/usr/lib/java|' \
    -i %{buildroot}%{_sysconfdir}/java/java.conf
# /usr path is hard-coded in xmvn
ln -s %{_datadir}/java-utils %{buildroot}%{_usr}/share/java-utils
%endif

%check
./check

%files -f files-tools
%if 0%{?flatpak}
%{_usr}/share/java-utils
%endif

%files -n javapackages-filesystem -f files-filesystem

%files -n javapackages-generators -f files-generators

%files -n javapackages-common -f files-common

%files -n javapackages-compat -f files-compat

%files -n javapackages-local

%files -n maven-local

%if %{with ivy}
%files -n ivy-local -f files-ivy
%endif

%files -n maven-local-openjdk8
%dir %{maven_home}/conf
%{maven_home}/conf/toolchains.xml-openjdk8

%files -n maven-local-openjdk11
%dir %{maven_home}/conf
%{maven_home}/conf/toolchains.xml-openjdk11

%files -n maven-local-openjdk17
%dir %{maven_home}/conf
%{maven_home}/conf/toolchains.xml-openjdk17

%files -n maven-local-openjdk21
%dir %{maven_home}/conf
%{maven_home}/conf/toolchains.xml-openjdk21

%files -n python-javapackages -f files-python
%license LICENSE
