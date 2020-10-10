%global _hardened_build 1
%global test_build 0

Name:    unrealircd
Version: 5.0.6
Release: 1%{?dist}
Summary: An open source IRC server

Group:   Applications/Communications
License: GPLv2
URL:     https://www.unrealircd.com
Source0: https://www.unrealircd.org/downloads/%{name}-%{version}.tar.gz
Source1: https://www.unrealircd.org/downloads/%{name}-%{version}.tar.gz.asc
Source2: https://www.unrealircd.org/downloads/release_key.gpg
Source3: %{name}.service
Source4: %{name}.logrotate

BuildRequires: coreutils
BuildRequires: gzip
BuildRequires: pkgconf-pkg-config
BuildRequires: gcc
BuildRequires: make
BuildRequires: curl
BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: pcre2
BuildRequires: pcre2-devel
BuildRequires: c-ares
BuildRequires: c-ares-devel
BuildRequires: libargon2-devel

# Source file verification
BuildRequires: gnupg2

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
UnrealIRCd is a highly advanced IRCd with a strong focus on modularity,
an advanced and highly configurable configuration file. Key features include
SSL, cloaking, its advanced anti-flood and anti-spam systems, swear filtering
and module support.

%package devel
Group:    Development/Libraries
Summary:  Development headers for %{name}
Requires: unrealircd = %{version}-%{release}

%description devel
The unrealircd-devel package contains the headers as part of the
unrealircd source. If you are planning on making your own modules
for unrealircd, you will need to install this package. If your
module will be using pcre2, tre, zlib, or c-ares, you will need
to install the -devel packages of those as well.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
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
rm -rf %{buildroot}

# Directories
install -d -m 0755 %{buildroot}%{_bindir}

install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/aliases
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/help
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/examples
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/tls

install -d -m 0755 %{buildroot}%{_docdir}/%{name}-%{version}

install -d -m 0755 %{buildroot}%{_libdir}/%{name}
install -d -m 0755 %{buildroot}%{_libdir}/%{name}/usermodes
install -d -m 0755 %{buildroot}%{_libdir}/%{name}/chanmodes
install -d -m 0755 %{buildroot}%{_libdir}/%{name}/snomasks
install -d -m 0755 %{buildroot}%{_libdir}/%{name}/extbans
install -d -m 0755 %{buildroot}%{_libdir}/%{name}/third

install -d -m 0755 %{buildroot}%{_libexecdir}/%{name}

install -d -m 0700 %{buildroot}%{_sharedstatedir}/%{name}
install -d -m 0700 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m 0700 %{buildroot}%{_localstatedir}/cache/%{name}

# Files
install -m 0755 src/ircd %{buildroot}%{_bindir}/unrealircd

