#coding:utf8
import os
import sys
import subprocess

if len(sys.argv) < 2:
    print "input cat id"
    exit()
idd = int(sys.argv[1])

#cd = [u'蹦出来-黑边', u'Walk-1黑边',  u'Walk-3黑边', ]
cd = [u'蹦出来黑边', u'Walk1黑边',  u'Walk3黑边', ]
f = os.listdir('.')
findBen = False
for i in f:
    if i.find((u'蹦').encode('gbk')) != -1:
        cd[0] = i.decode('gbk')
        findBen = True
    elif i.find('1') != -1:
        cd[1] = i.decode('gbk')
    elif i.find('3') != -1:
        cd[2] = i.decode('gbk')
print "findBen", findBen

for i in cd:
    print i

ed = ['jump', 'rb',  'rt', ]
k = 0
for k in xrange(0, len(cd)):
    #cmd = 'mv %s %s' % (cd[k].encode('utf8'), ed[k].encode('utf8'))
    #print cmd
    #os.system(cmd)
    print cd[k]
    subprocess.call(['mv', cd[k].encode('gbk'), ed[k].encode('gbk')])

con = open('name.py')
con = con.read()



#['lb', 'lt', 'rb', 'rt']
os.system('mkdir jumpRes')
os.system('mkdir res')

d = ed[:1]
for k in d:
    #os.system('cp %s/res/* res'%(k))
    nc = con.replace('[ID]', str(idd)).replace('[DIR]', k)
    nf = open('%s/name.py'%(k), 'w')
    nf.write(nc)
    nf.close()
    os.chdir(k)
    os.system('python name.py')
    os.system('cp res/* ../jumpRes ')
    os.chdir('..')

d = ed[1:]
for k in d:
    #os.system('cp %s/res/* res'%(k))
    nc = con.replace('[ID]', str(idd)).replace('[DIR]', k)
    nf = open('%s/name.py'%(k), 'w')
    nf.write(nc)
    nf.close()
    os.chdir(k)
    os.system('python name.py')
    os.system('cp  res/* ../res')
    os.chdir('..')


os.system('mkdir result')
TPCommand = "G:/texturepacker/bin/TexturePacker"
cmd = TPCommand + " --smart-update --format cocos2d --data %s\\%s.plist --sheet %s\\%s.png --dither-none-nn --opt RGBA4444 --trim --disable-rotation --scale %f %s" % ('result', 'cat_%d_jump'%(idd), 'result', 'cat_%d_jump'%(idd), 0.64, 'jumpRes')

print cmd
os.system(cmd)


cmd = TPCommand + " --smart-update --format cocos2d --data %s\\%s.plist --sheet %s\\%s.png --dither-none-nn --opt RGBA4444 --trim --disable-rotation --scale %f %s" % ('result', 'cat_%d_walk'%(idd), 'result', 'cat_%d_walk'%(idd), 0.64, 'res')

print cmd
os.system(cmd)
