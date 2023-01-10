# для запуска кода через терминал необходимо ввести следующую строку: pytest -v --driver Chrome --driver-path chromedriver.exe test_chukicheva_hw28.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import time

@pytest.fixture(autouse=True, scope="function")
def testing():
   # вместо 'C:/Skillfactory/chromedriver.exe' укажите путь к веб-драйверу
   pytest.driver = webdriver.Chrome('C:/Skillfactory/chromedriver.exe')
   pytest.driver.implicitly_wait(10)
   pytest.driver.get('https://b2c.passport.rt.ru/')
   pytest.driver.set_window_size(1280, 1024)

   yield

   pytest.driver.quit()



'''AUTHORISATION BLOCK'''

def test_auth_page_design():
   ''' 1. Проверка соответствия дизайна страницы авторизации требованиям заказчика. '''
   right = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "page-right")))
   try:
      assert right.find_element(By.CLASS_NAME, "what-is-container")
   except:
      raise Exception('Продуктовый слоган ЛК "Ростелеком ID" отсутствует в правой части страницы авторизации.')


def test_auth_form():
   ''' 2. Проверка формы авторизации на наличие необходимых элементов (меню выбора типа авторизации,
   формы ввода, кнопки "Войти", ссылки "Забыл пароль" и "Зарегистрироваться"). '''

   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='rt-tabs rt-tabs--orange rt-tabs--small tabs-input-container__tabs']")))
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-login")))


def test_auth_auto_tab_menu_mail_to_phone():
   ''' 3. Проверка автоматического переключения таба меню авторизации (на примере электронной почты и номера телефона). '''
   # проверка, что изначально активный таб "Номер телефона"
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="t-btn-tab-phone" and @class="rt-tab rt-tab--small rt-tab--active"]')))
   # вводит почту и проверяем, что таб меню сменился на "Почта"
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("example@pochta.net")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("pass")
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="t-btn-tab-mail" and @class="rt-tab rt-tab--small rt-tab--active"]')))


def test_auth_by_valid_phone():
   ''' 4. Проверка авторизации по валидному номеру телефона. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("89060759857")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("sf_te5t_M28")
   try:
      WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-login"))).click()
      # assert pytest.driver.save_screenshot('auth_by_valid_phone.png')
      assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "logout-btn")))
   except:
      WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rt-captcha__image")))
      raise Exception('Из-за большого количества запросов возникла капча, которую невозможно обойти автотестом.')


def test_auth_by_invalid_phone():
   ''' 5. Проверка авторизации по невалидному номеру телефона. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("86660759857")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("sf_te5t_M28")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-login"))).click()
   # assert pytest.driver.save_screenshot('auth_by_valid_phone.png')
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "form-error-message")))


def test_auth_by_valid_mail():
   ''' 6. Проверка авторизации по валидной электронной почте. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("eng.translators2015@mail.ru")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("te5t_EN6")
   try:
      WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-login"))).click()
      # assert pytest.driver.save_screenshot('auth_by_valid_mail.png')
      assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "logout-btn")))
   except:
      WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rt-captcha__image")))
      raise Exception('Из-за большого количества запросов возникла капча, которую невозможно обойти автотестом.')


def test_auth_by_invalid_mail():
   ''' 7. Проверка авторизации по невалидной электронной почте. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("eng.translators@mail.ru")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("te5t_EN6")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-login"))).click()
   # assert pytest.driver.save_screenshot('auth_by_valid_phone.png')
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "form-error-message")))


def test_auth_by_invalid_login():
   ''' 8. Проверка авторизации по невалидному логину. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("test_login")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("test_paS5")
   # assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="t-btn-tab-login" and @class="rt-tab rt-tab--small rt-tab--active"]')))
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-login"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "form-error-message")))


def test_auth_by_invalid_ls():
   ''' 9. Проверка авторизации по невалидному лицевому счету. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("000123000456")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("test_paS5")
   try:
      WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="t-btn-tab-ls" and @class="rt-tab rt-tab--small rt-tab--active"]')))
      WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-login"))).click()
      assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "form-error-message")))
   except:
      raise Exception('При вводе лицевого счета (12-значной комбинации) таб меню авторизации не сменился на "Лицевой счет".')



''' CODE AUTORISATION BLOCK '''

