# -*- coding: utf-8 -*-
import logging

from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour


class NoOPBehaviour(BaseBehaviour):
    """
    no-op behaviour doesn't do anything but just log
    to be used when there is no mapping available for a diff-item-type
    """

    @classmethod
    def associated_diff_type(cls):
        return None

    def execute(self, diff_item, *args, **kwargs):
        super(NoOPBehaviour, self).execute(diff_item, *args, **kwargs)

        logger = logging.getLogger(self.__class__.__name__)
        logger.warning("{n} has nothing to execute for diff-item {di}".format(n=self.__class__.__name__,
                                                                              di=repr(diff_item)))
