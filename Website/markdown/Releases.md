---
pagename: Releases
last-modified-date: 
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
# Releases

## Current Releases

### Core Library

* Axon: 1.13.31

### Component Library

* Kamaelia: 1.13.31

### Applications

* 


## Historical Note

Over time, Kamaelia and Axon have had numerous releases. As of Feb 2024, the
project is adopting semantic versioning inline with other projects the core
maintainer maintains. Previously the project used a numbering system akin to
Ubuntu (based on dates) and before that a more adhoc approach. This is
changing with immediate effect.

## Semver rationale:

Specifically this means for STABLE releases:

* MAJOR >= 1 - increases when the "project API" change in a non-backwards compatible manner
* MINOR - increases with new features in a backwards compatible manner
* PATCH - increases when functionality is fixed/minor improvements in a backwards compatible manner.

For DEVELOPMENT releases:

* MAJOR == 0 - Never increases.
* MINOR - increases with new features (Whether backwards compatible of not)
* PATCH - increases when functionality is fixed/minor improvements in a backwards compatible manner.

This aspect for Development/experimental releases is not something which
Semantic versioning tends to deal with by default.

## Version Mapping

* Kamaelia's last official release was version: 1.0.12.0
* Axon's last official release was version: 1.7.1

To simplify things, for both Axon & Kamaelia:

* Major version for both will become *1* - no breaking changes
* Minor verson for both will become *13* - this is a new feature
* Patch version will be a count of the number of releases that are listed
  below. That count is 30 (19 + 11)

That means the new release version numbers for BOTH Kamaelia and Axon going
forward will initially be:

* 1.13.31

The reason for 31 not 30, is because this is will be the 31st release.

## Historical Releases

### Kamaelia

19 versions:

* 0.1.1 - 2004/12/24
* 0.1.2 - 2005/04/01
* 0.2.0-ep - 2005/06/25
* 0.2.0 - 2005/07/20
* 0.3.0 - 2005/10/03
* 0.3.1 - 2005/10/11
* 0.4.0 - 2006/06/11
* 0.5.0 - 2006/09/19
* 0.5.1 - 2006/10/29
* 0.6.0 - 2008/10/14
* 0.9.6.0 - 2009/06/22
* 0.9.7.0 - 2009/07/03
* 0.9.8.0 - 2009/08/16
* 1.0.7.0 - 2010/07/22 - License change to Apache 2
* 1.0.9.0 - 2010/10/26
* 1.0.11.0 - 2010/11/19
* 1.0.12.0 - 2010/12/24
* 1.1.2.0 - 2011/01/13
* 1.12.0 - 2015/03/01 - Collapsed version number 

### Axon

11 Releases

* 1.0.0 - 2004/12/24
* 1.0.4 - 2005/06/02
* 1.1.0 - 2005/06/04
* 1.1.1-ep - 2005/06/25
* 1.1.1 - 2005/07/20
* 1.1.2 - 2005/10/11
* 1.5.0 - 2006/05/03
* 1.5.1 - 2006/09/28
* 1.6.0 - 2010/07/22 - License change to Apache 2
* 1.7.0 - 2011/02/15
* 1.7.1 - 2015/03/01

