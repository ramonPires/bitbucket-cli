format:
	@poetry run black bitbucketcli/ tests/

run-test-coverage:
	@pytest --cov=bibucketcli tests/

run-tests:
	@pytest tests/
