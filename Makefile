# ------------------------------------------------------------------------------
# Copyright 2020 Mike Pawlowski
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

.PHONY: help outdated install lint build
.DEFAULT: help

define HELP_CONTENT

Usage:

make [task [task ...]]

Available Tasks:

- help
- outdated
- install
- lint
- build

endef
export HELP_CONTENT

help:
	@echo "$$HELP_CONTENT"

outdated:
	@echo "[outdated]"
	python -m pip list --outdated

install:
	@echo "[install]"
	python -m pip install -r requirements.txt

lint:
	@echo "[lint]"
	python -m pylint lib index.py

build: lint
	@echo "[build]"
