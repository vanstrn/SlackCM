# SlackCM
A computer monitoring client for Slack to check aspects of a computer from Slack.
Has the ability to check resource usage and IP address of the computer the client is setup on.

## Setup 
1. Clone repo
2. [Register a Slack App](https://github.com/slackapi/python-slackclient/blob/master/tutorial/01-creating-the-slack-app.md) 
3. [Create environment variable of Slack Token](https://github.com/slackapi/python-slackclient/blob/master/tutorial/04-running-the-app.md)
4. Create slack compatible python environment. Look at `env.yml` for required packages
5. Modify startSlack.sh script to point to the compatible python and bash scipt
6. Create a service that will execute at boot.
    - Create service file: `sudo touch /etc/systemd/system/slackclient.service`
    - Edit service file to read:
    ```
    [Unit]
    Description=ethtool script

    [Service]
    ExecStart=/path/to/startup/script/startSlack.sh

    [Install]
    WantedBy=multi-user.target
    ```
    - Enable the service: `systemctl enable slackclient.service`
    
## Modifying
**Adding additional keywords in the standard client:**
1. Add additional parser conditions to the `message` function in `slackCM.py`.
2. Add a a to execute the desired task. If a response is desired make sure to create message with correct Slack syntax.

**Adding additional features to the client:**
Checkout https://github.com/slackapi/python-slackclient for a bunch of useful tutorials.
See [example](https://github.com/slackapi/python-slackclient/blob/master/tutorial/04-running-the-app.md) of adding different permissions to the client to add callbacks to the RTM Client.

## Possible upgrades:
1. Docker environment that minimizes setup of the client.
2. Some way to distinguish between PCs. Currently if client is run on multiple PCs with the same Slack App they will all publish to the same channel.



