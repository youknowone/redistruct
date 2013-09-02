
from __future__ import absolute_import

import redis
from .core import KeyValueObject, HashObject, ListObject, SetObject

class StrictRedis(redis.StrictRedis): # override
    def __init__(self, *args, **kwargs):
        super(StrictRedis, self).__init__(*args, **kwargs)
        self._keyobj = KeyValueObject(self)

    def __call__(self, prefix='', suffix='', keymaker=None):
        """

        :param prefix:
        :param suffix:
        :param keymaker:
        :return:
        :rtype: :class:`redistruct.core.KeyValueObject`
        """
        if not keymaker and not prefix and not suffix:
            return self._keyobj
        return KeyValueObject(self, prefix, suffix, keymaker)

    def __getitem__(self, item):
        return self._keyobj[item]

    def __setitem__(self, key, value):
        self._keyobj[key] = value

    def __delitem__(self, key):
        del self._keyobj[key]

    def __contains__(self, item):
        return item in self._keyobj

    @property
    def _result(self):
        return self._keyobj._result

    def hash(self, datakey, prefix='', suffix='', keymaker=None):
        """

        :param datakey:
        :param prefix:
        :param suffix:
        :param keymaker:
        :return:
        :rtype: :class:`redistruct.core.HashObject`
        """
        return HashObject(self, datakey, prefix, suffix, keymaker)

    def list(self, datakey):
        """

        :param datakey:
        :return:
        :rtype: :class:`redistruct.core.ListObject`
        """
        return ListObject(self, datakey)

    def seto(self, datakey):
        """

        :param datakey:
        :return:
        :rtype: :class:`redistruct.core.SetObject`
        """
        return SetObject(self, datakey)
