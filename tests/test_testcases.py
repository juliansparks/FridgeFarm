import pytest
import time
import functools
from flask import url_for

#: make all URLs external
url_for = functools.partial(url_for, _external=True)


@pytest.mark.usefixtures('live_server')
@pytest.mark.selenium
class TestCase:

    @pytest.mark.usefixtures('selenium')
    def test_register(self, selenium):
        """
        This Test Case tests that:
        - User can navigate to login page
        - There is a link on the login page to register 'Click to Register!'
        - This link goes to the registration page
        - The registration has forms:
          - username
          - email
          - password
          - password2
        - when the form is submitted user is redirected to the login page
        """
        selenium.get(url_for('auth.login'))

        assert 'Sign In' in selenium.title

        selenium.save_screenshot('tests/screenshots/singin.png')

        links = selenium.find_elements_by_link_text('Click to Register!')

        assert len(links) == 1

        links[0].click()
        time.sleep(1)

        assert url_for('auth.register') in selenium.current_url

        selenium.save_screenshot('tests/screenshots/register.png')

        selenium.find_element_by_id('username').send_keys('MrTest')
        selenium.find_element_by_id('email').send_keys('mrtest@test.com')
        selenium.find_element_by_id('password').send_keys('Password123')
        selenium.find_element_by_id('password2').send_keys('Password123')

        selenium.save_screenshot('tests/screenshots/formsfilled.png')

        selenium.find_element_by_id('submit').click()

        time.sleep(2)

        assert url_for('main.HomepageView:index') in selenium.current_url

        selenium.save_screenshot('tests/screenshots/formsubmitted.png')
