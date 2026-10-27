from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform

KV = """
BoxLayout:
    orientation: "vertical"
    padding: "20dp"
    spacing: "12dp"

    Label:
        text: "SMS Sender"
        font_size: "26sp"
        size_hint_y: None
        height: "48dp"

    TextInput:
        id: phone
        hint_text: "Recipient phone number (e.g. +98912...)"
        multiline: False
        size_hint_y: None
        height: "52dp"

    TextInput:
        id: message
        hint_text: "Type your message, including Persian text"
        multiline: True

    Button:
        text: "Send SMS"
        size_hint_y: None
        height: "54dp"
        on_release: app.send_sms()

    Label:
        id: status
        text: "Messages are sent only when you tap Send SMS."
        text_size: self.width, None
        halign: "center"
        valign: "middle"
        size_hint_y: None
        height: "64dp"
"""

class SmsSenderApp(App):
    def build(self):
        self.ui = Builder.load_string(KV)
        return self.ui

    def set_status(self, text):
        self.ui.ids.status.text = text

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
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            SmsManager = autoclass("android.telephony.SmsManager")
            String = autoclass("java.lang.String")

            activity = PythonActivity.mActivity
            manager = SmsManager.getDefault()
            parts = manager.divideMessage(String(message))
            if parts.size() > 1:
                manager.sendMultipartTextMessage(phone, None, parts, None, None)
                count = parts.size()
                self.set_status(
                    "Android accepted the message as " + str(count) +
                    " SMS parts. Delivery is not guaranteed."
                )
            else:
                manager.sendTextMessage(phone, None, String(message), None, None)
                self.set_status("Android accepted the SMS. Delivery is not guaranteed.")
        except Exception as exc:
            self.set_status("SMS sending failed: " + str(exc))

if __name__ == "__main__":
    SmsSenderApp().run()
