import os
from PIL import Image
if not os.path.exists('res'):
    os.mkdir('res')
f = os.listdir('.')
def cmp(a, b):
    try:
        a0 = int(a.split('.')[0][1:])
        b0 = int(b.split('.')[0][1:])
        return a0 > b0
    except:
        return a > b
f.sort(cmp=cmp)
c = 0
for i in f:
    if i.find('.png') != -1 and i.find('_') == -1:
        #im = Image.open(i)
        print i
        os.system('cp "%s" res/cat_[ID]_[DIR]_%d.png' % (i, c))
        c = c+1
