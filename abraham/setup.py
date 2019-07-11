__EXTERNAL_REPOS_ROOT__ = None
__EXTERNAL_REPOS__ = {}


def set_external_repos_root(path):
    global __EXTERNAL_REPOS_ROOT__
    __EXTERNAL_REPOS_ROOT__ = path
    set_external_repo_dir('neural-style', '%s/neural-style' % __EXTERNAL_REPOS_ROOT__, overwrite=False)
    set_external_repo_dir('deeplab-pytorch', '%s/deeplab-pytorch' % __EXTERNAL_REPOS_ROOT__, overwrite=False)
    set_external_repo_dir('spade', '%s/SPADE' % __EXTERNAL_REPOS_ROOT__, overwrite=False)
    set_external_repo_dir('stylegan', '%s/stylegan' % __EXTERNAL_REPOS_ROOT__, overwrite=False)
    
    
def get_external_repos_root():
    global __EXTERNAL_REPOS_ROOT__
    return __EXTERNAL_REPOS_ROOT__


def set_external_repo_dir(repo, path, overwrite=False):
    global __EXTERNAL_REPOS__
    if overwrite or repo not in __EXTERNAL_REPOS__:
        __EXTERNAL_REPOS__[repo] = path


def get_external_repo_dir(repo):
    global __EXTERNAL_REPOS__
    if repo in __EXTERNAL_REPOS__:
        return __EXTERNAL_REPOS__[repo]
    else:
        raise RuntimeError("Repo %s path has not been set! Must set manually using abraham.setup.set_external_repo_dir" % repo)
        