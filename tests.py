from unittest import TestCase, main

from pytelnet import Client


class PyTelnetTest(TestCase):
    def test_ssl_connect_done(self):
        app = Client()
        try:
            app.connect('smtp.yandex.ru', 465)
            assert True
        except:
            assert False

    def test_connect_done(self):
        app = Client(ssl=False)
        try:
            app.connect('smtp.yandex.ru', 25)
            assert True
        except:
            assert False

    def test_ssl_connect_fail(self):
        app = Client()
        try:
            app.connect('smtp.yandex.ru', 999)
            assert False
        except:
            assert True

    def test_received(self):
        app = Client()
        app.connect('smtp.yandex.ru', 465)
        self.assertRegex(app.received(),
                         '220 .*?\.mail\.yandex\.net ESMTP \(Want to use Yandex.Mail for your domain\? '
                         'Visit http://pdd.yandex.ru\)')

    def test_send(self):
        app = Client()
        app.connect('smtp.yandex.ru', 465)
        self.assertRegex(app.received(),
                         '220 .*?\.mail\.yandex\.net ESMTP \(Want to use Yandex.Mail for your domain\? '
                         'Visit http://pdd.yandex.ru\)')
        app.send('EHLO test')
        self.assertRegex(app.received(), '250-.*?\.mail\.yandex\.net.*?')

    def test_close(self):
        app = Client()
        app.connect('smtp.yandex.ru', 465)
        app.close()
        self.assertRaises(OSError, app.send, 'EHLO test')

if __name__ == '__main__':
    main()
