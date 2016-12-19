include resources/Makefile

# Override pycodestyle target
pycodestyle:
	@find $(CURDIR)/appengine_fixture_loader/ -name '*.py' -exec pycodestyle {} \;
	@find $(CURDIR)/tests/ -name '*.py' -exec pycodestyle {} \;

# The same for pyflakes
pyflakes:
	@find $(CURDIR)/appengine_fixture_loader/ -name '*.py' -exec pyflakes {} \;
	@find $(CURDIR)/tests/ -name '*.py' -exec pyflakes {} \;

package:
	@.env/bin/python2.7 setup.py sdist bdist

upload: clean
	@.env/bin/python2.7 setup.py sdist bdist upload -r pypi

# Overriding TravisCI
travis: venv package
	@.env/bin/coverage run --source=appengine_fixture_loader setup.py test

clean:
	@rm -f dist/*
