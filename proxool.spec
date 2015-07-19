%{?_javapackages_macros:%_javapackages_macros}
%define git_commit 659fc71

Summary:       Java connection pool library
Name:          proxool
Version:       0.9.1
Release:       13.1
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
BuildRequires: log4j12
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
%add_maven_depmap

%files -f .mfiles
%doc *.txt

%files javadoc
%doc LICENCE.txt
%doc %{_javadocdir}/%{name}

%changelog
* Sat Aug 17 2013 gil cattaneo <puntogil@libero.it> 0:0.9.1-11
- fix rhbz#992827
- fix BR list
- removed rpmlint problems
- minor changes to adapt to current guideline

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Andy Grimm <agrimm@gmail.com> - 0:0.9.1-7
- Fix cglib groupId in POM to match Fedora's cglib

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Andy Grimm <agrimm@gmail.com> - 0:0.9.1-5
- Remove executable permissions introduced in git repository

* Mon Dec 12 2011 Andy Grimm <agrimm@gmail.com> - 0:0.9.1-4
- Fix license, use git upstream source, and fix
  Requires for javadoc subpackage.

* Thu Oct 20 2011 Andy Grimm <agrimm@gmail.com> - 0:0.9.1-3
- add POM file

* Wed Oct 19 2011 Andy Grimm <agrimm@gmail.com> - 0:0.9.1-2
- spec file clean-up

* Fri Aug 26 2011 Andy Grimm <agrimm@gmail.com> - 0:0.9.1-1
- initial build

