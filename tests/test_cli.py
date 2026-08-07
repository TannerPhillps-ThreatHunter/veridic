import json
from io import StringIO

from veridic.cli import main


def invoke(*args):
    out = StringIO()
    err = StringIO()

    code = main(
        list(args),
        stdout=out,
        stderr=err,
    )

    return (
        code,
        out.getvalue(),
        err.getvalue(),
    )


def test_fields_command_exposes_catalog():
    code, out, err = invoke(
        "fields"
    )

    assert code == 0
    assert err == ""

    assert (
        "event.start"
        in out
    )

    assert (
        "network.bytes"
        in out
    )


def test_show_exposes_field_semantics():
    code, out, err = invoke(
        "show",
        "event.duration",
    )

    assert code == 0
    assert err == ""

    assert (
        "Temporal.Measurement.Duration"
        in out
    )

    assert (
        "non_negative"
        in out
    )


def test_resolve_timestamp_difference():
    code, out, err = invoke(
        "resolve",
        "sub",
        "event.end",
        "event.start",
    )

    assert code == 0
    assert err == ""

    assert (
        "admitted: yes"
        in out
    )

    assert (
        "Temporal.Measurement.Duration"
        in out
    )


def test_compute_timestamp_difference():
    code, out, err = invoke(
        "compute",
        "sub",
        "--as",
        "event.duration",
        "event.end=15.0",
        "event.start=10.0",
    )

    assert code == 0
    assert err == ""

    assert (
        "event.duration = 5.0 s"
        in out
    )

    assert (
        "semantic: admitted"
        in out
    )

    assert (
        "contextual: verified"
        in out
    )


def test_compute_data_rate():
    code, out, err = invoke(
        "compute",
        "div",
        "network.bytes=10000.0",
        "event.duration=5.0",
    )

    assert code == 0
    assert err == ""

    assert (
        "2000.0"
        in out
    )

    assert (
        "Quantitative.Rate.DataRate"
        not in err
    )


def test_semantically_invalid_operation_fails():
    code, out, err = invoke(
        "compute",
        "add",
        "source.ip=192.0.2.1",
        "destination.ip=198.51.100.1",
    )

    assert code == 2

    assert (
        "undefined"
        in err.lower()
    )


def test_contextual_violation_has_distinct_exit_code():
    code, out, err = invoke(
        "compute",
        "sub",
        "--as",
        "event.duration",
        "event.end=5.0",
        "event.start=10.0",
    )

    assert code == 3
    assert err == ""

    assert (
        "contextual: violated"
        in out
    )

    assert (
        "FAIL non_negative"
        in out
    )


def test_json_computation_is_machine_readable():
    code, out, err = invoke(
        "--json",
        "compute",
        "sub",
        "--as",
        "event.duration",
        "event.end=15.0",
        "event.start=10.0",
    )

    assert code == 0
    assert err == ""

    payload = json.loads(
        out
    )

    assert (
        payload["operation"]
        == "sub"
    )

    assert (
        payload["derived"]["value"]
        == 5.0
    )

    assert (
        payload[
            "contextual_validation"
        ]["status"]
        == "verified"
    )


def test_compute_without_binding_returns_derived_field():
    code, out, err = invoke(
        "compute",
        "sub",
        "event.end=15.0",
        "event.start=10.0",
    )

    assert code == 0
    assert err == ""

    assert (
        "(event.end-event.start) = 5.0 s"
        in out
    )

    assert (
        "binding: none"
        in out
    )

    assert (
        "contextual: not-applicable"
        in out
    )


def test_binding_requires_compatible_semantics():
    code, out, err = invoke(
        "compute",
        "sub",
        "--as",
        "network.bytes",
        "event.end=15.0",
        "event.start=10.0",
    )

    assert code == 2

    assert (
        "cannot bind"
        in err
    )
