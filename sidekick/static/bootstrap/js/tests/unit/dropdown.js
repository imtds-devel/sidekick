$(function () {
<<<<<<< HEAD
  'use strict'
=======
  'use strict';
>>>>>>> develop

  QUnit.module('dropdowns plugin')

  QUnit.test('should be defined on jquery object', function (assert) {
    assert.expect(1)
    assert.ok($(document.body).dropdown, 'dropdown method is defined')
  })

  QUnit.module('dropdowns', {
    beforeEach: function () {
      // Run all tests in noConflict mode -- it's the only way to ensure that the plugin works in noConflict mode
      $.fn.bootstrapDropdown = $.fn.dropdown.noConflict()
    },
    afterEach: function () {
      $.fn.dropdown = $.fn.bootstrapDropdown
      delete $.fn.bootstrapDropdown
    }
  })

  QUnit.test('should provide no conflict', function (assert) {
    assert.expect(1)
<<<<<<< HEAD
    assert.strictEqual(typeof $.fn.dropdown, 'undefined', 'dropdown was set back to undefined (org value)')
  })

  QUnit.test('should throw explicit error on undefined method', function (assert) {
    assert.expect(1)
    var $el = $('<div/>')
    $el.bootstrapDropdown()
    try {
      $el.bootstrapDropdown('noMethod')
    } catch (err) {
      assert.strictEqual(err.message, 'No method named "noMethod"')
    }
=======
    assert.strictEqual($.fn.dropdown, undefined, 'dropdown was set back to undefined (org value)')
>>>>>>> develop
  })

  QUnit.test('should return jquery collection containing the element', function (assert) {
    assert.expect(2)
    var $el = $('<div/>')
    var $dropdown = $el.bootstrapDropdown()
    assert.ok($dropdown instanceof $, 'returns jquery collection')
    assert.strictEqual($dropdown[0], $el[0], 'collection contains element')
  })

  QUnit.test('should not open dropdown if target is disabled via attribute', function (assert) {
    assert.expect(1)
<<<<<<< HEAD
    var done = assert.async()
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<button disabled href="#" class="btn dropdown-toggle" data-toggle="dropdown">Dropdown</button>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
    $(dropdownHTML).appendTo('#qunit-fixture')
    var $dropdown = $('#qunit-fixture').find('[data-toggle="dropdown"]').bootstrapDropdown()
    $dropdown.on('click', function () {
      assert.ok(!$dropdown.parent('.dropdown').hasClass('show'))
      done()
    })
    $dropdown.trigger($.Event('click'))
  })

  QUnit.test('should not add class position-static to dropdown if boundary not set', function (assert) {
    assert.expect(1)
    var done = assert.async()
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '</div>' +
        '</div>' +
        '</div>'
    var $dropdown = $(dropdownHTML).find('[data-toggle="dropdown"]').bootstrapDropdown()
    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok(!$dropdown.parent('.dropdown').hasClass('position-static'), '"position-static" class not added')
        done()
      })
    $dropdown.trigger('click')
  })

  QUnit.test('should add class position-static to dropdown if boundary not scrollParent', function (assert) {
    assert.expect(1)
    var done = assert.async()
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown" data-boundary="viewport">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '</div>' +
        '</div>' +
        '</div>'
    var $dropdown = $(dropdownHTML).find('[data-toggle="dropdown"]').bootstrapDropdown()
    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok($dropdown.parent('.dropdown').hasClass('position-static'), '"position-static" class added')
        done()
      })
    $dropdown.trigger('click')
=======
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<button disabled href="#" class="btn dropdown-toggle" data-toggle="dropdown">Dropdown</button>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Secondary link</a></li>'
        + '<li><a href="#">Something else here</a></li>'
        + '<li class="divider"/>'
        + '<li><a href="#">Another link</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
    var $dropdown = $(dropdownHTML).find('[data-toggle="dropdown"]').bootstrapDropdown().trigger('click')

    assert.ok(!$dropdown.parent('.dropdown').hasClass('open'), '"open" class added on click')
