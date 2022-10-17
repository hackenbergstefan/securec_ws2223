try:
    from .cw import cw_capture_generic
except:
    # If CW is not available continue anyway
    pass
from .elmo import elmo_capture_generic


def capture(platform, *args, **kwargs):
    if platform.startswith("cw"):
        return cw_capture_generic.capture(
            *args,
            **kwargs,
            platform=platform,
        )
    else:
        return elmo_capture_generic.capture(
            platform=platform,
            *args,
            **kwargs,
        )
