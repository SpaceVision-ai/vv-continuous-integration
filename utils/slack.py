from slackboy import SlackBoy

class SlackReporter:
    def __init__(self, token: str, channel: str, prefix: str, repository: str,
                 branch: str, target: str, pr_number: str, tag: str):
        self.client = SlackBoy.from_token(token)
        self.client.add_default_channel(channel)
        self.prefix = prefix
        self.repository = repository
        self.branch = branch
        self.target = target
        self.pr_number = pr_number
        self.tag = tag

    def get_pull_request_url(self) -> str:
        return f'https://github.com/teamdable/{self.repository}/pull/{self.pr_number}'


    def send_slack_header(self) -> str:
        
        msg = (
            f'*Repository: {self.repository}* \n\n'
            '*Pull-request info:*\n'
            f'- branch: {self.branch} -> {self.target}\n'
            f'- url: {self.get_pull_request_url()}\n\n'
            f'tag: {self.tag}_WARNING'
        )

        response = self.client.send_message(msg=msg, prefix=self.prefix)
        ts = response.get('ts', '')
        return ts

    def send_slack_message(self, msg: str):
        ts = self.send_slack_header()
        self.client.send_message(msg=f'```{msg}```', prefix=self.prefix, reply_ts=ts)
