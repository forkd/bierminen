.PHONY: clean

version := $(shell egrep -o '[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}' setup.py)

pypi:
	@pandoc --from=markdown --to=rst README.md --output=README.rst
	@python3 setup.py register -r pypi
	@python3 setup.py sdist upload -r pypi
	@git tag $(version)
	@git push --tags

clean:
	@rm -rf *rst dist build *egg-info
