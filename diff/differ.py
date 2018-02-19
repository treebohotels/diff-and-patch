# -*- coding: utf-8 -*-


class Differ(object):
    """
    Differ diffs between two booking objects or one booking and
    one CRS-order-details object
    """

    _diff_mech_registry = {}

    @classmethod
    def register_diff_mech(cls, diff_mech_cls):
        """
        decorator for registering diff-mech kits
        """
        from diff.diffing_mechanisms import BaseDiffMech
        assert BaseDiffMech in diff_mech_cls.mro()

        diff_mech_name = diff_mech_cls.name()
        cls._diff_mech_registry[diff_mech_name] = diff_mech_cls

        return diff_mech_cls

    @classmethod
    def get_diff_mech(cls, diff_mech):
        """
        get specified diffing mechanism
        :param diff_mech: name of the diffing mechanism (one of DiffConsts.DiffingMechanisms enum)
        """
        if diff_mech not in cls._diff_mech_registry:
            raise RuntimeError('Unknown diffing mechanism {d}'.format(d=str(diff_mech)))

        return cls._diff_mech_registry[diff_mech]()
