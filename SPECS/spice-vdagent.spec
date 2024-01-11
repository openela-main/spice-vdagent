Name:           spice-vdagent
Version:        0.20.0
Release:        5%{?dist}
Summary:        Agent for Spice guests
Group:          Applications/System
License:        GPLv3+
URL:            https://spice-space.org/
Source0:        https://spice-space.org/download/releases/%{name}-%{version}.tar.bz2
Source1:        https://spice-space.org/download/releases/%{name}-%{version}.tar.bz2.sig
Source2:        victortoso-E37A484F.keyring
Patch0001:      0001-vdagentd-work-around-GLib-s-fork-issues.patch
Patch0002:      0002-vdagentd-init-static-uinput-before-fork.patch
Patch0003:      0003-systemd-login-Avoid-a-crash-on-container.patch
Patch0004:      0004-Fix-possible-compile-error-using-former-GLib2-versio.patch
Patch0005:      0005-vdagentd-Use-bool-for-agent_owns_clipboard-and-clien.patch
Patch0006:      0006-vdagentd-Automatically-release-agent_data.patch
Patch0007:      0007-vdagent-connection-Pass-err-to-g_credentials_get_uni.patch
Patch0008:      0008-vdagentd-Better-check-for-vdagent_connection_get_pee.patch
Patch0009:      0009-vdagentd-Avoid-calling-chmod.patch
Patch0010:      0010-Avoids-unchecked-file-transfer-IDs-allocation-and-us.patch
Patch0011:      0011-Avoids-uncontrolled-active_xfers-allocations.patch
Patch0012:      0012-Avoids-unlimited-agent-connections.patch
Patch0013:      0013-Avoids-user-session-hijacking.patch
Patch0014:      0014-Better-check-for-sessions.patch
Patch0015:      0015-vdagentd-Limit-number-of-agents-per-session-to-1.patch
Patch0016:      0016-cleanup-active_xfers-when-the-client-disconnects.patch
Patch0017:      0017-vdagentd-do-not-allow-to-use-an-already-used-file-xf.patch
Patch0018:      0018-Add-a-test-for-session_info.patch
Patch0019:      0019-wayland-fix-monitor-mapping-issues.patch
Patch0020:      0020-vdagent-udscs-limit-retry-to-connect-to-vdagentd.patch
Patch0021:      0021-udscs-udscs_connect-return-error-to-caller.patch
Patch0022:      0022-Do-not-process-X11-events-in-vdagent_x11_create.patch
Patch0023:      0023-vdagent-Remove-watch-event-on-vdagent_display_destro.patch 

BuildRequires:  git-core gnupg2
BuildRequires:  systemd-devel
BuildRequires:  glib2-devel >= 2.50
BuildRequires:  spice-protocol >= 0.14.1
BuildRequires:  libpciaccess-devel libXrandr-devel libXinerama-devel
BuildRequires:  libXfixes-devel systemd desktop-file-utils libtool
BuildRequires:  alsa-lib-devel dbus-devel libdrm-devel
%{?systemd_requires}

%description
Spice agent for Linux guests offering the following features:

Features:
* Client mouse mode (no need to grab mouse by client, no mouse lag)
  this is handled by the daemon by feeding mouse events into the kernel
  via uinput. This will only work if the active X-session is running a
  spice-vdagent process so that its resolution can be determined.
* Automatic adjustment of the X-session resolution to the client resolution
* Support of copy and paste (text and images) between the active X-session
  and the client


%prep
gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -S git_am
#autoreconf -fi


%build
%configure --with-session-info=systemd --with-init-script=systemd
make %{?_smp_mflags} V=2


%install
make install DESTDIR=$RPM_BUILD_ROOT V=2


%post
%systemd_post spice-vdagentd.service spice-vdagentd.socket

%preun
%systemd_preun spice-vdagentd.service spice-vdagentd.socket

%postun
%systemd_postun_with_restart spice-vdagentd.service spice-vdagentd.socket


%files
%doc COPYING CHANGELOG.md README.md
/usr/lib/udev/rules.d/70-spice-vdagentd.rules
%{_unitdir}/spice-vdagentd.service
%{_unitdir}/spice-vdagentd.socket
%{_prefix}/lib/tmpfiles.d/spice-vdagentd.conf
%{_bindir}/spice-vdagent
%{_sbindir}/spice-vdagentd
%{_var}/run/spice-vdagentd
%{_sysconfdir}/xdg/autostart/spice-vdagent.desktop
# For /usr/share/gdm/autostart/LoginWindow/spice-vdagent.desktop
# We own the dir too, otherwise we must Require gdm
%{_datadir}/gdm
%{_mandir}/man1/%{name}*.1*


%changelog
* Mon Jan 16 2023 Victor Toso <victortoso@redhat.com> 0.20.0-5
- Fix upstream segfault on X11 events
  Resolves: rhbz#2145004

* Tue Dec 21 2021 Victor Toso <victortoso@redhat.com> 0.20.0-4
- Do not flood the journal with retry messages.
  Resolves: rhbz#2005802

* Wed Jan 20 2021 Julien Ropé <jrope@redhat.com> - 0.20.0-3
- Fix mouse problems in multi-monitor environments under Wayland
  Resolves: rhbz#1790904 rhbz#1824610

