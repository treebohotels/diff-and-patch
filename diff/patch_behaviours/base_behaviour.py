# -*- coding: utf-8 -*-
import abc


class BaseBehaviour(object):
    """
    base class for all patch-behaviours
    """
    __metaclass__ = abc.ABCMeta

    @classmethod
    @abc.abstractmethod
    def associated_diff_type(cls):
        """
        which diff-type this behaviour has an action for?

        :return: one of DiffConsts.DiffTypes enum
        """
        pass

    @classmethod
    @abc.abstractmethod
    def behaviour_kit(cls):
        """
        which patch-behaviour kit does this behaviour belong to?

        :return: one of DiffConsts.PatchBehaviours
        """
        pass

    def execute(self, diff_item, *args, **kwargs):
        """
        how to execute the action/behaviour.
        may need some addional resources, which can be passed via
         *args and **kwargs

        :param diff_item: DiffItem
        :return:
        """
        from diff.diffing_mechanisms import BaseDiffItem
        assert BaseDiffItem in type(diff_item).mro()

    def __repr__(self):
        return "{cls}".format(cls=self.__class__.__name__)
