import asyncio
import json
import os
from json import dumps
from pathlib import Path
import zmq
import git
from flask import Flask

GIT_ROOT_DIR = os.environ['git.RootDir']
URL = os.environ['zmq.SocketUrl']

assert GIT_ROOT_DIR

cache = {}


def getRepo(dir):
    dir = os.path.join(GIT_ROOT_DIR, dir)
    return git.Repo(dir)


def getDirectorySize(dir):
    root_directory = Path(dir)
    return sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())


def struct():
    fo = os.listdir(GIT_ROOT_DIR)
    res = {}
    for dir in fo:

        if not dir.startswith(".") :

            try:
                repo = getRepo(dir)
                commit = repo.head.object
                if not "dir" in res:
                    res[dir] = {}
                res[dir]['size'] = getDirectorySize(os.path.join(GIT_ROOT_DIR, dir))
                res[dir]['commitDate'] = commit.committed_date
                res[dir]['commitHash'] = commit.hexsha
                res[dir]['ci'] = fileInRepo(repo, "cic")
                tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)

                stringTags = []
                for tag in tags:
                    stringTags.append(tag.name)

                res[dir]['tags'] = stringTags
                print(stringTags)
            except Exception as e:
                print("Error error load dir (" + dir + "): " + str(e))

    return res


def fileInRepo(repo, filePath):
    pathdir = os.path.dirname(filePath)
    rsub = repo.head.commit.tree

    for path_element in pathdir.split(os.path.sep):
        try:
            rsub = rsub[path_element]
        except KeyError:
            return False

    return filePath in rsub


async def update_cache_func():
    print("Update cache start")
    global cache
    cache = struct()

    print("CACHE  STATE", cache)


def index(params: map):
    return dumps(os.listdir(GIT_ROOT_DIR))


def decode():
    cache


def init_repo(params: map):
    repo = git.Repo.init(os.path.join(GIT_ROOT_DIR, params['name']), bare=True)
    assert repo
    return dumps({"result": "created"})


def list_wide(params: map):
    return dumps(cache)


def update_cache(params: map):
    asyncio.run(update_cache_func())
    return dumps(cache)


def getTag(dir):
    repo = git.Repo(dir)
    repo.tags


requests = {}

requests['updateRepoCache'] = update_cache
requests['repositoriesListWide'] = list_wide
requests['repositoriesList'] = index
requests['repositoryInit'] = init_repo


def messageProcessing(message):
    print("MESSAGE ", len(message))
    user = message[6:8]
    header = message[:6]
    body = message[8:]
    decode = body.decode("utf-8")
    print("MESSAGE ", decode)
    dictData = json.loads(decode)
    func = requests[dictData['type']]
    params = dictData['params']
    res = func(params)
    print("RES ", res)
    return header + res.encode('utf-8')


def server(url):
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    print("START SERVER ", url)
    socket.bind(url)

    while True:
        body = socket.recv()
        result = messageProcessing(body)
        print("FOR SEND ", result)

        socket.send(result)


app = Flask(__name__)


@app.route('/')
def index():
    return 'Server Works!'


@app.route('/greet')
def say_hello():
    return 'Hello from Server'


if __name__ == '__main__':
    asyncio.run(update_cache_func())
    server(URL)
