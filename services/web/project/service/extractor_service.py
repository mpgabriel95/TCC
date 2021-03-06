from . import github_pull_request_extrator_service as pulls_service
from ..repository import github_repository_repository as repo_repository
from ..repository import github_user_repository as user_repository
from . import github_instance_service


def extract(user_name, steps):
    steps = int(steps)
    current_step = 1
    extract_from_user(user_name, current_step, steps)

def extract_from_user(user_name, current_step, steps):
    extract_pulls(user_name)
    extract_users(user_name)
    user_repository.set_extracted(user_name)

    current_step = current_step + 1
    if steps >= current_step:
        extract_next_step(user_name, current_step, steps)
    user_repository.set_extracted(user_name)

def extract_next_step(user_name, current_step, steps):
    neighbors = user_repository.get_non_extracted_neighbors(user_name)
    for n in neighbors:
        extract_from_user(n.login , current_step, steps)

def extract_pulls(user_name):
    print('Extracting pulls from user ' + user_name)
    save_pulls_from_issues( pulls_service.get_pulls_by_user_name(user_name))

def extract_users(user_name):
    repos = repo_repository.get_repos_by_user(user_name)
    print("Extracting pulls from " + str( len( repos ) ) + " repos")
    for r in repos: ## TODO extract only non extracted repos
        if( not repo_repository.is_extracted(r.github_id) ):
            print('Extracting pulls from repo ' + r.full_name)
            pull_issues = pulls_service.get_pulls_by_repo_full_name(r.full_name, user_name)
            save_pulls_from_issues(pull_issues)
            repo_repository.set_extracted(r.github_id)

def save_pulls_from_issues(pull_issues):
    try:
        print("Number of issues: " + str(pull_issues.totalCount))
        for issue in pull_issues:
            handle_requester(pull_issues)
            pulls_service.save_from_issue(issue)
    except:
        print('Error getting pull from issue')

def handle_requester(issues):
    current_requester = issues._PaginatedList__requester
    rate_limit = current_requester.rate_limiting
    if rate_limit[1] == 5000 and rate_limit[0] <= 300:
        g = github_instance_service.get_new_instance()
        issues._PaginatedList__requester =  g._Github__requester
