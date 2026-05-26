# Delegates to .wireframe-kit/
.PHONY: help parse-copy sync link-skills validate-blocks setup-github clean-content serve serve-stop serve-status \
	figma-install-deps figma-check figma-init-manifest figma-capture-all figma-capture-one figma-list-captures

KIT_DIR := ./.wireframe-kit

help parse-copy sync link-skills validate-blocks setup-github clean-content serve serve-stop serve-status \
	figma-install-deps figma-check figma-init-manifest figma-capture-all figma-capture-one figma-list-captures:
	@$(MAKE) -C $(KIT_DIR) $@
