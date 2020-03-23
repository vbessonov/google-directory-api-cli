import dataclasses
import json
import os.path
import pickle
from dataclasses import dataclass
from typing import Optional, List

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource


@dataclass
class PosixAccount:
    username: str
    uid: str
    gid: str
    homeDirectory: str
    shell: str
    gecos: str
    systemId: str
    primary: bool
    accountId: str
    operatingSystemType: str


@dataclass
class SSHPublicKey:
    expirationTimeUsec: int
    fingerprint: str
    key: str


class DirectoryAPI:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

    def __init__(self) -> None:
        self._service_instance: Optional[Resource] = None

    def _create_service(self) -> Resource:
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('admin', 'directory_v1', credentials=creds)

        return service

    @property
    def _service(self) -> Resource:
        if not self._service_instance:
            self._service_instance = self._create_service()

        return self._service_instance

    def list_users(self) -> List[Resource]:
        results = self._service\
            .users()\
            .list(
                customer='my_customer',
                maxResults=10,
                orderBy='email')\
            .execute()
        users = results.get('users', [])

        return users

    def update_user(self, user_key: str, body: str) -> None:
        self._service\
            .users()\
            .update(
                userKey=user_key,
                body=body
            )\
            .execute()

    def set_ssh_key(self, user_key: str, key: SSHPublicKey) -> None:
        self.update_user(user_key, json.dumps({'sshPublicKeys': None}))
        self.update_user(user_key, json.dumps({'sshPublicKeys': [json.dumps(dataclasses.asdict(key))]}))

    def set_posix_account(self, user_key: str, account: PosixAccount) -> None:
        self.update_user(user_key, json.dumps({'posixAccounts': None}))
        self.update_user(user_key, json.dumps({'posixAccounts': [json.dumps(dataclasses.asdict(account))]}))

    @staticmethod
    def generate_posix_username(user_key: str) -> str:
        posix_username = user_key
        at_index = user_key.index('@')

        if at_index:
            posix_username = user_key[0:at_index]

        posix_username = posix_username.replace('.', '_')

        return posix_username
