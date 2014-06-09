import cerridwen.api_server

from cerridwen import Moon, Sun, LatLong, jd2iso, iso2jd, parse_jd_or_iso_date

from nose.tools import assert_equal, assert_almost_equal, raises
import unittest

# misc
def test_age():
    assert_almost_equal(Moon(2456794.949305556).age(), 18.189345157705247)

def test_period_length():
    assert_almost_equal(Moon(2456794.949305556).period_length(), 29.517968974076211)

# new/full moons
def test_next_new_moon():
    assert_almost_equal(Moon(2456794.9541666).next_new_moon().jd, 2456806.2779293722)

def test_next_full_moon():
    assert_almost_equal(Moon(2456731.376389).next_full_moon().jd, 2456733.2141234726)

# sun/moon rise/set
# compared with data generated by
#   http://aa.usno.navy.mil/data/docs/RS_OneYear.php (Form B, long=13E, lat=52N)
def test_rise_set():
    obs = LatLong(52, 13)
    assert_equal(Moon(2456798.2, obs).next_rise().iso_date, "2014-05-20 23:37:17")
    assert_equal(Sun(2456799.9, obs).next_rise().iso_date, "2014-05-23 03:03:05")

def test_iso_jd():
    time_iso = jd2iso(cerridwen.jd_now())
    assert_equal(cerridwen.jd2iso(cerridwen.iso2jd(time_iso)), time_iso)

def test_parse_date_valid_jd():
    parse_jd_or_iso_date(1)
    parse_jd_or_iso_date(2456799.9897213)

def test_parse_date_valid_iso():
    parse_jd_or_iso_date("2014-05-20T23:37:17")
    parse_jd_or_iso_date("2014-05-20 23:37:17")

@raises(ValueError)
def test_parse_date_invalid_1():
    parse_jd_or_iso_date("2014-05-20T23:37:17Z")

@raises(ValueError)
def test_parse_date_invalid_2():
    parse_jd_or_iso_date("123garbage.5")

class HTTP_TestCase(unittest.TestCase):
    def setUp(self):
        self.app = cerridwen.api_server.app.test_client()

    def simple_sun_test(self):
        response = self.app.get('/v1/sun')
        self.assertEqual(response.status_code, 200)

    def simple_moon_test(self):
        response = self.app.get('/v1/moon')
        self.assertEqual(response.status_code, 200)

    def jd_date_test(self):
        response = self.app.get('/v1/sun?date=2456805.9347222224')
        print(response)
        self.assertEqual(response.status_code, 200)

    def bogus_date_test(self):
        response = self.app.get('/v1/sun?date=jumble81923')
        print(response)
        self.assertEqual(response.status_code, 400)

    def root_404(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)
