from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import os

root_path = "/home/ges/Documents/src"
repository_dirs = []

def find_all_repositories():
    for root, dirs, files in os.walk(root_path, followlinks=True):
        for d in dirs:
            subdir = os.path.join(root, d)
            if os.path.isdir(os.path.join(subdir, ".git/")):
                repository_dirs.append(subdir)

class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        repos = []
        for repo in repository_dirs:
            repos.append(ExtensionResultItem(icon='images/icon.png',
                                             name=os.path.basename(repo),
                                             description=repo,
                                             on_enter=HideWindowAction()))

        return RenderResultListAction(repos)

if __name__ == '__main__':
    DemoExtension().run()
