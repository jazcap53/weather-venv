import sys

if __name__ == '__main__':
    print(sys.argv[0])
    print(sys.executable)
    if 'pypoetry' in sys.executable:
        print('This program was run using poetry')
    else:
        print('nope')
