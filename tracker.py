#!/usr/bin/env python3

import ccxt
import rumps
import subprocess

# rumps.debug_mode(True)
exchange = ccxt.binance(
    {"options": {"adustForTimeDifference": True}, "enableRateLimit": True}
)
assets = ["BTCUSDT"]
assets = assets + ["DOGEBTC", "DOGEUSDT"]
interval = 20


def run(cmd):
    return subprocess.check_output(cmd, shell=True).strip()


def tracker_clock_string():
    msg = ""
    for asset in reversed(assets):
        output = exchange.fetch_ticker(asset)
        price = output["last"]
        if price < 1:
            price = "{:.8f}".format(price).strip("0")[1:].lstrip("0")
        elif price > 1000:
            price = round(price)

        if not msg:
            msg = f"{asset} {price}"
        else:
            msg = f"{asset} {price} | {msg}"

    return msg


class OrgClockStatusBarApp(rumps.App):
    @rumps.clicked("Refresh")
    def update_ticker(self, _):
        clock_title = tracker_clock_string()
        self.title = clock_title


def main():
    app = OrgClockStatusBarApp("starting...")

    def timer_func(_):
        _str = tracker_clock_string()
        print(_str)  # removing the print statement makes the app hang
        if _str:
            app.title = _str
        else:
            app.title = "Not tracking"

    timer = rumps.Timer(timer_func, interval)
    timer.start()
    app.run()


if __name__ == "__main__":
    main()
