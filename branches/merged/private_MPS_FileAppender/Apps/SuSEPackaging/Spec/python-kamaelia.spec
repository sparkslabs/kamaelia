
Name:           python-kamaelia
%define modname Kamaelia
BuildRequires:  python-devel
URL:            http://kamaelia.sourceforge.net/
License:        Mozilla tri-license scheme (MPL/GPL/LGPL)
Group:          Development/Languages
Autoreqprov:    on
Version:        0.5.0
Release:        1.1
Summary:        Python module to create scalable and safe concurrent systems
Source:         http://downloads.sourceforge.net/kamaelia/Kamaelia-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%{py_requires}

%description

A library of components you can take and bolt together, and customise. This
includes components for TCP/multicast clients and servers, backplanes, chassis,
Dirac video encoding & decoding, Vorbis decoding, pygame & Tk based user
interfaces and Tk, visualisation tools, presentation tools, games tools...

See http://edit.kamaelia.org/Home

Authors:
--------
    Michael.Sparks at rd.bbc.co.uk

%prep
%setup -n %{modname}-%{version}

%build
export CFLAGS="$RPM_OPT_FLAGS" 
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT --record-rpm=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc AUTHORS
%doc CHANGELOG
%doc COPYING
%doc Docs
%doc Examples
%doc Tools
%doc PKG-INFO
%doc README

%changelog
* Mon Sep 29 2008 poeml@suse.de
- initial package (0.5.0)
