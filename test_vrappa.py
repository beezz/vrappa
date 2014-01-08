# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 beezz <beezz@T500>

import pytest
import vrappa
import vrappa.misc


def test_default_impl():

    tacos = vrappa.VrappaBase()

    @tacos.decorate()
    def f():
        raise Exception

    with pytest.raises(Exception):
        f()


def test_simple():
    tacos = vrappa.VrappaBase()

    def resume(*args, **kwargs):
        pass

    @tacos.decorate(
        resume=resume,
        catch=(Exception, )
    )
    def f():
        raise Exception

    assert None == f()

    def resume(*args, **kwargs):
        return kwargs.get('result')

    @tacos.decorate(
        resume=resume,
    )
    def f():
        return 1

    assert 1 == f()


def test_prepare():
    tacos = vrappa.VrappaBase()

    arg1, arg2, kwarg2 = 1, 2, 3

    @tacos.decorate()
    def f(arg1, arg2, kwarg1=None, kwarg2=None):
        assert [arg1, arg2, kwarg1, kwarg2] == [1, 2, None, 3]

    f(arg1, arg2, kwarg2=kwarg2)

    def prep(args, kwargs):
        return (1, 2), {'kwarg2': 3}

    @tacos.decorate(prepare=prep)
    def f(arg1, arg2, kwarg1=None, kwarg2=None):
        assert [arg1, arg2, kwarg1, kwarg2] == [1, 2, None, 3]

    f(6, 7)


def test_catch():
    tacos = vrappa.VrappaBase()

    def action(exc, args=None, kwargs=None):
        assert exc

    @tacos.decorate(
        catch=Exception,
        resume=lambda res=None, exc=None, args=None, kwargs=None: None,
        action=action,
    )
    def f():
        raise Exception

    f()


def test_def_email_impl():

    vrappa.misc.SMTP_CONF_DEFAULT['port'] = 1025
    tacos = vrappa.misc.EmailOnException(
        app_str="PyTest",
    )

    @tacos.decorate()
    def f():
        raise Exception("Tralallaa")

    with pytest.raises(Exception):
        f()
