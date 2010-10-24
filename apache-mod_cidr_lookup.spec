#Module-Specific definitions
%define mod_name mod_cidr_lookup
%define mod_conf B44_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module which enables CIDR lookups
Name:		apache-%{mod_name}
Version:	1.2
Release: 	%mkrel 5
Group:		System/Servers
License:	Apache License
URL:		http://sourceforge.net/projects/modcidrlookup/
Source0:	http://ovh.dl.sourceforge.net/sourceforge/modcidrlookup/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The mod_cidr_lookup is an Apache module for version 2.2 and 2.0. The
mod_cidr_lookup detects client type by looking up the client's source IP
address in CIDR blocks. This module sets the environment variable X_CLIENT_TYPE
and the HTTP request header X-Client-Type, so it can be used in both Apache
(httpd.conf) and Web applications.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

%build
%{_sbindir}/apxs -c apache2/%{mod_name}.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 apache2/.libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changes NOTICE README LICENSE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