>>>>>>> develop
  })

  QUnit.test('should set aria-expanded="true" on target when dropdown menu is shown', function (assert) {
    assert.expect(1)
<<<<<<< HEAD
    var done = assert.async()
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()
    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.strictEqual($dropdown.attr('aria-expanded'), 'true', 'aria-expanded is set to string "true" on click')
        done()
      })
    $dropdown.trigger('click')
=======
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<a href="#" class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false">Dropdown</a>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Secondary link</a></li>'
        + '<li><a href="#">Something else here</a></li>'
        + '<li class="divider"/>'
        + '<li><a href="#">Another link</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
    var $dropdown = $(dropdownHTML)
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()
      .trigger('click')

    assert.strictEqual($dropdown.attr('aria-expanded'), 'true', 'aria-expanded is set to string "true" on click')
>>>>>>> develop
  })

  QUnit.test('should set aria-expanded="false" on target when dropdown menu is hidden', function (assert) {
    assert.expect(1)
    var done = assert.async()
<<<<<<< HEAD
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" aria-expanded="false" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
=======
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<a href="#" class="dropdown-toggle" aria-expanded="false" data-toggle="dropdown">Dropdown</a>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Secondary link</a></li>'
        + '<li><a href="#">Something else here</a></li>'
        + '<li class="divider"/>'
        + '<li><a href="#">Another link</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
>>>>>>> develop
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()

    $dropdown
      .parent('.dropdown')
      .on('hidden.bs.dropdown', function () {
        assert.strictEqual($dropdown.attr('aria-expanded'), 'false', 'aria-expanded is set to string "false" on hide')
        done()
      })

    $dropdown.trigger('click')
    $(document.body).trigger('click')
  })

  QUnit.test('should not open dropdown if target is disabled via class', function (assert) {
    assert.expect(1)
<<<<<<< HEAD
    var done = assert.async()
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<button href="#" class="btn dropdown-toggle disabled" data-toggle="dropdown">Dropdown</button>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'

    $(dropdownHTML).appendTo('#qunit-fixture')
    var $dropdown = $('#qunit-fixture').find('[data-toggle="dropdown"]').bootstrapDropdown()
    $dropdown.on('click', function () {
      assert.ok(!$dropdown.parent('.dropdown').hasClass('show'))
      done()
    })
    $dropdown.trigger($.Event('click'))
  })

  QUnit.test('should add class show to menu if clicked', function (assert) {
    assert.expect(1)
    var done = assert.async()
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
    var $dropdown = $(dropdownHTML).find('[data-toggle="dropdown"]').bootstrapDropdown()
    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok($dropdown.parent('.dropdown').hasClass('show'), '"show" class added on click')
        done()
      })
    $dropdown.trigger('click')
