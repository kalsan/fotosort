import os
import glob
import shutil


class Controller:
    def __init__(self, conf, location=None):
        self.conf = conf
        self.setLocation(location)

    def setLocation(self, location):
        self.curr_index = 0
        self.history = []
        self.file_list = []
        if location is not None:
            location = location.replace('file://', '')
            for e in self.conf.extensions:
                self.file_list.extend(glob.glob(location + '/' + e))
                self.file_list = sorted(self.file_list)

    def current(self):
        if not self.file_list:
            return None
        return self.file_list[self.curr_index]

    def first(self):
        if not self.file_list:
            return None
        self.curr_index = 0
        return self.file_list[self.curr_index]

    def prev(self):
        if not self.file_list:
            return None
        self.curr_index = max(0, self.curr_index - 1)
        return self.file_list[self.curr_index]

    def next(self):
        if not self.file_list:
            return None
        self.curr_index = min(len(self.file_list) - 1, self.curr_index + 1)
        return self.file_list[self.curr_index]

    def last(self):
        if not self.file_list:
            return None
        self.curr_index = len(self.file_list) - 1
        return self.file_list[self.curr_index]

    def copyCurrentFile(self, target_dir):
        if not self.file_list:
            return None
        source_file = self.file_list[self.curr_index]
        target_file = self.__collision_free_filename(source_file, target_dir)
        self.history.append(["Copy", source_file, target_file, self.curr_index])
        shutil.copy(source_file, target_file)
        return target_file

    def moveCurrentFile(self, target_dir, called_by_delete=False):
        if not self.file_list:
            return None
        source_file = self.file_list[self.curr_index]
        target_file = self.__collision_free_filename(source_file, target_dir)
        self.history.append(["Delete" if called_by_delete else "Move", source_file, target_file, self.curr_index])
        shutil.move(source_file, target_file)
        del self.file_list[self.curr_index]
        if self.curr_index >= len(self.file_list):
            self.prev()
        return target_file

    def trashCurrentFile(self):
        if not self.file_list:
            return
        target_dir = self.__trash_dir()
        self.ensure_dir_exists(target_dir)
        self.moveCurrentFile(target_dir, True)

    def ensure_dir_exists(self, target_dir):
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)

    def undo(self):
        if not self.history:
            return
        hist_item = self.history.pop()
        if hist_item[0] in ["Delete", "Move"]:
            shutil.move(hist_item[2], hist_item[1])
            self.file_list.insert(hist_item[3], hist_item[1])
            if os.path.isdir(self.__trash_dir()) and not os.listdir(self.__trash_dir()):
                os.rmdir(self.__trash_dir())
        elif hist_item[0] in ["Copy"]:
            os.remove(hist_item[2])
        self.curr_index = hist_item[3]

    def __collision_free_filename(self, source_file, target_dir):
        bn = os.path.basename(source_file)
        target_file = target_dir + '/' + bn
        ext = 1
        while os.path.isfile(target_file):
            ext += 1
            split = list(os.path.splitext(bn))
            target_name = split[0] + "_" + str(ext) + split[1]
            target_file = target_dir + '/' + target_name
        return target_file

    def __trash_dir(self):
        return os.path.dirname(self.file_list[self.curr_index]) + '/FOTOSORT-TRASH'
