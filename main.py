from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionCustomAction import ExtensionCustomAction
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
        find_all_repositories()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        repos = []
        
        for repo in repository_dirs:
            basename = os.path.basename(repo)
            if event.get_argument():
                if event.get_argument().lower() in basename.lower():
                    repos.append(ExtensionResultItem(icon='images/icon.png',
                                                     name=basename,
                                                     description=repo,
                                                     on_enter=ExtensionCustomAction(repo)))
            else:
                repos.append(ExtensionResultItem(icon='images/icon.png',
                                                 name=basename,
                                                 description=repo,
                                                 on_enter=ExtensionCustomAction(repo)))

        return RenderResultListAction(repos)

class ItemEnterEventListener(EventListener):
    
    def on_event(self, event, extension):
        data = event.get_data()
        cmd = ["nvim-qt", data]
        call(cmd)

if __name__ == '__main__':
    DemoExtension().run()
