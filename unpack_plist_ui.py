# -*- coding: utf-8 -*-
import os
import sys
import mainui
from PIL import Image
from xml.etree import ElementTree

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *

class StartRun(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filename = ''

    def setFilename(self,filename= ''):
        self.filename = filename

    def tree_to_dict(self,tree):
        d = {}
        for index, item in enumerate(tree):
            if item.tag == 'key':
                if tree[index + 1].tag == 'string':
                    d[item.text] = tree[index + 1].text
                elif tree[index + 1].tag == 'true':
                    d[item.text] = True
                elif tree[index + 1].tag == 'false':
                    d[item.text] = False
                elif tree[index + 1].tag == 'integer':
                    d[item.text] = int(tree[index + 1].text);
                elif tree[index + 1].tag == 'dict':
                    d[item.text] = self.tree_to_dict(tree[index + 1])
        return d


    def frames_from_data(self,filename, ext):
        data_filename = filename + ext
        if ext == '.plist':
            root = ElementTree.fromstring(open(data_filename, 'r').read())
            plist_dict = self.tree_to_dict(root[0])
            to_list = lambda x: x.replace('{', '').replace('}', '').split(',')
            frames = plist_dict['frames'].items()
            for k, v in frames:
                frame = v
                if(plist_dict["metadata"]["format"] == 3):
                    frame['frame'] = frame['textureRect']
                    frame['rotated'] = frame['textureRotated']
                    frame['sourceSize'] = frame['spriteSourceSize']
                    frame['offset'] = frame['spriteOffset']

                rectlist = to_list(frame['frame'])
                width = int(float(rectlist[3] if frame['rotated'] else rectlist[2]))
                height = int(float(rectlist[2] if frame['rotated'] else rectlist[3]))
                frame['box'] = (
                    int(float(rectlist[0])),
                    int(float(rectlist[1])),
                    int(float(rectlist[0])) + width,
                    int(float(rectlist[1])) + height
                )
                real_rectlist = to_list(frame['sourceSize'])
                real_width = int(float(real_rectlist[1] if frame['rotated'] else real_rectlist[0]))
                real_height = int(float(real_rectlist[0] if frame['rotated'] else real_rectlist[1]))
                real_sizelist = [real_width, real_height]
                frame['real_sizelist'] = real_sizelist
                offsetlist = to_list(frame['offset'])
                offset_x = int(float(offsetlist[1] if frame['rotated'] else offsetlist[0]))
                offset_y = int(float(offsetlist[0] if frame['rotated'] else offsetlist[1]))

                if frame['rotated']:
                    frame['result_box'] = (
                        int(float((real_sizelist[0] - width) / 2 + offset_x)),
                        int(float((real_sizelist[1] - height) / 2 + offset_y)),
                        int(float((real_sizelist[0] + width) / 2 + offset_x)),
                        int(float((real_sizelist[1] + height) / 2 + offset_y))
                    )
                else:
                    frame['result_box'] = (
                        int(float((real_sizelist[0] - width) / 2 + offset_x)),
                        int(float((real_sizelist[1] - height) / 2 - offset_y)),
                        int(float((real_sizelist[0] + width) / 2 + offset_x)),
                        int(float((real_sizelist[1] + height) / 2 - offset_y))
                    )
            return frames

        else:
            print("Warning:Wrong data format on parsing: '" + ext + "'!")
            ui.outputWritten("Warning:Wrong data format on parsing: '" + ext + "'!\n")
            exit(1)


    def gen_png_from_data(self,filename, ext):
        ui.outputWritten("unpack start!\n")
        big_image = Image.open(filename + ".png")
        frames = self.frames_from_data(filename, ext)
        for k, v in frames:
            frame = v
            box = frame['box']
            rect_on_big = big_image.crop(box)
            real_sizelist = frame['real_sizelist']
            result_image = Image.new('RGBA', real_sizelist, (0, 0, 0, 0))
            result_box = frame['result_box']
            result_image.paste(rect_on_big, result_box, mask=0)
            if frame['rotated']:
                result_image = result_image.transpose(Image.ROTATE_90)
            if not os.path.isdir(filename):
                os.mkdir(filename)
            outfile = (filename + '/' + k).replace('gift_', '')
            if not outfile.endswith('.png'):
                outfile += '.png'
            print(outfile, "generated")
            ui.outputWritten(outfile+" generated\n")
            result_image.save(outfile)
        ui.outputWritten("unpack end!\n")

    def endWith(self,s,*endstring):
        array = map(s.endswith,endstring)
        if True in array:
            return True
        else:
            return False


    def get_sources_file(self,filename,ext):
        data_filename = filename + ext
        png_filename = filename + '.png'
        if os.path.exists(data_filename) and os.path.exists(png_filename):
            self.gen_png_from_data(filename, ext)
        else:
            print("Warning:Make sure you have both " + data_filename + " and " + png_filename + " files in the same directory")
            ui.outputWritten("Warning:Make sure you have both " + data_filename + " and " + png_filename + " files in the same directory\n")

    def run(self):
        if self.filename == '':
            ui.outputWritten("Warning:请选择文件！\n")
            return
        # filename = sys.argv[1]
        path_or_name = self.filename.split('.')[0]
        ext = '.plist'
        self.get_sources_file(path_or_name,ext)

def start_run(filename):
    start_run_thread.setFilename(filename)
    start_run_thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = mainui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.btn_input.clicked.connect(ui.choose_png_file)
    ui.btn_output.clicked.connect(lambda:start_run(ui.lineEdit.text()))
    start_run_thread = StartRun()
    MainWindow.show()
    sys.exit(app.exec_())

