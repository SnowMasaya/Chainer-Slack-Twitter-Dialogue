from slackclient import SlackClient
import yaml
from collections import namedtuple


class SlackModel():

    def __init__(self):
        """
        setting paramater Slack model
        :return:
        """
        self.Slack = namedtuple("Slack", ["api_token", "channel", "user", "mecab"])
        self.config_file = "enviroment.yml"
        self.slack_channel = ""
        self.chan = ""
        self.user = ""
        self.mecab_dict = ""
        self.parameter_dict = {}
        train_path = "../data/"
        self.parameter_dict["source"] = train_path + "player_1_wakati"
        self.parameter_dict["target"] = train_path + "player_2_wakati"
        self.parameter_dict["test_source"] = train_path + "player_1_wakati"
        self.parameter_dict["test_target"] = train_path + "player_2_test"

        self.parameter_dict["vocab"] = 5000
        self.parameter_dict["embed"] = 300
        self.parameter_dict["hidden"] = 300
        self.parameter_dict["epoch"] = 20
        self.parameter_dict["minibatch"] = 64
        self.parameter_dict["generation_limit"] = 256
        self.parameter_dict["word2vec"] = "../word2vec/word2vec.model"
        self.parameter_dict["word2vecFlag"] = False
        self.parameter_dict["attention_dialogue"] = ""
        self.parameter_dict["model"] = ""

    def read_config(self):
        """
        read config file for slack
        """
        with open(self.config_file, encoding="utf-8") as cf:
           e = yaml.load(cf)
           slack = self.Slack(e["slack"]["api_token"], e["slack"]["channel"],
                              e["slack"]["user"], e["slack"]["mecab"])
           self.slack_channel = SlackClient(slack.api_token)
           self.chan = slack.channel
           self.user = slack.user
           self.mecab_dict = slack.mecab
