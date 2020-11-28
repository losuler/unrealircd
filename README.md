<div align="center">
<p align="center">
  <p align="center">
    <h3 align="center">UnrealIRCd RPM</h3>
    <p align="center">
      An RPM spec for UnrealIRCd.
    </p>
  </p>
</p>
</div>

## About

This is an RPM spec for [UnrealIRCd](https://www.unrealircd.org/) based on the original spec created by [nazunalika](https://github.com/nazunalika).

> **Update**: This package is now available in the official Fedora and EPEL repositories https://src.fedoraproject.org/rpms/unrealircd. It is recommended to migrate to this package. The spec and associated builds provided here will no longer be maintained.

## Builds

Builds are available on my Copr at https://copr.fedorainfracloud.org/coprs/losuler/unrealircd.

This repo can be added on all supported systems by:

```bash
dnf copr enable losuler/unrealircd 
```

## Config

In order to change the default location for tls certs (which is`/etc/unrealircd/tls`), when for example you are using `certbot`, use the following block in `/etc/unrealircd/unrealircd.conf`:

```
set {
    tls {
        certificate "/path/to/cert";
        key "/path/to/key";
    };
};
```
