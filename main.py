from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import os
import logging

root_path = "/home/ges/Documents/src"
repository_dirs = []
logger = logging.getLogger(__name__)

def find_all_repositories():
    for root, dirs, files in os.walk(root_path, followlinks=True):
        for d in dirs:
            subdir = os.path.join(root, d)
            if os.path.isdir(os.path.join(subdir, ".git/")):
                repository_dirs.append(subdir)

class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        find_all_repositories()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        repos = []
        arg = event.get_argument()
        with open("/home/ges/test.txt", "a") as myfile:
            myfile.write(arg)
        for repo in repository_dirs:
            logger.info("basename: " + basename)
            basename = os.path.basename(repo)

            if not arg or arg == "":
                repos.append(ExtensionResultItem(icon='images/icon.png',
                                                 name=basename,
                                                 description=repo,
                                                 on_enter=HideWindowAction()))
            else:
                if arg.lower in basename:
                    repos.append(ExtensionResultItem(icon='images/icon.png',
                                                     name=basename,
                                                     description=repo,
                                                     on_enter=HideWindowAction()))

        return RenderResultListAction(repos)

class ItemEnterEventListener(EventListener):
    
    def on_event(self, event, extension):
        data = event.get_data()
        cmd = ["nvim-qt", data]
        call(cmd)

if __name__ == '__main__':
    DemoExtension().run()
