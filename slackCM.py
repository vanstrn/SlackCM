import os
import slack
import ssl as ssl_lib
import certifi
import socket

from functions import *


class ComputerMonitor:
    def __init__(self, channel):
        """Initializes several variables for sending messages.

        Inputs:
        channel (str) - A string specifying which channel the messages will be posted to.

        Outputs:
        None
        """

        self.channel = channel
        self.username = "Computer Monitor Client"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""

    #Definition of static blocks that won't be changed.
    HELP_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "List of Commands to get computer information\n"
                "Use - Returns total CPU, RAM and GPU RAM usage.\n"
                "User - Returns CPU and RAM usage per user.\n"
                "IP - Returns current IP of the machine.\n"
            ),
        },
    }

    DIVIDER_BLOCK = {"type": "divider"}

    #Definitions of messages that
    def GetHelpMessage(self):
        """ Method for generating a message displaying all valid commands.
        Currently hardcoded based on the HELP_BLOCK.
        Inputs:
        None

        Outputs:
        -- (dict) - A dictionary of slack message.
        """

        return {
        "ts": self.timestamp,
        "channel": self.channel,
        "username": self.username,
        "icon_emoji": self.icon_emoji,
        "blocks": [
        self.DIVIDER_BLOCK,
        self.HELP_BLOCK,
        self.DIVIDER_BLOCK,
        ],
        }

    def GetMessage(self):
        """ Method for generating a message displaying the global resource usage
        of the computer.
        Inputs:
        None

        Outputs:
        -- (dict) - A dictionary of slack message.
        """
        res = QueryResourceUsages()

        title = (
        f" *Resource Utilization*\n"
        )
        text = (
        "CPU Percent - " +str(round(res['cpu_avg'],1)) +" %\n"
        "RAM - " +str(round(res['ram'],1)) +"% \n"
        "GPU RAM 0 - " +str(round(res['gpu_0_ram'],1)) +"% \n"
        "GPU RAM 1 - " +str(round(res['gpu_1_ram'],1)) +" %\n"
        )

        TextBlock = self._get_task_block(title, text)

        return {
        "ts": self.timestamp,
        "channel": self.channel,
        "username": self.username,
        "icon_emoji": self.icon_emoji,
        "blocks": [
        self.DIVIDER_BLOCK,
        TextBlock,
        self.DIVIDER_BLOCK,
        ],
        }

    def GetUserMessage(self):
        """ Method for generating a message displaying resource usage of the
        computer on a per person basis.
        Inputs:
        None

        Outputs:
        -- (dict) - A dictionary of slack message.
        """

        userUtil = QueryUserResourceUsages()
        title = (
        f" *Resource Utilization by User*\n"
        )
        msg = ""
        for username,usage in userUtil.items():
            msg +="_"+ username+"_" + "\nCPU Percent - " +str(round(usage['cpu_percent']*100,1)) +"\t RAM - " + str(round(usage['memory_percent'],1)) +" %\n"
        text = (msg)

        TextBlock = self._get_task_block(title, text)

        return {
        "ts": self.timestamp,
        "channel": self.channel,
        "username": self.username,
        "icon_emoji": self.icon_emoji,
        "blocks": [
        self.DIVIDER_BLOCK,
        TextBlock,
        self.DIVIDER_BLOCK,
        ],
        }

    def GetIPMessage(self):
        """ Method for generating a message displaying the IP address of the computer.
        Inputs:
        None

        Outputs:
        -- (dict) - A dictionary of slack message.
        """

        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        title = (
        f" *IP Address*\n"
        )
        text = (
        " " +str(IPAddr) +" \n"
        )

        TextBlock= self._get_task_block(title, text)

        return {
        "ts": self.timestamp,
        "channel": self.channel,
        "username": self.username,
        "icon_emoji": self.icon_emoji,
        "blocks": [
        self.DIVIDER_BLOCK,
        TextBlock,
        self.DIVIDER_BLOCK,
        ],
        }

    def _get_task_block(self, title, text):
        """ Internal method to process data into a block message for Slack.
        Inputs:
        title (str) - Title of the message
        text (str) - Main body text of the message

        Outputs:
        -- (dict) - A dictionary of processed text that is usable with slack.
        """

        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]


#Adding a hook to the Slack RTMClient. This hook processes every message sent to
#the app on slack.
@slack.RTMClient.run_on(event="message")
def message(**payload):
    """Message method which executes when a message is received in Slack. This
    method processes the message data and decides an appropriate response to be
    sent.
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    cm = ComputerMonitor(channel_id)

    #Set these to look for explicit messages.
    if text and text.lower() == "use":
        message = cm.GetMessage()
        response = web_client.chat_postMessage(**message)
    elif text and text.lower() == "user":
        message = cm.GetUserMessage()
        response = web_client.chat_postMessage(**message)
    elif text and text.lower() == "ip":
        message = cm.GetIPMessage()
        response = web_client.chat_postMessage(**message)
    elif text and text.lower() == "help":
        message = cm.GetHelpMessage()
        response = web_client.chat_postMessage(**message)


if __name__ == "__main__":

    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ['SLACK_API_TOKEN']
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()
