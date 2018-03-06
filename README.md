# Introduction
Diff-n-patch is a generic diffing/patching library that can be very easily configured to solve diverse diffing needs of a project. 
# Requirement
The aim of this library is to create a facade on the underlying infrastructure for diffing two python objects and to allow one or more patching behaviours for the same.

The library allows to custom define the actual diff (business logic) within the application's domain. Potentially, the library caters to enabling the developer to define diff on heterogeneous objects. Additionally, the library also permits configuring more than one patching behaviour.

For ex. If there is a requirement to diff two User objects, we create a diff-strategy for it. We create a diff item for the age and date of birth (as they are both inherently related) and possibly a diff item for name too. We also create a patch strategy that applies one object's change to the other.. There could also be a different strategy in which we may want to reverse patch the source object instead. Alternatively, we also want to use the patching strategy to publish the change to a queue.

# Getting Started
## Diff Strategy
The Diff Strategy is a class that groups similar diff items under the same head. This class needs to extend the diff.BaseDiffStrategy class. This class has a method name() that uniquely identifies the strategy. It also registers the various diff items that the strategy contains.
Use the @Differ.register_strategy decorator in order to register the strategy.
## Patch Behaviour
The Patch Behaviour, like Diff Strategy is a class that groups similar patch behaviour under the same head. This class needs to extend the diff.BasePatchBehaviour class. It has a method name() that uniquely identifies the behaviour. In this class, we may attach the various Patch Items.
Use the @Patcher.register_behaviour decorator in order to register the bevhaviour.
## DIff Item
A Diff Item is an atomic diff. This class actually implements an atomic diff behaviour. For example, for a User, the age diff could be a combination of dob + age diff. It needs to extend the diff.BaseDiffItem class. It needs to implement the diff_strategy() method, the unique diff_type that is used to map the patch behaviour. The is_applicable() method is the actual diff implementation. 
## Patch Item
A Patch Item is contains the actual patching mechanism. This class needs to extend the BaseBehaviour class. It needs to implment the behaviour_kit() method that associates the specific Patch Behaviour that it belongs to. The associated_diff_type() needs to map the Patch Item to the Diff Item
# Installation
# Configuration
# Usage
For a sample usage, please look at samples/diff_users.py and samples/diff_cars.py
# Limitations
# Roadmap
# Project History
