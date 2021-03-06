Changelog
=========
This log contains a list of bug fixes and added, modified or even removed
features.

0.6
---

*Currently in development*

Added Modules
  - :mod:`brownie.terminal`.
  - :mod:`brownie.context`.
  - :mod:`brownie.text`.

Added Classes
  - :class:`brownie.datastructures.PeekableIterator`.
  - :class:`brownie.datastructures.StackedObject`.

Changed Classes
  - Added :meth:`~brownie.datastructures.LazyList.index` to
    :class:`brownie.datastructures.LazyList`.

Added Functions
  - :func:`brownie.functional.fmap`.

Changed Functions
  - Added `doc` parameter to :func:`brownie.datastructures.namedtuple`.


0.5.1
-----

- Added missing `datastructures` package.

0.5 - Heinzelmännchen
---------------------

Added Classes
  - :class:`brownie.functional.Signature`.
  - :class:`brownie.datastructures.FixedDict`.
  - :class:`brownie.functional.curried`.
  - :class:`brownie.datastructures.CombinedSequence`.
  - :class:`brownie.datastructures.CombinedList`.

Changed Classes
  - Added :mod:`pickle` support to :class:`brownie.datastructures.LazyList`.
  - Made :class:`brownie.datastructures.ImmutableDict` hashable.
  - Made :class:`brownie.datastructures.CombinedDict` hashable.
  - Made :class:`brownie.datastructures.ImmutableMultiDict` hashable.
  - Made :class:`brownie.datastructures.ImmutableOrderedDict` hashable.

Added Functions
  - :func:`brownie.datastructures.namedtuple`.
  - :func:`brownie.itools.flatten`.
  - :func:`brownie.caching.memoize`.

Changed Functions
  - Allow using :func:`brownie.itools.unique` with non-hashable items.
  - Added `seen` parameter to :func:`brownie.itools.unique`.

0.4.1
-----

- Python 3.x support was totally broken which was undiscovered due to the
  way tests are run. Looking into the issue and considering the response
  I got so far I choose to drop 3.x support for now as fixing it would
  take way too much time and effort.

0.4 - Domovoi
-------------

- Added Python 3.x support. [See 0.4.1]
- Added :mod:`brownie.proxies`.
- Added :meth:`brownie.datastructures.OrderedDict.move_to_end`.

0.3.1
-----

- Fixed an issue with :meth:`brownie.datastructures.LazyList.insert`,
  which caused the internal stream not to be exhausted when used with
  negative indexes.

  Thanks to Trundle_ for the report and patch.

.. _Trundle: https://github.com/Trundle

0.3 - Tomte
-----------

- Added :class:`brownie.datastructures.SetQueue`.

0.2.2
-----

- Expose wrapper for :func:`multiprocessing.cpu_count` instead the
  function itself which was sometimes exposed as
  :func:`brownie.parallel.get_cpu_count` because the latter is supposed
  to have a `default` parameter which :func:`multiprocessing.cpu_count`
  does not.

0.2.1
-----

- Switched theme to minimalism.
- Fixed wrong use of :rst:role:`meth` in the documentation of
  :class:`brownie.abstract.AbstractClassMeta`.
- Added example to :class:`brownie.abstract.VirtualSubclassMeta`.
- Added example to :class:`brownie.abstract.AbstractClassMeta`.

0.2 - Boggart
-------------

Added Modules
  - :mod:`brownie.importing`
  - :mod:`brownie.abstract`

Added Classes
  - :class:`brownie.itools.chain`
  - :class:`brownie.datastructures.OrderedSet`
  - :class:`brownie.datastructures.CombinedDict`.
  - :class:`brownie.datastructures.CombinedMultiDict`.
  - :class:`brownie.datastructures.ImmutableOrderedDict`.

- Make type checks work for dictionaries based on interfaces and
  behaviour.

0.1.1
-----

- Fixed a :exc:`KeyError` and a :exc:`ValueError` which could occur
  by calling :func:`brownie.parallel.get_cpu_count` on Windows or Linux
  respectively.

0.1 - Fairy Land
----------------

Initial Release.
