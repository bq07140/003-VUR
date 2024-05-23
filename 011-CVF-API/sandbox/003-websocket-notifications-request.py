import websocket


def on_message(ws, message):
    print('--------tanwg--0001')
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("### connected ###")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://cardata.sandbox.cn.vcf.apps.vwautocloud.cn/notifications",
                                header={
                                    "Authorization": "Bearer eyJraWQiOiI3OThkNzA5NC1lNTljLTQwMDQtODE4OC1iZjdjMTdkYzlkZGIiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyZWEwN2E5Ni02NTdhLTQ1ZTAtYjVjNy0yZGM0ZWFjZmZmOGFAYXBwc192dy1kaWxhYl9jb20iLCJhdWQiOiIyZWEwN2E5Ni02NTdhLTQ1ZTAtYjVjNy0yZGM0ZWFjZmZmOGFAYXBwc192dy1kaWxhYl9jb20iLCJhYXQiOiJpZGVudGl0eWtpdCIsImlzcyI6Imh0dHBzOi8vaWRlbnRpdHktc2FuZGJveC52d2dyb3VwLmlvIiwianR0IjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzE1ODQ3OTg1LCJpYXQiOjE3MTU4NDQzODUsImxlZSI6WyJWV19BTkhVSSJdLCJqdGkiOiI3NDQzNjAwZS1iNzBkLTQzOWMtOTU5Ni0wMTlkMzNiMjRiYTkifQ.qW8gqX8ditTmwdyv9bZqy8pYPSrsAkP8sp0EDOO6Iq3Am5Pfx_rT5SowFFAU3OFcIIS8FrNA9hwUygMFwMS38lY29si2-jwBrY71_bYT90u6lQHXwKtcHB_e1eEtDXJ8jTurdUjjnORjE3RK1Uq00Af1xqeQtorlxeX1iiJh77YObsjrL5HXoa9pX7KGFkVHn1h5NChwFOmP8DFzSgYETh9i6vz4tIQXKR2TQRWj3SwPiOPdU3s3-ACv-VOL9kQqv1mZCMSI5rCu_24e8KCJEXs0IY2gRLIFK8PdNIcc8emeGJeohjBe9jOgICJvVAhI0KBJgN8QA0VUpA3na130mG9WD8J15xYY5tQjbCzHINzcsuGaeu4xtVCCWvdTAIy4QxervJSOnNp1M6au2JrAr6Af9-A7weNOFkCUE3uxNQf5Y0f3PkbiFkvxKwVhr-wy__ORQr8pIWeInvJ6r1nWG6GCyP2LlipADspHuwAVReML5nKjq-F3htlYylaqxVOSa6rAid4IU05-38w3nQmXQjvglg58IEBlbKz0M0_TVsNhyiD5njS3hxZgxmMKavugQ2YuJf3L4m1UIBTnTvVdcI-vRLWAhq0TXot1UzSYV46AUacvWwBxCAxW_w97voUkpg74FcoKUyfgVAOYiBlU2hucOyaM7HTQvIeE7x7Tc8g"},
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()






