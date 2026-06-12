import aiohttp
import asyncio

# ==========================
# CUSTOM EXCEPTIONS
# ==========================

class APIError(Exception):
    pass

class NotFoundError(APIError):
    pass

class RateLimitError(APIError):
    pass


# ==========================
# GITHUB API CLIENT
# ==========================

class GitHubAPI:

    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    # -----------------------
    # Internal Request Method
    # -----------------------
    async def _request(self, endpoint):

        url = f"{self.BASE_URL}/{endpoint}"

        async with self.session.get(url) as response:

            if response.status == 404:
                raise NotFoundError("Resource not found")

            if response.status == 403:
                raise RateLimitError("Rate limit exceeded")

            if response.status >= 400:
                raise APIError(
                    f"GitHub API Error: {response.status}"
                )

            return await response.json()

    # -----------------------
    # Get User Information
    # -----------------------
    async def get_user(self, username):

        return await self._request(
            f"users/{username}"
        )

    # -----------------------
    # Get Repositories
    # -----------------------
    async def get_repositories(self, username):

        return await self._request(
            f"users/{username}/repos"
        )


# ==========================
# MAIN PROGRAM
# ==========================

async def main():

    username = input(
        "Enter GitHub Username: "
    )

    async with GitHubAPI() as api:

        try:

            user = await api.get_user(
                username
            )

            print("\nUSER DETAILS")
            print("-" * 30)

            print("Name:",
                  user.get("name"))

            print("Followers:",
                  user.get("followers"))

            print("Public Repos:",
                  user.get("public_repos"))

            print("\nREPOSITORIES")
            print("-" * 30)

            repos = await api.get_repositories(
                username
            )

            for repo in repos[:10]:

                print(repo["name"])

        except Exception as e:

            print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())