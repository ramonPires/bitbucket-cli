# Setup:
The project uses [poetry](https://python-poetry.org) to manage dependencies, so you will need to install poetry and then run the command `poetry install` to install all required dependencies.

The project use the `dotenv` to load some variables, so there is a file called `.env.sample`, rename the file to `.env`
and automatically, when you run the project, the variables will be loaded as environment variables. Two variables require
some attention, `BITBUCKET_OAUTH_CONSUMER_KEY` and `BITBUCKET_OAUTH_CONSUMER_SECRET`, to fill the values, you will need to create
a new workspace consumer to allow the cli tool to access bitbucket cloud api using OAuth authentication .
You can find more details [here](https://support.atlassian.com/bitbucket-cloud/docs/use-oauth-on-bitbucket-cloud/) on how to create a new workspace consumer.


# Running:
In the root of the project, there is a file `bibucket-cli`, you will use this file to run the cli tool, to run the cli you will execute this command `./bitbucket-cli` and then you will see an output like this:
```bash
$ ./bitbucket-cli
Usage: bitbucket-cli [OPTIONS] COMMAND [ARGS]...

  A command line tool to access bitbucket cloud functionalities.

Options:
  --help  Show this message and exit.

Commands:
  add-user-to-repository          Add the user to a repository. An email with
                                  the invite will be sent to the user by
                                  default.
  create-project                  Create a new project in a specific
                                  workspace.
  create-repository               Create a new repository in a specific
                                  project.
  enable-bypass-branch-pull-request
                                  Enable users to use push force in a branch.
  remove-user-from-group          Remove a user from a group in a workspace.
  remove-user-from-repository     Remove a user from a repository.

```

## Commands:
- `add-user-to-repository`:
Provide a way to give access to a repository for a user with a bitbucket cloud account, as you can see here:
```bash
$ ./bitbucket-cli add-user-to-repository --help
Usage: bitbucket-cli add-user-to-repository [OPTIONS]

Options:
  --workspace TEXT                Workspace name where the repository belongs
  --email TEXT                    User email
  --repository TEXT               Repository name
  --permission [read|write|admin]
                                  Permission of the user inside of the
                                  repository
  --help                          Show this message and exit.
```
- `create-project`:
Provide a way to create a project inside a workspace in a bitbucket cloud account, as you can see here:
```bash
$ ./bitbucket-cli add-user-to-repository --help
Usage: bitbucket-cli add-user-to-repository [OPTIONS]

Options:
  --workspace TEXT                Workspace name where the repository belongs
  --email TEXT                    User email
  --repository TEXT               Repository name
  --permission [read|write|admin]
                                  Permission of the user inside of the
                                  repository
  --help                          Show this message and exit.
```
- `create-repository`:
Provide a way to create a repository inside a workspace in a bitbucket cloud account, as you can see here:
```bash
$ ./bitbucket-cli create-repository --help
Usage: bitbucket-cli create-repository [OPTIONS]

  Create a new repository in a specific project.

Options:
  --workspace TEXT      Workspace name where the project belongs
  --name TEXT           Project name
  --project-key TEXT    Project key
  --private / --public  [default: private]
  --help                Show this message and exit.
```
- `remove-user-from-group`:
Provide a way to remove a user from a group, as you can see here:
```bash
./bitbucket-cli remove-user-from-group --help
Usage: bitbucket-cli remove-user-from-group [OPTIONS]

Options:
  --workspace TEXT   Workspace name where the user group belongs
  --account-id TEXT  Account ID - You can obtain your account id here:
                     https://id.atlassian.com/gateway/api/me
  --group TEXT       Group name
  --help             Show this message and exit.
```
- `remove-user-from-repository`:
Provide a way to remove a user from a repository, as you can see here:
```bash
 ./bitbucket-cli remove-user-from-repository --help
Usage: bitbucket-cli remove-user-from-repository [OPTIONS]

Options:
  --workspace TEXT   Workspace name where the repository belongs
  --account-id TEXT  Account ID - You can obtain your account id here:
                     https://id.atlassian.com/gateway/api/me
  --repository TEXT  Repository name
  --help             Show this message and exit.
```


**OBS:
The project relies on some Bitbucket Cloud internal and some almost deprecated APIs due to some GDPR concerns of the Bitbucket Cloud team, like exposing the username or email through the API, some endpoints don't work with the OAuth yet, so some endpoints were not used due to this limitation.**
- https://developer.atlassian.com/cloud/bitbucket/deprecation-notice-v1-apis/
- https://developer.atlassian.com/cloud/bitbucket/bitbucket-api-changes-gdpr/
