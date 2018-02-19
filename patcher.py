# -*- coding: utf-8 -*-


class Patcher(object):
    """
    source for all different PatchBehaviour kits
    """

    _behaviours_registry = {}

    @classmethod
    def register_behaviour(cls, behaviour_cls):
        """
        decorator for registering behaviour kits
        :param behaviour_cls: class wanting to register with the patch-behaviour kit
        :return:
        """
        from b2b.domain.services.diffing.patch_behaviours.base_patch_behaviour import BasePatchBehaviour
        assert BasePatchBehaviour in behaviour_cls.mro()

        cls._behaviours_registry[behaviour_cls.name()] = behaviour_cls
        return behaviour_cls

    @classmethod
    def get_behaviour(cls, behaviour):
        """
        get specified patch behaviour
        :param behaviour:
        :return:
        """
        if behaviour not in cls._behaviours_registry:
            raise RuntimeError('Unknown behaviour {b}'.format(b=str(behaviour)))

        return cls._behaviours_registry[behaviour]()
