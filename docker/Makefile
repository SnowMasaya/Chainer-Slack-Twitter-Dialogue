# Original Author: Adam Hawkins
# Original Source: https://github.com/ahawkins/project-template
# See doc/RATIONAL.md for information
# Feel free to modify this file but do not remove this comment.

sha1=$(shell echo $(1) | sha1sum | cut -d ' ' -f 1)

# Define dependent images in this variable. pull, import, and export
# targets will be created for each. A global pull, import, and export
# task will be created to operate on the list.
# NOTE: relevant changes should be synced to fig.yml
DOCKER_IMAGES:=centos:7

# Template defining tasks to pull, export, and import an image. This
# These tasks use work arounds to ensure tasks around the dependent
# images are not executed more than once. This template is evaluated
# for each images. Every image name is hashed. This is an artifact
# name. The pull task creates an artfact. Other targets can use this
# artifact as dependency. Export depends on pull, and import depends
# on export. The clean target deletes these artifacts. Note that this
# template is used with eval so things are expanded twice. ":"
# characters are replaced with _ in image names so they become
# proper task names. Given an image "a" and it's sha "b" the following
# tasks are generated:
#
# tmp/images/b 		 	# pull the image and create the artifact
# pull/a 						# helper target depending on the previous
# tmp/images/b.tar  # generate a tar export
# export/a:					# helper taget depending on the previous
# import/a: 				# import a using the tar export

define IMAGE_template
tmp/images/$(call sha1,$(1)):
	docker pull $(1)
	mkdir -p $$(@D)
	docker images -q $(1) > $$@

pull/$(subst :,_,$(1)): tmp/images/$(call sha1,$(1))

tmp/images/$(call sha1,$(1)).tar: tmp/images/$(call sha1,$(1))
	docker save -o $$@ $(1)

export/$(subst :,_,$(1)): tmp/images/$(call sha1,$(1)).tar

import/$(subst :,_,$(1)): tmp/images/$(call sha1,$(1)).tar
	docker load -i $$<

.PHONY: import/$(subst :,_,$(1))
endef

$(foreach image,$(DOCKER_IMAGES),$(eval $(call IMAGE_template,$(image))))

PULL_DOCKER_IMAGES:=$(addprefix pull/,$(subst :,_,$(DOCKER_IMAGES)))
EXPORT_DOCKER_IMAGES:=$(addprefix export/,$(subst :,_,$(DOCKER_IMAGES)))
IMPORT_DOCKER_IMAGES:=$(addprefix import/,$(subst :,_,$(DOCKER_IMAGES)))

pull: $(PULL_DOCKER_IMAGES)
export: $(EXPORT_DOCKER_IMAGES)
import: $(IMPORT_DOCKER_IMAGES)

# TODO: set this to your poject name. Use _ instead of -. This
# variable is used to namespace fig and for pushing images.
REPO_NAME=docker_common
DOCKER_COMPOSE=docker-compose
TAG=$(shell echo $$CIRCLE_SHA1 | cut -c 1-7)

.DEFAULT_GOAL:= build

.PHONY: pull export import environment test test-ci test-crawler test-crawler-total test-elastic-search test-page teardown

# Define linked containers (these name should match keys in
# fig.ml). The test & test-ci targets wil be run with all links set
# correctly.
DOCKER_RUN_ELASTIC_SEARCH:=docker run --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro -i -t $(REPO_NAME)/elasticsearch /bin/sh -c ". /usr/share/elasticsearch/.bash_profile && bash"
DOCKER_RUN_ELASTIC_SEARCH_CENTOS:=docker run -i -t $(REPO_NAME)/elasticsearch_centos zsh

# Wildcard rule to build an image from a file inside dockerfiles/
# Use the tasks like any other dependency. Order may be controller
# as well.
# See http://www.gnu.org/software/make/manual/make.html#Pattern-Rules
# for info on how this work and what $< and $(@F) mean.
images/% : dockerfiles/% pull
	ln -sf $< Dockerfile
	docker build -t $(REPO_NAME)/$(@F) .
	#rm Dockerfile

environment: pull docker-compose.yml
	$(DOCKER_COMPOSE) up -d

build: images/common

test:
	$(DOCKER_RUN)

# NOTE: Cannot use --rm on Circle CI, hence the seemingly
# duplicate task.

test-elastic-search: images/elasticsearch
	$(DOCKER_RUN_ELASTIC_SEARCH)

test-elastic-search-centos: images/elasticsearch_centos
	$(DOCKER_RUN_ELASTIC_SEARCH_CENTOS)

teardown:
	$(DOCKER_COMPOSE) stop
	$(DOCKER_COMPOSE) rm --force

# Wildcard rule to push an image from a file inside dockerfiles/
# to the specified registry. Works the same way as above. Used
# in make deploy to push all required images.
push/% : images/%
	ifndef TAG
		$(error "CIRCLE_SHA1 variable missing!")
	endif
	ifndef REGISTRY
		$(error "REGISTRY missing!")
	endif
		docker tag $(REPO_NAME)/$(@F) $(REGISTRY)/$(REPO_NAME)/$(@F):$(TAG)
		docker tag $(REPO_NAME)/$(@F) $(REGISTRY)/$(REPO_NAME)/$(@F):latest
		docker push $(REGISTRY)/$(REPO_NAME)/$(@F)

clean: teardown
	rm -rf tmp/images
ifneq ($(shell docker ps -a -q),)
	docker stop $(shell docker ps -a -q)
	docker rm $(shell docker ps -a -q)
endif
ifneq ($(shell docker images -q),)
	docker rmi $(shell docker images -q)
endif
