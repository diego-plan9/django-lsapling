# django-lsapling
Utilities for working with tree structures in Django via the ltree postgresql
extension.

## Introduction

`django-lsapling` is a django module that provides support for tree-like
structures using the
[ltree](https://www.postgresql.org/docs/9.1/static/ltree.html) postgresql
extension.

### Features
* Ordered and unordered tree-like `Models`.
* Methods for managing and querying the hierarchy (`get_ascendants`,
`get_children`, `add_child`, `get_descendants`, `get_siblings`, `add_sibling`,
`pretty_print`) aimed to provide (near-)`django-mptt` compatibility.
* Mapping of a subset of `ltree` operators and functions to Django Lookups and
Transforms, using the underlying SQL primitives provided by `ltree`.


## Requirements
* Django 1.8
* PostgreSQL 9.1+, with the `LTREE` extension

## Known issues

This module is still in alpha state. Notable issues include:
* Support for Django > 1.8 and Python 3.x has not been tested.
* Only a subset of the operators ([Table F-12](https://www.postgresql.org/docs/9.1/static/ltree.html#LTREE-OP-TABLE)) 
of the `ltree` extension is currently implemented:

|  ltree                               |  lsapling lookup  |  lsapling class              |
|--------------------------------------|-------------------|------------------------------|
| `tree @> ltree`,`ltree <@ ltree[]`   | `ascendant`       | `lookups.LtreeAscendant`     |
| `ltree <@ ltree`, `ltree <@ ltree[]` | `descendant`      | `lookups.LtreeDescendant`    |
| `ltree ~ lquery`                     | `path_like`       | `lookups.LtreePathLike`      |
| `ltree @ ltxtquery`                  | `path_like_txt`   | `lookups.LtreePathLikeTxt`   |
| `ltree ? lquery[]`                   | `path_like_exact` | `lookups.LtreePathLikeExact` |

 * Only a subset of the functions ([Table F-13](https://www.postgresql.org/docs/9.1/static/ltree.html#LTREE-FUNC-TABLE)) 
of the `ltree` extension is currently implemented:

|  ltree                                |  lsapling lookup  |  lsapling class              |
|---------------------------------------|-------------------|------------------------------|
| `subpath(ltree, int offset, int len)` | `Subpath`         | `functions.Subpath`          |
| `nlevel(ltree)`                       | `Nlevel`          | `functions.Nlevel`           |


## Changelog

### 0.1.0a1 (2016/07/11):
* Initial public release.

## License

MIT license, Copyright (c) 2016 Diego M. Rodríguez.

The `ltree` module for PostgreSQL is released under BSD license, by Teodor
Sigaev (<teodor@stack.net>) and Oleg Bartunov (<oleg@sai.msu.su>).

