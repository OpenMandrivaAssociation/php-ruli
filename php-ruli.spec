%define modname ruli
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A28_%{modname}.ini

Summary:	PHP binding for RULI
Name:		php-%{modname}
Version:	0.36
Release:	%mkrel 3
License:	GPL
Group:		Development/PHP
URL:		http://savannah.nongnu.org/projects/ruli/
Source0:	php-ruli-%{version}.tar.bz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	ruli-devel >= %{version}
Provides:	php5-ruli
Obsoletes:	php5-ruli
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
PHP binding for RULI

RULI stands for Resolver User Layer Interface. It's a library built on top of
an asynchronous DNS stub resolver. RULI provides an easy-to-use interface for
querying DNS SRV resource records. The goal is to promote the wide deployment
of SRV-cognizant client programs. RULI aims to fully support SRV-related
standards.

%prep

%setup -q -n ruli-%{version}
mv php/ruli/* .
mv php/README .

%build

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc tests ruli_sync_query.php ruli_sync_smtp_query.php ruli.php README
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


