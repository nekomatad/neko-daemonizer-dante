import os.path
from typing import Callable, Coroutine

from neko_daemonizer_std import DaemonizerInterface
import uuid

from .integrations import neko_config

from ..daemonizer import Daemonizer


def _get_pidfile():
    if not os.path.isdir(neko_config.daemonizer_dante.pids_folder):
        os.makedirs(neko_config.daemonizer_dante.pids_folder)
    return (
        f'{neko_config.daemonizer_dante.pids_folder}/{uuid.uuid4().hex}.pid'
    )


class RDaemonizerInterface(DaemonizerInterface):
    @staticmethod
    def release_execution(
        main: Callable,
        setup: Callable = None,
        post_daemonized: Callable = None,
        pre_call: Callable = None,
    ) -> None:
        with Daemonizer() as (is_setup, daemonizer):
            if is_setup and setup:
                setup()

            is_parent, _ = daemonizer(
                _get_pidfile(),
                None
            )

            if is_parent and post_daemonized:
                post_daemonized()
            elif pre_call:
                pre_call()

        main()

    @staticmethod
    async def async_release_execution(
        main: Coroutine,
        setup: Coroutine = None,
        post_daemonized: Coroutine = None,
        pre_call: Coroutine = None,
    ) -> None:
        with Daemonizer() as (is_setup, daemonizer):
            if is_setup:
                await setup

            is_parent, _ = daemonizer(
                _get_pidfile(),
                None
            )

            if is_parent:
                await post_daemonized
            else:
                await pre_call

        await main


DaemonizerInterface = RDaemonizerInterface


__all__ = [DaemonizerInterface]
