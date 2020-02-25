run:
ifdef VIRTUAL_ENV
	@python -B main.py
else
	@python3.8 -B main.py
endif

install:
ifdef VIRTUAL_ENV
	@pip install --upgrade pip
	@pip install -r requirements.txt
else
	@echo "You are not in a virtual environment!!"
	@echo "All the requirements will be installed directly on the system."
	@echo "Press Ctrl+C to cancel or wait 10 seconds..."
	@sleep 10
	@pip3 install --upgrade pip
	@pip3 install -r requirements.txt
endif

style_tests:
	@pycodestyle --exclude=env,tests .

tests:
ifdef VIRTUAL_ENV
	@python -m pytest -v -p no:warnings
else
	@python3.8 -m pytest -v -p no:warnings
endif

.PHONY: install style_tests tests run