=======
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<button href="#" class="btn dropdown-toggle disabled" data-toggle="dropdown">Dropdown</button>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Secondary link</a></li>'
        + '<li><a href="#">Something else here</a></li>'
        + '<li class="divider"/>'
        + '<li><a href="#">Another link</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
    var $dropdown = $(dropdownHTML).find('[data-toggle="dropdown"]').bootstrapDropdown().trigger('click')

    assert.ok(!$dropdown.parent('.dropdown').hasClass('open'), '"open" class added on click')
  })

  QUnit.test('should add class open to menu if clicked', function (assert) {
    assert.expect(1)
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Secondary link</a></li>'
        + '<li><a href="#">Something else here</a></li>'
        + '<li class="divider"/>'
        + '<li><a href="#">Another link</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
    var $dropdown = $(dropdownHTML).find('[data-toggle="dropdown"]').bootstrapDropdown().trigger('click')

    assert.ok($dropdown.parent('.dropdown').hasClass('open'), '"open" class added on click')
>>>>>>> develop
  })

  QUnit.test('should test if element has a # before assuming it\'s a selector', function (assert) {
    assert.expect(1)
<<<<<<< HEAD
    var done = assert.async()
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="/foo/" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
    var $dropdown = $(dropdownHTML).find('[data-toggle="dropdown"]').bootstrapDropdown()
    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok($dropdown.parent('.dropdown').hasClass('show'), '"show" class added on click')
        done()
      })
    $dropdown.trigger('click')
  })

  QUnit.test('should remove "show" class if body is clicked', function (assert) {
    assert.expect(2)
    var done = assert.async()
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()

    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok($dropdown.parent('.dropdown').hasClass('show'), '"show" class added on click')
        $(document.body).trigger('click')
      }).on('hidden.bs.dropdown', function () {
        assert.ok(!$dropdown.parent('.dropdown').hasClass('show'), '"show" class removed')
        done()
      })
    $dropdown.trigger('click')
  })

  QUnit.test('should remove "show" class if tabbing outside of menu', function (assert) {
    assert.expect(2)
    var done = assert.async()
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="dropdown-divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
=======
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<a href="/foo/" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Secondary link</a></li>'
        + '<li><a href="#">Something else here</a></li>'
        + '<li class="divider"/>'
        + '<li><a href="#">Another link</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
    var $dropdown = $(dropdownHTML).find('[data-toggle="dropdown"]').bootstrapDropdown().trigger('click')

    assert.ok($dropdown.parent('.dropdown').hasClass('open'), '"open" class added on click')
  })


  QUnit.test('should remove "open" class if body is clicked', function (assert) {
    assert.expect(2)
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Secondary link</a></li>'
        + '<li><a href="#">Something else here</a></li>'
        + '<li class="divider"/>'
        + '<li><a href="#">Another link</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
>>>>>>> develop
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()
<<<<<<< HEAD
    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok($dropdown.parent('.dropdown').hasClass('show'), '"show" class added on click')
        var e = $.Event('keyup')
        e.which = 9 // Tab
        $(document.body).trigger(e)
      }).on('hidden.bs.dropdown', function () {
        assert.ok(!$dropdown.parent('.dropdown').hasClass('show'), '"show" class removed')
        done()
      })
    $dropdown.trigger('click')
  })

  QUnit.test('should remove "show" class if body is clicked, with multiple dropdowns', function (assert) {
    assert.expect(7)
    var done = assert.async()
    var dropdownHTML = '<div class="nav">' +
        '<div class="dropdown" id="testmenu">' +
        '<a class="dropdown-toggle" data-toggle="dropdown" href="#testmenu">Test menu <span class="caret"/></a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#sub1">Submenu 1</a>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '<div class="btn-group">' +
        '<button class="btn">Actions</button>' +
        '<button class="btn dropdown-toggle" data-toggle="dropdown"></button>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Action 1</a>' +
        '</div>' +
        '</div>'
    var $dropdowns = $(dropdownHTML).appendTo('#qunit-fixture').find('[data-toggle="dropdown"]')
    var $first = $dropdowns.first()
    var $last = $dropdowns.last()

    assert.strictEqual($dropdowns.length, 2, 'two dropdowns')

    $first.parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.strictEqual($first.parents('.show').length, 1, '"show" class added on click')
        assert.strictEqual($('#qunit-fixture .dropdown-menu.show').length, 1, 'only one dropdown is shown')
        $(document.body).trigger('click')
      }).on('hidden.bs.dropdown', function () {
        assert.strictEqual($('#qunit-fixture .dropdown-menu.show').length, 0, '"show" class removed')
        $last.trigger('click')
      })

    $last.parent('.btn-group')
      .on('shown.bs.dropdown', function () {
        assert.strictEqual($last.parent('.show').length, 1, '"show" class added on click')
        assert.strictEqual($('#qunit-fixture .dropdown-menu.show').length, 1, 'only one dropdown is shown')
        $(document.body).trigger('click')
      }).on('hidden.bs.dropdown', function () {
        assert.strictEqual($('#qunit-fixture .dropdown-menu.show').length, 0, '"show" class removed')
        done()
      })
    $first.trigger('click')
  })

  QUnit.test('should remove "show" class if body if tabbing outside of menu, with multiple dropdowns', function (assert) {
    assert.expect(7)
    var done = assert.async()
    var dropdownHTML = '<div class="nav">' +
        '<div class="dropdown" id="testmenu">' +
        '<a class="dropdown-toggle" data-toggle="dropdown" href="#testmenu">Test menu <span class="caret"/></a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#sub1">Submenu 1</a>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '<div class="btn-group">' +
        '<button class="btn">Actions</button>' +
        '<button class="btn dropdown-toggle" data-toggle="dropdown"><span class="caret"/></button>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Action 1</a>' +
        '</div>' +
        '</div>'
=======
      .trigger('click')

    assert.ok($dropdown.parent('.dropdown').hasClass('open'), '"open" class added on click')
    $(document.body).trigger('click')
    assert.ok(!$dropdown.parent('.dropdown').hasClass('open'), '"open" class removed')
  })

  QUnit.test('should remove "open" class if body is clicked, with multiple dropdowns', function (assert) {
    assert.expect(7)
    var dropdownHTML = '<ul class="nav">'
        + '<li><a href="#menu1">Menu 1</a></li>'
        + '<li class="dropdown" id="testmenu">'
        + '<a class="dropdown-toggle" data-toggle="dropdown" href="#testmenu">Test menu <span class="caret"/></a>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#sub1">Submenu 1</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
        + '<div class="btn-group">'
        + '<button class="btn">Actions</button>'
        + '<button class="btn dropdown-toggle" data-toggle="dropdown"><span class="caret"/></button>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Action 1</a></li>'
        + '</ul>'
        + '</div>'
>>>>>>> develop
    var $dropdowns = $(dropdownHTML).appendTo('#qunit-fixture').find('[data-toggle="dropdown"]')
    var $first = $dropdowns.first()
    var $last = $dropdowns.last()

    assert.strictEqual($dropdowns.length, 2, 'two dropdowns')

<<<<<<< HEAD
    $first.parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.strictEqual($first.parents('.show').length, 1, '"show" class added on click')
        assert.strictEqual($('#qunit-fixture .dropdown-menu.show').length, 1, 'only one dropdown is shown')
        var e = $.Event('keyup')
        e.which = 9 // Tab
        $(document.body).trigger(e)
      }).on('hidden.bs.dropdown', function () {
        assert.strictEqual($('#qunit-fixture .dropdown-menu.show').length, 0, '"show" class removed')
        $last.trigger('click')
      })

    $last.parent('.btn-group')
      .on('shown.bs.dropdown', function () {
        assert.strictEqual($last.parent('.show').length, 1, '"show" class added on click')
        assert.strictEqual($('#qunit-fixture .dropdown-menu.show').length, 1, 'only one dropdown is shown')
        var e = $.Event('keyup')
        e.which = 9 // Tab
        $(document.body).trigger(e)
      }).on('hidden.bs.dropdown', function () {
        assert.strictEqual($('#qunit-fixture .dropdown-menu.show').length, 0, '"show" class removed')
        done()
      })
    $first.trigger('click')
