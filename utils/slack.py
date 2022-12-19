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
        reply_prefix = 'details'
        total_message_length = len(msg + reply_prefix)
        if total_message_length > 4000:
            split_message_list = []
            reply_available_chunk = 3993  # except for codeblock "```{message}```"
            first_message_chunk_available = reply_available_chunk - len(reply_prefix) - 2  # 2 for ``
            first_message = msg[0: first_message_chunk_available]
            split_message_list.append(first_message)

            for i in range(first_message_chunk_available, total_message_length, reply_available_chunk):
                split_message = msg[i:i+reply_available_chunk]
                split_message_list.append(split_message)

            self.client.send_message(msg=f'```{split_message_list[0]}```', prefix=reply_prefix, reply_ts=ts)
            for split_message in split_message_list[1:]:
                self.client.send_message(msg=f'```{split_message}```', reply_ts=ts)

        else:
            self.client.send_message(msg=f'```{msg}```', prefix=reply_prefix, reply_ts=ts)
