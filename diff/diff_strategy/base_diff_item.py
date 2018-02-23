# -*- coding: utf-8 -*-
import abc
import logging
from functools import total_ordering


@total_ordering
class BaseDiffItem(object):
    """
    represents the smallest chunk of difference between two bookings or one booking and
    one CRS order
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, lhs, rhs, action=None):
        """
        initialise an applicable diff-item with two objects for comparison
        :param lhs: old state to change from (mostly a Booking model object)
        :param rhs: new state to update to (either a Booking model object, or a CRS order object)
        """
        self._current_state = lhs
        self._target_state = rhs
        self._action = action

    def __repr__(self):
        return "{cls}[curr:{c}, target:{t}, action:{ac_cls}]".format(cls=self.__class__.__name__,
                                                                     c=repr(self._current_state),
                                                                     t=repr(self._target_state),
                                                                     ac_cls=self._action.__class__.__name__)

    def set_action(self, action):
        """
        sets action (patch) for this diff

        :param action: Patch Behaviour object
        :return:
        """
        from diff.patch_behaviours import BaseBehaviour

        assert BaseBehaviour in type(action).mro()

        self._action = action

    def apply(self, *args, **kwargs):
        """
        executes an action (as set) for this diff => "applies the patch"
        :return: returns what the action returns
        """
        logger = logging.getLogger(self.__class__.__name__)

        if self._action is None:
            raise RuntimeError("No action specified for {cls}".format(cls=self.__class__.__name__))

        logger.info("executing action {ac} on diff-item {di}".format(ac=repr(self._action),
                                                                     di=repr(self)))
        return self._action.execute(self, *args, **kwargs)

    @classmethod
    @abc.abstractmethod
    def is_applicable(cls, lhs, rhs):
        """
        does this diff-item apply for given pair of booking objects?

        :param lhs: left-hand-side booking object
        :param rhs: right-hand-side booking object
        :return: True if diff is found (lhs-rhs), False otherwise
        """
        pass

    @classmethod
    @abc.abstractmethod
    def diff_strategy(cls):
        """
        :return: name of the diffing mechanism kit this diff-item belongs in
        """
        pass

    @classmethod
    @abc.abstractmethod
    def diff_type(cls):
        """
        :return: type of the diff-item (one of DiffConsts.DiffTypes)
        """
        pass

    def current_state(self):
        return self._current_state

    def target_state(self):
        return self._target_state

    def patch_priority(self):
        """
        defines priority of patch execution for this diff item

        :return: a number (lower the number higher the priority)
        """
        # by default, we start with insignificant priority
        return 999

    def __lt__(self, other):
        return self.patch_priority() < other.patch_priority()

    def __gt__(self, other):
        return self.patch_priority() > other.patch_priority()

    def __eq__(self, other):
        return self.patch_priority() == other.patch_priority()

    def __ne__(self, other):
        return self.patch_priority() != other.patch_priority()