=======
    $first.trigger('click')
    assert.strictEqual($first.parents('.open').length, 1, '"open" class added on click')
    assert.strictEqual($('#qunit-fixture .open').length, 1, 'only one dropdown is open')
    $(document.body).trigger('click')
    assert.strictEqual($('#qunit-fixture .open').length, 0, '"open" class removed')

    $last.trigger('click')
    assert.strictEqual($last.parent('.open').length, 1, '"open" class added on click')
    assert.strictEqual($('#qunit-fixture .open').length, 1, 'only one dropdown is open')
    $(document.body).trigger('click')
    assert.strictEqual($('#qunit-fixture .open').length, 0, '"open" class removed')
>>>>>>> develop
  })

  QUnit.test('should fire show and hide event', function (assert) {
    assert.expect(2)
<<<<<<< HEAD
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
=======
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Secondary link</a></li>'
        + '<li><a href="#">Something else here</a></li>'
        + '<li class="divider"/>'
        + '<li><a href="#">Another link</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
>>>>>>> develop
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()

    var done = assert.async()

    $dropdown
      .parent('.dropdown')
      .on('show.bs.dropdown', function () {
        assert.ok(true, 'show was fired')
      })
      .on('hide.bs.dropdown', function () {
        assert.ok(true, 'hide was fired')
        done()
      })

    $dropdown.trigger('click')
    $(document.body).trigger('click')
  })

