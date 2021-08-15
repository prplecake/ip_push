import json
import os
import unittest

from unittest import mock, TestCase

from setup import create_config, backup_config, main

unittest.TestLoader.sortTestMethodsUsing = None


class ConfigTest(TestCase):
	@classmethod
	def setUpClass(cls):
		with open('settings.json', 'r') as sf:
			SECRETS = json.load(sf)
		cls.SECRETS = SECRETS

	@mock.patch('setup.input', create=True)
	def test_create_config(self, mocked_input):
		mocked_input.side_effect = [
			'Y',
			self.SECRETS['keys']['user_key'],
			self.SECRETS['keys']['app_token'],
			self.SECRETS['server_location'],
		]
		create_config('test_settings.json')
		file_exists = os.path.exists('test_settings.json')
		self.assertTrue(file_exists)

	@mock.patch('setup.input', create=True)
	def test_main_no_overwrite(self, mocked_input):
		mocked_input.side_effect = [
			'n',
		]
		with self.assertRaises(SystemExit) as cm:
			main('test_settings.json')

	@mock.patch('setup.input', create=True)
	def test_main_overwrite(self, mocked_input):
		mocked_input.side_effect = [
			'Y',
			'Y',
			self.SECRETS['keys']['user_key'],
			self.SECRETS['keys']['app_token'],
			self.SECRETS['server_location'],
		]
		main('test_settings.json')
		file_exists = os.path.exists('test_settings.json')
		self.assertTrue(file_exists)

	@mock.patch('setup.input', create=True)
	def test_main_nonexistent_settings_file(self, mocked_input):
		os.remove('test_settings.json')
		mocked_input.side_effect = [
			'Y',
			'Y',
			self.SECRETS['keys']['user_key'],
			self.SECRETS['keys']['app_token'],
			self.SECRETS['server_location'],
		]
		main('test_settings.json')
		file_exists = os.path.exists('test_settings.json')
		self.assertTrue(file_exists)

	@mock.patch('setup.input', create=True)
	def test_cancel_create_config(self, mocked_input):
		mocked_input.side_effect = [
			'n'
		]
		with self.assertRaises(SystemExit) as cm:
			create_config('test_settings.json')

	def test_backup_config(self):
		backup_config('test_settings.json')
