include resources/Makefile

# Override pep8 target
pep8:
	find $(CURDIR)/appengine_fixture_loader/ -name '*.py' -exec pep8 {} \;
	find $(CURDIR)/tests/ -name '*.py' -exec pep8 {} \;

# The same for pyflakes
pyflakes:
	find $(CURDIR)/appengine_fixture_loader/ -name '*.py' -exec pyflakes {} \;
	find $(CURDIR)/tests/ -name '*.py' -exec pyflakes {} \;
