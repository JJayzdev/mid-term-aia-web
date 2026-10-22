"""Publish an already-verified static build using the user's existing Git login.

Credentials are obtained from Git Credential Manager in memory, never logged or
written to disk. No source PDFs, OCR cache, or environment files are uploaded.
Run --check for a read-only account/repository check. Publishing is explicit.
"""
import argparse
import json
import subprocess
import shutil
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def credential():
    result = subprocess.run(
        ['git', 'credential-manager', 'get'],
        input='protocol=https\nhost=github.com\n\n',
        text=True, capture_output=True, check=False,
        env={**__import__('os').environ, 'GCM_INTERACTIVE': 'never'},
    )
    if result.returncode:
        raise RuntimeError('Cannot access an existing GitHub login. Sign in using Git Credential Manager.')
    values = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    token = values.get('password')
    if not token:
        raise RuntimeError('No GitHub credential was returned.')
    return token


def api(token, endpoint, method='GET', payload=None, allow404=False):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request('https://api.github.com' + endpoint, data=data, method=method,
        headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json',
                 'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'aia-study-deployer',
                 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        if exc.code == 404 and allow404:
            return None
        # Do not print request headers or credential material.
        raise RuntimeError('GitHub API returned HTTP %s for %s %s' % (exc.code, method, endpoint)) from None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', default='mid-term-aia-web')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--status', action='store_true')
    args = parser.parse_args()
    if sum([args.check, args.publish, args.status]) != 1:
        parser.error('Choose exactly one: --check, --publish, --status.')
    token = credential()
    account = api(token, '/user')['login']
    repo = api(token, '/repos/%s/%s' % (account, args.repo), allow404=True)
    endpoint = '/repos/%s/%s' % (account, args.repo)
    if args.check:
        print(json.dumps({'account': account, 'repository': args.repo, 'exists': repo is not None,
                          'repository_url': repo.get('html_url') if repo else None}, ensure_ascii=True))
        return
    if args.status:
        pages = api(token, endpoint + '/pages', allow404=True)
        build = api(token, endpoint + '/pages/builds/latest', allow404=True)
        print(json.dumps({'url': pages.get('html_url') if pages else None,
                          'status': pages.get('status') if pages else None,
                          'build': build.get('status') if build else None,
                          'error': build.get('error') if build else None}, ensure_ascii=True))
        return
    def git(*argv, cwd=ROOT, capture=False):
        result = subprocess.run(['git', *argv], cwd=cwd, text=True,
                                capture_output=capture, check=True)
        return result.stdout.strip() if capture else None
    if git('status', '--porcelain', capture=True):
        raise RuntimeError('Commit the reviewed source before publishing.')
    if git('branch', '--show-current', capture=True) != 'main':
        raise RuntimeError('Publish from the main branch.')
    dist = ROOT / 'dist'
    if not (dist / 'index.html').is_file() or not (dist / 'data/bank.json').is_file():
        raise RuntimeError('Run release validation, tests, and npm run build first.')
    forbidden = [p for p in dist.rglob('*') if p.is_file() and (p.suffix.lower() in {'.pdf', '.pptx', '.env'} or p.name.startswith('.env'))]
    if forbidden:
        raise RuntimeError('Unexpected source/secret file in static build.')
    remote = 'https://github.com/%s/%s.git' % (account, args.repo)
    remotes = git('remote', capture=True).splitlines()
    if 'origin' in remotes and git('remote', 'get-url', 'origin', capture=True) != remote:
        raise RuntimeError('Existing origin does not match the destination repository.')
    if repo is not None and 'origin' not in remotes:
        raise RuntimeError('Destination exists but is not the checkout origin; refusing to overwrite.')
    if repo is None:
        repo = api(token, '/user/repos', 'POST', {'name': args.repo, 'private': False,
            'description': 'Vietnamese AIA study and practice exam app with source-reviewed questions',
            'auto_init': False, 'has_wiki': False})
    if 'origin' not in remotes:
        git('remote', 'add', 'origin', remote)
    git('push', '-u', 'origin', 'main')
    temporary_root = ROOT / 'tmp'
    temporary_root.mkdir(exist_ok=True)
    deploy_dir = Path(tempfile.mkdtemp(prefix='pages-', dir=temporary_root))
    if git('ls-remote', '--heads', 'origin', 'gh-pages', capture=True):
        git('clone', '--single-branch', '--branch', 'gh-pages', remote, str(deploy_dir))
        git('rm', '-r', '--ignore-unmatch', '.', cwd=deploy_dir)
    else:
        git('init', '-b', 'gh-pages', cwd=deploy_dir)
        git('remote', 'add', 'origin', remote, cwd=deploy_dir)
    shutil.copytree(dist, deploy_dir, dirs_exist_ok=True)
    (deploy_dir / '.nojekyll').write_text('', encoding='utf-8')
    git('add', '.', cwd=deploy_dir)
    source_commit = git('rev-parse', 'HEAD', capture=True)
    if git('status', '--porcelain', cwd=deploy_dir, capture=True):
        git('commit', '-m', 'Deploy reviewed static release ' + source_commit[:12], cwd=deploy_dir)
        git('push', '-u', 'origin', 'gh-pages', cwd=deploy_dir)
    pages = api(token, endpoint + '/pages', allow404=True)
    if pages is None:
        pages = api(token, endpoint + '/pages', 'POST', {'build_type': 'legacy', 'source': {'branch': 'gh-pages', 'path': '/'}})
    elif pages.get('source') != {'branch': 'gh-pages', 'path': '/'}:
        raise RuntimeError('Pages already uses another source; deployment branch pushed but settings unchanged.')
    result = {'repository': repo['html_url'], 'url': pages.get('html_url'),
              'source_commit': source_commit, 'pages_commit': git('rev-parse', 'HEAD', cwd=deploy_dir, capture=True)}
    (temporary_root / 'deployment.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=True))


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as exc:
        raise SystemExit(str(exc))
