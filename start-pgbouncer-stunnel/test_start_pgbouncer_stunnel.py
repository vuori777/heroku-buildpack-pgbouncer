# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import unittest

start_python = __import__("start-python")

class DatabaseTestSuite(unittest.TestCase):

    def test_postgres_parsing(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = start_python.parse(url)

        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_postgres_unix_socket_parsing(self):
        url = 'postgres://%2Fvar%2Frun%2Fpostgresql/d8r82722r2kuvn'
        url = start_python.parse(url)

        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == '/var/run/postgresql'
        assert url['USER'] == ''
        assert url['PASSWORD'] == ''
        assert url['PORT'] == ''

    def test_postgis_parsing(self):
        url = 'postgresql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = start_python.parse(url)

        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_database_url(self):
        del os.environ['DATABASE_URL']
        a = start_python.config()
        assert not a

        os.environ['DATABASE_URL'] = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'

        url = start_python.config()

        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

if __name__ == '__main__':
    unittest.main()
