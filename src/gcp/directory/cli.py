import click
from gcp.directory.api import DirectoryAPI, PosixAccount, SSHPublicKey
from gcp.ssh.generator import Generator


@click.group()
def directory() -> None:
    pass


@directory.command()
def list() -> None:
    api = DirectoryAPI()

    users = api.list_users()

    for user in users:
        print(user)


@directory.command()
@click.option('--user-keys', '-c', help='Comma separated user emails', type=str, required=True)
@click.option('--start-uid', '-c', help='UID to start from', type=int, required=True)
@click.option('--gid', '-c', help='GID of a primary group all users will belong to', type=int, required=True)
def create_posix_accounts(user_keys: str, start_uid: int, gid: int) -> None:
    user_keys = user_keys.split(',')
    generator = Generator()
    api = DirectoryAPI()
    uid = start_uid

    for user_key in user_keys:
        user_key = user_key.strip()
        username = api.generate_posix_username(user_key)
        posix_account = PosixAccount(
            username=username,
            uid=str(uid),
            gid=str(gid),
            homeDirectory=f'/home/{username}',
            shell=None,
            gecos=None,
            systemId='',
            primary=True,
            accountId=None,
            operatingSystemType='linux'
        )

        uid += 1

        key_pair = generator.generate_key_pair()
        ssh_key = SSHPublicKey(
            expirationTimeUsec=None,
            fingerprint=key_pair.fingerprint,
            key=key_pair.public_key
        )

        api.set_posix_account(user_key, posix_account)
        api.set_ssh_key(user_key, ssh_key)

        print(
            f'User: {user_key}.\n'
            f'Passphrase: {key_pair.passphrase}.\n'
            f'Public key: {key_pair.public_key}.\n'
            f'Private key: \n{key_pair.private_key}\n')

