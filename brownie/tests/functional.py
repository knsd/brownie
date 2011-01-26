# coding: utf-8
"""
    brownie.tests.functional
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for :mod:`brownie.functional`.

    :copyright: 2010 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
from __future__ import with_statement
import re

from attest import Tests, Assert, TestBase, test

from brownie.functional import compose, flip, Signature, bind_arguments, curried


tests = Tests()


@tests.test
def test_compose():
    with Assert.raises(TypeError):
        compose()
    add_one = lambda x: x + 1
    mul_two = lambda x: x * 2
    Assert(compose(add_one, mul_two)(1)) == 3


@tests.test
def test_flip():
    f = lambda a, b, **kws: (a, kws)
    Assert(f(1, 2)) == (1, {})
    Assert(flip(f)(1, 2)) == (2, {})
    kwargs = {'foo': 'bar'}
    Assert(flip(f)(1, 2, **kwargs)) == (2, kwargs)


class TestSignature(TestBase):
    @test
    def positionals(self):
        func = lambda a, b, c: None
        Assert(Signature.from_function(func)) == (['a', 'b', 'c'], [], None, None)

    @test
    def keyword_arguments(self):
        func = lambda a=1, b=2, c=3: None
        Assert(Signature.from_function(func)) == (
            [], [('a', 1), ('b', 2), ('c', 3)], None, None
        )

    @test
    def mixed_positionals_keyword_arguments(self):
        func = lambda a, b, c=3: None
        Assert(Signature.from_function(func)) == (
            ['a', 'b'], [('c', 3)], None, None
        )
        func = lambda a, b, c=3, d=4: None
        Assert(Signature.from_function(func)) == (
            ['a', 'b'], [('c', 3), ('d', 4)], None, None
        )

    @test
    def arbitary_positionals(self):
        foo = lambda *foo: None
        bar = lambda *bar: None
        for func, name in [(foo, 'foo'), (bar, 'bar')]:
            Assert(Signature.from_function(func)) == ([], [], name, None)

    @test
    def arbitary_keyword_arguments(self):
        spam = lambda **spam: None
        eggs = lambda **eggs: None
        for func, name in [(spam, 'spam'), (eggs, 'eggs')]:
            Assert(Signature.from_function(func)) == ([], [], None, name)

tests.register(TestSignature)


class TestBindArguments(TestBase):
    @test
    def no_args(self):
        func = lambda: None

        Assert(bind_arguments(func)) == {}

        with Assert.raises(ValueError) as exc:
            bind_arguments(func, (1, ), {})
        Assert(exc.args[0]) == 'expected at most 0 positional arguments, got 1'

        tests = [
            ({'a': 1}, "got unexpected keyword argument '.'"),
            ({'a': 1, 'b': 2}, "got unexpected keyword arguments '.' and '.'"),
            (
                {'a': 1, 'b': 2, 'c': 3},
                "got unexpected keyword arguments '.', '.' and '.'"
            )
        ]

        for kwargs, message in tests:
            with Assert.raises(ValueError) as exc:
                bind_arguments(func, kwargs=kwargs)
            err_msg = exc.args[0].obj
            assert re.match(message, err_msg) is not None
            for name in kwargs:
                assert name in err_msg

    @test
    def only_positionals(self):
        func = lambda a, b, c: None

        Assert(bind_arguments(func, (1, 2, 3))) == dict(a=1, b=2, c=3)
        Assert(bind_arguments(func, (1, 2), {'c': 3})) == dict(a=1, b=2, c=3)

        tests = [
            ([('a', 1), ('b', 2)], "'.' is missing"),
            ([('a', 1)], "'.' and '.' are missing"),
            ([], "'.', '.' and '.' are missing")
        ]
        all_names = set('abc')
        for args, message in tests:
            names, values = [], []
            for name, value in args:
                names.append(name)
                values.append(value)

            with Assert.raises(ValueError) as exc_args:
                bind_arguments(func, values)

            with Assert.raises(ValueError) as exc_kwargs:
                bind_arguments(func, kwargs=dict(args))

            for exc in [exc_args, exc_kwargs]:
                err_msg = exc.args[0].obj
                assert re.match(message, err_msg) is not None
                for name in all_names.difference(names):
                    assert name in err_msg

        with Assert.raises(ValueError) as exc:
            bind_arguments(func, (1, 2, 3), {'c': 4})
        Assert(exc.args[0]) == "got multiple values for 'c'"

    @test
    def only_keyword_arguments(self):
        func = lambda a=1, b=2, c=3: None

        Assert(bind_arguments(func)) == dict(a=1, b=2, c=3)
        Assert(bind_arguments(func, ('a', ))) == dict(a='a', b=2, c=3)
        Assert(bind_arguments(func, (), {'a': 'a'})) == dict(a='a', b=2, c=3)

    @test
    def arbitary_positionals(self):
        func = lambda *args: None
        Assert(bind_arguments(func)) == {'args': ()}
        Assert(bind_arguments(func, (1, 2, 3))) == {'args': (1, 2, 3)}

    @test
    def mixed_positionals(self):
        func = lambda a, b, *args: None
        Assert(bind_arguments(func, (1, 2))) == dict(a=1, b=2, args=())
        Assert(bind_arguments(func, (1, 2, 3))) == dict(a=1, b=2, args=(3, ))
        with Assert.raises(ValueError):
            Assert(bind_arguments(func))

    @test
    def arbitary_keyword_arguments(self):
        func = lambda **kwargs: None
        Assert(bind_arguments(func)) == {'kwargs': {}}
        Assert(bind_arguments(func, (), {'a': 1})) == {'kwargs': {'a': 1}}

    @test
    def mixed_keyword_arguments(self):
        func = lambda a=1, b=2, **kwargs: None
        Assert(bind_arguments(func)) == dict(a=1, b=2, kwargs={})
        Assert(bind_arguments(func, (3, 4))) == dict(a=3, b=4, kwargs={})
        Assert(bind_arguments(func, (), {'c': 3})) == dict(
            a=1,
            b=2,
            kwargs=dict(c=3)
        )

    @test
    def mixed_positional_arbitary_keyword_arguments(self):
        func = lambda a, b, **kwargs: None
        Assert(bind_arguments(func, (1, 2))) == dict(a=1, b=2, kwargs={})
        Assert(bind_arguments(func, (1, 2), {'c': 3})) == dict(
            a=1,
            b=2,
            kwargs=dict(c=3)
        )
        Assert(bind_arguments(func, (), dict(a=1, b=2))) == dict(
            a=1,
            b=2,
            kwargs={}
        )
        with Assert.raises(ValueError):
            bind_arguments(func)
        with Assert.raises(ValueError):
            bind_arguments(func, (1, 2), {'a': 3})

    @test
    def mixed_keyword_arguments_arbitary_positionals(self):
        func = lambda a=1, b=2, *args: None
        Assert(bind_arguments(func)) == dict(a=1, b=2, args=())
        Assert(bind_arguments(func, (3, 4))) == dict(a=3, b=4, args=())
        Assert(bind_arguments(func, (3, 4, 5))) == dict(a=3, b=4, args=(5, ))
        Assert(bind_arguments(func, (), {'a': 3, 'b': 4})) == dict(
            a=3, b=4, args=()
        )
        with Assert.raises(ValueError):
            bind_arguments(func, (3, ), {'a': 4})

tests.register(TestBindArguments)


class TestCurried(TestBase):
    @test
    def positional(self):
        func = curried(lambda a, b, c: (a, b, c))
        Assert(func(1, 2, 3)) == (1, 2, 3)
        Assert(func(1, 2)(3)) == (1, 2, 3)
        Assert(func(1)(2, 3)) == (1, 2, 3)
        Assert(func(1)(2)(3)) == (1, 2, 3)

        Assert(func(c=3, b=2, a=1)) == (1, 2, 3)
        Assert(func(c=3)(a=1)(2)) == (1, 2, 3)

    @test
    def keyword_arguments(self):
        func = curried(lambda a=1, b=2, c=3: (a, b, c))
        Assert(func()) == (1, 2, 3)
        Assert(func(c=4)) == (1, 2, 4)
        Assert(func(4)) == (4, 2, 3)

    @test
    def mixed_positional_keyword_arguments(self):
        func = curried(lambda a, b, c=3: (a, b, c))
        Assert(func(1, 2)) == (1, 2, 3)
        Assert(func(1, 2, 4)) == (1, 2, 4)

    @test
    def arbitary_positionals(self):
        func = curried(lambda a, b, c, *args: (a, b, c, args))
        Assert(func(1, 2, 3)) == (1, 2, 3, ())
        Assert(func(1, 2, 3, 4, 5)) == (1, 2, 3, (4, 5))
        Assert(func(1)(2, 3, 4, 5)) == (1, 2, 3, (4, 5))
        Assert(func(1, 2)(3, 4, 5)) == (1, 2, 3, (4, 5))
        Assert(func(1)(2, 3, 4, 5)) == (1, 2, 3, (4, 5))

        Assert(func(1)(b=2)(3, 4, 5)) == (1, 2, 3, (4, 5))
        Assert(func(a=1)(b=2)(3, 4, 5)) == (1, 2, 3, (4, 5))
        Assert(func(a=1, b=2)(3, 4, 5)) == (1, 2, 3, (4, 5))

    @test
    def arbitary_keyword_arguments(self):
        func = curried(lambda a, b, c, **kwargs: (a, b, c, kwargs))
        Assert(func(1, 2, 3)) == (1, 2, 3, {})
        with Assert.raises(TypeError):
            func(1, 2)(3, c=4)
        Assert(func(1, 2, 3, foo=4)) == (1, 2, 3, dict(foo=4))
        Assert(func(1)(2, 3, foo=4)) == (1, 2, 3, dict(foo=4))
        Assert(func(1, 2)(3, foo=4)) == (1, 2, 3, dict(foo=4))

    @test
    def mixed_arbitary_arguments(self):
        func = curried(lambda a, b, c, *args, **kwargs: (a, b, c, args, kwargs))
        Assert(func(1, 2, 3)) == (1, 2, 3, (), {})
        Assert(func(1, 2, 3, 4, 5)) == (1, 2, 3, (4, 5), {})
        Assert(func(1, 2, 3, foo=4)) == (1, 2, 3, (), dict(foo=4))
        Assert(func(1, 2, 3, 4, foo=5)) == (1, 2, 3, (4, ), dict(foo=5))


tests.register(TestCurried)
