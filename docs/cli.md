# CLI

## Init
Initializes envadmin git repository.

```python
envadmin init -p /path/to/repo -e my@email.com
```

Options:
 -  -p, --path PATH         git repo to store environment variables.  [required]
 -  -c, --config-path PATH  Folder to create .envadmin file.
 -  -e, --gpg-email TEXT    E-mail of gpg key to use for encrypting git repo.
 -  --push / --no-push      Don't persist changes to remote git.
 -  --help                  Show this message and exit.
