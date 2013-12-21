%_javapackages_macros
%define git_commit 659fc71

Summary:       Java connection pool library
Name:          proxool
Version:       0.9.1
Release:       11.0%{?dist}
Epoch:         0
License:       ASL 2.0
URL:           http://proxool.sourceforge.net/
# Grabbing a newer version from git due to license change
# https://github.com/proxool/proxool/tarball/master
# (commit 659fc71e617151327779802a5171f0da8205918d)
Source0:       proxool-proxool-%{git_commit}.tar.gz
Source1:       proxool.pom
Patch0:        proxool-no-embedded-cglib.patch

BuildRequires: jpackage-utils
BuildRequires: java-devel >= 0:1.6.0
BuildRequires: ant >= 0:1.7.1
BuildRequires: ant-junit
BuildRequires: apache-commons-collections
BuildRequires: apache-commons-lang
BuildRequires: apache-commons-logging
BuildRequires: cglib
BuildRequires: dom4j
BuildRequires: avalon-framework
BuildRequires: hsqldb1
BuildRequires: junit
BuildRequires: log4j
BuildRequires: tomcat-servlet-3.0-api
BuildRequires: checkstyle

Requires: java >= 0:1.6.0
Requires: avalon-logkit
Requires: dom4j
Requires: jta
Requires: jpackage-utils
BuildArch: noarch

%description
Transparently adds connection pooling to your existing JDBC driver.
Complies with the J2SE API, giving you the confidence to develop to
standards. You can monitor the performance of your database
connections and listen to connection events.
It's easy to configure using the JDBC API, XML, or Java property
files - you decide.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{git_commit}
#find . -name "*.jar" -exec rm {} \;
find . -type f -a -executable -exec chmod -x {} \;
rm -rf lib jarjar

%patch0 -p1 -b .sav0

%build
CLASSPATH=$(build-classpath cglib avalon-framework servlet) ant build-jar javadoc

%install
# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}
install -m 0644 build/%{name}-%{version}.jar \
$RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# pom
install -d -m 0755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -m 0644 %{S:1} $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%doc *.txt
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENCE.txt
%doc %{_javadocdir}/%{name}
