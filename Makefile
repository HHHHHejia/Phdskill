.PHONY: init status validate lock test stage0 stage1 stage2 stage3 stage4 stage5 stage6 stage7 stage8

init:
	python scripts/init_project.py

status:
	python scripts/status.py

validate:
	python scripts/validate_stage.py

lock:
	python scripts/lock_stage.py

stage0:
	python scripts/run_stage.py 0

stage1:
	python scripts/run_stage.py 1

stage2:
	python scripts/run_stage.py 2

stage3:
	python scripts/run_stage.py 3

stage4:
	python scripts/run_stage.py 4

stage5:
	python scripts/run_stage.py 5

stage6:
	python scripts/run_stage.py 6

stage7:
	python scripts/run_stage.py 7

stage8:
	python scripts/run_stage.py 8

test:
	python -m pytest -q
