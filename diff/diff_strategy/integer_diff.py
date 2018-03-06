from diff import BaseDiffItem


class IntegerDiff(BaseDiffItem):
    def __init__(self, strategy, diff_type, model, attr_name):
        self.strategy = strategy
        self.type = diff_type
        self.model = model
        self.attr_name = attr_name

    @classmethod
    def diff_strategy(cls):
        return cls.strategy

    @classmethod
    def diff_type(cls):
        return cls.diff_type

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is cls.model
        assert type(rhs) is cls.model
        return getattr(lhs, cls.atrr_name) != getattr(rhs, cls.attr_name)
