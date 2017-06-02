#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pytest  # type: ignore

from sensibility.language import Language
from sensibility.language.javascript import javascript
from sensibility.token_utils import Position

from location_factory import LocationFactory

test_file = r"""#!/usr/bin/env node
/*!
 * This is an example file.
 */

import {ಠ_ಠ} from "-_-";

/* TODO: crazy ES2017 features. */
"""

def test_sanity_check() -> None:
    assert isinstance(javascript, Language)


def test_tokenize() -> None:
    tokens = javascript.tokenize(test_file)
    # TODO: more robust tests for this.
    assert len(tokens) == 7
    assert tokens[2].value == 'ಠ_ಠ'


def test_check_syntax() -> None:
    assert not javascript.check_syntax('import #')
    assert javascript.check_syntax(test_file)


def test_summarize() -> None:
    summary = javascript.summarize(test_file)
    assert summary.sloc == 1
    assert summary.n_tokens == 7


@pytest.mark.skip
def test_pipeline() -> None:
    loc = LocationFactory(Position(line=6, column=0))
    result = list(javascript.pipeline.execute_with_locations(test_file))
    assert result[:4] == [
        (loc.across(len("import")),         'import'),
        (loc.space().across(1),             '{'),
        (loc.space().across(len("ಠ_ಠ")),    'IDENTIFIER'),
        (loc.space().across(1),             '}'),
    ]
    # TODO: Test more locations?
