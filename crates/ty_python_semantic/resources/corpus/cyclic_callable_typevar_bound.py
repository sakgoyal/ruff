"""Minimal reproduction for ty cycle crash (20 lines).

Regression test for https://github.com/astral-sh/ty/issues/2243

The crash requires this specific combination:
1. A TypeVar with a forward-reference union bound: `TypeVar("T", bound="X[Any] | int")`
2. A Callable type alias using that TypeVar: `TypeAlias = Callable[[T], None]`
3. A Protocol using Self in a method returning another Protocol with that TypeVar
4. A subclass Protocol inheriting from the parent with the TypeVar
5. Another Protocol using ExprT (bounded by forward ref) in a method

Run with: ty check --python-version 3.14
Expected: Should not crash with "too many cycle iterations"
"""
from collections.abc import Callable
from typing import Protocol, Self, Any, TypeVar, TypeAlias

FrameT = TypeVar("FrameT", bound="Frame[Any] | int")
Fn: TypeAlias = Callable[[FrameT], None]
ExprT = TypeVar("ExprT", bound="Expr[Any]")

class NS(Protocol[FrameT, ExprT]):
    def when(self) -> Then[FrameT]: ...

class Expr(Protocol[FrameT]):
    def ns(self) -> NS[FrameT, Self]: ...
    @classmethod
    def col(cls, f: Fn[FrameT]) -> Self: ...

class Then(Expr[FrameT], Protocol[FrameT]):
    pass

class Frame(Protocol[ExprT]):
    def with_columns(self, e: ExprT) -> None: ...
