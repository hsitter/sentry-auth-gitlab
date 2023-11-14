from sentry.auth.view import AuthView

from .client import GitLabClient
from .constants import GROUPS
class FetchUser(AuthView):
    def handle(self, request, helper):
        with GitLabClient(helper.fetch_state('data')['access_token']) as client:
            user = client.get_user()

            if GROUPS and not any(group in user['groups'] for group in GROUPS):
                return helper.error(f'Only members of {GROUPS} are allowed to log in. If you are a Qt developer you can request access in a KDE sysadmin ticket — https://go.kde.org/systickets . Your groups are {user["groups"]}')

            helper.bind_state('user', user)
            return helper.next_step()
