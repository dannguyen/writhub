.DEFAULT_GOAL := help
.PHONY : publish_examples


publish_examples:
	find examples/* -maxdepth 0 -type dir -not -name '_published' | while read -r dname; do \
		pname="examples/_published/$$(basename $$dname)"; \
		writhub md "$${dname}" --output-path "$${pname}"; \
	done
