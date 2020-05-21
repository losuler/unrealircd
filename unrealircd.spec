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

BuildRequires:	openssl-devel
BuildRequires:	tre-devel
BuildRequires:	zlib-devel
BuildRequires:	pcre2-devel
BuildRequires:	c-ares-devel
Requires:	openssl
Requires:	tre
Requires:	pcre2
Requires:	c-ares

BuildRequires:	systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:	systemd

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
	--with-showlistmodes \
	--with-bindir=%{_bindir} \
	--with-datadir=%{_sharedstatedir}/%{name} \
	--with-pidfile=%{_localstatedir}/run/%{name}/ircd.pid \
	--with-confdir=%{_sysconfdir}/%{name} \
	--with-modulesdir=%{_libdir}/%{name} \
	--with-logdir=%{_localstatedir}/log/%{name} \
	--with-cachedir=%{_localstatedir}/cache/%{name} \
	--with-docdir=%{_docdir}/%{name}-%{version} \
	--with-tmpdir=%{_tmppath}/%{name} \
	--with-scriptdir=%{_libexecdir}/%{name} \
	--with-nick-history=2000 \
	--with-sendq=3000000 \
	--with-permissions=0644 \
	--with-fd-setsize=1024 \
	--with-system-tre \
	--with-system-pcre2 \
	--with-system-cares \
	--with-shunnotices \
	--with-topicisnuhost \
	--enable-dynamic-linking \
	--enable-ssl=%{_prefix}

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}

# Unfortunately, the unrealircd folks have a broken make install.
# They even have a commit from 2001 where they put in:
# + @echo "Now install by hand; make install is broken."

# And...
# "Their fix was to make it broken." -remyabel

# Directories
## /etc/unrealircd, /usr/share/doc/unrealircd, /usr/bin
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_bindir}
%{__install} -d -m 0750 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
%{__install} -d -m 0750 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/aliases
%{__install} -d -m 0750 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/help
%{__install} -d -m 0750 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/examples
%{__install} -d -m 0750 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/ssl
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}
## /usr/lib64/unrealircd
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/usermodes
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/chanmodes
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/snomasks
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/extbans
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/third
# /usr/libexec/unrealircd
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libexecdir}/%{name}

## /var
%{__install} -d -m 0700 \
	${RPM_BUILD_ROOT}%{_sharedstatedir}/%{name}
%{__install} -d -m 0700 \
	${RPM_BUILD_ROOT}%{_localstatedir}/log/%{name}
%{__install} -d -m 0700 \
	${RPM_BUILD_ROOT}%{_localstatedir}/cache/%{name}

# Files
%{__install} -m 0755 src/ircd \
	${RPM_BUILD_ROOT}%{_bindir}/unrealircd
%{__install} -m 0644 doc/conf/*.conf \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
%{__install} -m 0644 doc/conf/aliases/*.conf \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/aliases
%{__install} -m 0644 doc/conf/help/*.conf \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/help
%{__install} -m 0600 doc/conf/examples/*.conf \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/examples
%{__install} -m 0644 doc/conf/ssl/curl-ca-bundle.crt \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/ssl

%{__install} -m 0755 src/modules/*.so \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}
%{__install} -m 0755 src/modules/usermodes/*.so \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/usermodes
%{__install} -m 0755 src/modules/chanmodes/*.so \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/chanmodes
%{__install} -m 0755 src/modules/snomasks/*.so \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/snomasks
%{__install} -m 0755 src/modules/extbans/*.so \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/extbans

# Extras
%{__install} -m 0644 %{SOURCE1} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/ircd.motd
%{__install} -m 0644 %{SOURCE2} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/ircd.rules
%{__install} -m 0644 %{SOURCE3} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/oper.motd
%{__install} -m 0644 %{SOURCE4} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/bot.motd
%{__install} -m 0770 %{SOURCE5} \
	${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/ircdutil
%{__install} -m 0600 %{SOURCE9} \
	${RPM_BUILD_ROOT}%{_sharedstatedir}/unrealircd/ircd.tune
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d 
%{__install} -m 0644 %{SOURCE11} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/unrealircd

# OS Specific
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -m 0644 %{SOURCE8} \
	${RPM_BUILD_ROOT}%{_unitdir}/unrealircd.service

# development headers
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_includedir}/%{name}
%{__install} -m 0755 include/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}

%pre
# Since we are not an official Fedora build, we don't get an
# assigned uid/gid. This may make it difficult when installed
# on multiple systems.
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

