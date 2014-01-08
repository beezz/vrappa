# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import functools


class VrappaBase(object):

    def __init__(self, prepare=None, catch=None, action=None, resume=None):
        self._prepare = prepare
        self._catch = catch
        self._action = action
        self._resume = resume

    def prepare(self, args, kwargs):
        """Prepare args and kwargs for wrapped function.
        Returns tuple (args, kwargs).
        """
        if self._prepare is None:
            return args, kwargs
        return self._prepare(args, kwargs)

    def catch(self, args=None, kwargs=None):
        """Returns tuple of exceptions that should be catched.
        """
        return self._catch

    def action(self, exc, args=None, kwargs=None):
        """Action taken on exception.
        """
        if self._action is not None:
            return self._action(exc, args=args, kwargs=kwargs)

    def resume(self, result=None, exc=None, args=None, kwargs=None):
        """How to resume processing.

        Resuming function handle two paths. One where exception
        is caught and second where we got result from
        wrapped function.

        In base implementation exception is reraised and result is
        simply returned back.
        """
        if self._resume is not None:
            return self._resume(
                result=result,
                exc=exc,
                args=args,
                kwargs=kwargs,
            )
        if exc is not None:
            raise exc
        return result

    def decorate(self, prepare=None, catch=None, action=None, resume=None):
        """Decorator factory.

        Override class implementation by supplying your own functions
        for prepare, catch, action and resume functions.
        """

        prepare = prepare or self.prepare
        catch = catch or self.catch
        try:
            catch_iter = iter(catch)
        except TypeError:
            catch_iter = None
        action = action or self.action
        resume = resume or self.resume

        def _decorate(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                args, kwargs = prepare(args, kwargs)
                if catch_iter:
                    exc_to_catch = catch
                if callable(catch):
                    try:
                        issubclass(catch, Exception)
                        exc_to_catch = catch
                    except TypeError:
                        exc_to_catch = catch(args=args, kwargs=kwargs)
                else:
                    exc_to_catch = catch

                try:
                    return resume(
                        result=func(*args, **kwargs),
                        args=args, kwargs=kwargs,
                    )
                except exc_to_catch as exc:
                    action(exc, args=args, kwargs=kwargs)
                    return resume(exc=exc, args=args, kwargs=kwargs)
            return wrapper
        return _decorate
