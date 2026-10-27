# SMS Sender

A small Python/Kivy Android app for sending SMS messages, including long and Persian messages.

## How it works

- The app requests Android's `SEND_SMS` permission when you tap **Send SMS**.
- It uses Android's native `SmsManager` API.
- Long messages are split with `divideMessage` and submitted through `sendMultipartTextMessage`.
- The app does not intentionally send MMS.

**Important:** This cannot guarantee that every device, carrier, or recipient setup will handle a long message as separate SMS segments. SMS charges may apply per segment. Test with a number you control. The app reports that Android accepted the send request, not that the recipient received it.

## Get the APK

GitHub Actions builds a debug APK for you.

1. Open the repository's **Actions** tab.
2. Select **Build Android APK** and open the latest run.
3. Wait for the workflow to finish successfully.
4. Download the `sms-sender-debug-apk` artifact from the run's **Artifacts** section.
5. Extract the ZIP and install the APK on your Android phone. You may need to allow installation from that source.

You can also trigger a build manually from **Actions → Build Android APK → Run workflow**.

The first build can take several minutes while Android build dependencies are downloaded.

## Local build (optional)

On Linux, install Buildozer and its Android build dependencies, then run:

```bash
buildozer android debug
```

The APK is generated under `bin/`.

## Permissions and safety

The app requests the sensitive `SEND_SMS` permission. Review the code before installing and only send messages to recipients you intend to contact. Android may show permission or carrier-related warnings.
