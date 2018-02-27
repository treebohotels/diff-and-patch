from diff.differ import Differ
from diff.patcher import Patcher
from diff import BaseDiffItem
from diff import BaseDiffStrategy
from diff.patch_behaviours import BaseBehaviour, BasePatchBehaviour


USER_AGE_DIFF_STRATEGY = 1
USER_AGE_PATCH_STRATEGY = 2

NUMBER_DIFF_TYPE = 3

USER_DIFF_STRATEGY = 4

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class NameDiff(BaseDiffItem):
    @classmethod
    def diff_strategy(cls):
        return USER_AGE_DIFF_STRATEGY

    @classmethod
    def diff_type(cls):
        return NUMBER_DIFF_TYPE

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert isinstance(lhs, User)
        assert isinstance(rhs, User)
        return True


@Differ.register_strategy
class UserDiffStrategy(BaseDiffStrategy):
    def __init__(self):
        super(UserDiffStrategy, self).__init__(diff_items=[
            NameDiff
        ])

    @classmethod
    def name(cls):
        return USER_DIFF_STRATEGY


class UserNamePatch(BaseBehaviour):

    @classmethod
    def behaviour_kit(cls):
        return USER_AGE_PATCH_STRATEGY

    @classmethod
    def associated_diff_type(cls):
        return NUMBER_DIFF_TYPE

    def execute(self, diff_item, *args, **kwargs):
        super(UserNamePatch, self).execute(diff_item, *args, **kwargs)

        parent_user = diff_item.current_state()
        target_user = diff_item.target_state()

        if parent_user.age < target_user.age:
            print("user has aged")
        elif parent_user.age > target_user.age:
            print("user went back in time")
        else:
            print("nothing happened")



@Patcher.register_behaviour
class UserPatch(BasePatchBehaviour):
    def __init__(self):
        super(UserPatch, self).__init__(behaviours=[
            UserNamePatch
        ])

    @classmethod
    def name(cls):
        return USER_AGE_PATCH_STRATEGY


def diff_users(user1, user2):
    diff_strategy = Differ.get_strategy(USER_DIFF_STRATEGY)
    diff = diff_strategy.diff(user1, user2)

    user_patcher = Patcher.get_behaviour(USER_AGE_PATCH_STRATEGY)
    diff.attach_behaviour(patch_behaviour_kit=user_patcher)

    diff.execute()

    return diff


def main():
    user_1 = User("TW", 1)
    user_2 = User("TW", 2)


    diff_users(user_1, user_2)
    diff_users(user_2, user_1)
    diff_users(user_1, user_1)

main()
