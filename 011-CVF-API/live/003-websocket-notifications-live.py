import websocket


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    print(f"Close status code: {close_status_code}, Close message: {close_msg}")


def on_open(ws):
    print("### connected ###")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://cardata.production.cn.vcf.apps.vwautocloud.cn/notifications",
                                header={
                                    "Authorization": "Bearer eyJraWQiOiJkNTBmNjUwYy04NzY2LTQ5OGQtOThjMS0yNmNhYTRmNDYyYzkiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhNzViYWI1Mi0wMzNjLTRmZDctYWQ5YS0xYjQyZmNkNGVkMTNAYXBwc192dy1kaWxhYl9jb20iLCJhdWQiOiJhNzViYWI1Mi0wMzNjLTRmZDctYWQ5YS0xYjQyZmNkNGVkMTNAYXBwc192dy1kaWxhYl9jb20iLCJhYXQiOiJpZGVudGl0eWtpdCIsImlzcyI6Imh0dHBzOi8vaWRlbnRpdHkuaWRrLnZ3YXV0b2Nsb3VkLmNuIiwianR0IjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzE2MTc3MTU1LCJpYXQiOjE3MTYxNzM1NTUsImxlZSI6WyJWV19BTkhVSSJdLCJqdGkiOiIzMDkzMmQ4OC0yZjA5LTQ1ZWMtYjYxMy1mMGM4MzQxZTA5NTQifQ.Pe1mCfG40Y9R7B9WmH6TFSMke1_Xx4u32uvWlWMhleG7WHKrs-2nsBigPEMSBne4YvPzuovOonsjiZUqu340Tx0RtdUECGi92s8QcOhdLsxnU1Oo7sZQV8FefZ7FDTPt89tIm0nst-5GTC40VC5g5hmT_uFRHoQyxKVTYKc2xx-IFfU0ydjTY2-7IP4EdmzBXO-TiNk1Muv_Nc4quS8QzQcdGTNCkMOWteh52dxT5s_zZpt7g5AtmWYm2X0aICKgNUQFDlSPvpklamyFcc4F7b0kkIM3oFXs4AuVLmEbjBw1T2qXM_J762aKIFWj6a7oYkBBZ83etzsNXeW48J-QJ8zTeQYvL_lhY9t0oFYkFgcPidk8fT3rQ6P04J4E9HuXuydlNohFaRqs9D1eqVN-cedaRPmc1G0PScmrF80jSnmKcghc3mTBURIrYz0YLoi7a5FpmFlelNoMGxHPBo3yxSiG0oTSmBISw-B_ftM_91pqS5k_xWl9UdcAEW0Cs_z2WgEG0R3uG21AJYdnIplRx56fS2Jn6i4qpIorpnFyqdZlbx0sf5LWOzNFNxKp0vWS_7e9mYn3uOddp8v628pVNi1mS1UG5NWNPXm_gacsIUsR10gmHfwwMEJv8IFYf5uBh2INJRcs__sKfNne9n0kQqD1u4R8pU2tZRKGFFb9wFM"},
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

