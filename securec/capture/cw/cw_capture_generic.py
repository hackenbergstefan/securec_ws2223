#!/usr/bin/env python
import os
import numpy as np
import tqdm

import jinja2

from . import cw_helper

filedir = os.path.abspath(os.path.dirname(__file__))

TEMPLATE = open(os.path.join(filedir, "generic_simpleserial.j2")).read()


def _capture_simpleserial_single(data, cmd=0x01, samples=500):
    cw_helper.scope.adc.samples = samples
    cw_helper.scope.arm()
    cw_helper.target.flush()
    cw_helper.target.simpleserial_write(cmd, data)
    return cw_helper.capture()


def _capture_simpleserial(
    number_of_traces,
    inputfunction,
    number_of_samples=500,
    checkoutput=None,
):
    data = np.zeros(
        number_of_traces,
        dtype=[
            ("trace", "f8", number_of_samples),
            ("input", "u1", len(inputfunction())),
        ],
    )
    for i in tqdm.tqdm(range(number_of_traces)):
        data["input"][i, :] = inputfunction()
        data["trace"][i, :] = _capture_simpleserial_single(
            bytes(data["input"][i, :]),
            samples=number_of_samples,
        )

        if checkoutput and i in (0, number_of_traces - 1):
            actual_output = cw_helper.target.simpleserial_read(0x01)
            expected_output = checkoutput(data["input"][i])
            if list(actual_output) != list(expected_output):
                raise Exception(f"{actual_output} != {expected_output}")
    return data


def capture(
    number_of_traces,
    inputfunction,
    code=None,
    fromfile=None,
    number_of_samples=500,
    platform="cwlitearm",
    checkoutput=None,
    **kwargs,
):
    if code or fromfile:
        # Generate program
        template = jinja2.Environment().from_string(TEMPLATE)
        rendered = template.render(
            dict(number_of_traces=number_of_traces, code=code, fromfile=fromfile)
        )
        with open(os.path.join(filedir, "_generic_simpleserial.c"), "w") as fp:
            fp.write(rendered)

    # Setup, compile and flash
    scope, _ = cw_helper.init_scope_and_target(platform_=platform.upper())

    if code or fromfile:
        cw_helper.compile_and_flash(os.path.join(filedir, "_generic_simpleserial.c"))

    scope.default_setup()
    cw_helper.reset_target()

    data = _capture_simpleserial(
        number_of_traces=number_of_traces,
        inputfunction=inputfunction,
        number_of_samples=number_of_samples,
        checkoutput=checkoutput,
    )
    cw_helper.exit_scope_and_target()
    return data