* Mon Oct 19 2020 Frediano Ziglio <fziglio@redhat.com> 0.20.0-2
- Resolves: CVE-2020-25650, CVE-2020-25651, CVE-2020-25652, CVE-2020-25653

* Fri May 15 2020 Victor Toso <victortoso@redhat.com> 0.20.0-1
- Update to 0.20.0
- Backport fixes post-release
  Resolves: rhbz#1817476

* Tue Aug 27 2019 Victor Toso <victortoso@redhat.com> 0.19.0-3
- Fix two new covscan warnings
  Resolves: rhbz#1660566

* Mon Aug 19 2019 Victor Toso <victortoso@redhat.com> 0.19.0-2
- Fix some covscan warnings from latest build
  Resolves: rhbz#1660566

* Mon May 20 2019 Victor Toso <victortoso@redhat.com> 0.19.0-1
- Update to 0.19.0
  Resolves: rhbz#1711975
- Validate tarball with gpg

* Tue Dec 18 2018 Victor Toso <victortoso@redhat.com> 0.18.0-3
- Fix leak of unix sockets.
  Resolves: rhbz#1660108

* Thu Nov 15 2018 Victor Toso <victortoso@redhat.com> 0.18.0-2
- Fix unusable mouse on xorg resolution event in wayland
  Resolves: rhbz#1641723

* Tue Jun 12 2018 Victor Toso <victortoso@redhat.com> 0.18.0-1
- Update to spice-vdagent 0.18.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.17.0-5
- Fix systemd executions/requirements

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 22 2016 Christophe Fergeau <cfergeau@redhat.com> 0.17.0-1
- Update to spice-vdagent 0.17.0

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 05 2015 Christophe Fergeau <cfergeau@redhat.com> 0.16.0-2
- Add upstream patch fixing a memory corruption bug (double free)
  Resolves: rhbz#1268666
  Exit with a non-0 exit code when the virtio device cannot be opened by the
  agent

* Tue Jun 30 2015 Christophe Fergeau <cfergeau@redhat.com> 0.16.0-1
- Update to 0.16.0 release

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.15.0-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 14 2013 Alon Levy <alevy@redhat.com> - 0.15.0-1
- New upstream release 0.15.0

* Tue Sep 10 2013 Hans de Goede <hdegoede@redhat.com> - 0.14.0-5
- Silence session agent error logging when not running in a vm (rhbz#999804)
- Release guest clipboard ownership on client disconnect (rhbz#1003977)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul  3 2013 Hans de Goede <hdegoede@redhat.com> - 0.14.0-3
- Advertise clipboard line-endings for copy and paste line-ending conversion
- Build spice-vdagentd as pie + relro

* Mon May 20 2013 Hans de Goede <hdegoede@redhat.com> - 0.14.0-2
- Drop the no longer needed /etc/modules-load.d/spice-vdagentd.conf (#963201)

* Fri Apr 12 2013 Hans de Goede <hdegoede@redhat.com> - 0.14.0-1
- New upstream release 0.14.0
- Adds support for file transfers from client to guest
- Adds manpages for spice-vdagent and spice-vdagentd

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Hans de Goede <hdegoede@redhat.com> - 0.12.1-1
- New upstream release 0.12.1
- Fixes various issues with dynamic monitor / resolution support

* Mon Nov 12 2012 Hans de Goede <hdegoede@redhat.com> - 0.12.0-2
- Fix setting of mode on non arbitrary resolution capable X driver
- Fix wrong mouse coordinates on vms with multiple qxl devices

* Sat Sep  1 2012 Hans de Goede <hdegoede@redhat.com> - 0.12.0-1
- New upstream release 0.12.0
- This moves the tmpfiles.d to /usr/lib/tmpfiles.d (rhbz#840194)
- This adds a systemd .service file (rhbz#848102)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Hans de Goede <hdegoede@redhat.com> - 0.10.1-1
- New upstream release 0.10.1

* Thu Mar 22 2012 Hans de Goede <hdegoede@redhat.com> - 0.10.0-1
- New upstream release 0.10.0
- This supports using systemd-logind instead of console-kit (rhbz#756398)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Hans de Goede <hdegoede@redhat.com> 0.8.1-1
- New upstream release 0.8.1

* Fri Jul 15 2011 Hans de Goede <hdegoede@redhat.com> 0.8.0-2
- Make the per session agent process automatically reconnect to the system
  spice-vdagentd when the system daemon gets restarted

* Tue Apr 19 2011 Hans de Goede <hdegoede@redhat.com> 0.8.0-1
- New upstream release 0.8.0

* Mon Mar 07 2011 Hans de Goede <hdegoede@redhat.com> 0.6.3-6
- Fix setting of the guest resolution from a multi monitor client

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Hans de Goede <hdegoede@redhat.com> 0.6.3-4
- Make sysvinit script exit cleanly when not running on a spice enabled vm

* Fri Nov 19 2010 Hans de Goede <hdegoede@redhat.com> 0.6.3-3
- Put the pid and log files into their own subdir (#648553)

* Mon Nov  8 2010 Hans de Goede <hdegoede@redhat.com> 0.6.3-2
- Fix broken multiline description in initscript lsb header (#648549)

* Sat Oct 30 2010 Hans de Goede <hdegoede@redhat.com> 0.6.3-1
- Initial Fedora package
