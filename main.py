import os
import threading
import yt_dlp

from kivy.app import App
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.clock import Clock

DOWNLOAD_DIR = "/storage/emulated/0/Download/"
HTML_PATH = "file:///storage/emulated/0/Android/data/ru.iiec.pydroid3/files/webapp/index.html"


class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_webview, 0)

    def create_webview(self, *args):
        from jnius import autoclass, cast, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread

        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        WebSettings = autoclass('android.webkit.WebSettings')
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        ClipboardManager = autoclass('android.content.ClipboardManager')
        Context = autoclass('android.content.Context')

        self.activity = activity

        class JSBridge(PythonJavaClass):
            __javainterfaces__ = ['android/webkit/JavascriptInterface']
            __javacontext__ = 'app'

            def __init__(self, outer):
                super().__init__()
                self.outer = outer

            @java_method('(Ljava/lang/String;)V')
            def downloadVideo(self, url):
                self.outer.handle_download(url)

            @java_method('()V')
            def pasteClipboard(self):
                self.outer.handle_paste()

        @run_on_ui_thread
        def build_webview():
            webview = WebView(activity)
            settings = webview.getSettings()
            settings.setJavaScriptEnabled(True)
            webview.setWebViewClient(WebViewClient())

            self.bridge = JSBridge(self)
            webview.addJavascriptInterface(self.bridge, "android")

            webview.loadUrl(HTML_PATH)
            activity.setContentView(webview)
            self.webview = webview

        build_webview()

    def handle_paste(self):
        from jnius import autoclass, cast
        Context = autoclass('android.content.Context')
        ClipboardManager = autoclass('android.content.ClipboardManager')
        clipboard = cast('android.content.ClipboardManager', self.activity.getSystemService(Context.CLIPBOARD_SERVICE))
        if clipboard.hasPrimaryClip():
            item = clipboard.getPrimaryClip().getItemAt(0)
            text = str(item.getText())
            escaped = text.replace("'", "\\'")
            self.run_js(f"setPastedText('{escaped}')")

    def handle_download(self, url):
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.daemon = True
        thread.start()

    def download_video(self, url):
        try:
            ydl_opts = {
                "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
                "quiet": True,
                "no_warnings": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            Clock.schedule_once(lambda dt: self.run_js("onDownloadResult(true, 'دانلود کامل شد ✅')"), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.run_js("onDownloadResult(false, 'خطا: دانلود ناموفق بود')"), 0)

    def run_js(self, code):
        from android.runnable import run_on_ui_thread

        @run_on_ui_thread
        def _run():
            self.webview.evaluateJavascript(code, None)

        _run()


class ShahramDownloaderApp(App):
    def build(self):
        self.title = "Shahram Downloader"
        if platform == "android":
            return WebViewWidget()
        else:
            from kivy.uix.label import Label
            return Label(text="این اپ فقط روی اندروید (بعد از build) کار می‌کند")


if __name__ == "__main__":
    ShahramDownloaderApp().run()
