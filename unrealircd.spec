## Define global settings
%global _hardened_build 1
%global major_version 4
%global minor_version 0
%global micro_version 2

Name:		unrealircd
Version:	%{major_version}.%{minor_version}.%{micro_version}
Release:	2%{?dist}
Summary:	UnrealIRC Daemon

Group:		Applications/Communications
License:	GPLv2
URL:		http://www.unrealircd.com/
Source0:	https://www.unrealircd.org/unrealircd4/%{name}-%{version}.tar.gz
Source8:	%{name}.service
Source11:	%{name}.logrotate

BuildRequires: coreutils
BuildRequires: gzip
BuildRequires: pkgconf-pkg-config
BuildRequires: gcc
BuildRequires: make
BuildRequires: curl
BuildRequires: openssl
BuildRequires: pcre2
BuildRequires: c-ares
BuildRequires: argon2

BuildRequires: openssl-devel
BuildRequires: pcre2-devel
BuildRequires: c-ares-devel

BuildRequires: epel-release
BuildRequires: libargon2-devel

Requires: openssl
Requires: pcre2
Requires: c-ares
Requires: argon2

BuildRequires: systemd

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires:         systemd

%description
UnrealIRCd is an advanced IRC server that provides features for just
about everything.

%package devel
Group:		Development/Libraries
Summary:	Development headers for %{name}
Requires:	unrealircd = %{version}-%{release}

%description devel
The unrealircd-devel package contains the headers as part of the
unrealircd source. If you are planning on making your own modules
for unrealircd, you will need to install this package. If your
module will be using pcre2, tre, zlib, or c-ares, you will need
to install the -devel packages of those as well.

%prep
%setup -q

%build
%configure \
	--with-bindir=%{_bindir} \
	--with-datadir=%{_sharedstatedir}/%{name} \
	--with-confdir=%{_sysconfdir}/%{name} \
	--with-modulesdir=%{_libdir}/%{name} \
	--with-logdir=%{_localstatedir}/log/%{name} \
	--with-cachedir=%{_localstatedir}/cache/%{name} \
	--with-docdir=%{_docdir}/%{name}-%{version} \
	--with-tmpdir=%{_tmppath}/%{name} \
	--with-scriptdir=%{_libexecdir}/%{name} \
	--with-nick-history=2000 \
	--with-permissions=0644 \
	--with-system-pcre2 \
	--with-system-argon2 \
	--with-system-cares \
	--without-pidfile \
	--without-privatelibdir \
	--enable-dynamic-linking \
	--enable-ssl=%{_prefix}

make %{?_smp_mflags}

%install
rm -rf ${buildroot}

install -d -m 0755 ${buildroot}%{_bindir}

install -d -m 0750 ${buildroot}%{_sysconfdir}/%{name}
install -d -m 0750 ${buildroot}%{_sysconfdir}/%{name}/aliases
install -d -m 0750 ${buildroot}%{_sysconfdir}/%{name}/help
install -d -m 0750 ${buildroot}%{_sysconfdir}/%{name}/examples
install -d -m 0750 ${buildroot}%{_sysconfdir}/%{name}/ssl

install -d -m 0755 ${buildroot}%{_docdir}/%{name}-%{version}

install -d -m 0755 ${buildroot}%{_libdir}/%{name}
install -d -m 0755 ${buildroot}%{_libdir}/%{name}/usermodes
install -d -m 0755 ${buildroot}%{_libdir}/%{name}/chanmodes
install -d -m 0755 ${buildroot}%{_libdir}/%{name}/snomasks
install -d -m 0755 ${buildroot}%{_libdir}/%{name}/extbans
install -d -m 0755 ${buildroot}%{_libdir}/%{name}/third

install -d -m 0755 ${buildroot}%{_libexecdir}/%{name}

install -d -m 0700 ${buildroot}%{_sharedstatedir}/%{name}
install -d -m 0700 ${buildroot}%{_localstatedir}/log/%{name}
install -d -m 0700 ${buildroot}%{_localstatedir}/cache/%{name}

install -m 0755 src/ircd ${buildroot}%{_bindir}/unrealircd

