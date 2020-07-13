# GitHub Search

A Python application that searches for code in GitHub repositories based on a user-defined queries.

## (1) Setup

```shell
make install
```

## (2) Usage

```shell
$ python index.py --help
usage: index.py [-h] -q QUERY [-o {github.ibm.com,api.github.com}] [-d]

A Python application that searches for code in GitHub repositories based on a user-defined queries.

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        A user-defined GitHub query.
  -o {github.ibm.com,api.github.com}, --hostname {github.ibm.com,api.github.com}
                        The target GitHub API domain. Default: github.ibm.com.
  -d, --debug           Enable debug mode. Default: False.

=== Documentation ===

https://docs.github.com/en/github/searching-for-information-on-github/searching-code

=== Environment Variables ===

GITHUB_ACCESS_TOKEN : A personal access token with the "repo" scope selected.

=== Examples ===

export GITHUB_ACCESS_TOKEN=cabfe35410755fbb6c281e92902ed122144886c5

python index.py -q "org:dap path:/ filename:package.json request"
python index.py -q "org:dap filename:deploy.properties k8s_yp_prod_eu_de_STAGE"
python index.py -q "org:dap org:data-platform path:/ filename:package.json lodash"
```

## (3) Documentation

- [Searching code on GitHub](https://docs.github.com/en/github/searching-for-information-on-github/searching-code)
