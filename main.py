from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
from kivy.metrics import dp

Window.clearcolor = (0.035, 0.047, 0.075, 1)

KV = """
#:import dp kivy.metrics.dp

<RoundedCard@BoxLayout>:
    padding: dp(18)
    spacing: dp(12)
    canvas.before:
        Color:
            rgba: 0.075, 0.092, 0.135, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(22)]

<RootLayout@BoxLayout>:
    orientation: "vertical"
    padding: dp(22)
    spacing: dp(18)
    canvas.before:
        Color:
            rgba: 0.035, 0.047, 0.075, 1
        Rectangle:
            pos: self.pos
            size: self.size

BoxLayout:
    orientation: "vertical"
    padding: dp(22)
    spacing: dp(18)
    canvas.before:
        Color:
            rgba: 0.035, 0.047, 0.075, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: "vertical"
        size_hint_y: None
        height: dp(86)
        spacing: dp(4)

        Label:
            text: "SMS Sender"
            color: 0.94, 0.96, 1, 1
            font_size: "29sp"
            bold: True
            halign: "left"
            valign: "middle"
            text_size: self.size

        Label:
            text: "Simple, direct text messaging"
            color: 0.58, 0.65, 0.78, 1
            font_size: "14sp"
            halign: "left"
            valign: "middle"
            text_size: self.size

    BoxLayout:
        orientation: "vertical"
        padding: dp(18)
        spacing: dp(10)
        size_hint_y: None
        height: dp(132)
        canvas.before:
            Color:
                rgba: 0.075, 0.092, 0.135, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(20)]

        Label:
            text: "RECIPIENT"
            color: 0.58, 0.69, 0.88, 1
            font_size: "11sp"
            bold: True
            size_hint_y: None
            height: dp(18)
            halign: "left"
            text_size: self.size

        TextInput:
            id: phone
            hint_text: "+98912..."
            multiline: False
            write_tab: False
            font_size: "17sp"
            padding: [dp(13), dp(14), dp(13), dp(14)]
            size_hint_y: None
            height: dp(54)
            background_normal: ""
            background_active: ""
            background_color: 0.12, 0.15, 0.21, 1
            foreground_color: 0.95, 0.97, 1, 1
            hint_text_color: 0.48, 0.55, 0.67, 1
            cursor_color: 0.36, 0.76, 1, 1
            selection_color: 0.18, 0.45, 0.72, 0.7

    BoxLayout:
        orientation: "vertical"
        padding: dp(18)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: 0.075, 0.092, 0.135, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(20)]

        BoxLayout:
            size_hint_y: None
            height: dp(22)

            Label:
                text: "MESSAGE"
                color: 0.58, 0.69, 0.88, 1
                font_size: "11sp"
                bold: True
                halign: "left"
                text_size: self.size

            Label:
                id: counter
                text: "0 characters"
                color: 0.58, 0.65, 0.78, 1
                font_size: "11sp"
                halign: "right"
                text_size: self.size

        TextInput:
            id: message
            hint_text: "Write your message — Persian is supported"
            multiline: True
            font_size: "17sp"
            padding: [dp(13), dp(13), dp(13), dp(13)]
            background_normal: ""
            background_active: ""
            background_color: 0.12, 0.15, 0.21, 1
            foreground_color: 0.96, 0.97, 1, 1
            hint_text_color: 0.48, 0.55, 0.67, 1
            cursor_color: 0.36, 0.76, 1, 1
            selection_color: 0.18, 0.45, 0.72, 0.7
            base_direction: "rtl"
            on_text: app.update_counter(self.text)

        Label:
            id: segment_hint
            text: "SMS segment estimate appears here"
            color: 0.58, 0.65, 0.78, 1
            font_size: "12sp"
            size_hint_y: None
            height: dp(22)
            halign: "left"
            text_size: self.size

    Button:
        text: "Send SMS"
        size_hint_y: None
        height: dp(56)
        font_size: "17sp"
        bold: True
        color: 0.03, 0.07, 0.12, 1
        background_normal: ""
        background_down: ""
        background_color: 0.36, 0.76, 1, 1
        on_release: app.send_sms()

    Label:
        id: status
        text: "Your message is sent only when you tap Send SMS."
        color: 0.68, 0.74, 0.84, 1
        font_size: "12sp"
        text_size: self.width, None
        halign: "center"
        valign: "middle"
        size_hint_y: None
        height: dp(42)
"""

class SmsSenderApp(App):
    def build(self):
        self.title = "SMS Sender"
        self.ui = Builder.load_string(KV)
        self.update_counter(self.ui.ids.message.text)
        return self.ui

    def set_status(self, text):
        self.ui.ids.status.text = text

    def update_counter(self, message):
        count = len(message)
        self.ui.ids.counter.text = str(count) + (" character" if count == 1 else " characters")

        # Persian and other non-GSM characters use Unicode SMS encoding.
        gsm_basic = (
            "@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ "
            "!\"#¤%&'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿"
            "abcdefghijklmnopqrstuvwxyzäöñüà"
        )
        is_unicode = any(char not in gsm_basic for char in message)
        if not message:
            estimate = "Unicode-safe text entry · estimate appears as you type"
        elif is_unicode:
            parts = 1 if count <= 70 else (count + 66) // 67
            estimate = "Unicode SMS · about " + str(parts) + (" part" if parts == 1 else " parts")
        else:
            parts = 1 if count <= 160 else (count + 152) // 153
            estimate = "Standard SMS · about " + str(parts) + (" part" if parts == 1 else " parts")
        self.ui.ids.segment_hint.text = estimate

    def send_sms(self):
        phone = self.ui.ids.phone.text.strip()
        message = self.ui.ids.message.text

        if not phone:
            self.set_status("Enter a recipient phone number.")
            return
        if not message.strip():
            self.set_status("Enter a message first.")
            return

        if platform != "android":
            self.set_status("SMS sending works only in the Android APK.")
            return

        self.set_status("Requesting SMS permission…")
        try:
            from android.permissions import request_permissions, Permission
            request_permissions(
                [Permission.SEND_SMS],
                lambda permissions, grants: Clock.schedule_once(
                    lambda _dt: self._send_after_permission(phone, message, grants), 0
                ),
            )
        except Exception as exc:
            self.set_status("Could not request SMS permission: " + str(exc))

    def _send_after_permission(self, phone, message, grants):
        if not grants or not grants[0]:
            self.set_status("SMS permission was denied. Allow it in Android settings.")
            return

        try:
            from jnius import autoclass
            SmsManager = autoclass("android.telephony.SmsManager")
            JavaString = autoclass("java.lang.String")

            # Keep the message as Unicode when passing it to Android.
            java_message = JavaString(message)
            manager = SmsManager.getDefault()
            parts = manager.divideMessage(java_message)
            count = parts.size()

            if count > 1:
                manager.sendMultipartTextMessage(phone, None, parts, None, None)
                self.set_status(
                    "Android accepted the message as " + str(count) +
                    " SMS parts. Delivery is not guaranteed."
                )
            else:
                manager.sendTextMessage(phone, None, java_message, None, None)
                self.set_status("Android accepted the SMS. Delivery is not guaranteed.")
        except Exception as exc:
            self.set_status("SMS sending failed: " + str(exc))

if __name__ == "__main__":
    SmsSenderApp().run()
