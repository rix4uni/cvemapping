IMG = vim-cve-2019-12735

.PHONY: build run stop attach root

build:
	docker build -t $(IMG) .

run:
	docker run --rm -v $(CURDIR):/pwd --cap-add=SYS_PTRACE --security-opt \
		seccomp=unconfined -d --name $(IMG) -i $(IMG)

stop:
	docker stop $(IMG)

attach:
	docker exec -it $(IMG) /bin/bash

root:
	docker exec -u root -it $(IMG) /bin/bash
