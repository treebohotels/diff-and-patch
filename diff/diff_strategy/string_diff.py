from diff import BaseDiffItem


class StringDiff(BaseDiffItem):
    def __init__(self, strategy, diffing_type, model, attr_name):
        self.strategy = strategy
        self.diffing_type = diffing_type
        self.model = model
        self.attr_name = attr_name

    @classmethod
    def diff_strategy(cls):
        return cls.strategy

    @classmethod
    def diff_type(cls):
        return cls.diffing_type

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is cls.model
        assert type(rhs) is cls.model
        return getattr(lhs, cls.attr_name) != getattr(rhs, cls.attr_name)
