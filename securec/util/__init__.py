import os
import subprocess
import time
import warnings

import chipwhisperer as cw

from .. import config


def exit():
    if config.scope is not None:
        config.target.dis()
        config.scope.dis()
        cw.util.DisableNewAttr._read_only_attrs.clear()
        config.target = None
        config.scope = None


def init():
    if config.scope is None:
        config.scope = cw.scope()
        config.target = cw.target(config.scope, target_type=cw.targets.SimpleSerial2)
    return config.scope, config.target


def compile(path, cryptooptions=None):
    cryptooptions = cryptooptions or ["CRYPTO_TARGET=NONE"]
    try:
        proc = subprocess.run(
            [
                "make",
                "-f",
                f'{os.path.join(os.path.dirname(__file__), "Makefile")}',
                "PLATFORM=CWLITEXMEGA",
                f"FIRMWAREPATH={config.firmwarepath}",
                f"TARGET={os.path.splitext(os.path.basename(path))[0]}",
            ]
            + cryptooptions,
            cwd=os.path.dirname(path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        if config.print_output and config.debug:
            print("\x1b[32m✓\x1b[0m " + proc.stdout.decode())
    except subprocess.CalledProcessError as e:
        if config.print_output:
            print(
                f'\x1b[31m✗ "{" ".join(e.args[1])}" returned:\x1b[0m\n'
                + e.stderr.decode()
            )
        raise


def flash(path):
    prog = cw.programmers.XMEGAProgrammer
    programmed = cw.program_target(
        scope=config.scope,
        prog_type=prog,
        fw_path=os.path.join(
            os.path.dirname(path),
            f"{os.path.splitext(os.path.basename(path))[0]}-CWLITEXMEGA.hex",
        ),
    )
    if config.print_output and config.debug:
        print(programmed)


def compile_and_flash(path, cryptooptions=None):
    compile(path, cryptooptions)
    flash(path)
    if config.print_output:
        print("\x1b[32m✓\x1b[0m")
    config.scope.default_setup()
    reset_target()


def reset_target():
    scope = config.scope
    target = config.target
    scope.io.pdic = False
    time.sleep(0.2)
    scope.io.pdic = "high_z"
    time.sleep(0.2)
    target.flush()


def capture():
    scope = config.scope
    target = config.target
    ret = scope.capture()

    for i in range(101):
        if target.is_done():
            break
        time.sleep(0.05)
        if i == 100:
            warnings.warn("Target did not finish operation")
            return None
    if ret:
        warnings.warn("Timeout happened during capture")
        return None

    return scope.get_last_trace()