def test_auth_code_link_by_mail():
   ''' 10. Проверка открытия страницы с полем ввода временного кода при использовании незарегистрированной почты. '''
   pytest.driver.get('https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_decosystems&redirect_uri=https://start.rt.ru/&response_type=code&scope=openid&theme=light')
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("chukichka@mail.net")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "otp_get_code"))).click()
   try:
      assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text == "Код подтверждения отправлен"
      assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "otp-code-form-container__desc"))).text == "На почту chukichka@mail.net"
   except:
      if WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rt-captcha__image"))):
         raise Exception('Из-за большого количества запросов возникла капча, которую невозможно обойти автотестом.')
      elif WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "otp-form__timeout"))):
         raise Exception(f'{WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "otp-form__timeout"))).text}')

def test_auth_code_link_by_phone():
   ''' 11 Проверка открытия страницы с полем ввода временного кода при использовании зарегистрированного номера телефона. '''
   pytest.driver.get('https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_decosystems&redirect_uri=https://start.rt.ru/&response_type=code&scope=openid&theme=light')
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("+79060759857")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "otp_get_code"))).click()
   try:
      assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text == "Код подтверждения отправлен"
      assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "otp-code-form-container__desc"))).text == "По SMS на номер +7 906 075-98-57"
   except:
      if WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rt-captcha__image"))):
         raise Exception('Из-за большого количества запросов возникла капча, которую невозможно обойти автотестом.')
      elif WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "otp-form__timeout"))):
         raise Exception(f'{WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "otp-form__timeout"))).text}')



'''REGISTER BLOCK'''

def test_register_redirect():
   ''' 12. Проверка перехода на страницу с формой регистрации по ссылке "Зарегистрироваться". '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'


def test_register_design():
   ''' 13. Проверка соответствия дизайна страницы регистрации с требованиями заказчика. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()
   left = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "page-left")))
   try:
      assert left.find_element(By.CLASS_NAME, "what-is-container").text != ''
   except:
      raise Exception('Продуктовый слоган ЛК "Ростелеком ID" отсутствует в левой части страницы регистрации.')


def test_register_form():
   ''' 14. Проверка формы регистрации на наличие необходимых элементов (поля ввода имени, фамилии, региона,
   почты/телефона, пароля, подтверждения пароля и кнопки "Зарегистрироваться"). '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()

   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName")))
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName")))
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Регион')]")))
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address")))
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password-confirm")))
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'register')))


def test_register_btn_names():
   ''' 15. Проверка наименований элементов в форме "Регистрация" на соответствие требованиям. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()

   register_required_elm_names = ['Имя', 'Фамилия', 'Регион', 'E-mail или мобильный телефон', 'Пароль', 'Подтверждение пароля', 'Продолжить']
   register_element_names = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__content'))).text
   register_element_names = register_element_names.split('\n')
   for i in range(len(register_element_names)):
      try:
         assert register_element_names[i] in register_required_elm_names
      except:
         raise Exception('Название элемента в форме «Регистрация» не соответствует требованиям.')


def test_register_by_mail():
   ''' 16. Проверка регистрации нового пользователя с использованием электронной почты. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("Жан-Жак")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys("Руссо")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("eng.translators@mail.ru")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("600D_password")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password-confirm"))).send_keys("600D_password")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1'))).text == 'Подтверждение email'


def test_register_by_phone():
   ''' 17. Проверка регистрации нового пользователя с использованием номера телефона. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("Жан-Жак")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys("Руссо")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("89667898812")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("600D_password")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password-confirm"))).send_keys("600D_password")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1'))).text == 'Подтверждение телефона'


def test_register_invalid_password_check():
   ''' 18. Проверка ввода невалидного пароля при регистрации нового пользователя и появляющихся сообщений. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("hello")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[4]/div[1]/span'))).text == 'Длина пароля должна быть не менее 8 символов'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("tyteperпароль")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[4]/div[1]/span'))).text == 'Пароль должен содержать только латинские буквы'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("yetonemoretry")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[4]/div[1]/span'))).text == 'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("yet1moretry")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[4]/div[1]/span'))).text == 'Пароль должен содержать хотя бы одну заглавную букву'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("averyl0nGpassword21sb")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[4]/div[1]/span'))).text == 'Длина пароля должна быть не более 20 символов'
   # time.sleep(5)


def test_register_exist_mail():
   ''' 19. Проверка регистрации пользователя с уже зарегистрированной почтой. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("Жан-Жак")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys("Руссо")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("chukichka-neko@mail.ru")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("600D_password")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password-confirm"))).send_keys("600D_password")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h2'))).text == 'Учётная запись уже существует'


