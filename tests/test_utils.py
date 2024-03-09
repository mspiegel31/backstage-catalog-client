from typing import Dict

import pytest

from backstage_catalog_client.models import EntityRef
from backstage_catalog_client.utils import parse_ref_string


class TestParseEntityRef:
    @staticmethod
    @pytest.mark.parametrize(
        "ref,expected",
        [
            (
                "kind:namespace/name",
                {"kind": "kind", "namespace": "namespace", "name": "name"},
            ),
            ("kind:name", {"kind": "kind", "namespace": "default", "name": "name"}),
        ],
    )
    def test_it_handles_some_omissions(ref: str, expected: Dict[str, str]):
        assert parse_ref_string(ref) == EntityRef(**expected)

    @staticmethod
    @pytest.mark.parametrize(
        "ref,expected",
        [
            ("a:b:c", {"kind": "a", "namespace": "ns", "name": "b:c"}),
            ("a/b/c", {"kind": "k", "namespace": "a", "name": "b/c"}),
            ("a/b:c", {"kind": "k", "namespace": "a", "name": "b:c"}),
        ],
    )
    def test_it_allows_names(ref: str, expected: Dict[str, str]):
        assert parse_ref_string(ref, default_kind="k", default_namespace="ns") == EntityRef(**expected)

    @staticmethod
    @pytest.mark.parametrize("ref", ["", ":", "a:", ":b", "a/b:", "a/:b", "a/b:c:", "a/b:c:d", "a/b:c:d:e"])
    def test_it_rejects_empty_parts_in_strings(ref: str):
        with pytest.raises(ValueError):
            parse_ref_string(ref)
