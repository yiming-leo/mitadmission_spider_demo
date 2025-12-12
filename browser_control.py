import time

from DrissionPage import ChromiumOptions, Chromium


class BrowserManager:
    def __init__(self):
        self.browser_configs = []  # 存 options
        self.browser_instances = []  # 存正在运行的 browser/tab 实例（可能为 None）
        self.last_used = []
        self.current_index = -1

    def add_browser(self, chromium_options, name=None):
        if name is None:
            name = f"browser_{len(self.browser_configs)}"

        self.browser_configs.append({
            "name": name,
            "options": chromium_options
        })

        self.browser_instances.append(None)  # 还没启动浏览器
        self.last_used.append(None)

    def _start_browser(self, index):
        """真正启动浏览器"""
        print(f"[BrowserManager] Starting browser: {self.browser_configs[index]['name']}")
        browser = Chromium(self.browser_configs[index]["options"]).latest_tab
        self.browser_instances[index] = browser
        return browser

    def get_next_browser(self):
        """选择一个浏览器并返回其实例（必要时启动）"""
        # 第一次使用
        if all(t is None for t in self.last_used):
            self.current_index = 0
        else:
            # 优先选从未使用过的浏览器
            unused = [i for i, t in enumerate(self.last_used) if t is None]
            if unused:
                self.current_index = unused[0]
            else:
                # 否则选最久未使用的
                self.current_index = min(range(len(self.last_used)),
                                         key=lambda i: self.last_used[i])

        self.last_used[self.current_index] = time.time()

        # 如果浏览器实例不存在 → 启动一个
        if self.browser_instances[self.current_index] is None:
            return self._start_browser(self.current_index), self.current_index

        return self.browser_instances[self.current_index], self.current_index

    def mark_current_failed(self):
        if 0 <= self.current_index < len(self.browser_instances):
            # 关闭当前浏览器
            try:
                self.browser_instances[self.current_index].browser.quit()
            except:
                pass

            # 下一次使用时重新启动
            self.browser_instances[self.current_index] = None

            # 设置 last_used，让它尽量排后
            self.last_used[self.current_index] = 0


def init_browsers():
    manager = BrowserManager()

    # 浏览器 1
    co = ChromiumOptions()
    co.set_user_data_path(r"C:\Users\24797\AppData\Local\Google\Chrome\User Data\Default")
    co.set_address('127.0.0.1:9333')
    co.set_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.1 Safari/537.36")
    co.set_argument("--accept-language=zh-CN,zh;q=0.9")
    co.set_argument("--window-size=1400,900")
    manager.add_browser(co, "Default Profile")

    # 浏览器 2
    co2 = ChromiumOptions()
    co2.set_user_data_path(r"C:\Users\24797\AppData\Local\Google\Chrome\User Data\Profile 11")
    co2.set_address('127.0.0.1:9222')
    co2.set_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/15.1 Safari/605.1.15")
    co2.set_argument("--accept-language=en-US,en;q=0.8")
    co2.set_argument("--window-size=1280,720")
    manager.add_browser(co2, "Profile 11")

    # 浏览器 3
    co3 = ChromiumOptions()
    co3.set_user_data_path(r"C:\Users\24797\AppData\Local\Google\Chrome\User Data\Profile 2")
    co3.set_address('127.0.0.1:9444')
    co3.set_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/121.0")
    co3.set_argument("--accept-language=ja,en;q=0.8")
    co3.set_argument("--window-size=1366,768")
    manager.add_browser(co3, "Profile 2")

    # 浏览器 4
    co4 = ChromiumOptions()
    co4.set_user_data_path(r"C:\Users\24797\AppData\Local\Google\Chrome\User Data\Profile 16")
    co4.set_address('127.0.0.1:9555')
    co4.set_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.1 Safari/537.36")
    co4.set_argument("--accept-language=en-GB,en;q=0.7")
    co4.set_argument("--window-size=1536,864")
    manager.add_browser(co4, "Profile 16")

    # 浏览器 5
    co5 = ChromiumOptions()
    co5.set_user_data_path(r"C:\Users\24797\AppData\Local\Google\Chrome\User Data\Profile 1")
    co5.set_address('127.0.0.1:9666')
    co5.set_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0")
    co5.set_argument("--accept-language=ko-KR,ko;q=0.8")
    co5.set_argument("--window-size=1600,900")
    manager.add_browser(co5, "Profile 1")

    return manager
