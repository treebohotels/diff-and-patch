# -*- coding: utf-8 -*-
import abc
import logging

from diff.diff_strategy import DiffSet


class BaseDiffStrategy(object):
    """
    base class for all diffing mechanisms
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, diff_items):
        """
        initialize the diffing-mechanism with diff-items
        :param diff_items: list of diff-item classes that constitute this DiffMech kit
        """
        self._diff_item_registry = {}

        for diff_item_cls in diff_items:
            from diff import BaseDiffItem
            assert BaseDiffItem in diff_item_cls.mro()

            diff_item_type = diff_item_cls.diff_type()

            # todo: what do we do if the diff_type is not one of the DiffConsts.DiffTypes?
            self._diff_item_registry[diff_item_type] = diff_item_cls

    def mapping(self):
        """
        maps DiffConsts.DiffTypes to DiffItems in the diffing mechanism kit
        :return: dict(DiffType: DiffItemClass)
        """
        return self._diff_item_registry

    @classmethod
    @abc.abstractmethod
    def name(cls):
        """
        :return: name of the diffing mechanism
        """
        return "unknown"

    def diff(self, lhs, rhs):
        """
        orchestrates the diffing mechanism

        :param lhs: left-hand-side of the diff
        :param rhs: right-hand-side of the diff
        :return: DiffSet (lhs - rhs)
        """
        logger = logging.getLogger(self.__class__.__name__)

        mapping = self.mapping()
        diff_set = DiffSet()

        for diff_type in mapping:
            logger.debug("checking if {dt} is applicable in diff-mech {dm}".format(dt=str(diff_type),
                                                                                   dm=self.name()))
            diff_item_cls = mapping[diff_type]
            if not diff_item_cls.is_applicable(lhs, rhs):
                continue

            logger.debug("{dic} is applicable, adding it to diff-set".format(dic=diff_item_cls.__name__))
            diff_set.add(diff_item_cls(lhs, rhs))

        return diff_set
