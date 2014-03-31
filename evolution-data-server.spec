%define		basever		3.12
%define		apiver		1.2
%define		apiver3		3.0

Summary:	Evolution data server
Name:		evolution-data-server
Version:	3.12.0
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/evolution-data-server/%{basever}/%{name}-%{version}.tar.xz
# Source0-md5:	a2e5b9dbf1ee8f879a7a7f162e5ea88c
URL:		http://www.ximian.com/products/ximian_evolution/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	db-devel
BuildRequires:	gnome-online-accounts-devel >= 3.12.0
BuildRequires:	intltool
BuildRequires:	krb5-devel
BuildRequires:	libgdata-devel >= 0.14.0
BuildRequires:	libgnome-keyring-devel >= 3.12.0
BuildRequires:	libgweather-devel >= 3.12.0
BuildRequires:	libical-devel
BuildRequires:	libsoup-devel >= 2.46.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	nspr-devel
BuildRequires:	nss-devel
BuildRequires:	openldap-devel
BuildRequires:	pkg-config
BuildRequires:	vala-vapigen >= 0.24.0
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
The Evolution data server for the calendar and addressbook.

%package libs
Summary:	Evolution Data Server library
Group:		Libraries

%description libs
This package contains Evolution Data Server library.

%package devel
Summary:	Evolution data server development files
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the files necessary to develop applications
using Evolution's data server libraries.

%package apidocs
Summary:	e-d-s API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
e-d-s API documentation.

%prep
%setup -q
# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' 		\
    -i -e '/GNOME_CODE_COVERAGE/d' configure.ac
find . -name Makefile.am -print | xargs sed -i -e '/@GNOME_CODE_COVERAGE_RULES@/d'
%{__sed} -i -e 's/services tests docs/services docs/' Makefile.am

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules		\
	--disable-static		\
	--disable-uoa			\
	--enable-vala-bindings		\
	--with-html-dir=%{_gtkdocdir}	\
	--with-krb5=%{_prefix}		\
	--with-libdb=%{_libdir}		\
	--with-openldap=yes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT		\
	HTML_DIR=%{_gtkdocdir}		\
	pkgconfigdir=%{_pkgconfigdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libexecdir}/*/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS* README
%dir %{_libexecdir}
%dir %{_libexecdir}/addressbook-backends
%dir %{_libexecdir}/calendar-backends
%dir %{_libexecdir}/camel-providers
%dir %{_libexecdir}/registry-modules
%attr(755,root,root) %{_libexecdir}/addressbook-backends/*.so
%attr(755,root,root) %{_libexecdir}/calendar-backends/*.so
%attr(755,root,root) %{_libexecdir}/camel-index-control-%{apiver}
%attr(755,root,root) %{_libexecdir}/camel-lock-helper-%{apiver}
%attr(755,root,root) %{_libexecdir}/camel-providers/*.so
%attr(755,root,root) %{_libexecdir}/evolution-addressbook-factory
%attr(755,root,root) %{_libexecdir}/evolution-calendar-factory
%attr(755,root,root) %{_libexecdir}/evolution-source-registry
%attr(755,root,root) %{_libexecdir}/evolution-user-prompter
%attr(755,root,root) %{_libexecdir}/registry-modules/*.so
%{_libdir}/%{name}/camel-providers/*.urls
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.AddressBook.service
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.Calendar.service
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.Sources.service
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.UserPrompter.service
%{_datadir}/glib-2.0/schemas/*.xml
%{_pixmapsdir}/%{name}

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libcamel-%{apiver}.so.??
%attr(755,root,root) %ghost %{_libdir}/libebackend-%{apiver}.so.?
%attr(755,root,root) %ghost %{_libdir}/libebook-%{apiver}.so.??
%attr(755,root,root) %ghost %{_libdir}/libebook-contacts-%{apiver}.so.?
%attr(755,root,root) %ghost %{_libdir}/libecal-%{apiver}.so.??
%attr(755,root,root) %ghost %{_libdir}/libedata-book-%{apiver}.so.??
%attr(755,root,root) %ghost %{_libdir}/libedata-cal-%{apiver}.so.??
%attr(755,root,root) %ghost %{_libdir}/libedataserver-%{apiver}.so.??
%attr(755,root,root) %{_libdir}/libcamel-%{apiver}.so.*.*.*
%attr(755,root,root) %{_libdir}/libebackend-%{apiver}.so.*.*.*
%attr(755,root,root) %{_libdir}/libebook-%{apiver}.so.*.*.*
%attr(755,root,root) %{_libdir}/libebook-contacts-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebook-contacts-%{apiver}.so.*.*.*
%attr(755,root,root) %{_libdir}/libecal-%{apiver}.so.*.*.*
%attr(755,root,root) %{_libdir}/libedata-book-%{apiver}.so.*.*.*
%attr(755,root,root) %{_libdir}/libedata-cal-%{apiver}.so.*.*.*
%attr(755,root,root) %{_libdir}/libedataserver-%{apiver}.so.*.*.*
%{_libdir}/girepository-1.0/EBook-%{apiver}.typelib
%{_libdir}/girepository-1.0/EBookContacts-%{apiver}.typelib
%{_libdir}/girepository-1.0/EDataServer-%{apiver}.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamel-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebackend-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebook-%{apiver}.so
%attr(755,root,root) %{_libdir}/libecal-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedata-book-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedata-cal-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedataserver-%{apiver}.so
%{_includedir}/evolution-data-server
%{_pkgconfigdir}/*.pc
%{_datadir}/gir-1.0/EBook-1.2.gir
%{_datadir}/gir-1.0/EBookContacts-1.2.gir
%{_datadir}/gir-1.0/EDataServer-1.2.gir
%{_datadir}/vala/vapi/libebook-1.2.deps
%{_datadir}/vala/vapi/libebook-1.2.vapi
%{_datadir}/vala/vapi/libebook-contacts-1.2.deps
%{_datadir}/vala/vapi/libebook-contacts-1.2.vapi
%{_datadir}/vala/vapi/libedataserver-1.2.deps
%{_datadir}/vala/vapi/libedataserver-1.2.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/camel
%{_gtkdocdir}/eds

