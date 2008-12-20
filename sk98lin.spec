#
# TODO:
#   - NAPI support is not ported and fails to build with
#     kernels >= 2.6.24, workarounded by disabling NAPI
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		pname	sk98lin
%define		rel	10
#
Summary:	Linux driver for family of Marvell Yukon adapters
Summary(pl.UTF-8):	Sterownik do kart z rodziny Marvell Yukon
Name:		%{pname}%{_alt_kernel}
Version:	10.61.3.3
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
# Repackaged from original tarball, only sources for kernel 2.6 were left.
Source0:	%{pname}-%{version}.tar.bz2
# Source0-md5:	b80a2ac971f3aac77be6b91e92b5d5a0
Patch0:		%{pname}-disable-napi.patch
URL:		http://www.marvell.com/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for Marvell Yukon family of
adapters.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych z rodziny
Marvell Yukon.

%package -n kernel%{_alt_kernel}-net-sk98lin
Summary:	Linux driver for family of Marvell Yukon adapters
Summary(pl.UTF-8):	Sterownik do kart z rodziny Marvell Yukon
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(sk98lin)
Obsoletes:	sk98lin
Obsoletes:	linux-net-sk98lin

%description -n kernel%{_alt_kernel}-net-sk98lin
This package contains the Linux driver for Marvell Yukon family of
adapters.

%description -n kernel%{_alt_kernel}-net-sk98lin -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych z rodziny
Marvell Yukon.

%prep
%setup -q -n %{pname}-%{version}
%if "%{_kernel_ver}" >= "2.6.24"
%patch0 -p1
%endif

%build
%build_kernel_modules -m %{pname}

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m %{pname} -d kernel/drivers/net -n %{pname} -s current
# blacklist kernel module
cat > $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf <<'EOF'
blacklist sk98lin
alias sk98lin sk98lin-current
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-sk98lin
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-sk98lin
%depmod %{_kernel_ver}

%files	-n kernel%{_alt_kernel}-net-sk98lin
%defattr(644,root,root,755)
%doc sk98lin.4 sk98lin.htm sk98lin.txt
/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/%{pname}*.ko*
