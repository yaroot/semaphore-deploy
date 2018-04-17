all: build

clean:
	rm -rf *.pex

build: clean
	pex . -r requirements.txt -m semaphore_deploy -o semaphore.pex --disable-cache

.PHONY: build
