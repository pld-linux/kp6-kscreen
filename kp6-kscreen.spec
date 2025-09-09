#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.4.5
%define		qtver		5.15.2
%define		kpname		kscreen
Summary:	KDE's screen management software
Name:		kp6-%{kpname}
Version:	6.4.5
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	f6c549d14a00f329135d11688750dab4
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	kf6-kconfig-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-kdbusaddons-devel
BuildRequires:	kf6-kglobalaccel-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-kxmlgui-devel
BuildRequires:	kp6-libkscreen-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KDE's screen management software.

%package data
Summary:	Data files for %{kpname}
Summary(pl.UTF-8):	Dane dla %{kpname}
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Obsoletes:	kp5-%{kpname}-data < 6
BuildArch:	noarch

%description data
Data files for %{kpname}.

%description data -l pl.UTF-8
Dane dla %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post data
%update_desktop_database_post

%postun data
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hdrcalibrator
%attr(755,root,root) %{_bindir}/kscreen-console
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/kscreen.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_kscreen.so
%attr(755,root,root) %{_prefix}/libexec/kscreen_osd_service
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/applets/org.kde.kscreen.so

%files data -f %{kpname}.lang
%defattr(644,root,root,755)
%{_datadir}/qlogging-categories6/kscreen.categories
%{systemduserunitdir}/plasma-kscreen-osd.service
%{_desktopdir}/kcm_kscreen.desktop
%{_datadir}/dbus-1/services/org.kde.kscreen.osdService.service
%{_datadir}/kglobalaccel/org.kde.kscreen.desktop
%{_datadir}/kscreen