def test_register_exist_phone_window_design():
   ''' 20. Проверка дизайна окна "Учетная запись уже существует" по уже зарегистрированному номеру телефона. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("Жан-Жак")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys("Руссо")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("89060759857")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("600D_password")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "password-confirm"))).send_keys("600D_password")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'gotoLogin')))
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'registration_confirm_btn')))


def test_register_firstname_check():
   ''' 21. Проверка ввода имени в поле регистрации. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[1]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("Samantha")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[1]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("!@#$%^&*")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[1]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("我不会说汉语请做不辣的怎么样你会说英语")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[1]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("моеимясостоитизтридцатичетырехбукв")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[1]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("Анна Мария")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[1]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys("12345")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[1]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)


def test_register_lastname_check():
   ''' 22. Проверка ввода фамилии в поле регистрации. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys("")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[2]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys("Samantha")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[2]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys("!@#$%^&*")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[2]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys("我不会说汉语请做不辣的怎么样你会说英语")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[2]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys("моеимясостоитизтридцатичетырехбукв")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[2]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys("Римский Корсаков")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[2]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys("12345")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form/div[1]/div[2]/span'))).text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
   # time.sleep(5)


def test_register_mail_phone_check():
   ''' 23. Проверка ввода почты / номера телефона в поле регистрации. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "kc-register"))).click()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div/div/div/form/div[3]/span'))).text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("случайнаяфраза")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div/div/div/form/div[3]/span'))).text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("randomphrase")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div/div/div/form/div[3]/span'))).text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("!@#$%^&*")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div/div/div/form/div[3]/span'))).text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("我不会说汉语请做不辣的怎么样你会说英语")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div/div/div/form/div[3]/span'))).text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("моеимясостоитизтридцатичетырехбукв")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div/div/div/form/div[3]/span'))).text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("12345")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div/div/div/form/div[3]/span'))).text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("89012345678")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-right']/div/div/div/form/div[3]/div/span[1]/span[1]")))
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("+79012345678")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-right']/div/div/div/form/div[3]/div/span[1]/span[1]")))
   # time.sleep(5)
   pytest.driver.refresh()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "address"))).send_keys("79012345678")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "register"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page-right']/div/div/div/form/div[3]/div/span[1]/span[1]")))
   # time.sleep(5)



'''RESET PASSWORD BLOCK'''

def test_reset_password_redirect():
   ''' 24. Проверка перехода на страницу "Восстановление пароля". '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "forgot_password"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text == "Восстановление пароля"


def test_reset_password_elements_names():
   ''' 25. Проверка названий элементов в форме восстановления пароля на соответствие требованиям. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "forgot_password"))).click()

   respass_required_elm_names = ['Телефон', 'Почта', 'Логин', 'Лицевой счёт', 'Капча',
                                  'Вернуться', 'Далее']
   respass_element_names = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__content'))).text
   respass_element_names = respass_element_names.split('\n')
   for i in range(len(respass_element_names)):
      try:
         assert respass_element_names[i] in respass_required_elm_names
      except:
         raise Exception('Название элемента в форме восстановаления пароля не соответствует требованиям.')


def test_reset_password_invalid_login_captcha():
   ''' 26. Проверка функции восстановления пароля с невалидным логином и невалидной комбинацией-капчей. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "forgot_password"))).click()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("te5t_login")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "captcha"))).send_keys("Random5tR")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "reset"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "form-error-message"))).text == "Неверный логин или текст с картинки"


def test_reset_password_invalid_ls_captcha():
   ''' 27. Проверка функции восстановления пароля с невалидным лиц.счетом и невалидной комбинацией-капчей. '''
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "forgot_password"))).click()

   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "t-btn-tab-ls"))).click()
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("000123000456")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "captcha"))).send_keys("Random5tR")
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, "reset"))).click()
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "form-error-message"))).text == "Неверный логин или текст с картинки"