<<<<<<< HEAD
  QUnit.test('should fire shown and hidden event', function (assert) {
    assert.expect(2)
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
=======

  QUnit.test('should fire shown and hidden event', function (assert) {
    assert.expect(2)
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Secondary link</a></li>'
        + '<li><a href="#">Something else here</a></li>'
        + '<li class="divider"/>'
        + '<li><a href="#">Another link</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
>>>>>>> develop
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()

    var done = assert.async()

    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok(true, 'shown was fired')
      })
      .on('hidden.bs.dropdown', function () {
        assert.ok(true, 'hidden was fired')
        done()
      })

    $dropdown.trigger('click')
    $(document.body).trigger('click')
  })

  QUnit.test('should fire shown and hidden event with a relatedTarget', function (assert) {
    assert.expect(2)
<<<<<<< HEAD
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
=======
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Secondary link</a></li>'
        + '<li><a href="#">Something else here</a></li>'
        + '<li class="divider"/>'
        + '<li><a href="#">Another link</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
>>>>>>> develop
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()
    var done = assert.async()

    $dropdown.parent('.dropdown')
      .on('hidden.bs.dropdown', function (e) {
        assert.strictEqual(e.relatedTarget, $dropdown[0])
        done()
      })
      .on('shown.bs.dropdown', function (e) {
        assert.strictEqual(e.relatedTarget, $dropdown[0])
        $(document.body).trigger('click')
      })

    $dropdown.trigger('click')
  })

  QUnit.test('should ignore keyboard events within <input>s and <textarea>s', function (assert) {
    assert.expect(3)
    var done = assert.async()

<<<<<<< HEAD
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '<input type="text" id="input">' +
        '<textarea id="textarea"/>' +
        '</div>' +
        '</div>' +
        '</div>'
=======
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>'
        + '<ul class="dropdown-menu">'
        + '<li><a href="#">Secondary link</a></li>'
        + '<li><a href="#">Something else here</a></li>'
        + '<li class="divider"/>'
        + '<li><a href="#">Another link</a></li>'
        + '<li><input type="text" id="input"></li>'
        + '<li><textarea id="textarea"/></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
>>>>>>> develop
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()

    var $input = $('#input')
    var $textarea = $('#textarea')

    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok(true, 'shown was fired')

<<<<<<< HEAD
        $input.trigger('focus').trigger($.Event('keydown', {
          which: 38
        }))
        assert.ok($(document.activeElement).is($input), 'input still focused')

        $textarea.trigger('focus').trigger($.Event('keydown', {
          which: 38
        }))
=======
        $input.trigger('focus').trigger($.Event('keydown', { which: 38 }))
        assert.ok($(document.activeElement).is($input), 'input still focused')

        $textarea.trigger('focus').trigger($.Event('keydown', { which: 38 }))
>>>>>>> develop
        assert.ok($(document.activeElement).is($textarea), 'textarea still focused')

        done()
      })

    $dropdown.trigger('click')
  })

  QUnit.test('should skip disabled element when using keyboard navigation', function (assert) {
<<<<<<< HEAD
    assert.expect(2)
    var done = assert.async()
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item disabled" href="#">Disabled link</a>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
=======
    assert.expect(1)
    var dropdownHTML = '<ul class="tabs">'
        + '<li class="dropdown">'
        + '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>'
        + '<ul class="dropdown-menu">'
        + '<li class="disabled"><a href="#">Disabled link</a></li>'
        + '<li><a href="#">Another link</a></li>'
        + '</ul>'
        + '</li>'
        + '</ul>'
>>>>>>> develop
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()
<<<<<<< HEAD

    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok(true, 'shown was fired')
        $dropdown.trigger($.Event('keydown', {
          which: 40
        }))
        $dropdown.trigger($.Event('keydown', {
          which: 40
        }))
        assert.ok(!$(document.activeElement).is('.disabled'), '.disabled is not focused')
        done()
      })
    $dropdown.trigger('click')
  })

  QUnit.test('should focus next/previous element when using keyboard navigation', function (assert) {
    assert.expect(4)
    var done = assert.async()
    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a id="item1" class="dropdown-item" href="#">A link</a>' +
        '<a id="item2" class="dropdown-item" href="#">Another link</a>' +
        '</div>' +
        '</div>' +
        '</div>'
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()

    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok(true, 'shown was fired')
        $dropdown.trigger($.Event('keydown', {
          which: 40
        }))
        assert.ok($(document.activeElement).is($('#item1')), 'item1 is focused')

        $(document.activeElement).trigger($.Event('keydown', {
          which: 40
        }))
        assert.ok($(document.activeElement).is($('#item2')), 'item2 is focused')

        $(document.activeElement).trigger($.Event('keydown', {
          which: 38
        }))
        assert.ok($(document.activeElement).is($('#item1')), 'item1 is focused')
        done()
      })
    $dropdown.trigger('click')
  })

  QUnit.test('should not close the dropdown if the user clicks on a text field', function (assert) {
    assert.expect(2)
    var done = assert.async()
    var dropdownHTML = '<div class="dropdown">' +
        '<button type="button" data-toggle="dropdown">Dropdown</button>' +
        '<div class="dropdown-menu">' +
        '<input id="textField" type="text" />' +
        '</div>' +
        '</div>'
=======
      .trigger('click')

    $dropdown.trigger($.Event('keydown', { which: 40 }))
    $dropdown.trigger($.Event('keydown', { which: 40 }))

    assert.ok(!$(document.activeElement).parent().is('.disabled'), '.disabled is not focused')
  })

  QUnit.test('should not close the dropdown if the user clicks on a text field', function (assert) {
    assert.expect(1)
    var dropdownHTML = '<div class="btn-group">'
        + '<button type="button" data-toggle="dropdown">Dropdown</button>'
        + '<ul class="dropdown-menu">'
        + '<li><input id="textField" type="text" /></li>'
        + '</ul>'
        + '</div>'
>>>>>>> develop
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()
<<<<<<< HEAD

    var $textfield = $('#textField')
    $textfield.on('click', function () {
      assert.ok($dropdown.parent('.dropdown').hasClass('show'), 'dropdown menu is shown')
      done()
    })

    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok($dropdown.parent('.dropdown').hasClass('show'), 'dropdown menu is shown')
        $textfield.trigger($.Event('click'))
      })
    $dropdown.trigger('click')
  })

  QUnit.test('should not close the dropdown if the user clicks on a textarea', function (assert) {
    assert.expect(2)
    var done = assert.async()
    var dropdownHTML = '<div class="dropdown">' +
        '<button type="button" data-toggle="dropdown">Dropdown</button>' +
        '<div class="dropdown-menu">' +
        '<textarea id="textArea"></textarea>' +
        '</div>' +
        '</div>'
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()

    var $textarea = $('#textArea')
    $textarea.on('click', function () {
      assert.ok($dropdown.parent('.dropdown').hasClass('show'), 'dropdown menu is shown')
      done()
    })

    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok($dropdown.parent('.dropdown').hasClass('show'), 'dropdown menu is shown')
        $textarea.trigger($.Event('click'))
      })
    $dropdown.trigger('click')
  })

  QUnit.test('Dropdown should not use Popper.js in navbar', function (assert) {
    assert.expect(1)
    var done = assert.async()
    var html = '<nav class="navbar navbar-expand-md navbar-light bg-light">' +
        '<div class="dropdown">' +
        '  <a class="nav-link dropdown-toggle" href="#" id="dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Dropdown</a>' +
        '  <div class="dropdown-menu" aria-labelledby="dropdown">' +
        '    <a class="dropdown-item" href="#">Action</a>' +
        '    <a class="dropdown-item" href="#">Another action</a>' +
        '    <a class="dropdown-item" href="#">Something else here</a>' +
        '  </div>' +
        '</div>' +
        '</nav>'

    $(html).appendTo('#qunit-fixture')
    var $triggerDropdown = $('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()
    var $dropdownMenu = $triggerDropdown.next()

    $triggerDropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        assert.ok(typeof $dropdownMenu.attr('style') === 'undefined', 'No inline style applied by Popper.js')
        done()
      })
    $triggerDropdown.trigger($.Event('click'))
  })

  QUnit.test('should ignore keyboard events for <input>s and <textarea>s within dropdown-menu, except for escape key', function (assert) {
    assert.expect(7)
    var done = assert.async()

    var dropdownHTML = '<div class="tabs">' +
        '<div class="dropdown">' +
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown</a>' +
        '<div class="dropdown-menu">' +
        '<a class="dropdown-item" href="#">Secondary link</a>' +
        '<a class="dropdown-item" href="#">Something else here</a>' +
        '<div class="divider"/>' +
        '<a class="dropdown-item" href="#">Another link</a>' +
        '<input type="text" id="input">' +
        '<textarea id="textarea"/>' +
        '</div>' +
        '</div>' +
        '</div>'
=======
      .trigger('click')

    $('#textField').trigger('click')

    assert.ok($dropdown.parent('.btn-group').hasClass('open'), 'dropdown menu is open')
  })

  QUnit.test('should not close the dropdown if the user clicks on a textarea', function (assert) {
    assert.expect(1)
    var dropdownHTML = '<div class="btn-group">'
        + '<button type="button" data-toggle="dropdown">Dropdown</button>'
        + '<ul class="dropdown-menu">'
        + '<li><textarea id="textArea"></textarea></li>'
        + '</ul>'
        + '</div>'
>>>>>>> develop
    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()
<<<<<<< HEAD

    var $input = $('#input')
    var $textarea = $('#textarea')

    $dropdown
      .parent('.dropdown')
      .on('shown.bs.dropdown', function () {
        // Space key
        $input.trigger('focus').trigger($.Event('keydown', {
          which: 32
        }))
        assert.ok($(document.activeElement)[0] === $input[0], 'input still focused')
        $textarea.trigger('focus').trigger($.Event('keydown', {
          which: 32
        }))
        assert.ok($(document.activeElement)[0] === $textarea[0], 'textarea still focused')

        // Key up
        $input.trigger('focus').trigger($.Event('keydown', {
          which: 38
        }))
        assert.ok($(document.activeElement)[0] === $input[0], 'input still focused')
        $textarea.trigger('focus').trigger($.Event('keydown', {
          which: 38
        }))
        assert.ok($(document.activeElement)[0] === $textarea[0], 'textarea still focused')

        // Key down
        $input.trigger('focus').trigger($.Event('keydown', {
          which: 40
        }))
        assert.ok($(document.activeElement)[0] === $input[0], 'input still focused')
        $textarea.trigger('focus').trigger($.Event('keydown', {
          which: 40
        }))
        assert.ok($(document.activeElement)[0] === $textarea[0], 'textarea still focused')

        // Key escape
        $input.trigger('focus').trigger($.Event('keydown', {
          which: 27
        }))
        assert.ok(!$dropdown.parent('.dropdown').hasClass('show'), 'dropdown menu is not shown')
        done()
      })

    $dropdown.trigger('click')
  })

  QUnit.test('should ignore space key events for <input>s within dropdown, and accept up, down and escape', function (assert) {
    assert.expect(6)
    var done = assert.async()

    var dropdownHTML =
        '<ul class="nav tabs">' +
        '  <li class="dropdown">' +
        '    <input type="text" id="input" data-toggle="dropdown">' +
        '    <div class="dropdown-menu" role="menu">' +
        '      <a id="item1" class="dropdown-item" href="#">Secondary link</a>' +
        '      <a id="item2" class="dropdown-item" href="#">Something else here</a>' +
        '      <div class="divider"></div>' +
        '      <a class="dropdown-item" href="#">Another link</a>' +
        '    </div>' +
        '  </li>' +
        '</ul>'

    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()

    var $input = $('#input')

    $dropdown
      .parent('.dropdown')
      .one('shown.bs.dropdown', function () {
        assert.ok(true, 'shown was fired')

        // Key space
        $input.trigger('focus').trigger($.Event('keydown', {
          which: 32
        }))
        assert.ok($dropdown.parent('.dropdown').hasClass('show'), 'dropdown menu is shown')
        assert.ok($(document.activeElement).is($input), 'input is still focused')

        // Key escape
        $input.trigger('focus').trigger($.Event('keydown', {
          which: 27
        }))
        assert.ok(!$dropdown.parent('.dropdown').hasClass('show'), 'dropdown menu is not shown')

        $dropdown
          .parent('.dropdown')
          .one('shown.bs.dropdown', function () {
            // Key down
            $input.trigger('focus').trigger($.Event('keydown', {
              which: 40
            }))
            assert.ok(document.activeElement === $('#item1')[0], 'item1 is focused')

            $dropdown
              .parent('.dropdown')
              .one('shown.bs.dropdown', function () {
                // Key up
                $input.trigger('focus').trigger($.Event('keydown', {
                  which: 38
                }))
                assert.ok(document.activeElement === $('#item1')[0], 'item1 is focused')
                done()
              }).bootstrapDropdown('toggle')
            $input.trigger('click')
          })
        $input.trigger('click')
      })
    $input.trigger('click')
  })

  QUnit.test('should ignore space key events for <textarea>s within dropdown, and accept up, down and escape', function (assert) {
    assert.expect(6)
    var done = assert.async()

    var dropdownHTML =
        '<ul class="nav tabs">' +
        '  <li class="dropdown">' +
        '    <textarea id="textarea" data-toggle="dropdown"></textarea>' +
        '    <div class="dropdown-menu" role="menu">' +
        '      <a id="item1" class="dropdown-item" href="#">Secondary link</a>' +
        '      <a id="item2" class="dropdown-item" href="#">Something else here</a>' +
        '      <div class="divider"></div>' +
        '      <a class="dropdown-item" href="#">Another link</a>' +
        '    </div>' +
        '  </li>' +
        '</ul>'

    var $dropdown = $(dropdownHTML)
      .appendTo('#qunit-fixture')
      .find('[data-toggle="dropdown"]')
      .bootstrapDropdown()

    var $textarea = $('#textarea')

    $dropdown
      .parent('.dropdown')
      .one('shown.bs.dropdown', function () {
        assert.ok(true, 'shown was fired')

        // Key space
        $textarea.trigger('focus').trigger($.Event('keydown', {
          which: 32
        }))
        assert.ok($dropdown.parent('.dropdown').hasClass('show'), 'dropdown menu is shown')
        assert.ok($(document.activeElement).is($textarea), 'textarea is still focused')

        // Key escape
        $textarea.trigger('focus').trigger($.Event('keydown', {
          which: 27
        }))
        assert.ok(!$dropdown.parent('.dropdown').hasClass('show'), 'dropdown menu is not shown')

        $dropdown
          .parent('.dropdown')
          .one('shown.bs.dropdown', function () {
            // Key down
            $textarea.trigger('focus').trigger($.Event('keydown', {
              which: 40
            }))
            assert.ok(document.activeElement === $('#item1')[0], 'item1 is focused')

            $dropdown
              .parent('.dropdown')
              .one('shown.bs.dropdown', function () {
                // Key up
                $textarea.trigger('focus').trigger($.Event('keydown', {
                  which: 38
                }))
                assert.ok(document.activeElement === $('#item1')[0], 'item1 is focused')
                done()
              }).bootstrapDropdown('toggle')
            $textarea.trigger('click')
          })
        $textarea.trigger('click')
      })
    $textarea.trigger('click')
=======
      .trigger('click')

    $('#textArea').trigger('click')

    assert.ok($dropdown.parent('.btn-group').hasClass('open'), 'dropdown menu is open')
>>>>>>> develop
  })
})
