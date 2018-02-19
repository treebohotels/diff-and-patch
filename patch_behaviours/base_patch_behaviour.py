# -*- coding: utf-8 -*-
import abc


class BasePatchBehaviour(object):
    """
    base class for all patch-behaviours

    patch-behaviours define a set of individual behaviours mapped to individual diff-items
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, behaviours):
        """
        initialize the diffing-mechanism with diff-items
        :param behaviours: list of behaviour classes that constitute the PatchBehaviour kit
        """
        self._behaviour_registry = {}

        for behaviour_cls in behaviours:
            from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
            assert BaseBehaviour in behaviour_cls.mro()

            associated_diff_type = behaviour_cls.associated_diff_type()

            # todo: what do we do if the diff_type is not one of the DiffConsts.DiffTypes?
            self._behaviour_registry[associated_diff_type] = behaviour_cls

    @classmethod
    @abc.abstractmethod
    def name(cls):
        """
        :return: name of the patching behaviour
        """
        return "unknown"

    def __getitem__(self, diff_type):
        """
        used to get behaviour in the patch-behaviour kit, that's associated with the specified
        diff-item-type

        :param diff_type: one of the DiffConsts.DiffTypes
        :return: Behaviour object, associated with the diff-type
        """
        try:
            return self._behaviour_registry[diff_type]()

        except KeyError:
            from b2b.domain.services.diffing.patch_behaviours import NoOPBehaviour

            return NoOPBehaviour()



