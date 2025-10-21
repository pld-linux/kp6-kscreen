#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.5.0
%define		kframever	6.14.0
%define		qtver		6.8.0
%define		kpname		kscreen
Summary:	KDE's screen management software
Name:		kp6-%{kpname}
Version:	6.5.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	11eb944d9aeb139e10e2f7f261a81d89
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Sensors-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6WaylandClient-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-ksvg-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	kp6-layer-shell-qt-devel >= %{version}
BuildRequires:	kp6-libkscreen-devel >= %{version}
BuildRequires:	kp6-libplasma-devel >= %{version}
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	wayland-protocols >= 1.41
BuildRequires:	xcb-util-devel
BuildRequires:	xorg-lib-libX11-devel
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
%{_libdir}/qt6/plugins/kf6/kded/kscreen.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_kscreen.so
%attr(755,root,root) %{_prefix}/libexec/kscreen_osd_service
%{_libdir}/qt6/plugins/plasma/applets/org.kde.kscreen.so

%files data -f %{kpname}.lang
%defattr(644,root,root,755)
%{_datadir}/qlogging-categories6/kscreen.categories
%{systemduserunitdir}/plasma-kscreen-osd.service
%{_desktopdir}/kcm_kscreen.desktop
%{_datadir}/dbus-1/services/org.kde.kscreen.osdService.service
%{_datadir}/kglobalaccel/org.kde.kscreen.desktop
