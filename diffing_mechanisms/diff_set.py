# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict

from base_diff_item import BaseDiffItem


class DiffSet(object):
    """
    set of all diffs between bookings, with some additional methods
    """
    def __init__(self):
        # type:diff-item-object
        self._diff_items = OrderedDict()

    def add(self, diff_item):
        """
        add a diff-item to the set
        :param diff_item: DiffItem object
        :return:
        """
        # diff_item_type = type(diff_item)
        assert BaseDiffItem in type(diff_item).mro()

        # ensure the current set doesn't contain the diff-item
        if diff_item.diff_type() in self._diff_items:
            raise RuntimeError("Same diff-item {t} is being added twice to the DiffSet".format(
                t=str(diff_item.diff_type())))

        self._diff_items[diff_item.diff_type()] = diff_item

    def remove(self, diff_item_type):
        """
        removes a diff-item after orchestrator has processed it
        :param diff_item_type: diff-item-type to remove
        :return:
        """
        del self._diff_items[diff_item_type]

    def attach_behaviour(self, patch_behaviour_kit):
        """
        attach a corresponding PatchBehaviour to the DiffItems

        :param patch_behaviour_kit: patch-behaviour that knows which behaviour to
                                attach to the given diff-item
        :return: nothing
        """
        # importing locally to avoid possibility of circular dependency
        from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour

        for diff_item in self._diff_items.values():
            action = patch_behaviour_kit[diff_item.diff_type()]

            assert BaseBehaviour in type(action).mro()
            diff_item.set_action(action)

    def execute(self, remove_on_success=False, *args, **kwargs):
        """
        execeutes the action on each of the diff-items
        :param remove_on_success: should the diff-item be removed on success?
        :return: list of return values for successfully executed actions/diff-items
        """
        logger = logging.getLogger(self.__class__.__name__)

        retvals = OrderedDict()
        try:
            for di in sorted(self._diff_items.values()):
                retvals[di.diff_type()] = di.apply(*args, **kwargs)

        except Exception as e:
            logger.exception("error running action on {di}".format(di=repr(di)))

        if remove_on_success:
            map(self.remove, retvals)

        return retvals

    def is_empty(self):
        return len(self._diff_items) == 0
