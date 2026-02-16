"""
Internet Speed X Complainer Bot (Angela Yu–style, using X instead of Twitter).

1. InternetSpeedXBot: Selenium driver + down/up (Mbps).
2. get_internet_speed(): Run speedtest.net, set self.down / self.up.
3. post_at_provider(): Log in at x.com, post complaint if speed below promised.
4. Main: create bot, get_internet_speed(), then post_at_provider().
"""

import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import (
    CHROME_DRIVER_PATH,
    PROMISED_DOWN,
    PROMISED_UP,
    X_EMAIL,
    X_PASSWORD,
    require_x_credentials,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SPEEDTEST_URL = "https://www.speedtest.net/"
X_LOGIN_URL = "https://x.com/i/flow/login"
X_HOME_URL = "https://x.com/home"
# X's DOM changes often; these selectors may need updating (see README).
X_USERNAME_INPUT_NAME = "text"
X_PASSWORD_INPUT_NAME = "password"
SPEEDTEST_GO_SELECTOR = "a.js-start-test"
SPEEDTEST_RESULT_DOWN = ".result-item-download .result-data-value"
SPEEDTEST_RESULT_UP = ".result-item-upload .result-data-value"
DEFAULT_WAIT_SEC = 30
HUMAN_DELAY_SEC = 1.5


def _create_driver() -> webdriver.Chrome:
    """Create Chrome WebDriver; use webdriver-manager if no path set."""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if CHROME_DRIVER_PATH:
        service = Service(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        from webdriver_manager.chrome import ChromeDriverManager

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(10)
    return driver


class InternetSpeedXBot:
    """Bot that measures internet speed and posts a complaint on X if below promised."""

    def __init__(self) -> None:
        self.driver = _create_driver()
        self.down: float = 0.0
        self.up: float = 0.0

    def get_internet_speed(self) -> None:
        """Open speedtest.net, run test, set self.down and self.up (Mbps)."""
        self.driver.get(SPEEDTEST_URL)
        wait = WebDriverWait(self.driver, DEFAULT_WAIT_SEC)

        # Dismiss cookie/overlay if present, then start test
        time.sleep(HUMAN_DELAY_SEC)
        try:
            go_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SPEEDTEST_GO_SELECTOR))
            )
            go_btn.click()
        except Exception:
            # Fallback: try by link text
            go_btn = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "GO"))
            )
            go_btn.click()

        # Wait for result rows (download then upload)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SPEEDTEST_RESULT_DOWN))
        )
        time.sleep(2)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SPEEDTEST_RESULT_UP))
        )
        time.sleep(1)

        down_el = self.driver.find_element(By.CSS_SELECTOR, SPEEDTEST_RESULT_DOWN)
        up_el = self.driver.find_element(By.CSS_SELECTOR, SPEEDTEST_RESULT_UP)
        self.down = float(down_el.text.strip())
        self.up = float(up_el.text.strip())
        logger.info("Speed: down=%.2f Mbps, up=%.2f Mbps", self.down, self.up)

    def post_at_provider(self) -> None:
        """Log in at x.com and post a complaint if current speed is below promised."""
        require_x_credentials()
        if self.down >= PROMISED_DOWN and self.up >= PROMISED_UP:
            logger.info(
                "Speed meets or exceeds promised %d/%d Mbps; skipping post.",
                PROMISED_DOWN,
                PROMISED_UP,
            )
            return

        self.driver.get(X_LOGIN_URL)
        wait = WebDriverWait(self.driver, DEFAULT_WAIT_SEC)
        time.sleep(HUMAN_DELAY_SEC)

        # Username/email step (X uses input name "text")
        username_input = wait.until(
            EC.presence_of_element_located((By.NAME, X_USERNAME_INPUT_NAME))
        )
        username_input.send_keys(X_EMAIL)
        time.sleep(HUMAN_DELAY_SEC)
        username_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # Password step (handle "unusual activity" if X asks for username again)
        try:
            password_input = wait.until(
                EC.presence_of_element_located((By.NAME, X_PASSWORD_INPUT_NAME))
            )
        except Exception:
            # Sometimes X asks for username again in a second field
            again = wait.until(
                EC.presence_of_element_located((By.NAME, X_USERNAME_INPUT_NAME))
            )
            again.send_keys(X_EMAIL)
            time.sleep(HUMAN_DELAY_SEC)
            again.send_keys(Keys.RETURN)
            time.sleep(2)
            password_input = wait.until(
                EC.presence_of_element_located((By.NAME, X_PASSWORD_INPUT_NAME))
            )

        password_input.send_keys(X_PASSWORD)
        time.sleep(HUMAN_DELAY_SEC)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        # Compose post: X's tweet composer (selectors may need updating)
        self.driver.get(X_HOME_URL)
        time.sleep(3)
        message = (
            f"Hey ISP, why is my internet speed {self.down:.1f} down / {self.up:.1f} up Mbps "
            f"when I was promised {PROMISED_DOWN}/{PROMISED_UP} Mbps?"
        )
        try:
            # Common composer: data-testid or role="textbox"
            composer = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
                )
            )
            composer.click()
            time.sleep(HUMAN_DELAY_SEC)
            composer.send_keys(message)
            time.sleep(HUMAN_DELAY_SEC)
            # Post button
            post_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '[data-testid="tweetButton"]')
                )
            )
            post_btn.click()
            logger.info("Posted complaint on X.")
        except Exception as e:
            logger.warning(
                "Could not find tweet composer or post button (X UI may have changed): %s",
                e,
            )

    def quit(self) -> None:
        """Close the browser."""
        self.driver.quit()


def main() -> None:
    """Run: get speed, then post at provider if below promised."""
    require_x_credentials()
    bot = InternetSpeedXBot()
    try:
        bot.get_internet_speed()
        bot.post_at_provider()
    finally:
        bot.quit()


if __name__ == "__main__":
    main()
