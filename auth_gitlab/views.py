from sentry.auth.view import AuthView

from .client import GitLabClient
from .constants import GROUP
class FetchUser(AuthView):
    def handle(self, request, helper):
        with GitLabClient(helper.fetch_state('data')['access_token']) as client:
            user = client.get_user()

            if GROUP and (not GROUP in user['groups']):
                return helper.error(f'Only members of {GROUP} are allowed to log in')

            helper.bind_state('user', user)
            return helper.next_step()
