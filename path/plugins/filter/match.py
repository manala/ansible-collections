from __future__ import annotations

from ..test.match import _match as _test_match


def _match(paths, pattern):

    return [path for path in paths if _test_match(path, pattern)]


class FilterModule(object):
    """ Manala path match jinja2 filters """

    def filters(self):
        return {
            "match": _match,
        }
