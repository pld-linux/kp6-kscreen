#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.0.3
%define		qtver		5.15.2
%define		kpname		kscreen
Summary:	KDE's screen management software
Name:		kp6-%{kpname}
Version:	6.0.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	8e1c31ac47e3f5751fa0415c77ffdb93
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
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KDE's screen management software.

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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kscreen-console
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/kscreen.so
%{_datadir}/metainfo/org.kde.kscreen.appdata.xml
%dir %{_datadir}/plasma/plasmoids/org.kde.kscreen
%dir %{_datadir}/plasma/plasmoids/org.kde.kscreen/contents
%dir %{_datadir}/plasma/plasmoids/org.kde.kscreen/contents/ui
%{_datadir}/plasma/plasmoids/org.kde.kscreen/contents/ui/InhibitionHint.qml
%{_datadir}/plasma/plasmoids/org.kde.kscreen/contents/ui/PresentationModeItem.qml
%{_datadir}/plasma/plasmoids/org.kde.kscreen/contents/ui/ScreenLayoutSelection.qml
%{_datadir}/plasma/plasmoids/org.kde.kscreen/contents/ui/main.qml
%{_datadir}/plasma/plasmoids/org.kde.kscreen/metadata.json
%{_datadir}/qlogging-categories6/kscreen.categories
%{systemduserunitdir}/plasma-kscreen-osd.service
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_kscreen.so
%attr(755,root,root) %{_prefix}/libexec/kscreen_osd_service
%{_desktopdir}/kcm_kscreen.desktop
%{_datadir}/dbus-1/services/org.kde.kscreen.osdService.service
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/applets/org.kde.kscreen.so
%{_datadir}/kglobalaccel/org.kde.kscreen.desktop
