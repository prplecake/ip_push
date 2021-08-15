import os

from unittest import TestCase

from ippush import (
	read_settings,
	IPPush,	
)


class StartLoggerTestCase(TestCase):
	def test_start_logger(self):
		self.assertTrue(os.path.exists('log'))


class ReadSettingsTestCase(TestCase):
	def test_read_settings(self):
		settings = read_settings('test_settings.json')
		self.assertTrue(settings is not None)


class IPPushTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		settings = read_settings('test_settings.json')
		cls.ippush = IPPush(settings)

	def test_get_current_ip(self):
		ippush = self.ippush
		ippush.get_current_ip()

	def test_get_old_ip(self):
		ippush = self.ippush
		ippush.write_new_ip()
		ippush.get_old_ip()

	def test_get_old_ip_file_not_found(self):
		os.remove('ip.old')
		ippush = self.ippush
		ippush.get_old_ip()
		ippush.write_new_ip()

	def test_get_old_ipv6_file_not_found(self):
		os.remove('ipv6.old')
		ippush = self.ippush
		ippush.get_old_ip()
		ippush.write_new_ip()

	def test_send_ip_push(self):
		ippush = self.ippush
		ippush.send_ip_push()

	def test_do_update(self):
		ippush = self.ippush
		ippush.do_update()

	def test_do_update_no_old_ip(self):
		os.remove('ip.old')
		ippush = self.ippush
		ippush.do_update()
