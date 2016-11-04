from unittest import TestCase

from click.testing import CliRunner
import mock

from . import CURRENT_PATH
import cli


class TestGetProfiles(TestCase):
    """Unit test class to get list of profiles."""

    def test_read_profile_file(self):
        file_path = '/'.join([CURRENT_PATH, 'profiles_test.json'])
        profiles = cli.get_all_profiles(file_path)
        self.assertEqual(len(profiles), 2)
        self.assertIs(type(profiles), dict)

    @mock.patch('gincher.get_all_profiles')
    def test_display_profiles(self, mock_profiles):
        mock_profiles.return_value = {"ghe": {"name": "test", "email": "test@example.com"}}
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['list'])
        self.assertIs(result.exit_code, 0)
        self.assertTrue('ghe' in result.output)

    @mock.patch('gincher.get_all_profiles')
    def test_display_empty_profiles(self, mock_profiles):
        mock_profiles.return_value = None
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['list'])
        self.assertIs(result.exit_code, 0)
        self.assertTrue('--no profile--' in result.output)
