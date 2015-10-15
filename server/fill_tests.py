import os

files = []
for dirname, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        if (filename.endswith('.py') and
                not dirname.startswith('./test') and
                'simulation' not in dirname and
                '/' in dirname):
            files.append(os.path.join(dirname, filename))

for f in files:
    testname = f.replace('./', 'test_').replace('/', '_')

    try:
        open('./test/' + testname)
    except:
        open('./test/' + testname, 'w')