install -m 0644 doc/conf/*.default.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 doc/conf/*.optional.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 doc/conf/modules.sources.list %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 doc/conf/spamfilter.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 doc/conf/badwords.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 doc/conf/dccallow.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 doc/conf/aliases/*.conf %{buildroot}%{_sysconfdir}/%{name}/aliases
install -m 0644 doc/conf/help/*.conf %{buildroot}%{_sysconfdir}/%{name}/help
install -m 0640 doc/conf/examples/*.conf %{buildroot}%{_sysconfdir}/%{name}/examples
install -m 0640 doc/conf/examples/example.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m 0644 doc/conf/tls/curl-ca-bundle.crt %{buildroot}%{_sysconfdir}/%{name}/tls

install -m 0755 src/modules/*.so %{buildroot}%{_libdir}/%{name}
install -m 0755 src/modules/usermodes/*.so %{buildroot}%{_libdir}/%{name}/usermodes
install -m 0755 src/modules/chanmodes/*.so %{buildroot}%{_libdir}/%{name}/chanmodes
install -m 0755 src/modules/snomasks/*.so %{buildroot}%{_libdir}/%{name}/snomasks
install -m 0755 src/modules/extbans/*.so %{buildroot}%{_libdir}/%{name}/extbans

# Package specific
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d 
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/unrealircd

install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/unrealircd.service

# Development headers
install -d -m 0755 %{buildroot}%{_includedir}/%{name}
install -m 0655 include/*.h %{buildroot}%{_includedir}/%{name}

%pre
%{_sbindir}/groupadd -r unrealircd 2>/dev/null || :
%{_sbindir}/useradd -r -g unrealircd \
    -s /sbin/nologin -d %{_sysconfdir}/unrealircd \
    -c 'Unreal IRC Server' unrealircd 2>/dev/null || :

%preun
%systemd_preun %{name}.service

%post
%if "%{test_build}" == "1"
%{_bindir}/openssl ecparam -out %{_sysconfdir}/%{name}/tls/server.key.pem \
    -name secp384r1 -genkey

%{_bindir}/openssl req -new -sha256 \
    -out %{_sysconfdir}/%{name}/tls/server.req.pem \
    -subj "/C=US/ST=New York/O=IRC geeks/OU=IRCd/CN=localhost" \
    -key %{_sysconfdir}/%{name}/tls/server.key.pem -nodes

%{_bindir}/openssl req -x509 -days 3650 -sha256 \
    -in %{_sysconfdir}/%{name}/tls/server.req.pem \
    -key %{_sysconfdir}/%{name}/tls/server.key.pem \
    -out %{_sysconfdir}/%{name}/tls/server.cert.pem

%{_bindir}/chmod 0700 %{_sysconfdir}/%{name}/tls/server.key.pem \
    %{_sysconfdir}/%{name}/tls/server.req.pem \
    %{_sysconfdir}/%{name}/tls/server.cert.pem

%{_bindir}/chown unrealircd:unrealircd %{_sysconfdir}/%{name}/tls/server.key.pem \
    %{_sysconfdir}/%{name}/tls/server.req.pem \
    %{_sysconfdir}/%{name}/tls/server.cert.pem

%{_bindir}/sed -i 's/password "test";/password "bobsmith";/g' \
    %{_sysconfdir}/%{name}/%{name}.conf

%{_bindir}/sed -i 's/set.this.to.email.address/example@example.com/' \
    %{_sysconfdir}/%{name}/%{name}.conf

%{_bindir}/sed -i '0,/and another one/s//boAr1HnR6gl3sJ7hVz4Zb7x4YwpW/' \
    %{_sysconfdir}/%{name}/%{name}.conf

%{_bindir}/sed -i '0,/and another one/s//coAr1HnR6gl3sJ7hVz4Zb7x4YwpW/' \
    %{_sysconfdir}/%{name}/%{name}.conf
%endif

%systemd_post %{name}.service

%postun
%if "%{test_build}" == "1"
%{_bindir}/rm %{_sysconfdir}/%{name}/tls/server.key.pem \
    %{_sysconfdir}/%{name}/tls/server.req.pem \
    %{_sysconfdir}/%{name}/tls/server.cert.pem
%endif

%systemd_postun %{name}.service

%files
%defattr(-, unrealircd, unrealircd, -)
%doc doc/Authors doc/coding-guidelines doc/tao.of.irc
%attr(-,root,root) %{_bindir}/unrealircd

%attr(-,root,root) %{_sysconfdir}/logrotate.d/unrealircd
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/help
%dir %{_sysconfdir}/%{name}/examples
%dir %{_sysconfdir}/%{name}/tls
%dir %{_sysconfdir}/%{name}/aliases
%config(noreplace) %{_sysconfdir}/%{name}/*.default.conf
%config(noreplace) %{_sysconfdir}/%{name}/*.optional.conf
%config(noreplace) %{_sysconfdir}/%{name}/modules.sources.list
%config(noreplace) %{_sysconfdir}/%{name}/spamfilter.conf
%config(noreplace) %{_sysconfdir}/%{name}/badwords.conf
%config(noreplace) %{_sysconfdir}/%{name}/dccallow.conf
%config(noreplace) %{_sysconfdir}/%{name}/help/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_sysconfdir}/%{name}/examples/*.conf
%{_sysconfdir}/%{name}/tls/curl-ca-bundle.crt
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
* Fri Jul 17 2020 losuler <losuler@posteo.net> - 5.0.6-1
- Update to UnrealIRCd 5.0.6
- Remove epel dependencies for fedora builds

* Fri May 29 2020 losuler <losuler@posteo.net> - 5.0.5.1-1
- Update to UnrealIRCd 5.0.5.1
- Fix for simpler version macro

* Fri May 22 2020 losuler <losuler@posteo.net> - 5.0.4-1
- Update to UnrealIRCd 5.0.4
- Remove various plugins
- Remove init wrapper script
- Add default config file
- Add source file verification
- Add test build macro

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
