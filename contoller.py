from flask import Flask, request, render_template
from runners.runner import ChromeCommander
from runners.commands import DriverCommand
import os
app = Flask(__name__)
__name__ = "__main__"

commander = ChromeCommander()


@app.route("/commands/run")
def run_command():
    command = request.args.get("cmd")
    commander.run_command(DriverCommand[command], request.args)
    return ""


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5201))
    app.run(host='0.0.0.0', port=port)