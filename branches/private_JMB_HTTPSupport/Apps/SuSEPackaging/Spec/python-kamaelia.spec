
Name:           python-kamaelia
%define modname Kamaelia
BuildRequires:  python-devel
URL:            http://www.kamaelia.org/
License:        Mozilla tri-license scheme (MPL/GPL/LGPL)
Group:          Development/Languages
Autoreqprov:    on
Version:        0.6.0
Release:        1.1
Summary:        Python module to create scalable and safe concurrent systems
Source:         http://www.kamaelia.org/release/Kamaelia-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%{py_requires}

%description

A library/framework for concurrency using message passing components as the
concurrency metaphor. Consists of a kernel (Axon) and collection of
components (Kamaelia). Support for generator, thread & process based
components. Targetted towards supporting maintenance, so /accessible/ to
novices, but general purpose. Uses concurrency to make life simpler, not
harder. Designed as a practical toolkit.

This toolkit includes components for TCP/multicast clients and servers,
backplanes, chassis, Dirac video encoding & decoding, Vorbis decoding,
pygame & Tk based user interfaces and Tk, visualisation tools, presentation
tools, games tools...

See http://www.kamaelia.org/Home

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
%doc COPYING
%doc Docs
%doc Examples
%doc Tools
%doc PKG-INFO
%doc Axon.CHANGELOG
%doc Kamaelia.CHANGELOG
%doc Axon.README
%doc Kamaelia.README
%doc DetailedReleaseNotes.txt

%changelog
* Sat Oct 25 2008 michael.sparks@rd.bbc.ci.uk
- updated package to 0.6.0
- included Axon directly as well (as per current release)
* Mon Sep 29 2008 poeml@suse.de
- initial package (0.5.0)
