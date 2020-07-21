from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from _auth.models import ResetCode
from _auth.utils import get_code, get_hash


class TestAuth(TestCase):
    c = Client()

    def setUp(self):
        user = User()
        user.username = "username"
        user.email = "email@email.com"
        user.set_password("password")
        user.save()

    def testLogin1(self):
        """check login with valid username credentials"""
        res = self.c.post(reverse('login_page'), {
            'username': 'username',
            'password': 'password'
        })
        self.assertEqual(res.json()['status'], 200)

    def testLogin2(self):
        """check login with valid email credentials"""
        res = self.c.post(reverse('login_page'), {
            'username': 'email@email.com',
            'password': 'password'
        })
        self.assertEqual(res.json()['status'], 200)

    def testLogin3(self):
        """check login with invalid username credentials"""
        res = self.c.post(reverse('login_page'), {
            'username': 'usernam',
            'password': 'password'
        })
        self.assertEqual(res.json()['status'], 404)

    def testLogin4(self):
        """check login with invalid email credentials"""
        res = self.c.post(reverse('login_page'), {
            'email': 'email@emai.com',
            'password': 'password'
        })
        self.assertEqual(res.json()['status'], 404)

    def testLogin5(self):
        """check login with blank credentials"""
        res = self.c.post(reverse('login_page'), {
            'username': '',
            'password': '',
            'email': ''
        })
        self.assertEqual(res.json()['status'], 400)

    def testSignup1(self):
        """check sign up with valid credentials"""
        res = self.c.post(reverse("signup_page"), {
            'username': 'username1',
            'email': 'email1@email.com',
            'password': 'password'
        })
        self.assertEqual(res.json()['status'], 200)

    def testSignup2(self):
        """check sign up with invalid credentials"""
        res = self.c.post(reverse("signup_page"), {
            'username': '',
            'email': 'email1email.com',
            'password': 'pass'
        })
        self.assertEqual(res.json()['status'], 400)

    def testSignup3(self):
        """check sign up with used username"""
        res = self.c.post(reverse("signup_page"), {
            'username': 'username',
            'email': 'email2@email.com',
            'password': 'pass'
        })
        self.assertEqual(res.json()['status'], 400)

    def testSignup4(self):
        """check sign up with used email"""
        res = self.c.post(reverse("signup_page"), {
            'username': 'username3',
            'email': 'email@email.com',
            'password': 'pass'
        })
        self.assertEqual(res.json()['status'], 400)

    def testForgetPassword1(self):
        """check forget password with valid username"""
        res = self.c.post(reverse('forget_password_page'), {
            'username_email': 'username'
        })
        self.assertEqual(res.json()['status'], 200)

    def testForgetPassword2(self):
        """check forget password with valid email"""
        res = self.c.post(reverse('forget_password_page'), {
            'username_email': 'email@email.com'
        })
        self.assertEqual(res.json()['status'], 200)

    def testForgetPassword3(self):
        """check forget password with invalid credentials"""
        res = self.c.post(reverse('forget_password_page'), {
            'username_email': ''
        })
        self.assertEqual(res.json()['status'], 404)

    def testUsername1(self):
        """check checkusername with unused username"""
        res = self.c.post(reverse('checkusername'), {
            'username': 'username'
        })
        self.assertEqual(res.json()['status'], 200)

    def testUsername2(self):
        """check checkusername with used username"""
        res = self.c.post(reverse('checkusername'), {
            'username': ''
        })
        self.assertEqual(res.json()['status'], 404)

    def testEmail1(self):
        """check checkusername with unused username"""
        res = self.c.post(reverse('checkemail'), {
            'email': 'email@email.com'
        })
        self.assertEqual(res.json()['status'], 200)

    def testEmail2(self):
        """check checkusername with used username"""
        res = self.c.post(reverse('checkemail'), {
            'email': ''
        })
        self.assertEqual(res.json()['status'], 404)

    def testReset1(self):
        """check reset password with valid credentials"""
        code = get_code()
        c_obj = ResetCode(user=User.objects.get(
            username='username'), code=get_hash(code))
        c_obj.save()
        res = self.c.post(reverse('reset_password_page', args=['username']), {
            'username': 'username',
            'code': code,
            'password1': 'password1',
            'password2': 'password1',
        })
        self.assertEqual(res.json()['status'], 200)

    def testReset2(self):
        """check reset password with not matched passsword"""
        code = get_code()
        c_obj = ResetCode(user=User.objects.get(
            username='username'), code=get_hash(code))
        c_obj.save()
        res = self.c.post(reverse('reset_password_page', args=['username']), {
            'username': 'username',
            'code': code,
            'password1': 'password1',
            'password2': 'password12',
        })
        self.assertEqual(res.json()['status'], 400)

    def testReset3(self):
        """check reset password with wrong username"""

        res = self.c.post(reverse('reset_password_page', args=['username']), {
            'username': '',
            'code': 'code',
            'password1': 'password1',
            'password2': 'password1',
        })
        self.assertEqual(res.json()['status'], 404)

    def testReset4(self):
        """check reset password with wrong code"""
        code = get_code()
        c_obj = ResetCode(user=User.objects.get(
            username='username'), code=get_hash(code))
        c_obj.save()
        res = self.c.post(reverse('reset_password_page', args=['username']), {
            'username': 'username',
            'code': code+"1",
            'password1': 'password1',
            'password2': 'password1',
        })
        self.assertEqual(res.json()['status'], 404)
