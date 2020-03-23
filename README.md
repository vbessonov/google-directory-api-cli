# google-directory-api-cli
CLI tool automating administrative tasks in GCP like creating POSIX users and managing their SSH keys.

## Usage
To set up users POSIX accounts and accompanying SSH keys run the following command: 
```bash
python -m gcp directory create_posix_accounts \
    --user-keys="user1@example.com, user2@example.com, user3@example.com" \
    --start-uid=10001
    --gid=10000
```

It will print the created keys and passphrases.
