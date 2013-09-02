
from redistruct import StrictRedis

r = StrictRedis()

def test_keyobj():
    r.set('a', 1)
    assert r.get('a') == '1'

    assert r['a'] == '1'
    assert r()['a'] == '1'

    r['a'] = '2'
    assert r()['a'] == '2'

def test_prefix():
    r.set('x1', '1')
    assert r('x')['1'] == '1'

def test_hash():
    del r['x']
    h = r.hash('x')
    r.hset('x', 'a', '1')
    assert r.hget('x', 'a') == h['a'] == '1'

    assert h.values() == ['1']
    assert h.keys() == ['a']

    assert h.dict() == {'a': '1'}
    for k, v in h.items():
        assert k == 'a'
        assert v == '1'

    h['a'] = '2'
    assert r.hget('x', 'a') == h['a'] == '2'

    for k in h:
        assert k == 'a'
        assert h[k] == '2'

    del h['a']
    assert h['a'] is None

def test_list():
    del r['l']
    l = r.list('l')
    assert len(l) == 0

    l.append('1', '2', '3')
    assert ''.join(l) == '123'
    assert '1' == l.pop()
    assert ''.join(l) == '23'
    assert len(l) == 2
    count = 2
    for i in l:
        assert str(count) == i
        count += 1

def test_set():
    del r['s']
    s = r.seto('s')
    assert len(s) == 0

    s.add('a', 'b', 'c')
    assert len(s) == 3
    s.add('a', 'b', 'd')
    assert len(s) == 4
    assert s.pop() in 'abcd'

    del r['s']
    s.add('a', 'b', 'c')
    ss = r.seto('ss')
    ss.add('a', 'c', 'e')
    assert set(['a', 'b', 'c', 'e']) == s.union(ss)
    assert set(['b']) == s - ss
    assert set(['a', 'c']) == s.intersection(ss)