install -m 0644 doc/conf/*.conf ${buildroot}%{_sysconfdir}/%{name}
install -m 0644 doc/conf/aliases/*.conf ${buildroot}%{_sysconfdir}/%{name}/aliases
install -m 0644 doc/conf/help/*.conf ${buildroot}%{_sysconfdir}/%{name}/help
install -m 0600 doc/conf/examples/*.conf ${buildroot}%{_sysconfdir}/%{name}/examples
install -m 0644 doc/conf/ssl/curl-ca-bundle.crt ${buildroot}%{_sysconfdir}/%{name}/ssl

install -m 0755 src/modules/*.so ${buildroot}%{_libdir}/%{name}
install -m 0755 src/modules/usermodes/*.so ${buildroot}%{_libdir}/%{name}/usermodes
install -m 0755 src/modules/chanmodes/*.so ${buildroot}%{_libdir}/%{name}/chanmodes
install -m 0755 src/modules/snomasks/*.so ${buildroot}%{_libdir}/%{name}/snomasks
install -m 0755 src/modules/extbans/*.so ${buildroot}%{_libdir}/%{name}/extbans

install -m 0644 %{SOURCE1} ${buildroot}%{_sysconfdir}/%{name}/ircd.motd
install -m 0644 %{SOURCE2} ${buildroot}%{_sysconfdir}/%{name}/ircd.rules
install -m 0644 %{SOURCE3} ${buildroot}%{_sysconfdir}/%{name}/oper.motd
install -m 0644 %{SOURCE4} ${buildroot}%{_sysconfdir}/%{name}/bot.motd
install -m 0770 %{SOURCE5} ${buildroot}%{_libexecdir}/%{name}/ircdutil
install -m 0600 %{SOURCE9} ${buildroot}%{_sharedstatedir}/unrealircd/ircd.tune

install -d -m 0755 ${buildroot}%{_sysconfdir}/logrotate.d 
install -m 0644 %{SOURCE11} ${buildroot}%{_sysconfdir}/logrotate.d/unrealircd

install -d -m 0755 ${buildroot}%{_unitdir}
install -m 0644 %{SOURCE8} ${buildroot}%{_unitdir}/unrealircd.service

install -d -m 0755 ${buildroot}%{_includedir}/%{name}
install -m 0755 include/*.h ${buildroot}%{_includedir}/%{name}

%pre
%{_sbindir}/groupadd -r unrealircd 2>/dev/null || :
%{_sbindir}/useradd -r -g unrealircd \
	-s /sbin/nologin -d %{_sysconfdir}/unrealircd \
	-c 'Unreal IRC Server' unrealircd 2>/dev/null || :

%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-, unrealircd, unrealircd, -)
%doc doc/Authors doc/coding-guidelines doc/tao.of.irc README
%attr(-,root,root) %{_bindir}/unrealircd

%attr(-,root,root) %{_sysconfdir}/logrotate.d/unrealircd
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/help
%dir %{_sysconfdir}/%{name}/examples
%dir %{_sysconfdir}/%{name}/ssl
%dir %{_sysconfdir}/%{name}/aliases
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/*.motd
%config(noreplace) %{_sysconfdir}/%{name}/*.rules
%config(noreplace) %{_sysconfdir}/%{name}/help/*.conf
%{_sysconfdir}/%{name}/examples/*.conf
%{_sysconfdir}/%{name}/ssl/curl-ca-bundle.crt
%config(noreplace) %{_sysconfdir}/%{name}/aliases/*.conf

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/usermodes
%dir %{_libdir}/%{name}/chanmodes
%dir %{_libdir}/%{name}/snomasks
%dir %{_libdir}/%{name}/extbans
%dir %{_libdir}/%{name}/third
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/usermodes/*.so
%{_libdir}/%{name}/chanmodes/*.so
%{_libdir}/%{name}/snomasks/*.so
%{_libdir}/%{name}/extbans/*.so

%dir %{_localstatedir}/log/%{name}
%dir %{_localstatedir}/cache/%{name}
%dir %{_sharedstatedir}/%{name}

%{_unitdir}/unrealircd.service

%files devel
%defattr (0644,root,root,0755)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h

%changelog
* Sun Apr 3 2016 Louis Abel <louis@shootthej.net> - 4.0.2-2
- Added -devel package for headers
- Added various plugins
- Updated License to GPLv2
- Updated Group

* Sat Apr 2 2016 Louis Abel <louis@shootthej.net> - 4.0.2-1
- Initial build for UnrealIRCd 4.0.2
- Enterprise Linux 6: Most functions moved to initscript
- util script created to compensate for lack of initscript in
- Enterprise Linux 7

