# [Project Sidekick](https://sidekick.apu.edu)
Project Sidekick is a web portal for IMT Device Solutions at APU that offers a shift covers system, a quote creation tool, quick links to helpful tools, and more!

## Table of Contents

* [Features](#features)
* [Components](#components)
* [Documentation](#documentation)
* [Versioning](#versioning)
* [License](#license)

### Features
#### Home/Overview Page
* Homing Beacon
  * Keep track of which employees have checked in to their shifts
  * Check in employees when they call in to begin their shifts
  * Allow staff members to update their locations
  * Read out-of-office information and holidays from a Google calendar
* Announcements & Events
  * Allow managers and staff to post announcements and events
* Newsletter
  * Embedded PDF of an employee newsletter

#### Roster Page
* Hero Card
  * Display at-a-glance information about employees
  * Click to see a drop-down modal
* Employee Modal
  * Display detailed information about the employee (changes depending on level of access)
  * Track discipline marks and proficiencies
  * View and add trophies
* Trophy Case
  * Track employee trophies and rewards
* Search and sort
  * Search for employees by netid, name, and position
  * Sort by position, proficiency, last name, or year

#### Shift Covers Page
* View Open Shifts
  * See a list of open shifts for the positions you are eligible to take shift covers for
* View My shifts
  * See a list of your shifts with their locations
* Shift Modal
  * Detailed view of shift, including context and any metadata about shift covers
* MoD View
  * For managers only: see a list of shifts for the locations you are managing
* Google Calendar Synchronization
  * Synchronize with Google Calendars for each location
* Post & Take Covers
  * Post or take covers
  * Single or permanent covers
  * Full or partial covers

#### Passwords Page
* View passwords for different accounts depending on access level

#### Quote Tool
* Create and edit quotes for:
  * Data backup
  * Hardware Repair (w/ shipping cost)
  * OS Install
  * Data Recovery
  * Virus Scan
  * Tune-up
* Automatically calculate sales tax
* Add labor costs & apply discounts
* Line-by-line editing of quote

#### Quick Links
* Provide easy access to different online tools used by APU


### Components
Sidekick uses the following tools and frameworks:
* [The Django Web Framework 1.11](https://www.djangoproject.com/)
  * [Python 3.6](https://docs.python.org/3/)
  * [django-cas](https://github.com/kstateome/django-cas)
* [Twitter Bootstrap](http://getbootstrap.com/)
  * [Node.js](https://nodejs.org/)
  * [Grunt](https://gruntjs.com/)
* [Google APIs](https://developers.google.com/google-apps/calendar/) for Python
* [PostgreSQL Database](https://www.postgresql.org/about/)

### Documentation
For information about documentation, please see our [Wiki](https://github.com/azusapacificuniversity/sidekick/wiki)

### Versioning
When possible, Sidekick uses [Semantic Versioning](http://semver.org) for version numbering. 
New releases should be tagged as such with their version numbers in the repository

### License
Sidekick is released under [GPL v3.0](https://github.com/azusapacificuniversity/sidekick/blob/master/LICENSE).
