#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		rel	0.1
Summary:	Compressed Caching for Linux
Name:		compcache
Version:	0.6.2
Release:	%{rel}
License:	CC 3.0 BY-SA
Group:		Base/Kernel
Source0:	http://compcache.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	27aec78dc50e34fb800c74e879057743
URL:		http://code.google.com/p/compcache/
%if %{with kernel}
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
%{?with_userspace:BuildRequires:	perl-tools-pod}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project creates RAM based block device (named ramzswap) which
acts as swap disk. Pages swapped to this disk are compressed and
stored in memory itself.

Compressing pages and keeping them in RAM virtually increases its
capacity. This allows more applications to fit in given amount of
memory.

%package -n kernel%{_alt_kernel}-drivers-compcache
Summary:	Compressed Caching for Linux
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-drivers-compcache
compcache Linux kernel driver.

%prep
%setup -qn %{name}-%{version}

%build
%if %{with kernel}
%build_kernel_modules -m ramzswap
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with kernel}
%install_kernel_modules -m ramzswap -d kernel/drivers/md
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-drivers-compcache
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-drivers-compcache
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-drivers-compcache
%defattr(644,root,root,755)
%doc README Changelog
/lib/modules/%{_kernel_ver}/kernel/drivers/md/*.ko*
%endif
